"""Tests para acciones de sistema seguras con permisos."""

from __future__ import annotations

from moslib.core.acciones_sistema import (
    listar_comandos_sistema,
    ejecutar_accion_sistema,
    COMANDOS_REPOSITORIO_EXCLUIDOS,
)


def test_listar_comandos():
    cmds = listar_comandos_sistema()
    for excluido in COMANDOS_REPOSITORIO_EXCLUIDOS:
        assert excluido not in cmds
    assert "clear" in cmds
    assert "echo" in cmds


def test_ejecucion_excluida():
    ok, msg = ejecutar_accion_sistema("git", ["status"])
    assert ok is False
    assert "restringido" in msg.lower() or "repositorio" in msg.lower()


def test_ejecucion_segura():
    ok, msg = ejecutar_accion_sistema("echo", ["hola"])
    assert ok is True
    assert "éxito" in msg.lower()
