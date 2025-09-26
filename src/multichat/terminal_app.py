import os
import signal
import socket
import threading
import sys
import ipaddress

from broadcast import broadcast_listener, send_broadcast
from multicast import multicast_listener, send_multicast
from utils import get_network_info, peer_discovery, print_app_info, signal_handler
from values import BROADCAST_PORT, MULTICAST_GROUP, MULTICAST_PORT,\
                   running, peers_lock, ignored_hosts, active_multicast_peers,\
                   active_broadcast_peers, options, BROADCAST_MODE, MULTICAST_MODE

from rich.console import Console

console = Console()

in_multicast_group = True
mreq = None

def terminal_app() -> None:
    global BROADCAST_MODE, MULTICAST_MODE, running, in_multicast_group, mreq, options

    local_ip, netmask, broadcast_addr = get_network_info()
    if not local_ip or not netmask or not broadcast_addr:
        console.print("[bold red]Не удалось определить сетевые параметры.[/bold red]")
        return

    broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_sock.settimeout(1.0)
    try:
        broadcast_sock.bind(('', BROADCAST_PORT))
    except OSError as e:
        console.print(f"[bold red]Ошибка привязки широковещательного сокета:[/bold red] {e}")
        console.print("[yellow]Попробуйте запустить программу с правами администратора или изменить BROADCAST_PORT в values.py.[/yellow]")
        return

    multicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    multicast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    multicast_sock.settimeout(1.0)
    try:
        multicast_sock.bind(('', MULTICAST_PORT))
        multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
        multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(local_ip))
        mreq = socket.inet_aton(MULTICAST_GROUP) + socket.inet_aton(local_ip)
        multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    except Exception as e:
        console.print(f"[bold red]Ошибка настройки многоадресного сокета:[/bold red] {e}")
        console.print("[yellow]Многоадресная передача отключена из-за ошибки.[/yellow]")
        console.print("[yellow]Проверьте сетевые настройки.[/yellow]")
        in_multicast_group = False
        mreq = None

    threads = [
        threading.Thread(target=broadcast_listener, args=(broadcast_sock, local_ip), daemon=True),
        threading.Thread(target=multicast_listener, args=(multicast_sock, local_ip), daemon=True),
        threading.Thread(target=peer_discovery, args=(broadcast_sock, broadcast_addr, local_ip), daemon=True)
    ]

    for thread in threads:
        thread.start()

    signal.signal(signal.SIGINT, signal_handler)
    active_multicast_peers.add(local_ip)
    active_broadcast_peers.add(local_ip)

    print_app_info(local_ip,netmask,broadcast_addr,options)

    while running:
        try:
            message = input("---> ")

            if message == "/exit":
                running = False
                break

            elif message == "/h":
                print_app_info(local_ip,netmask,broadcast_addr,options)

            elif message == "/b":
                if not BROADCAST_MODE or (BROADCAST_MODE and MULTICAST_MODE):
                    BROADCAST_MODE = True
                    MULTICAST_MODE = False
                    console.print("[yellow]Переход в broadcast-режим[/yellow]")
                else:
                    console.print("[yellow]Вы уже находитесь в broadcast-режиме[/yellow]")
            
            elif message == "/m":
                if not MULTICAST_MODE or (BROADCAST_MODE and MULTICAST_MODE):    
                    BROADCAST_MODE = False
                    MULTICAST_MODE = True
                    console.print("[yellow]Переход в multicast-режим[/yellow]")
                else:
                    console.print("[yellow]Вы уже находитесь в multicast-режиме[/yellow]")
            
            elif message == "/bm":
                if not (BROADCAST_MODE and MULTICAST_MODE):    
                    BROADCAST_MODE = True
                    MULTICAST_MODE = True
                    console.print("[yellow]Переход в shared-режим[/yellow]")
                else:
                    console.print("[yellow]Вы уже находитесь в shared-режиме[/yellow]")

            elif message == "/clear":
                os.system('cls' if os.name == 'nt' else 'clear')

            elif message == "/leave_group":
                if in_multicast_group and mreq is not None:
                    try:
                        send_multicast(multicast_sock, f"LEAVE_GROUP:{local_ip}")

                        multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
                        in_multicast_group = False
                        active_multicast_peers.remove(local_ip)
                        console.print("[green]Покинута многоадресная группа.[/green]")
                    except Exception as e:
                        console.print(f"[bold red]Ошибка при выходе из многоадресной группы:[/bold red] {e}")
                else:
                    console.print("[yellow]Уже покинута многоадресная группа или она не была настроена.[/yellow]")


            elif message == "/join_group":
                if not in_multicast_group and mreq is not None:
                    try:
                        multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
                        in_multicast_group = True
                        active_multicast_peers.add(local_ip)
                        console.print("[green]Вход в многоадресную группу выполнен успешно.[/green]")
                    except Exception as e:
                        console.print(f"[bold red]Ошибка при входе в многоадресную группу:[/bold red] {e}")
                else:
                    console.print("[yellow]Вы уже состоите в многоадресной.[/yellow]")

            elif message.startswith("/ignore "):
                ip = message.split()[1]
                try:
                    ipaddress.ip_address(ip)
                except ValueError:
                    console.print(f"[bold red]Некорректный IP-адрес:[/bold red] {ip}")
                else:
                    with peers_lock:
                        ignored_hosts.add(ip)
                    console.print(f"[green]Хост {ip} добавлен в игнорируемые.[/green]")

            elif message.startswith("/unignore "):
                ip = message.split()[1]
                with peers_lock:
                    ignored_hosts.remove(ip)
                console.print(f"[green]Хост {ip} исключен из игнорируемых.[/green]")

            elif message == "/peers_ignore":
                with peers_lock:
                    peers_str = ", ".join(ignored_hosts) if ignored_hosts else "-"
                console.print(f"[green]Игнорируемые хосты: {peers_str}[/green]")

            elif message == "/peers_multicast":
                with peers_lock:
                    peers_str = ", ".join(active_multicast_peers) if active_multicast_peers else "Нет участников"
                console.print(f"[bold]Активные multicast участники:[/bold] {peers_str}")

            elif message == "/peers_broadcast":
                with peers_lock:
                    peers_str = ", ".join(active_broadcast_peers) if active_broadcast_peers else "Нет участников"
                console.print(f"[bold]Активные broadcast участники:[/bold] {peers_str}")


            else:
                if BROADCAST_MODE:
                    send_broadcast(broadcast_sock, f"{local_ip}: {message}", broadcast_addr)

                if MULTICAST_MODE:
                    if in_multicast_group:
                        try:
                            send_multicast(multicast_sock, f"{local_ip}: {message}")
                        except Exception as e:
                            console.print(f"[bold red]Не удалось отправить многоадресное сообщение:[/bold red] {e}")
                            in_multicast_group = False
                            mreq = None
                            console.print("[yellow]Многоадресная передача отключена из-за ошибки.[/yellow]")
                            console.print("[yellow]Проверьте сетевые настройки.[/yellow]")
                    else:
                        console.print("[yellow]Не отправлено многоадресное сообщение: не в группе.[/yellow]")


        except KeyboardInterrupt:
            running = False
            break
        except Exception as e:
            console.print(f"[bold red]Ошибка при обработке ввода:[/bold red] {e}")

    try:
        broadcast_sock.close()
    except Exception:
        pass

    try:
        multicast_sock.close()
    except Exception:
        pass

    for thread in threads:
        thread.join(timeout=3.0)
        if thread.is_alive():
            console.print(f"[dim]Поток {thread.name} не завершился вовремя[/dim]")

    console.print("[bold green]Программа завершена.[/bold green]")
    sys.exit(0)
