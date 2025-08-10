import threading

BROADCAST_PORT = 5002
MULTICAST_PORT = 5003
BUFFER_SIZE = 1024

MULTICAST_GROUP = '224.0.0.1'

active_multicast_peers = set()
active_broadcast_peers = set()

ignored_hosts = set()
running = True

local_ip = None
netmask = None
broadcast_addr = None

peers_lock = threading.Lock()

BROADCAST_MODE = True
MULTICAST_MODE = False

options = {
    '/h' : 'вывести посказку',
    '/b' : 'перейти в broadcast-режим (по умолчанию)',
    '/m' : 'перейти в multicast-режим',
    '/bm' : 'перейти в совмещенный режим (broadcast + multicast)',
    '/clear' : 'очистит вывод чата',
    '/exit':'выйти из программы',
    '/leave_group':'покинуть многоадресную группу',
    '/join_group':'присоединится к многоадресной группе',
    '/peers_broadcast':'показать участников broadcast',
    '/peers_multicast':'показать участников multicast группы',
    '/ignore <IP>':'игнорировать хост',
    '/unignore <IP>':'перестать игнорировать хост',
    '/peers_ignore': 'показать участников ignore'
}