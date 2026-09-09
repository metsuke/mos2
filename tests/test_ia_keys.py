from moslib.core import ia_keys as K
from moslib.core import secreto


def test_save_and_resolve(tmp_path, monkeypatch):
    monkeypatch.setattr(K, "_dir", lambda: tmp_path)
    ok, msg = K.save_key("grok", "secreto-de-prueba")
    assert ok, msg
    assert K.has_stored_key("grok") is True
    assert K.resolve_key("grok") == "secreto-de-prueba"
    texto = (tmp_path / "ia_keys.json").read_text(encoding="utf-8")
    assert "secreto-de-prueba" not in texto


def test_tamper_fails(tmp_path, monkeypatch):
    monkeypatch.setattr(K, "_dir", lambda: tmp_path)
    K.save_key("grok", "abc")
    path = tmp_path / "ia_keys.json"
    path.write_text(path.read_text(encoding="utf-8").replace("A", "B"), encoding="utf-8")
    assert K.load_key("grok") is None


def test_ingest_env(tmp_path, monkeypatch):
    monkeypatch.setattr(K, "_dir", lambda: tmp_path)
    monkeypatch.setenv("OPENROUTER_API_KEY", "env-or")
    hechos = K.ingest_env()
    assert "openrouter" in hechos
    assert K.load_key("openrouter") == "env-or"


def test_secreto_roundtrip(tmp_path):
    wrap = secreto.crear_wrap(tmp_path / ".ia_wrap")
    blob = secreto.envolver(b"hola", wrap)
    assert secreto.desenvolver(blob, wrap) == b"hola"


def test_delete(tmp_path, monkeypatch):
    monkeypatch.setattr(K, "_dir", lambda: tmp_path)
    K.save_key("jan", "k")
    ok, _ = K.delete_key("jan")
    assert ok
    assert K.load_key("jan") is None