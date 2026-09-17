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
from moslib.core.entorno import (
    debe_bloquear_locale,
    descripcion,
    etiqueta,
    mensaje_locale_bloqueado,
    pide_simular_bloqueo,
)
from moslib.core.shell_hist import cargar_historial
from moslib.core.tasks import start_worker, stop_worker
from moslib.core.user import (
    get_username,
    ensure_user_space,
    get_user_apps_dir,
    get_system_apps_dir,
)


class MOSh:
    def __init__(self):
        self.username = get_username()
        self.mos_dir = ensure_user_space(self.username)
        self.env_tag = etiqueta()
        self.cmd_manager = CommandManager(
            system_commands_dir=current_dir.parent / "commands",
            user_commands_dir=self.mos_dir / "commands",
            apps_root=get_user_apps_dir(),
            system_apps_root=get_system_apps_dir(),
            enforce_security=True,
        )
        self.running = True
        self.prompt = f"mosh/{self.env_tag}/{self.username}@metsuos:~$ "

    def _run_startup_tests(self) -> bool:
        print("[MetsuOS] Ejecutando tests de arranque (unitarios + seguridad)...")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--tb=line"],
            cwd=str(project_root),
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("[MetsuOS] Tests de arranque: OK\n")
            return True
        print("[MetsuOS] Error: fallo en los tests de arranque.")
        print(result.stdout or "")
        print(result.stderr or "")
        print("El sistema no arrancará hasta que todos los tests pasen.")
        return False

    def _una_linea(self, line: str) -> None:
        parts = line.split()
        cmd_name, args = parts[0], parts[1:]
        if cmd_name == "exit":
            self.running = False
            return
        mod = self.cmd_manager.get_command(cmd_name)
        if mod and hasattr(mod, "execute"):
            mod.execute(args)
            return
        print(f"mosh: comando no encontrado: {cmd_name}")

    def run(self, argv=None):
        if debe_bloquear_locale(argv):
            print(mensaje_locale_bloqueado(prueba=pide_simular_bloqueo(argv)))
            sys.exit(1)
        if not self._run_startup_tests():
            sys.exit(1)
        cargar_historial(self.mos_dir)
        start_worker(30.0)
        print("Iniciando MOSh para MetsuOS...")
        print(f"Usuario: {self.username}")
        print(f"Entorno: {self.env_tag} ({descripcion(self.env_tag)})")
        print(f"Espacio personal: {self.mos_dir}")
        print("Historial: flechas arriba/abajo. Pegado multilínea activo.")
        print("Usa 'exit' para salir, 'help', 'docs', 'a11y'")
        print()
        try:
            while self.running:
                try:
                    bruto = input(self.prompt)
                    for line in bruto.replace("\r\n", "\n").split("\n"):
                        line = line.strip()
                        if line and self.running:
                            self._una_linea(line)
                except KeyboardInterrupt:
                    print("\nUsa 'exit' para salir")
                except Exception as e:
                    print(f"Error de ejecución: {e}")
        finally:
            stop_worker()