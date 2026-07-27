import os
import sys

# Ajustar el path dinámicamente para que encuentre moslib
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from mos2.moslib.core.cmd_loader import CommandManager

class MOSh:
    def __init__(self):
        # La ruta base para los comandos asume que se lanza dentro del proyecto
        base_cmd_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../commands")
        self.cmd_manager = CommandManager(commands_dir=base_cmd_path)
        self.running = True

    def run(self):
        print("Iniciando MOSh para MetsuOS...")
        print("Usa 'exit' para salir, 'help' para ayuda")
        while self.running:
            try:
                line = input("mosh/metsuke@metsuos:~$ ").strip()
                if not line:
                    continue
                
                parts = line.split()
                cmd_name = parts[0]
                args = parts[1:]

                if cmd_name == "exit":
                    self.running = False
                    continue

                command_module = self.cmd_manager.get_command(cmd_name)
                
                if command_module and hasattr(command_module, 'execute'):
                    command_module.execute(args)
                else:
                    print(f"mosh: comando no encontrado: {cmd_name}")

            except KeyboardInterrupt:
                print("Usa 'exit' para salir, 'help' para ayuda")
            except Exception as e:
                print(f"Error de ejecución: {e}")
