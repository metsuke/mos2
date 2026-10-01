"""Bucle mos2ai. El contexto vive en disco. Al rotar no se espera al humano."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

PARTES = ("investigacion", "acciones")
ROLES = ("system", "user", "assistant", "cambio", "resumen")
MAX_CHARS = 100000


def raiz(base: Path | None = None) -> Path:
    if base is not None:
        return Path(base)
    from moslib.core.user import ensure_user_space, get_user_mos_dir

    ensure_user_space()
    return get_user_mos_dir() / "ia"


def sesion_dir(sesion: str = "actual", base: Path | None = None) -> Path:
    nombre = (sesion or "actual").strip() or "actual"
    if nombre in (".", "..") or "/" in nombre or "\\" in nombre:
        raise ValueError("id de sesion no valido")
    d = raiz(base) / "sesiones" / nombre
    d.mkdir(parents=True, exist_ok=True)
    (d / "investigacion").mkdir(exist_ok=True)
    (d / "acciones").mkdir(exist_ok=True)
    return d


def _escribir(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        fh.write(text)
        fh.flush()
        os.fsync(fh.fileno())
    tmp.replace(path)


def _leer(path: Path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeError):
        return None
    return data if isinstance(data, dict) else None


def anotar(parte: str, rol: str, texto: str, modelo: str = "", base: Path | None = None) -> None:
    d = sesion_dir("actual", base) / parte
    nums = []
    for path in d.glob("[0-9]" * 6 + ".json"):
        try:
            nums.append(int(path.stem))
        except ValueError:
            continue
    n = (max(nums) + 1) if nums else 1
    trozo = {
        "n": n,
        "ts": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "parte": parte,
        "rol": rol,
        "modelo": modelo,
        "texto": texto or "",
    }
    _escribir(d / f"{n:06d}.json", json.dumps(trozo, ensure_ascii=False, indent=2))


def cargar(parte: str, base: Path | None = None) -> list[dict]:
    d = sesion_dir("actual", base) / parte
    buenos = []
    for path in sorted(d.glob("*.json")):
        data = _leer(path)
        if data and "texto" in data:
            buenos.append(data)
    buenos.sort(key=lambda item: int(item.get("n") or 0))
    return buenos


def ultimo_encargo(base: Path | None = None) -> str:
    for trozo in reversed(cargar("acciones", base)):
        if trozo.get("rol") == "user" and str(trozo.get("texto") or "").strip():
            return str(trozo["texto"]).strip()
    return ""


def orden_continuar(encargo: str, pendiente: str = "") -> str:
    extra = ""
    if pendiente.strip():
        extra = "\nResultado de herramienta aun no leido:\n" + pendiente.strip()
    return (
        "Has tomado el relevo de otro modelo. No esperes instrucciones nuevas. "
        "Continua el proceso con el contexto inyectado. Ultimo encargo:\n"
        + encargo
        + extra
    )


def montar(max_chars: int = MAX_CHARS, base: Path | None = None) -> list[dict]:
    inv = cargar("investigacion", base)
    acc = cargar("acciones", base)
    if sum(len(str(t.get("texto") or "")) for t in inv) > max_chars:
        return []
    usadas = []
    usado = sum(len(str(t.get("texto") or "")) for t in inv)
    for trozo in reversed(acc):
        coste = len(str(trozo.get("texto") or ""))
        if usado + coste > max_chars:
            break
        usadas.append(trozo)
        usado += coste
    usadas.reverse()
    mensajes = []
    for trozo in inv + usadas:
        rol = trozo.get("rol") or "system"
        if rol not in ("system", "user", "assistant"):
            rol = "system"
        mensajes.append({"role": rol, "content": str(trozo.get("texto") or "")})
    return mensajes


def rotar(modelo_nuevo: str, pendiente: str, llamar) -> str:
    """llamar(mensajes) -> texto del modelo nuevo. No abre el prompt humano."""
    encargo = ultimo_encargo()
    anotar("acciones", "cambio", f"Cuota. Siguiente: {modelo_nuevo}. Continuar.", modelo_nuevo)
    if pendiente.strip():
        anotar("acciones", "assistant", pendiente, modelo_nuevo)
    if not encargo and not pendiente.strip():
        return "Sin encargo previo. Nada que continuar."
    orden = orden_continuar(encargo or pendiente, pendiente)
    mensajes = montar()
    if not mensajes:
        mensajes = [{"role": "user", "content": orden}]
    else:
        mensajes.append({"role": "user", "content": orden})
    anotar("acciones", "user", orden, modelo_nuevo)
    texto = llamar(mensajes)
    anotar("acciones", "assistant", texto, modelo_nuevo)
    return texto


def main() -> None:
    print("mos2ai: bucle de sesion cargado. La rotacion llama a rotar(), no al prompt humano.")