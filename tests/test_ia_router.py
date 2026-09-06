from moslib.core import ia_router as R


def test_default_off_no_network(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    monkeypatch.setattr(
        R,
        "detectar",
        lambda: [
            {"id": "jan", "tipo": "local", "disponible": False, "motivo": "test"},
            {"id": "gpt4all", "tipo": "local", "disponible": False, "motivo": "test"},
            {"id": "grok", "tipo": "remoto", "disponible": False, "motivo": "test"},
            {"id": "openrouter", "tipo": "remoto", "disponible": False, "motivo": "test"},
        ],
    )
    st = R.status()
    assert st["enabled"] is False
    assert "jan" in st["providers"]
    assert "gpt4all" in st["providers"]
    assert "grok" in st["providers"]
    assert "openrouter" in st["providers"]
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
    monkeypatch.setattr(
        R,
        "detectar",
        lambda: [
            {"id": "jan", "tipo": "local", "disponible": False, "motivo": "caido"},
            {"id": "gpt4all", "tipo": "local", "disponible": False, "motivo": "caido"},
            {"id": "grok", "tipo": "remoto", "disponible": False, "motivo": "sin clave"},
            {"id": "openrouter", "tipo": "remoto", "disponible": False, "motivo": "sin clave"},
        ],
    )
    ok, msg = R.set_provider("jan")
    assert ok is False
    assert "disponible" in msg
    assert R.load_policy()["enabled"] is False


def test_set_provider_ok(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    monkeypatch.setattr(
        R,
        "detectar",
        lambda: [
            {"id": "jan", "tipo": "local", "disponible": True, "motivo": "ok"},
            {"id": "gpt4all", "tipo": "local", "disponible": False, "motivo": "caido"},
            {"id": "grok", "tipo": "remoto", "disponible": False, "motivo": "sin clave"},
            {"id": "openrouter", "tipo": "remoto", "disponible": False, "motivo": "sin clave"},
        ],
    )
    ok, msg = R.set_provider("jan")
    assert ok is True
    pol = R.load_policy()
    assert pol["provider"] == "jan"
    assert pol["enabled"] is True