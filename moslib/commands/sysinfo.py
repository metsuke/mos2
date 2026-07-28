import sys
import platform
import subprocess
import time
import os

def get_linux_cpu_usage():
    """Calcula el % de uso de CPU leyendo /proc/stat dos veces con un pequeño intervalo."""
    try:
        def get_times():
            with open('/proc/stat', 'r') as f:
                times = [float(x) for x in f.readline().split()[1:]]
            return sum(times), times[3] # total_time, idle_time
        
        t1, i1 = get_times()
        time.sleep(0.1) # Pequeña pausa para medir la diferencia
        t2, i2 = get_times()
        
        if t2 - t1 > 0:
            return round(100.0 * (1.0 - ((i2 - i1) / (t2 - t1))), 1)
    except Exception:
        pass
    return None

def get_sysinfo():
    """Obtiene la información del sistema operativo anfitrión sin usar sudo."""
    info = {
        "os": f"{platform.system()} {platform.release()}",
        "cpu_model": platform.processor() or "Desconocido",
        "ram_total": "Desconocida",
        "ram_libre": "Desconocida",
        "cpu_uso": "Desconocido",
        "temperatura": "N/D (Requiere Admin/Sudo)"
    }

    try:
        # --- LINUX ---
        if sys.platform.startswith('linux'):
            # RAM
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
            
            total = [line.split()[1] for line in meminfo.split('\n') if 'MemTotal:' in line][0]
            avail = [line.split()[1] for line in meminfo.split('\n') if 'MemAvailable:' in line]
            if not avail: # Fallback si MemAvailable no existe
                avail = [line.split()[1] for line in meminfo.split('\n') if 'MemFree:' in line]
                
            info["ram_total"] = f"{round(int(total) / (1024**2), 2)} GB"
            info["ram_libre"] = f"{round(int(avail[0]) / (1024**2), 2)} GB"

            # Temperatura CPU (Linux suele permitir leer esto sin sudo)
            temp_paths = ['/sys/class/thermal/thermal_zone0/temp', '/sys/class/hwmon/hwmon0/temp1_input']
            for path in temp_paths:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        info["temperatura"] = f"{int(f.read().strip()) / 1000.0}°C"
                    break

            # CPU Uso
            cpu_pct = get_linux_cpu_usage()
            if cpu_pct is not None:
                info["cpu_uso"] = f"{cpu_pct}%"

        # --- WINDOWS ---
        elif sys.platform == 'win32':
            # wmic devuelve la memoria total en Bytes y la libre en KiloBytes
            mem_total = subprocess.check_output('wmic computersystem get TotalPhysicalMemory', shell=True, text=True).split('\n')[1].strip()
            mem_free = subprocess.check_output('wmic os get FreePhysicalMemory', shell=True, text=True).split('\n')[1].strip()
            
            info["ram_total"] = f"{round(int(mem_total) / (1024**3), 2)} GB"
            info["ram_libre"] = f"{round(int(mem_free) / (1024**2), 2)} GB"
            
            cpu_load = subprocess.check_output('wmic cpu get loadpercentage', shell=True, text=True).split('\n')[1].strip()
            info["cpu_uso"] = f"{cpu_load}%"
            # Nota: La temperatura en Windows requiere invocaciones WMI que piden permisos de Administrador.

        # --- macOS ---
        elif sys.platform == 'darwin':
            # Hardware model
            info["cpu_model"] = subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string'], text=True).strip()
            
            # RAM Total (Bytes)
            mem_total = subprocess.check_output(['sysctl', '-n', 'hw.memsize'], text=True).strip()
            info["ram_total"] = f"{round(int(mem_total) / (1024**3), 2)} GB"
            
            # macOS no tiene un comando sencillo para RAM libre y CPU% sin parsear top/vm_stat
            # Se requiere top o psutil para datos precisos sin admin.
            
    except Exception:
        pass # Capturamos cualquier fallo de lectura para mostrar la info parcial obtenida

    return info

def execute(args):
    print()
    info = get_sysinfo()
    print("--- Información del Sistema (MetsuOS) ---")
    print(f"Sistema Operativo : {info['os']}")
    print(f"Procesador        : {info['cpu_model']}")
    print(f"Uso de CPU        : {info['cpu_uso']}")
    print(f"Temperatura CPU   : {info['temperatura']}")
    print(f"Memoria RAM Total : {info['ram_total']}")
    print(f"Memoria RAM Libre : {info['ram_libre']}")
    print()

def help():
    return "Uso: sysinfo - Muestra hardware, memoria y estado de la CPU sin requerir privilegios de administrador."