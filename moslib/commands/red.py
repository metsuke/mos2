"""red — inventario de red del anfitrión. No barre la LAN ni abre puertos."""

import os

from moslib.core.red_data import arp, dns, hostname, ips, pasarela, perfil


def execute(args):
    print("Red del anfitrión (inventario lícito)")
    print()
    print(f"Perfil: {perfil()}")
    print(f"Hostname: {hostname()}")
    print(f"Usuario proceso: {os.environ.get('USER') or os.environ.get('USERNAME') or '?'}")
    print()
    print("Direcciones IPv4 de esta máquina")
    print("-------------------------------")
    lista = ips()
    if not lista:
        print("(ninguna además de localhost)")
    else:
        for ip in lista:
            print(ip)
    print()
    print("DNS (resolv.conf si existe)")
    print("---------------------------")
    servidores = dns()
    if servidores:
        for d in servidores:
            print(d)
    else:
        print("(no hay /etc/resolv.conf o está vacío)")
    print()
    print("Rutas / pasarela (salida del SO)")
    print("--------------------------------")
    print()
    print(pasarela())
    print()
    print("Vecinos en caché ARP (no es un barrido)")
    print("---------------------------------------")
    print()
    print(arp())
    print()
    print("Detalle")
    print("-------")
    print()
    print(
        "Esto no explora puertos ni hosts que el sistema no conozca ya. "
        "Un inventario ofensivo o reglas de enfrentamiento cibernético "
        "no forman parte de este comando."
    )


def help():
    return (
        "Uso: red - Muestra red local lícita: hostname, IP, DNS, pasarela y caché ARP. "
        "No barre la LAN."
    )
