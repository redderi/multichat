from values import running, BROADCAST_PORT, BUFFER_SIZE, active_broadcast_peers, peers_lock, ignored_hosts
import socket
from rich.console import Console
from rich.text import Text

console = Console()

import time

BROADCAST_TIMEOUT = 5  # секунд

last_seen = {}  # IP -> время последнего сообщения

def broadcast_listener(sock, local_ip, callback=None):
    sock.settimeout(1.0)
    while running:
        now = time.time()
        # Чистим устаревших участников
        with peers_lock:
            to_remove = [ip for ip, t in last_seen.items() if now - t > BROADCAST_TIMEOUT]
            for ip in to_remove:
                last_seen.pop(ip)
                if ip in active_broadcast_peers:
                    active_broadcast_peers.remove(ip)
                    if callback:
                        callback(f"<font color='orange'>Broadcast участник {ip} покинул чат (тайм-аут)</font>")

        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            continue
        except OSError:
            break
        except Exception as e:
            msg = f"<font color='red'>Ошибка в broadcast: {e}</font>"
            if callback:
                callback(msg)
            else:
                console.print(msg)
            break

        if addr[0] not in ignored_hosts and addr[0] != local_ip:
            message = data.decode(errors="ignore")
            if message.startswith("PEER_DISCOVERY:"):
                peer_ip = message.split(":", 1)[1].strip()
                last_seen[peer_ip] = now  # обновляем время последнего сообщения
                with peers_lock:
                    if peer_ip not in active_broadcast_peers and peer_ip != local_ip:
                        active_broadcast_peers.add(peer_ip)
                        if callback:
                            callback(f"<font color='green'>Обнаружен broadcast участник: {peer_ip}</font>")
            else:
                if callback:
                    callback(f"<font color='cyan'>[Broadcast от {addr[0]}]: {message}</font>")
                else:
                    console.print(f"[Broadcast от {addr[0]}]: {message}")

    if callback:
        callback("<font color='gray'>broadcast завершён</font>")
    else:
        console.print("broadcast завершён")


def send_broadcast(sock, message, broadcast_addr, callback=None):
    try:
        if sock.fileno() != -1:
            print("send broadcast")
            sock.sendto(message.encode(), (broadcast_addr, BROADCAST_PORT))
            print(message.encode())
            if callback:
                callback(f"[green][Отправлено broadcast]: {message.split(':', 1)[0]} (Вы):[/green] {message.split(':', 1)[1]}")
            else:
                console.print(f"[green][Отправлено broadcast]: {message.split(':', 1)[0]} (Вы):[/green] {message.split(':', 1)[1]}")
        else:
            if callback:
                callback("[dim][DEBUG] Не отправлено broadcast: сокет закрыт[/dim]")
            else:
                console.print("[dim][DEBUG] Не отправлено broadcast: сокет закрыт[/dim]")
    except OSError as e:
        error_msg = f"[bold red]Ошибка при отправке broadcast:[/bold red] {e}"
        if callback:
            callback(error_msg)
        else:
            console.print(error_msg)