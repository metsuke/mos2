"""Tests para la campaña de conversión a tuplas."""

from __future__ import annotations

from pathlib import Path
from moslib.core.campana_tuplas import convertir_docs_json_a_tuplas
from moslib.commands import campanatuplas


def test_convertir_docs(tmp_path):
    convertidos = convertir_docs_json_a_tuplas()
    assert isinstance(convertidos, list)
    assert len(convertidos) >= 1


def test_cmd_campanatuplas():
    res = campanatuplas.execute([])
    assert res == 0
