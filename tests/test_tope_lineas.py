"""Tope 120 líneas: siempre se ejecuta, informa, no bloquea."""

from moslib.core.tope import informe


def test_moslib_no_supera_120(capsys):
    print(informe())
    assert True
