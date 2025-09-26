import sys
import socket
import threading
import ipaddress
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from broadcast import broadcast_listener, send_broadcast
from multicast import multicast_listener, send_multicast
from utils import get_network_info, peer_discovery, signal_handler
from values import BROADCAST_PORT, MULTICAST_GROUP, MULTICAST_PORT, running, peers_lock, ignored_hosts, active_multicast_peers, active_broadcast_peers, options, BROADCAST_MODE, MULTICAST_MODE
from rich.console import Console
from PySide6.QtWidgets import QListWidgetItem, QLabel

console = Console()

from ui_interface import Ui_MainWindow


class MultichatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.setup_network()
        self.setup_signals()
        self.console = Console()
        self.running = True

        # 🔹 Таймер для автообновления списка участников
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_peers_list)
        self.timer.start(1000)  # обновлять раз в секунду

    def load_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.menubar.setVisible(True)
        self.ui.menubar.setNativeMenuBar(False)
        self.ui.statusbar.setVisible(True)

    def setup_network(self):
        self.local_ip, self.netmask, self.broadcast_addr = get_network_info()
        if not self.local_ip or not self.netmask or not self.broadcast_addr:
            self.ui.chatDisplay.append("<font color='red'>Не удалось определить сетевые параметры.</font>")
            return

        self.broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_sock.settimeout(1.0)
        try:
            self.broadcast_sock.bind(('', BROADCAST_PORT))
            self.ui.chatDisplay.append(f"<font color='cyan'>Широковещательный сокет привязан к порту {BROADCAST_PORT}.</font>")
        except OSError as e:
            self.ui.chatDisplay.append(f"<font color='red'>Ошибка привязки широковещательного сокета: {e}</font>")
            return

        self.multicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.multicast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.multicast_sock.settimeout(1.0)
        try:
            self.multicast_sock.bind(('', MULTICAST_PORT))
            self.multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
            self.multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(self.local_ip))
            self.mreq = socket.inet_aton(MULTICAST_GROUP) + socket.inet_aton(self.local_ip)
            self.multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)
            self.ui.chatDisplay.append(f"<font color='cyan'>Многоадресный сокет привязан к порту {MULTICAST_PORT} и группе {MULTICAST_GROUP}.</font>")
        except Exception as e:
            self.ui.chatDisplay.append(f"<font color='red'>Ошибка настройки многоадресного сокета: {e}</font>")
            self.in_multicast_group = False
            self.mreq = None

        self.threads = [
            threading.Thread(
                target=broadcast_listener,
                args=(self.broadcast_sock, self.local_ip, self.ui.chatDisplay.append),
                daemon=True
            ),
            threading.Thread(
                target=multicast_listener,
                args=(self.multicast_sock, self.local_ip, self.ui.chatDisplay.append),
                daemon=True
            ),
            threading.Thread(
                target=peer_discovery,
                args=(self.broadcast_sock, self.broadcast_addr, self.local_ip, self, self.multicast_sock),
                daemon=True
            )
        ]
        for thread in self.threads:
            thread.start()

        self.in_multicast_group = True
        active_multicast_peers.add(self.local_ip)
        active_broadcast_peers.add(self.local_ip)
        self.update_peers_list()

    def setup_signals(self):
        self.ui.sendButton.clicked.connect(self.send_message)
        self.ui.messageInput.returnPressed.connect(self.send_message)
        self.ui.broadcastButton.clicked.connect(self.switch_to_broadcast)
        self.ui.multicastButton.clicked.connect(self.switch_to_multicast)
        self.ui.sharedButton.clicked.connect(self.switch_to_shared)
        self.ui.clearButton.clicked.connect(self.clear_chat)
        self.ui.infoButton.clicked.connect(self.show_info)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionLeaveGroup.triggered.connect(self.leave_group)
        self.ui.actionJoinGroup.triggered.connect(self.join_group)
        self.ui.actionPeersBroadcast.triggered.connect(self.show_peers_broadcast)
        self.ui.actionPeersMulticast.triggered.connect(self.show_peers_multicast)
        self.ui.actionPeersIgnore.triggered.connect(self.show_peers_ignore)

    def send_message(self):
        global BROADCAST_MODE, MULTICAST_MODE, SHARED_MODE, running
        message = self.ui.messageInput.text().strip()
        if not message:
            return
        self.ui.messageInput.clear()

        def display_message(text):
            self.ui.chatDisplay.append(
                text.replace("[green]", "<font color='green'>")
                .replace("[/green]", "</font>")
                .replace("[dim]", "<font color='gray'>")
                .replace("[/dim]", "</font>")
                .replace("[bold red]", "<font color='red'>")
                .replace("[/bold red]", "</font>")
            )

        if message == "/exit":
            self.running = False
            running = False
            self.close()
        elif message == "/h":
            self.show_info()
        elif message == "/b":
            if not BROADCAST_MODE or (BROADCAST_MODE and MULTICAST_MODE):
                BROADCAST_MODE = True
                MULTICAST_MODE = False
                self.ui.chatDisplay.append("<font color='yellow'>Переход в broadcast-режим</font>")
            else:
                self.ui.chatDisplay.append("<font color='yellow'>Вы уже находитесь в broadcast-режиме</font>")
        elif message == "/m":
            if not MULTICAST_MODE or (BROADCAST_MODE and MULTICAST_MODE):
                BROADCAST_MODE = False
                MULTICAST_MODE = True
                self.ui.chatDisplay.append("<font color='yellow'>Переход в multicast-режим</font>")
            else:
                self.ui.chatDisplay.append("<font color='yellow'>Вы уже находитесь в multicast-режиме</font>")
        elif message == "/bm":
            if not (BROADCAST_MODE and MULTICAST_MODE):
                BROADCAST_MODE = True
                MULTICAST_MODE = True
                self.ui.chatDisplay.append("<font color='yellow'>Переход в shared-режим</font>")
            else:
                self.ui.chatDisplay.append("<font color='yellow'>Вы уже находитесь в shared-режиме</font>")
        elif message == "/clear":
            self.clear_chat()
        elif message == "/leave_group":
            self.leave_group()
        elif message == "/join_group":
            self.join_group()
        elif message.startswith("/ignore "):
            ip = message.split()[1]
            try:
                ipaddress.ip_address(ip)
                with peers_lock:
                    ignored_hosts.add(ip)
                self.ui.chatDisplay.append(f"<font color='green'>Хост {ip} добавлен в игнорируемые.</font>")
                self.update_peers_list()
            except ValueError:
                self.ui.chatDisplay.append(f"<font color='red'>Некорректный IP-адрес: {ip}</font>")
        elif message.startswith("/unignore "):
            ip = message.split()[1]
            try:
                with peers_lock:
                    ignored_hosts.remove(ip)
                self.ui.chatDisplay.append(f"<font color='green'>Хост {ip} исключен из игнорируемых.</font>")
                self.update_peers_list()
            except KeyError:
                self.ui.chatDisplay.append(f"<font color='red'>Хост {ip} не находится в списке игнорируемых.</font>")
        elif message == "/peers_ignore":
            self.show_peers_ignore()
        elif message == "/peers_broadcast":
            self.show_peers_broadcast()
        elif message == "/peers_multicast":
            self.show_peers_multicast()
        else:
            if BROADCAST_MODE:
                send_broadcast(self.broadcast_sock, f"{self.local_ip}: {message}", self.broadcast_addr, callback=display_message)
            if MULTICAST_MODE and self.in_multicast_group:
                try:
                    send_multicast(self.multicast_sock, f"{self.local_ip}: {message}", callback=display_message)
                except Exception as e:
                    self.ui.chatDisplay.append(f"<font color='red'>Не удалось отправить многоадресное сообщение: {e}</font>")
                    self.in_multicast_group = False
                    self.mreq = None
                    self.ui.chatDisplay.append("<font color='yellow'>Многоадресная передача отключена из-за ошибки.</font>")
            elif MULTICAST_MODE and not self.in_multicast_group:
                self.ui.chatDisplay.append("<font color='yellow'>Не отправлено многоадресное сообщение: не в группе.</font>")

    def update_peers_list(self):
        self.ui.peersList.clear()
        with peers_lock:
            added = False

            if active_broadcast_peers:
                text = "Broadcast: " + ", ".join(sorted(active_broadcast_peers))
                item = QListWidgetItem()
                label = QLabel(text)
                label.setWordWrap(True)  # Включаем перенос
                self.ui.peersList.addItem(item)
                self.ui.peersList.setItemWidget(item, label)
                added = True

            if active_multicast_peers:
                text = "Multicast: " + ", ".join(sorted(active_multicast_peers))
                item = QListWidgetItem()
                label = QLabel(text)
                label.setWordWrap(True)
                self.ui.peersList.addItem(item)
                self.ui.peersList.setItemWidget(item, label)
                added = True

            if ignored_hosts:
                text = "Ignored: " + ", ".join(sorted(ignored_hosts))
                item = QListWidgetItem()
                label = QLabel(text)
                label.setWordWrap(True)
                self.ui.peersList.addItem(item)
                self.ui.peersList.setItemWidget(item, label)
                added = True

            if not added:
                self.ui.peersList.addItem("Нет активных пиров")

    def switch_to_broadcast(self):
        global BROADCAST_MODE, MULTICAST_MODE
        if not BROADCAST_MODE or (BROADCAST_MODE and MULTICAST_MODE):
            BROADCAST_MODE = True
            MULTICAST_MODE = False
            self.ui.chatDisplay.append("<font color='yellow'>Переход в broadcast-режим</font>")
        else:
            self.ui.chatDisplay.append("<font color='yellow'>Вы уже находитесь в broadcast-режиме</font>")

    def switch_to_multicast(self):
        global BROADCAST_MODE, MULTICAST_MODE
        if not MULTICAST_MODE or (BROADCAST_MODE and MULTICAST_MODE):
            BROADCAST_MODE = False
            MULTICAST_MODE = True
            self.ui.chatDisplay.append("<font color='yellow'>Переход в multicast-режим</font>")
        else:
            self.ui.chatDisplay.append("<font color='yellow'>Вы уже находитесь в multicast-режиме</font>")

    def switch_to_shared(self):
        global BROADCAST_MODE, MULTICAST_MODE
        if not (BROADCAST_MODE and MULTICAST_MODE):
            BROADCAST_MODE = True
            MULTICAST_MODE = True
            self.ui.chatDisplay.append("<font color='yellow'>Переход в shared-режим</font>")
        else:
            self.ui.chatDisplay.append("<font color='yellow'>Вы уже находитесь в shared-режиме</font>")

    def clear_chat(self):
        self.ui.chatDisplay.clear()

    def show_info(self):
        ip = self.local_ip or "<font color='red'>Не определён</font>"
        mask = self.netmask or "<font color='red'>Не определена</font>"
        broadcast = self.broadcast_addr or "<font color='red'>Не определён</font>"
        info = (
            f"<font color='cyan'>Локальный IP: {ip}</font><br>"
            f"<font color='cyan'>Маска подсети: {mask}</font><br>"
            f"<font color='cyan'>Широковещательный адрес: {broadcast}</font><br><br>"
            f"<font color='blue'>Чат запущен. Введите сообщение или команду:</font><br>"
        )
        for cmd, desc in options.items():
            info += f"<font color='yellow'>{cmd}</font> — {desc}<br>"
        self.ui.chatDisplay.append(info)

    def leave_group(self):
        if self.in_multicast_group and self.mreq is not None:
            try:
                send_multicast(self.multicast_sock, f"LEAVE_GROUP:{self.local_ip}", callback=self.ui.chatDisplay.append)
                self.multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, self.mreq)
                self.in_multicast_group = False
                active_multicast_peers.remove(self.local_ip)
                self.ui.chatDisplay.append("<font color='green'>Покинута многоадресная группа.</font>")
                self.update_peers_list()
            except Exception as e:
                self.ui.chatDisplay.append(f"<font color='red'>Ошибка при выходе из многоадресной группы: {e}</font>")
        else:
            self.ui.chatDisplay.append("<font color='yellow'>Уже покинута многоадресная группа или она не была настроена.</font>")

    def join_group(self):
        if not self.in_multicast_group and self.mreq is not None:
            try:
                self.multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)
                self.in_multicast_group = True
                active_multicast_peers.add(self.local_ip)
                self.ui.chatDisplay.append("<font color='green'>Вход в многоадресную группу выполнен успешно.</font>")
                self.update_peers_list()
            except Exception as e:
                self.ui.chatDisplay.append(f"<font color='red'>Ошибка при входе в многоадресную группу: {e}</font>")
        else:
            self.ui.chatDisplay.append("<font color='yellow'>Вы уже состоите в многоадресной группе.</font>")

    def show_peers_broadcast(self):
        with peers_lock:
            peers_str = ", ".join(active_broadcast_peers) if active_broadcast_peers else "Нет участников"
        self.ui.chatDisplay.append(f"<font color='cyan'>Активные broadcast участники: {peers_str}</font>")

    def show_peers_multicast(self):
        with peers_lock:
            peers_str = ", ".join(active_multicast_peers) if active_multicast_peers else "Нет участников"
        self.ui.chatDisplay.append(f"<font color='cyan'>Активные multicast участники: {peers_str}</font>")

    def show_peers_ignore(self):
        with peers_lock:
            peers_str = ", ".join(ignored_hosts) if ignored_hosts else "-"
        self.ui.chatDisplay.append(f"<font color='cyan'>Игнорируемые хосты: {peers_str}</font>")

    def closeEvent(self, event):
        global running
        self.running = False
        running = False
        try:
            self.broadcast_sock.close()
        except Exception:
            pass
        try:
            self.multicast_sock.close()
        except Exception:
            pass
        for thread in self.threads:
            thread.join(timeout=3.0)
            if thread.is_alive():
                self.ui.chatDisplay.append(f"<font color='yellow'>Поток {thread.name} не завершился вовремя</font>")
        event.accept()


def window_app():
    app = QApplication(sys.argv)
    window = MultichatWindow()
    window.show()
    sys.exit(app.exec())
