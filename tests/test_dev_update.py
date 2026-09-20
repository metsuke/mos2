"""update / dev / git no avanzan main a ciegas."""

from moslib.commands import dev, git, update


def test_sinopsis_update_incluye_dev():
    assert "update dev" in update.sinopsis()


def test_sinopsis_dev():
    assert "dev publicar" in dev.sinopsis()
    assert "dev consolidar" in dev.sinopsis()


def test_git_bloquea_commit_en_main(monkeypatch):
    visto = []

    def fake_run(_cmd):
        visto.append("run")
        return 0

    monkeypatch.setattr(git, "rama_actual", lambda _cwd: "main")
    monkeypatch.setattr(git, "run_host", fake_run)
    git.execute(["commit", "-m", "x"])
    assert visto == []


def test_git_permite_status_en_main(monkeypatch):
    visto = []

    def fake_run(cmd):
        visto.append(cmd)
        return 0

    monkeypatch.setattr(git, "rama_actual", lambda _cwd: "main")
    monkeypatch.setattr(git, "run_host", fake_run)
    git.execute(["status"])
    assert visto and visto[0][0] == "git"


def test_dev_no_publica_main(monkeypatch, capsys):
    monkeypatch.setattr("moslib.commands.dev.rama_actual", lambda _cwd: "main")
    monkeypatch.setattr("moslib.commands.dev.raiz", lambda: ".")
    dev.execute(["publicar"])
    assert "Prohibido" in capsys.readouterr().out


def test_update_help():
    assert "update dev" in update.help()
