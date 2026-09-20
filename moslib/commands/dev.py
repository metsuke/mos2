"""dev publicar / consolidar."""

from moslib.core.dev_git import raiz, rama_actual, sucio
from moslib.core.update_git import run


def execute(args):
    args = list(args or [])
    cwd = raiz()
    if not args or args[0] not in ("publicar", "consolidar"):
        print(help())
        return
    rama = rama_actual(cwd)
    if rama == "main":
        print("[dev] Prohibido sobre main. Crea una rama paralela.")
        return
    if args[0] == "publicar":
        if sucio(cwd):
            run(["git", "add", "-A"], cwd, check=False)
            msg = f"wip: prueba en otras máquinas (rama {rama}, no merge a main)"
            run(["git", "commit", "-m", msg], cwd, check=False)
        run(["git", "push", "-u", "origin", rama], cwd, check=False)
        print(f"[dev] Publicada {rama}. En la otra máquina: update dev")
        return
    print("[dev] consolidar: push rama, merge a main, borrar rama.")
    run(["git", "push", "origin", rama], cwd, check=False)
    run(["git", "checkout", "main"], cwd)
    run(["git", "pull", "origin", "main"], cwd)
    m = run(["git", "merge", "--ff-only", rama], cwd, check=False)
    if m.returncode != 0:
        print("[dev] No hay fast-forward. No se borra la rama.")
        return
    run(["git", "push", "origin", "main"], cwd)
    run(["git", "branch", "-d", rama], cwd, check=False)
    run(["git", "push", "origin", "--delete", rama], cwd, check=False)
    print("[dev] main actualizado y rama borrada.")


def help():
    return "Uso: dev publicar|consolidar"


def sinopsis():
    return ["dev publicar", "dev consolidar"]
