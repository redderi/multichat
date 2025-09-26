from values import running, BROADCAST_PORT, BUFFER_SIZE, active_broadcast_peers, peers_lock, ignored_hosts
import socket
from rich.console import Console
from rich.text import Text

console = Console()

def broadcast_listener(sock, local_ip):
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
                console.print(f"[bold red]Ошибка в broadcast:[/bold red] {e}")
            break

        if addr[0] not in ignored_hosts and addr[0] != local_ip:
            message = data.decode(errors="ignore")
            if message.startswith("PEER_DISCOVERY:"):
                peer_ip = message.split(":", 1)[1]
                with peers_lock:
                    if peer_ip not in active_broadcast_peers and peer_ip != local_ip:
                        active_broadcast_peers.add(peer_ip)
                        #console.print(f"[green]Обнаружен участник:[/green] {peer_ip}")
            else:
                console.print(f"[Получено Broadcast] {addr[0]}: {message}")
        elif addr[0] == local_ip:
            #console.print(f"[dim][DEBUG][/dim] Пропущено собственное broadcast-сообщение от [cyan]{addr[0]}[/cyan]")
            pass

    console.print("[dim]broadcast завершён[/dim]")

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