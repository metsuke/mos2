import sys
import time
from datetime import timedelta

def get_uptime():
    """Calcula el tiempo de actividad del sistema según el SO anfitrión."""
    uptime_seconds = 0
    try:
        # Plataformas basadas en Linux
        if sys.platform.startswith('linux'):
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                
        # Plataformas Windows
        elif sys.platform == 'win32':
            import ctypes
            # GetTickCount64 devuelve los milisegundos desde el arranque
            uptime_seconds = ctypes.windll.kernel32.GetTickCount64() / 1000.0
            
        # Plataformas macOS (Darwin) o BSD
        elif sys.platform == 'darwin' or sys.platform.startswith('freebsd'):
            import subprocess
            import re
            # kern.boottime devuelve información del arranque que podemos parsear
            output = subprocess.check_output(['sysctl', '-n', 'kern.boottime']).decode('utf-8')
            match = re.search(r'sec = (\d+)', output)
            if match:
                boot_time = int(match.group(1))
                uptime_seconds = time.time() - boot_time
            else:
                return "No se pudo determinar el arranque en macOS."
                
        else:
            return f"SO anfitrión ({sys.platform}) no soportado para este cálculo."

        # Convertimos los segundos a un formato legible (X days, H:MM:SS)
        delta = timedelta(seconds=int(uptime_seconds))
        return f"up {delta}"
        
    except Exception as e:
        return f"Error al obtener el uptime: {e}"

def execute(args):
    print()
    uptime_str = get_uptime()
    print(f"MetsuOS - {uptime_str}")
    print()

def help():
    return "Uso: uptime - Muestra el tiempo que lleva encendido el sistema operativo anfitrión."