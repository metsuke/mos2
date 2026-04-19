#!/usr/bin/env /Users/Metsuke/mos2/.venv/bin/python
import sys
import os
import time

# Añadir raíz al path para localizar moslib
sys.path.append("/Users/Metsuke/mos2")
from moslib import memo, disk

@disk
def boot_test():
    return "Kernel mos2 Online"

if __name__ == "__main__":
    print(boot_test())
    print("Path del intérprete:", sys.executable)
