from values import running, MULTICAST_GROUP, MULTICAST_PORT, BUFFER_SIZE, ignored_hosts, active_multicast_peers, peers_lock
import socket
from rich.console import Console

console = Console()

def multicast_listener(sock, local_ip):
    sock.settimeout(1.0)
    while running:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            continue
        except OSError:
            break
        except Exception as e:
            if running:
                console.print(f"[bold red]Ошибка в multicast_listener:[/bold red] {e}")
            break

        try:
            message = data.decode(errors="ignore")
        except Exception as e:
            console.print(f"[bold red]Не удалось декодировать сообщение от {addr[0]}: {e}[/bold red]")
            continue

        # --- Отладка ---
        console.print(f"[dim]Получено от {addr[0]}: {message}[/dim]")

        # Игнорируем свои пакеты и игнорируемые хосты
        if addr[0] in ignored_hosts:
            continue

        # Добавляем новый IP, если это PEER_DISCOVERY
        if message.startswith("PEER_DISCOVERY:"):
            peer_ip = message.split(":", 1)[1].strip()
            if peer_ip != local_ip:
                with peers_lock:
                    if peer_ip not in active_multicast_peers:
                        active_multicast_peers.add(peer_ip)
                        console.print(f"[green]Обнаружен новый участник через multicast: {peer_ip}[/green]")
            continue

        # LEAVE_GROUP
        if message.startswith("LEAVE_GROUP:"):
            peer_ip = message.split(":", 1)[1].strip()
            with peers_lock:
                if peer_ip in active_multicast_peers:
                    active_multicast_peers.remove(peer_ip)
                    console.print(f"[yellow]Участник {peer_ip} покинул multicast группу.[/yellow]")
            continue

        # Обычные сообщения
        console.print(f"[cyan][Multicast от {addr[0]}]:[/cyan] {message}")

    console.print("[dim]multicast_listener завершён[/dim]")


def send_multicast(sock, message, callback=None):
    try:
        if sock.fileno() != -1:
            sock.sendto(message.encode(), (MULTICAST_GROUP, MULTICAST_PORT))
            print(f"{message.encode()} to {MULTICAST_GROUP} + {MULTICAST_PORT}")
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
        error_msg = f"[bold red]Ошибка при отправке multicast:[/bold red] {e}"
        if callback:
            callback(error_msg)
        else:
            console.print(error_msg)