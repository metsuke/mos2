"""
moslib.core.shell
Shell principal de MetsuOS (MOSh)
"""

import sys
import subprocess
from pathlib import Path

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from moslib.core.cmd_loader import CommandManager
from moslib.core.user import get_username, ensure_user_space


class MOSh:
    def __init__(self):
        self.username = get_username()
        self.mos_dir = ensure_user_space(self.username)

        system_commands_dir = current_dir.parent / "commands"
        user_commands_dir = self.mos_dir / "commands"

        self.cmd_manager = CommandManager(
            system_commands_dir=system_commands_dir,
            user_commands_dir=user_commands_dir,
            enforce_security=True,
        )

        self.running = True
        self.prompt = f"mosh/{self.username}@metsuos:~$ "

    def _run_startup_tests(self) -> bool:
        """Ejecuta la batería de tests. Si falla alguno, el sistema no arranca."""
        print("[MetsuOS] Ejecutando tests de arranque (unitarios + seguridad)...")
        print("-" * 60)

        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--tb=line"],
            cwd=str(project_root),
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("[MetsuOS] ✅ Todos los tests pasaron correctamente.")
            print("-" * 60)
            print()
            return True

        print("[MetsuOS] ❌ FALLO EN LOS TESTS DE ARRANQUE")
        print("-" * 60)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print("-" * 60)
        print("El sistema NO arrancará hasta que todos los tests pasen.")
        print("Revisa los comandos con imports ilegales o ejecuta: poetry run pytest")
        return False

    def run(self):
        if not self._run_startup_tests():
            sys.exit(1)

        print("Iniciando MOSh para MetsuOS...")
        print(f"Usuario: {self.username}")
        print(f"Espacio personal: {self.mos_dir}")
        print("Usa 'exit' para salir, 'help' para ayuda")
        print()

        while self.running:
            try:
                line = input(self.prompt).strip()
                if not line:
                    continue

                parts = line.split()
                cmd_name = parts[0]
                args = parts[1:]

                if cmd_name == "exit":
                    self.running = False
                    continue

                command_module = self.cmd_manager.get_command(cmd_name)

                if command_module and hasattr(command_module, "execute"):
                    command_module.execute(args)
                else:
                    print(f"mosh: comando no encontrado: {cmd_name}")

            except KeyboardInterrupt:
                print("\nUsa 'exit' para salir, 'help' para ayuda")
            except Exception as e:
                print(f"Error de ejecución: {e}")