import hashlib
import base64

def normalizar_eol(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

content = '''"""Tests unitarios para el saneamiento y atomización de JSONs corruptos."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from moslib.core.json_saneamiento import (
    extraer_parte_valida,
    sanitizar_y_atomizar,
    formatear_humano,
)


def test_extraer_parte_valida_correcto(tmp_path: Path):
    f = tmp_path / "test.json"
    data = {"a": 1, "b": 2}
    f.write_text(json.dumps(data))
    
    parsed, logs = extraer_parte_valida(f.read_text())
    assert parsed == data
    assert any("válido" in l.lower() for l in logs)


def test_sanitizar_y_atomizar(tmp_path: Path):
    f = tmp_path / "corrupto.json"
    # Contenido con líneas válidas parciales o JSON malformado
    f.write_text('{"a": 1}\\n{"b": 2}\\n[corrupto sin cerrar')

    exito, mensaje, ensamblado = sanitizar_y_atomizar(f, "test_sesion")
    assert exito is True
    assert isinstance(ensamblado, (dict, list))
    assert len(ensamblado) > 0


def test_formatear_humano():
    datos = {"clave_larga": "valor", "lista": [1, 2, 3]}
    res = formatear_humano(datos)
    assert "clave_larga" in res
    assert "valor" in res
'''

data = content.encode("utf-8")
norm = normalizar_eol(data)
sha = hashlib.sha256(norm).hexdigest()

b64 = base64.b64encode(data).decode()

def wrap(text, width=80):
    return "\n".join(text[i:i+width] for i in range(0, len(text), width))

print(f"SHA: {sha}")
print("B64:")
print(wrap(b64))
