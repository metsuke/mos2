    if len(branches) <= keep:
        return
    for branch in branches[:-keep]:
        print(f"[update] Eliminando rama de backup antigua: {branch}")
        run(["git", "branch", "-D", branch], cwd, check=False)
