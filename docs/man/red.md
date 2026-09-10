# red

## NOMBRE
red – inventario lícito de la red del anfitrión

## SINOPSIS
red

## DESCRIPCIÓN
Muestra lo que el sistema operativo ya conoce de esta máquina:

- perfil de entorno
- hostname
- direcciones IPv4 propias
- DNS de /etc/resolv.conf si existe
- tabla de rutas / pasarela (salida de route, ip route o netstat)
- caché ARP (vecinos que el SO ya ha visto)

No barre la LAN, no explora puertos ajenos y no cambia el firewall.
No es un inventario ofensivo ni un laboratorio de enfrentamiento
cibernético. Eso queda para una campaña de seguridad futura y un
documento ético específico.

## SEGURIDAD
Comando de sistema. Solo lectura. stdlib y herramientas del anfitrión
(arp, route, ip, netstat).

## VÉASE TAMBIÉN
iarouter, sysinfo