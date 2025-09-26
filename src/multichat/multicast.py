from values import running, MULTICAST_GROUP, MULTICAST_PORT, BUFFER_SIZE, ignored_hosts, active_multicast_peers, peers_lock
import socket
from rich.console import Console
import time

console = Console()
MULTICAST_TIMEOUT = 5  # секунд
last_seen_multicast = {}  # IP -> время последнего сообщения

def multicast_listener(sock, local_ip, callback=None):
    sock.settimeout(1.0)
    while running:
        now = time.time()
        # Удаляем устаревших участников (не трогаем локальный IP)
        with peers_lock:
            to_remove = [ip for ip, t in last_seen_multicast.items()
                         if ip != local_ip and now - t > MULTICAST_TIMEOUT]
            for ip in to_remove:
                last_seen_multicast.pop(ip)
                if ip in active_multicast_peers:
                    active_multicast_peers.remove(ip)
                    if callback:
                        callback(f"<font color='orange'>Multicast участник {ip} покинул группу (тайм-аут)</font>")

        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            continue
        except OSError:
            break
        except Exception as e:
            msg = f"<font color='red'>Ошибка в multicast_listener: {e}</font>"
            if callback:
                callback(msg)
            else:
                console.print(msg)
            break

        try:
            message = data.decode(errors="ignore")
        except Exception as e:
            msg = f"<font color='red'>Не удалось декодировать сообщение от {addr[0]}: {e}</font>"
            if callback:
                callback(msg)
            else:
                console.print(msg)
            continue

        if addr[0] in ignored_hosts:
            continue

        # PEER_DISCOVERY
        if message.startswith("PEER_DISCOVERY:"):
            peer_ip = message.split(":", 1)[1].strip()
            if peer_ip == local_ip:
                continue
            last_seen_multicast[peer_ip] = now
            with peers_lock:
                if peer_ip not in active_multicast_peers:
                    active_multicast_peers.add(peer_ip)
                    if callback:
                        callback(f"<font color='green'>Обнаружен новый участник через multicast: {peer_ip}</font>")
            continue

        # LEAVE_GROUP
        if message.startswith("LEAVE_GROUP:"):
            peer_ip = message.split(":", 1)[1].strip()
            if peer_ip == local_ip:
                # Игнорируем собственный выход
                continue
            with peers_lock:
                if peer_ip in active_multicast_peers:
                    active_multicast_peers.remove(peer_ip)
                    last_seen_multicast.pop(peer_ip, None)
                    if callback:
                        callback(f"<font color='yellow'>Multicast участник {peer_ip} покинул группу.</font>")
            continue

        # Обычные сообщения
        if callback:
            callback(f"<font color='cyan'>[Multicast от {addr[0]}]: {message}</font>")
        else:
            console.print(f"[Multicast от {addr[0]}]: {message}")


            

def send_multicast(sock, message, callback=None):
    try:
        if sock.fileno() != -1:
            sock.sendto(message.encode(), (MULTICAST_GROUP, MULTICAST_PORT))
            if message.split(":", 1)[0] != "LEAVE_GROUP":
                if callback:
                    callback(f"[green][Отправлено multicast]: {message.split(':', 1)[0]} (Вы):[/green] {message.split(':', 1)[1]}")
                else:
                    console.print(f"[green][Отправлено multicast]: {message.split(':', 1)[0]} (Вы):[/green] {message.split(':', 1)[1]}")
        else:
            if callback:
                callback("[dim]Не отправлено multicast: сокет закрыт[/dim]")
            else:
                console.print("[dim]Не отправлено multicast: сокет закрыт[/dim]")
    except OSError as e:
        error_msg = f"<font color='red'>Ошибка при отправке multicast: {e}</font>"
        if callback:
            callback(error_msg)
        else:
            console.print(error_msg)
