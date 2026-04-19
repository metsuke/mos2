import os
import getpass
import platform
from pathlib import Path

class Kernel:
    def __init__(self, project_root):
        """
        Inicializa el núcleo del sistema MOS2.
        Establece la identidad, las rutas virtuales y los puntos de montaje.
        """
        # 1. Identidad y Contexto del Host
        self.project_root = Path(project_root).resolve()
        self.user = getpass.getuser()
        self.hostname = platform.node()
        self.os_type = platform.system()
        
        # 2. Tabla de Montajes (VFS: Virtual File System)
        # Mapeamos rutas lógicas a rutas físicas dentro del proyecto
        self.mounts = {
            "/": self.project_root,
            f"/home/{self.user}": self.project_root / "home" / self.user,
            "/etc": self.project_root / "etc",
            "/bin": self.project_root / "bin"
        }
        
        # 3. Configuración del Espacio de Usuario (Home)
        self.virtual_home = self.mounts[f"/home/{self.user}"]
        
        # Aseguramos que la carpeta de usuario exista físicamente en el proyecto
        os.makedirs(self.virtual_home, exist_ok=True)
        
        # 4. Estado Inicial del Proceso
        # Al arrancar, situamos al usuario en su HOME virtual
        self.cwd = self.virtual_home
        os.chdir(self.cwd)
        
    def boot(self):
        """Muestra la secuencia de arranque en la consola."""
        print(f"--- MOS2 System Booting ---")
        print(f"Kernel: OS {self.os_type} detectado.")
        print(f"Kernel: Modo Autónomo Activo.")
        print(f"Kernel: {len(self.mounts)} puntos de montaje inicializados.")
        print(f"Kernel: Sesión iniciada para '{self.user}'.\n")

    def get_prompt_info(self):
        """
        Genera la cadena de texto para el prompt del shell traduciendo 
        rutas físicas a rutas lógicas de MOS2.
        """
        try:
            # Caso: Estamos dentro de nuestro Home Virtual
            if str(self.cwd).startswith(str(self.virtual_home)):
                rel_path = os.path.relpath(self.cwd, self.virtual_home)
                display_path = "~" if rel_path == "." else f"~/{rel_path}"
            
            # Caso: Estamos en la raíz o carpetas de sistema de MOS2
            elif str(self.cwd).startswith(str(self.project_root)):
                rel_path = os.path.relpath(self.cwd, self.project_root)
                display_path = "/" if rel_path == "." else f"/{rel_path}"
            
            # Caso: Estamos fuera de la estructura de MOS2
            else:
                display_path = self.cwd
        except Exception:
            display_path = "?"
            
        # Verde Bright para usuario, Cyan Bright para ruta
        user_host = f"\033[1;92m{self.user}@{self.hostname}\033[0m"
        path_color = f"\033[1;96m{display_path}\033[0m"
        
        return f"{user_host}\033[1;97m:\033[0m{path_color}"

    def translate_path(self, virtual_path):
        """
        Traduce una ruta virtual a una ruta física absoluta.
        Útil para futuros comandos de montaje externos.
        """
        if virtual_path.startswith("~"):
            return Path(str(virtual_path).replace("~", str(self.virtual_home)))
        
        # Por ahora resolvemos relativo a la raíz del proyecto
        return (self.project_root / virtual_path.lstrip("/")).resolve()