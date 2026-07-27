import subprocess

def get_git_version():
    """Extrae la versión basada en los tags y commits del repositorio Git local."""
    try:
        # Ejecuta el comando git y captura la salida
        version = subprocess.check_output(
            ["git", "describe", "--tags", "--always", "--dirty"], 
            stderr=subprocess.STDOUT, 
            text=True
        ).strip()
        return version
    except FileNotFoundError:
        return "Desconocida (Git no está instalado)"
    except subprocess.CalledProcessError:
        return "Desconocida (El directorio no es un repositorio Git)"

def execute(args):
    version = get_git_version()
    print(f"MetsuOS v{version}")

def help():
    return "Uso: version - Muestra la versión actual del sistema basada en el repositorio Git."