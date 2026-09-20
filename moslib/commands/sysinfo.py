"""Comando sysinfo."""

from moslib.core.sysinfo_data import get_sysinfo


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
    return (
        "Uso: sysinfo - Muestra hardware, memoria y estado de la CPU "
        "sin requerir privilegios de administrador."
    )


def sinopsis():
    return ["sysinfo"]
