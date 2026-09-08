from moslib.core import ia_router as R


def _fake_detect(jan_ok=False):
    return [
        {"id": "jan", "tipo": "local", "disponible": jan_ok, "motivo": "test"},
        {"id": "gpt4all", "tipo": "local", "disponible": False, "motivo": "test"},
        {"id": "grok", "tipo": "remoto", "disponible": False, "motivo": "test"},
        {"id": "openrouter", "tipo": "remoto", "disponible": False, "motivo": "test"},
    ]


def test_default_off_no_network(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    monkeypatch.setattr(R, "detectar", lambda: _fake_detect())
    st = R.status()
    assert st["enabled"] is False
    assert "jan" in st["providers"]
    ok, msg = R.complete("hola")
    assert ok is False
    assert "enabled=false" in msg


def test_reject_mos_path(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    R.save_policy({"enabled": True, "allow_mos_paths": [], "provider": "jan"})
    ok, msg = R.complete("lee /x/.mos/secret")
    assert ok is False
    assert ".mos" in msg


def test_unknown_provider(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    R.save_policy({"enabled": True, "allow_mos_paths": [], "provider": "jan"})
    ok, msg = R.complete("hola", {"provider": "noexiste"})
    assert ok is False
    assert "noexiste" in msg


def test_set_provider_rejects_unavailable(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    monkeypatch.setattr(R, "detectar", lambda: _fake_detect(False))
    ok, msg = R.set_provider("jan")
    assert ok is False
    assert "disponible" in msg
    assert R.load_policy()["enabled"] is False


def test_set_provider_ok(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    monkeypatch.setattr(R, "detectar", lambda: _fake_detect(True))
    ok, msg = R.set_provider("jan")
    assert ok is True
    pol = R.load_policy()
    assert pol["provider"] == "jan"
    assert pol["enabled"] is True


def test_set_modelo_auto(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    ok, msg = R.set_modelo("auto", "jan")
    assert ok is True
    assert R.modelo_activo("jan") == "auto"


def test_set_modelo_must_be_in_list(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    monkeypatch.setattr(R, "listar_modelos", lambda provider=None: (True, "jan", ["aaa", "bbb"]))
    ok, msg = R.set_modelo("zzz", "jan")
    assert ok is False
    assert "zzz" in msg


def test_set_modelo_from_list(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    monkeypatch.setattr(R, "listar_modelos", lambda provider=None: (True, "jan", ["aaa", "bbb"]))
    ok, msg = R.set_modelo("bbb", "jan")
    assert ok is True
    assert R.modelo_activo("jan") == "bbb"