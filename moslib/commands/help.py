"""Comando help. Sistema, apps y user_."""

from moslib.core.help_scan import (
    find_app_file,
    list_app_commands,
    list_commands,
    load_help_from_file,
    print_bloque,
    system_commands_dir,
    user_commands_dir,
)
from moslib.core.user import get_system_apps_dir, get_user_apps_dir


def execute(args):
    system_dir = system_commands_dir()
    user_dir = user_commands_dir()
    sys_apps = get_system_apps_dir()
    usr_apps = get_user_apps_dir()
    if len(args) == 0:
        print_bloque(
            "Comandos del sistema",
            [f"  {n.ljust(16)} - {h}" for n, h in list_commands(system_dir)],
        )
        sapps = list_app_commands(sys_apps)
        lineas = []
        for name, aliases, help_text in sapps:
            lineas.append(f"  {name}  [{aliases}]")
            lineas.append(f"      {help_text}")
        print_bloque("Comandos de app (sistema)", lineas)
        uapps = list_app_commands(usr_apps)
        lineas = []
        for name, aliases, help_text in uapps:
            lineas.append(f"  {name}  [{aliases}]")
            lineas.append(f"      {help_text}")
        print_bloque("Comandos de app (usuario)", lineas)
        user_cmds = list_commands(user_dir)
        lineas = []
        for name, help_text in user_cmds:
            short = name[5:] if name.startswith("user_") else name
            display = f"{name}  (o solo '{short}')" if name.startswith("user_") else name
            lineas.append(f"  {display.ljust(32)} - {help_text}")
        print_bloque("Comandos de usuario", lineas or ["  (ninguno todavía)", f"  {user_dir}"])
        print("=" * 60)
        print()
        return
    cmd_name = args[0]
    system_file = system_dir / f"{cmd_name}.py"
    if system_file.is_file():
        print(f"\n[Comando del sistema]  {cmd_name}")
        print("-" * 50)
        print(load_help_from_file(system_file))
        print()
        return
    app_sys = find_app_file(cmd_name, sys_apps)
    if app_sys is not None:
        print(f"\n[Comando de app de sistema]  {app_sys.stem}")
        print("-" * 50)
        print(load_help_from_file(app_sys))
        print()
        return
    app_usr = find_app_file(cmd_name, usr_apps)
    if app_usr is not None:
        print(f"\n[Comando de app de usuario]  {app_usr.stem}")
        print("-" * 50)
        print(load_help_from_file(app_usr))
        print()
        return
    user_file = user_dir / (cmd_name if cmd_name.startswith("user_") else f"user_{cmd_name}.py")
    if not cmd_name.startswith("user_"):
        alt = user_dir / f"user_{cmd_name}.py"
        user_file = user_dir / f"{cmd_name}.py"
        if alt.is_file():
            user_file = alt
    if user_file.is_file():
        print(f"\n[Comando de usuario]  {user_file.stem}")
        print("-" * 50)
        print(load_help_from_file(user_file))
        print()
        return
    print(f"help: comando no encontrado: '{cmd_name}'")


def help():
    return "Uso: help [comando] - Lista sistema, apps y usuario, o la ayuda de uno."


def sinopsis():
    return ["help", "help [comando]"]