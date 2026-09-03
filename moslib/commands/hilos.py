"""Vista tipo tele de hilos de tareas."""

from moslib.core import tasks as T


def execute(args):
    items = T.load_all()
    if not items:
        print("No hay hilos.")
        return
    print("Hilos por clase:")
    for clase in T.CLASES:
        grupo = [t for t in items if t.get("clase") == clase]
        print(f"[{clase}] {len(grupo)}")
        for t in grupo:
            print("  " + T.format_line(t))


def help():
    return "Uso: hilos - Lista tareas por clase (texto lineal, vista tele)."