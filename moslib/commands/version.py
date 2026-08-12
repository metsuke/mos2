import subprocess

def get_git_version():
    """Extrae la versión actual basada en tags y commits."""
    try:
        version = subprocess.check_output(
            ["git", "describe", "--tags", "--always", "--dirty"],
            stderr=subprocess.STDOUT, text=True
        ).strip()
        return version
    except Exception:
        return "Desconocida"

def get_version_history(n):
    """
    Obtiene el historial de las últimas 'n' versiones.
    - Primero muestra los tags (versiones).
    - Si se piden más de los tags existentes, completa con commits recientes.
    """
    try:
        # 1. Obtener tags ordenados por fecha (más recientes primero)
        tags_result = subprocess.check_output(
            [
                "git", "for-each-ref",
                "--sort=-creatordate",
                f"--count={n}",
                "--format=%(creatordate:short)  |  %(refname:short)  |  %(subject)",
                "refs/tags"
            ],
            stderr=subprocess.STDOUT, text=True
        ).strip()

        tags = [line for line in tags_result.splitlines() if line.strip()] if tags_result else []
        remaining = n - len(tags)

        lines = []

        # Añadir los tags
        for tag in tags:
            lines.append(f"  {tag}")

        # 2. Si faltan entradas, completar con commits
        if remaining > 0:
            commits_result = subprocess.check_output(
                [
                    "git", "log",
                    f"-n{remaining}",
                    "--date=short",
                    "--pretty=format:%cd  |  %h  |  %s"
                ],
                stderr=subprocess.STDOUT, text=True
            ).strip()

            if commits_result:
                for commit in commits_result.splitlines():
                    lines.append(f"  {commit}")

        return "\n".join(lines) if lines else None

    except Exception as e:
        return f"  Error al obtener el historial de Git: {e}"

def execute(args):
    if "-h" in args:
        idx = args.index("-h")
        n = 10  # valor por defecto

        if len(args) > idx + 1 and args[idx + 1].isdigit():
            n = int(args[idx + 1])

        print(f"Historial de las últimas {n} versiones en MetsuOS:")
        print("-" * 75)

        history = get_version_history(n)
        if history:
            print(history)
        else:
            print("  No se encontraron versiones en el repositorio.")
    else:
        version = get_git_version()
        print(f"MetsuOS v{version}")

def help():
    return "Uso: version [-h [n]] - Muestra la versión actual. Con -h muestra el historial de 'n' versiones (tags + commits)."