import sys
import os

# Añadimos la raíz al path para que los imports desde mos2.moslib funcionen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from moslib.core.shell import MOSh

if __name__ == "__main__":
    shell = MOSh()
    shell.run()
