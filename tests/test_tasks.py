import time

from moslib.core import tasks as T


def test_create_list_done(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "_store_path", lambda: tmp_path / "tareas.json")
    t = T.create_task(comando="help")
    assert t["estado"] == "pendiente"
    assert T.get_task(t["id"])["comando"] == "help"
    T.set_estado(t["id"], "hecha")
    assert T.get_task(t["id"])["estado"] == "hecha"


def test_blocked_cannot_run(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "_store_path", lambda: tmp_path / "tareas.json")
    t = T.create_task(comando="echo", estado="bloqueada_a11y_sec")
    assert T.can_run(t) is False


def test_sistema_requeue(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "_store_path", lambda: tmp_path / "tareas.json")
    t = T.create_task(
        modo="automatica",
        clase="sistema",
        comando="echo",
        estado="hecha",
        recurrencia="cada_n_minutos",
        intervalo=5,
    )
    log = T.tick()
    assert t["id"] in " ".join(log)
    assert T.get_task(t["id"])["estado"] == "pendiente"


def test_worker_starts_and_stops(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "_store_path", lambda: tmp_path / "tareas.json")
    T.stop_worker()
    assert T.start_worker(5.0) is True
    assert T.worker_running() is True
    time.sleep(0.2)
    T.stop_worker()
    assert T.worker_running() is False