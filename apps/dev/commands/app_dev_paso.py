"""Muestra el paso actual. No escribe ficheros."""

# Si al instalar no existe el paquete 'apps', usa la misma carga que campania:
# importamos la función copiando load_estado para no depender de paquetes extra.


def execute(args):
    try:
        from moslib.core.user import ensure_user_space, get_user_mos_dir
        import json
        from pathlib import Path
    except Exception as exc:
        print(f"Error: {exc}")
        return

    ensure_user_space()
    path = get_user_mos_dir() / "dev" / "estado.json"
    if not path.is_file():
        print("No hay estado. Ejecuta antes: app_dev_campania")
        return
    try:
        e = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        print("estado.json no es válido.")
        return

    print(f"Campaña {e.get('campana')} · bloque {e.get('bloque')} · paso {e.get('paso')}")
    print(f"Fichero: {e.get('fichero')}")
    print("---")
    contenido = e.get("contenido")
    if contenido:
        print(contenido)
    else:
        print("Aún no hay texto que aplicar. En 8.2.C lo rellenará 'aceptar'.")


def help():
    return "Uso: app_dev_paso - Muestra el paso actual sin escribir el disco."