import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from moslib.core.shell import MOSh

if __name__ == "__main__":
    shell = MOSh()
    shell.run()