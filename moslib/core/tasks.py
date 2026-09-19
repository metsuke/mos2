"""Tareas locales. Worker en segundo plano."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from moslib.core.tasks_crud import create_task, get_task, set_estado
from moslib.core.tasks_worker import start_worker, stop_worker, worker_running
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
    return data if isinstance(data, list) else []


def save_all(items: list[dict]) -> None:
    _store_path().write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def can_run(task: dict) -> bool:
    return task.get("estado") != "bloqueada_a11y_sec"


def tick() -> list[str]:
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
