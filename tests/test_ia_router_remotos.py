from moslib.core import ia_router as R


def test_listar_grok_usa_url_de_politica(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    R.save_policy({"provider": "grok", "enabled": True})
    visto = {}

    def fake_list(url, provider):
        visto["url"] = url
        visto["provider"] = provider
        return ["grok-3"], "ok"

    monkeypatch.setattr(R, "_listar_modelos", fake_list)
    ok, pid, ids = R.listar_modelos("grok")
    assert ok is True
    assert pid == "grok"
    assert ids == ["grok-3"]
    assert visto["url"].endswith("/chat/completions") or "x.ai" in visto["url"]


def test_listar_openrouter(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    R.save_policy({"provider": "openrouter", "enabled": True})
    monkeypatch.setattr(
        R,
        "_listar_modelos",
        lambda url, provider: (["openrouter/auto"], "ok"),
    )
    ok, pid, ids = R.listar_modelos("openrouter")
    assert ok is True
    assert pid == "openrouter"
    assert "openrouter/auto" in ids


def test_preguntar_respeta_modelo_fijado(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    R.save_policy(
        {
            "provider": "grok",
            "enabled": True,
            "allow_mos_paths": [],
            "grok_model": "grok-3",
        }
    )
    monkeypatch.setattr(R.ia_keys, "has_any_key", lambda p: True)
    capturado = {}

    def fake_complete(prompt, url, model, etiqueta, provider):
        capturado["model"] = model
        capturado["provider"] = provider
        return True, "ok"

    monkeypatch.setattr(R, "_complete_openai", fake_complete)
    ok, text = R.complete("hola")
    assert ok is True
    assert capturado["model"] == "grok-3"
    assert capturado["provider"] == "grok"