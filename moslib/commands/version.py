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
    """Obtiene el historial de las últimas 'n' versiones (tags) o commits con fecha."""
    try:
        # Añadimos %(creatordate:short) para obtener la fecha de creación del tag en formato aaaa-mm-dd
        result = subprocess.check_output(
            ["git", "for-each-ref", "--sort=-creatordate", f"--count={n}", 
             "--format=  %(creatordate:short)  |  %(refname:short)  |  %(subject)", "refs/tags"],
            stderr=subprocess.STDOUT, text=True
        ).strip()
        
        # Si no hay tags, hacemos el fallback a commits
        if not result:
            # Usamos %cd (commit date) y --date=short para forzar el formato aaaa-mm-dd
            result = subprocess.check_output(
                ["git", "log", f"-n{n}", "--date=short", "--pretty=format:  %cd  |  %h  |  %s"],
                stderr=subprocess.STDOUT, text=True
            ).strip()
            
        return result
    except Exception as e:
        return f"  Error al obtener el historial de Git: {e}"

def execute(args):
    # Verificamos si se ha pasado el parámetro de historial
    if "-h" in args:
        idx = args.index("-h")
        n = 10 # Valor por defecto
        
        # Comprobamos si hay un argumento después de -h y si es un número válido
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
        # Comportamiento por defecto sin argumentos
        version = get_git_version()
        print(f"MetsuOS v{version}")

def help():
    return "Uso: version [-h [n]] - Muestra la versión actual. Con -h muestra el historial de 'n' versiones (con fecha)."