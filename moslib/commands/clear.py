import os

def execute(args):
    os.system('cls' if os.name == 'nt' else 'clear')

def help():
    return "Uso: clear - Limpia la pantalla de la terminal."
