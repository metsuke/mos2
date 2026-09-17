# uptime

## NOMBRE
uptime – tiempo de actividad del sistema anfitrión

## SINOPSIS

- uptime
- uptime_seconds = 0
- uptime_seconds = float(f.readline().split()[0])
- uptime_seconds = ctypes.windll.kernel32.GetTickCount64() / 1000.0
- uptime_seconds = time.time() - boot_time
- uptime_str = get_uptime()

## DESCRIPCIÓN
Muestra cuánto tiempo lleva activo el sistema operativo anfitrión, no el tiempo de sesión de MOSh.

## OPCIONES
Ninguna en esta baseline.

## EJEMPLOS

- uptime

## SEGURIDAD
Comando de sistema. Solo lectura de información del host.

## VÉASE TAMBIÉN
sysinfo, version, help

## HELP DEL COMANDO
Uso: uptime - Muestra el tiempo que lleva encendido el sistema operativo anfitrión.

## HELP DEL COMANDO
Uso: uptime - Muestra el tiempo que lleva encendido el sistema operativo anfitrión.