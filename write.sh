#!/usr/bin/env python3
"""Lanza multi real. Sin emular el lote en bash."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from moslib.commands.multi import execute

if __name__ == "__main__":
    execute([])
