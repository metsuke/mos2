import os
import importlib.util

def get_command_help(cmd_name, commands_dir):
    """Carga dinámicamente un comando y extrae su función help()"""
    file_path = os.path.join(commands_dir, f"{cmd_name}.py")
    
    if not os.path.exists(file_path):
        return None
    
    try:
        # Cargamos el módulo temporalmente solo para leer su ayuda
        spec = importlib.util.spec_from_file_location(cmd_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, 'help'):
            return module.help()
        return "Sin descripción disponible."
    except Exception:
        return "Error al leer la ayuda del comando."

def execute(args):
    # Obtenemos la ruta de la carpeta 'commands' dinámicamente
    commands_dir = os.path.dirname(os.path.abspath(__file__))
    
    # CASO 1: Sin parámetros -> Mostrar todos los comandos
    if len(args) == 0:
        print("Comandos disponibles en MetsuOS:")
        print("-" * 50)
        
        # Iteramos sobre todos los ficheros .py en el directorio
        for filename in sorted(os.listdir(commands_dir)):
            if filename.endswith(".py") and not filename.startswith("__"):
                cmd_name = filename[:-3] # Quitamos el .py
                help_text = get_command_help(cmd_name, commands_dir)
                
                # Formateamos la salida para que quede alineada
                print(f"  {cmd_name.ljust(12)} - {help_text}")
                
    # CASO 2: Con parámetros -> Mostrar ayuda de un comando específico
    else:
        cmd_name = args[0]
        help_text = get_command_help(cmd_name, commands_dir)
        
        if help_text:
            print(help_text)
        else:
            print(f"help: comando no encontrado: '{cmd_name}'")

def help():
    return "Uso: help [comando] - Muestra la lista de comandos o la ayuda de uno específico."