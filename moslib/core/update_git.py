"""Git de update: backup, prune, fetch tags."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run(cmd, cwd, check=True):
    result = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error ejecutando: {' '.join(cmd)}")
        if result.stderr:
            print(result.stderr.strip())
        sys.exit(result.returncode)
    return result


def has_pending_changes(cwd: Path) -> bool:
    result = run(["git", "status", "--porcelain"], cwd, check=False)
    return bool(result.stdout.strip())


def create_backup_branch(cwd: Path) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    branch_name = f"backup/{timestamp}"
    print(f"[update] Creando rama de backup: {branch_name}")
    run(["git", "checkout", "-b", branch_name], cwd)
    if has_pending_changes(cwd):
        run(["git", "add", "-A"], cwd)
        run(
            ["git", "commit", "-m", f"Backup automático antes de update ({timestamp})"],
            cwd,
            check=False,
        )
    return branch_name


def prune_old_backups(cwd: Path, keep: int = 10):
    result = run(["git", "branch", "--list", "backup/*"], cwd, check=False)
    branches = [
        line.strip().lstrip("* ").strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]
    branches = sorted(branches)
    if len(branches) <= keep:
        return
    for branch in branches[:-keep]:
        print(f"[update] Eliminando rama de backup antigua: {branch}")
        run(["git", "branch", "-D", branch], cwd, check=False)


def sync_tags_with_origin(cwd: Path):
    print("[update] Sincronizando tags con origin...")
    run(["git", "fetch", "origin", "--tags", "--prune", "--prune-tags"], cwd)
