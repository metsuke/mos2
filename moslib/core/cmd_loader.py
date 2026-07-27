import os
import importlib.util

class CommandManager:
    def __init__(self, commands_dir="moslib/commands"):
        
        self.commands_dir = commands_dir
        self.cache = {}
        self.mtimes = {}

    def get_command(self, cmd_name):
        
        file_path = os.path.join(self.commands_dir, f"{cmd_name}.py")
        
        if not os.path.exists(file_path):
            return None

        current_mtime = os.path.getmtime(file_path)
        
        if cmd_name in self.cache and self.mtimes.get(cmd_name) == current_mtime:
            return self.cache[cmd_name]

        spec = importlib.util.spec_from_file_location(cmd_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.cache[cmd_name] = module
        self.mtimes[cmd_name] = current_mtime
        
        return module
