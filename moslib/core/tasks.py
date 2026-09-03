"""
moslib.core.tasks
Tareas manuales y automáticas locales (campaña 07).
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from moslib.core.user import ensure_user_space, get_user_mos_dir

MODOS = ("manual", "automatica")
PRIV = ("root", "no-root")
CLASES = ("realtime", "heavy", "normal", "sistema")
ESTADOS = ("pendiente", "en_curso", "hecha", "fallida", "bloqueada_a11y_sec")
RECUR = ("una_vez", "cada_n_minutos", "cada_n_dias")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _store_path() -> Path:
    ensure_user_space()
    d = get_user_mos_dir() / "data"
    d.mkdir(parents=True, exist_ok=True)
    return d / "tareas.json"


def load_all() -> list[dict]:
    path = _store_path()
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(data, list):
        return []
    return data


def save_all(items: list[dict]) -> None:
    path = _store_path()
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


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
    for t in load_all():
        if t.get("id") == task_id:
            return t
    return None


def set_estado(task_id: str, estado: str) -> dict | None:
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


def can_run(task: dict) -> bool:
    return task.get("estado") != "bloqueada_a11y_sec"


def tick() -> list[str]:
    """
    Avanza automáticas locales.
    Clase sistema + hecha + no una_vez → vuelve a pendiente (reencola).
    """
    log = []
    items = load_all()
    changed = False
    for t in items:
        if t.get("modo") != "automatica":
            continue
        if not can_run(t):
            log.append(f"{t['id']} bloqueada; no se ejecuta")
            continue
        if t.get("clase") == "sistema" and t.get("estado") == "hecha":
            t["estado"] = "pendiente"
            t["actualizado"] = _now()
            changed = True
            log.append(f"{t['id']} sistema reencolada")
    if changed:
        save_all(items)
    return log


def format_line(task: dict) -> str:
    return (
        f"{task['id']}  {task['estado']}  {task['modo']}/{task['clase']}  "
        f"{task['privilegio']}  prio={task['prioridad']}  {task['comando']}"
    )