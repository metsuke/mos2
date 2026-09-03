from moslib.core import ia_router as R


def test_default_off_no_network(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    st = R.status()
    assert st["enabled"] is False
    ok, msg = R.complete("hola")
    assert ok is False
    assert "enabled=false" in msg


def test_reject_mos_path(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "policy_path", lambda: tmp_path / "ia_router.json")
    R.save_policy({"enabled": True, "allow_mos_paths": []})
    ok, msg = R.complete("lee /x/.mos/secret")
    assert ok is False
    assert ".mos" in msg