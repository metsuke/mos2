"""Tests para el comando sanearjson."""

from __future__ import annotations

from pathlib import Path
import json
from moslib.commands import sanearjson


def test_sanearjson_comando(tmp_path: Path, monkeypatch):
    f = tmp_path / "roto.json"
    f.write_text('{"item1": 10}\n{"item2": 20}')

    # Simular input 'n' para no guardar en disco o 's'
    monkeypatch.setattr("builtins.input", lambda prompt="": "n")

    res = sanearjson.execute([str(f), "sesion_test"])
    assert res == 0
