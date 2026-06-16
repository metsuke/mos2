import os
from pathlib import Path

class MOSShell:
    def __init__(self, kernel):
        self.kernel = kernel

    def _fetch(self, args):
        info = {
            "OS": "MOS2 Core",
            "Kernel": "Python-based VFS",
            "User": self.kernel.user,
            "Root": self.kernel.project_root,
            "Home": f"/home/{self.kernel.user}",
            "Active Mounts": len(self.kernel.mounts)
        }
        print("\n \033[1;32mMOS2 System Information\033[0m")
        for k, v in info.items():
            print(f" \033[1;34m{k}:\033[0m {v}")
        print()

    def run(self):
        while True:
            try:
                # [MOSh] en Magenta para consistencia de marca
                prefix = "\033[1;95m[MOSh]\033[0m "
                prompt = f"{prefix}{self.kernel.get_prompt_info()}\033[1;97m$\033[0m "
                                
                user_input = input(prompt).strip()
                
                if not user_input: continue
                if user_input.lower() in ["exit", "logout", "quit"]:
                    print("\033[1;31mCerrando sesión en MOS2...\033[0m")
                    break
                
                self.execute(user_input)
            except (KeyboardInterrupt, EOFError):
                print("\n\033[1;31mSaliendo de MOS2...\033[0m")
                break

    def execute(self, cmd_line):
        parts = cmd_line.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == "cd":
            self._cd(args)
        elif cmd == "pwd":
            # Mostramos la ruta relativa a la raíz de MOS2 para mantener la ilusión
            print(f"/{os.path.relpath(os.getcwd(), self.kernel.project_root)}")
            # Tambien la ruta real
            os.system(cmd_line)
        else:
            # Los comandos externos siguen funcionando pero sobre los archivos de MOS2
            os.system(cmd_line)

    def _cd(self, args):
        try:
            # 1. Determinamos la ruta de destino preliminar
            if not args or args[0] == "~":
                target_str = str(self.kernel.virtual_home)
            elif args[0].startswith("~"):
                target_str = args[0].replace("~", str(self.kernel.virtual_home), 1)
            elif args[0] == "/":
                # Si el usuario pide ir a la raíz "/", lo mandamos a la raíz del proyecto
                target_str = str(self.kernel.project_root)
            elif args[0].startswith("/"):
                # Si pide una ruta absoluta virtual (ej: "/usr/bin")
                # Quitamos la barra inicial para poder concatenarla de forma segura a la raíz del proyecto
                target_str = os.path.join(str(self.kernel.project_root), args[0].lstrip("/"))
            else:
                target_str = args[0]

            # 2. Convertimos a ruta absoluta real para resolver los '../' matemáticamente
            target_path = Path(os.path.abspath(target_str))
            root_path = Path(self.kernel.project_root)

            # 3. Validamos si el destino está dentro de la raíz (o es la propia raíz)
            if not target_path.is_relative_to(root_path):
                print("cd: Permiso denegado (fuera de la raíz de MOS2)")
                return

            # 4. Si la validación es correcta, efectuamos el cambio real en el sistema
            os.chdir(target_path)
            self.kernel.cwd = target_path

        except Exception as e:
            print(f"cd: {e}")