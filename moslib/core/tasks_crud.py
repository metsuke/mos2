"""Alta, lectura y estado de tareas."""

from __future__ import annotations

import uuid


def create_task(
    *,
    origen: str = "usuario",
    modo: str = "manual",
    privilegio: str = "no-root",
    clase: str = "normal",
    proyecto: str | None = None,
    prioridad: int = 10,
    maslow: int | None = None,
    recurrencia: str = "una_vez",
    intervalo: int | None = None,
    comando: str,
    estado: str = "pendiente",
) -> dict:
    from moslib.core.tasks import CLASES, ESTADOS, MODOS, PRIV, RECUR, _now, load_all, save_all

    if modo not in MODOS or privilegio not in PRIV or clase not in CLASES:
        raise ValueError("modo, privilegio o clase no válidos")
    if recurrencia not in RECUR or estado not in ESTADOS:
        raise ValueError("recurrencia o estado no válidos")
    task = {
        "id": uuid.uuid4().hex[:12],
        "origen": origen,
        "modo": modo,
        "privilegio": privilegio,
        "clase": clase,
        "proyecto": proyecto,
        "prioridad": int(prioridad),
        "maslow": maslow,
        "recurrencia": recurrencia,
        "intervalo": intervalo,
        "estado": estado,
        "comando": comando,
        "creado": _now(),
        "actualizado": _now(),
    }
    items = load_all()
    items.append(task)
    save_all(items)
    return task


def get_task(task_id: str) -> dict | None:
    from moslib.core.tasks import load_all

    for t in load_all():
        if t.get("id") == task_id:
            return t
    return None


def set_estado(task_id: str, estado: str) -> dict | None:
    from moslib.core.tasks import ESTADOS, _now, load_all, save_all

    if estado not in ESTADOS:
        raise ValueError("estado no válido")
    items = load_all()
    found = None
    for t in items:
        if t.get("id") == task_id:
            t["estado"] = estado
            t["actualizado"] = _now()
            found = t
            break
    if found:
        save_all(items)
    return found
