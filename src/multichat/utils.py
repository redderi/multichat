import netifaces
import time
import socket
from values import BROADCAST_PORT
from values import MULTICAST_GROUP, MULTICAST_PORT, running
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from multicast import send_multicast

console = Console()

def get_network_info():
    try:
        interfaces = netifaces.interfaces()
        for iface in interfaces:
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    ip = addr.get('addr')
                    netmask = addr.get('netmask')
                    broadcast = addr.get('broadcast')
                    if ip and netmask and broadcast and not ip.startswith('127.'):
                        return ip, netmask, broadcast
        return None, None, None
    except Exception as e:
        console.print(f"[bold red]Ошибка при получении сетевых параметров:[/bold red] {e}")
        return None, None, None

def peer_discovery(broadcast_sock, broadcast_addr, local_ip, window=None, multicast_sock=None):
    while running:
        message = f"PEER_DISCOVERY:{local_ip}"

        # --- Broadcast ---
        try:
            if broadcast_sock.fileno() != -1:
                broadcast_sock.sendto(message.encode(), (broadcast_addr, BROADCAST_PORT))
                console.print(f"[green][Отправлено broadcast]:[/green] {message}")
        except Exception as e:
            console.print(f"[bold red]Ошибка при отправке broadcast: {e}[/bold red]")

        # --- Multicast ---
        try:
            if window and window.in_multicast_group and multicast_sock:
                send_multicast(multicast_sock, message)
                console.print(f"[cyan][Отправлено multicast]:[/cyan] {message}")
        except Exception as e:
            console.print(f"[bold red]Ошибка при отправке multicast: {e}[/bold red]")

        time.sleep(2)


def signal_handler(sig, frame):
    global running
    running = False
    console.print("\n[bold yellow]Получен сигнал завершения, выход...[/bold yellow]")

def print_app_info(local_ip, netmask, broadcast_addr, options):
    ip = local_ip or "[red]Не определён[/red]"
    mask = netmask or "[red]Не определена[/red]"
    broadcast = broadcast_addr or "[red]Не определён[/red]"

    lines = [
        f"[bold green]Локальный IP:[/bold green] {ip}",
        f"[bold green]Маска подсети:[/bold green] {mask}",
        f"[bold green]Широковещательный адрес:[/bold green] {broadcast}",
        "",
        "[bold blue]Чат запущен. Введите сообщение или команду:[/bold blue]",
        ""
    ]

    for cmd, desc in options.items():
        lines.append(f"[yellow]{cmd}[/yellow] — {desc}")

    panel = Panel(Group(*lines), title="Информация о приложении", border_style="cyan")
    console.print(panel)