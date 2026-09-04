"""Estado de la campaña en curso (app dev)."""

import json
from pathlib import Path

from moslib.core.user import ensure_user_space, get_user_mos_dir

DEFAULT = {
    "campana": "08",
    "bloque": "8.2",
    "paso": "A",
    "fichero": None,
    "nota": "esqueleto; paso/aceptar aún no escriben el repo",
}


def _path() -> Path:
    ensure_user_space()
    d = get_user_mos_dir() / "dev"
    d.mkdir(parents=True, exist_ok=True)
    return d / "estado.json"


def load_estado() -> dict:
    p = _path()
    if not p.is_file():
        p.write_text(json.dumps(DEFAULT, ensure_ascii=False, indent=2), encoding="utf-8")
        return dict(DEFAULT)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return dict(DEFAULT)
    out = dict(DEFAULT)
    if isinstance(data, dict):
        out.update(data)
    return out


def execute(args):
    e = load_estado()
    print("App de desarrollo — estado")
    print(f"campaña: {e.get('campana')}")
    print(f"bloque: {e.get('bloque')}")
    print(f"paso: {e.get('paso')}")
    print(f"fichero: {e.get('fichero')}")
    if e.get("nota"):
        print(f"nota: {e.get('nota')}")


def help():
    return "Uso: app_dev_campania - Muestra el estado de la suite de desarrollo."