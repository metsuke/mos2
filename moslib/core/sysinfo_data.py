"""Inventario de hardware del anfitrión (sin sudo)."""

import os
import platform
import subprocess
import sys
import time


def cpu_linux():
    try:
        def tiempos():
            with open("/proc/stat", "r") as f:
                vals = [float(x) for x in f.readline().split()[1:]]
            return sum(vals), vals[3]
        t1, i1 = tiempos()
        time.sleep(0.1)
        t2, i2 = tiempos()
        if t2 - t1 > 0:
            return round(100.0 * (1.0 - ((i2 - i1) / (t2 - t1))), 1)
    except Exception:
        pass
    return None


def _linux(info):
    with open("/proc/meminfo", "r") as f:
        mem = f.read()
    total = [line.split()[1] for line in mem.split("\n") if "MemTotal:" in line][0]
    avail = [line.split()[1] for line in mem.split("\n") if "MemAvailable:" in line]
    if not avail:
        avail = [line.split()[1] for line in mem.split("\n") if "MemFree:" in line]
    info["ram_total"] = f"{round(int(total) / (1024 ** 2), 2)} GB"
    info["ram_libre"] = f"{round(int(avail[0]) / (1024 ** 2), 2)} GB"
    for path in (
        "/sys/class/thermal/thermal_zone0/temp",
        "/sys/class/hwmon/hwmon0/temp1_input",
    ):
        if os.path.exists(path):
            with open(path, "r") as f:
                info["temperatura"] = f"{int(f.read().strip()) / 1000.0}°C"
            break
    pct = cpu_linux()
    if pct is not None:
        info["cpu_uso"] = f"{pct}%"


def _windows(info):
    tot = subprocess.check_output(
        "wmic computersystem get TotalPhysicalMemory", shell=True, text=True
    ).split("\n")[1].strip()
    free = subprocess.check_output(
        "wmic os get FreePhysicalMemory", shell=True, text=True
    ).split("\n")[1].strip()
    info["ram_total"] = f"{round(int(tot) / (1024 ** 3), 2)} GB"
    info["ram_libre"] = f"{round(int(free) / (1024 ** 2), 2)} GB"
    load = subprocess.check_output(
        "wmic cpu get loadpercentage", shell=True, text=True
    ).split("\n")[1].strip()
    info["cpu_uso"] = f"{load}%"


def _macos(info):
    info["cpu_model"] = subprocess.check_output(
        ["sysctl", "-n", "machdep.cpu.brand_string"], text=True
    ).strip()
    tot = subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True).strip()
    info["ram_total"] = f"{round(int(tot) / (1024 ** 3), 2)} GB"


def get_sysinfo():
    info = {
        "os": f"{platform.system()} {platform.release()}",
        "cpu_model": platform.processor() or "Desconocido",
        "ram_total": "Desconocida",
        "ram_libre": "Desconocida",
        "cpu_uso": "Desconocido",
        "temperatura": "N/D (Requiere Admin/Sudo)",
    }
    try:
        if sys.platform.startswith("linux"):
            _linux(info)
        elif sys.platform == "win32":
            _windows(info)
        elif sys.platform == "darwin":
            _macos(info)
    except Exception:
        pass
    return info
