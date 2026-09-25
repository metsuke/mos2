"""Comando autoria."""

from moslib.core import autoria as core


def help():
    return (
        "autoria [show|set <campo> <valor>]\n"
        "Campos: programa autor email email_alt anio_desde anio_hasta contacto."
    )


def execute(args=None, stdin_data=""):
    args = list(args or [])
    if not args or args[0] in ("show", "list"):
        data = core.load()
        lineas = []
        for k in list(core.CAMPOS) + ["anio"]:
            if k == "anio":
                lineas.append("anio=" + core.anio_rango(data))
            else:
                lineas.append(f"{k}={data.get(k) or ''}")
        return "\n".join(lineas)
    if args[0] == "set" and len(args) >= 3:
        core.set_campo(args[1], " ".join(args[2:]))
        return execute(["show"])
    return help()
