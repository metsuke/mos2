from moslib.core.cmd_loader import CommandManager, invocation_names


def test_invocation_names():
    n = invocation_names("dev", "app_dev_paso")
    assert n == {"app_dev_paso", "dev_paso", "paso"}


def test_priority_system_over_app(tmp_path):
    sysd = tmp_path / "sys"
    sysd.mkdir()
    (sysd / "paso.py").write_text(
        "def execute(args):\n    pass\ndef help():\n    return 'SYS'\n",
        encoding="utf-8",
    )
    uapps = tmp_path / "uapps" / "dev" / "commands"
    uapps.mkdir(parents=True)
    (uapps / "app_dev_paso.py").write_text(
        "def execute(args):\n    pass\ndef help():\n    return 'APP'\n",
        encoding="utf-8",
    )
    mgr = CommandManager(sysd, apps_root=tmp_path / "uapps")
    assert mgr.get_command("paso").help() == "SYS"


def test_short_name_app(tmp_path):
    sysd = tmp_path / "sys"
    sysd.mkdir()
    uapps = tmp_path / "uapps" / "dev" / "commands"
    uapps.mkdir(parents=True)
    (uapps / "app_dev_paso.py").write_text(
        "def execute(args):\n    pass\ndef help():\n    return 'APP'\n",
        encoding="utf-8",
    )
    mgr = CommandManager(sysd, apps_root=tmp_path / "uapps")
    assert mgr.get_command("paso").help() == "APP"
    assert mgr.get_command("dev_paso").help() == "APP"
    assert mgr.get_command("app_dev_paso").help() == "APP"


def test_system_app_beats_user_app(tmp_path):
    sysd = tmp_path / "sys"
    sysd.mkdir()
    sapps = tmp_path / "sapps" / "dev" / "commands"
    sapps.mkdir(parents=True)
    (sapps / "app_dev_paso.py").write_text(
        "def execute(args):\n    pass\ndef help():\n    return 'SYSAPP'\n",
        encoding="utf-8",
    )
    uapps = tmp_path / "uapps" / "dev" / "commands"
    uapps.mkdir(parents=True)
    (uapps / "app_dev_paso.py").write_text(
        "def execute(args):\n    pass\ndef help():\n    return 'USRAPP'\n",
        encoding="utf-8",
    )
    mgr = CommandManager(
        sysd,
        apps_root=tmp_path / "uapps",
        system_apps_root=tmp_path / "sapps",
    )
    assert mgr.get_command("paso").help() == "SYSAPP"