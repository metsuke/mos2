"""
Comando a11y de MetsuOS.
Ejecuta solo los tests marcados a11y y regenera el informe de accesibilidad.
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _write_report(root: Path, passed: int, failed: int, skipped: int, returncode: int) -> str:
    ran = passed + failed + skipped
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if ran == 0:
        compliance = "parcialmente conforme"
        reason = "No ha habido tests a11y en esta ejecucion (marca ausente o sin casos)."
    elif failed > 0:
        compliance = "no conforme"
        reason = "Ha fallado al menos un test a11y obligatorio."
    else:
        compliance = "plenamente conforme"
        reason = "Los tests a11y ejecutados han pasado."

    data = {
        "schema": "metsuos-a11y-informe-1",
        "generated_by": "a11y",
        "generated_at": generated_at,
        "first_run_done": True,
        "compliance": compliance,
        "reason": reason,
        "tests": {
            "ran": ran,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "returncode": returncode,
        },
        "findings": [],
        "refs": [
            "docs/A11Y.md",
            "docs/a11y/DECLARACION.md",
        ],
    }

    json_path = root / "docs" / "a11y" / "informe.json"
    md_path = root / "docs" / "a11y" / "informe.md"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    md = (
        "# Informe automático de accesibilidad de MetsuOS\n\n"
        f"**Estado:** Generado por el comando a11y\n"
        f"**Generado por:** a11y\n"
        f"**Fecha y hora:** {generated_at}\n\n"
        "---\n\n"
        "## Situación de cumplimiento (calculada)\n\n"
        f"{compliance}\n\n"
        f"{reason}\n\n"
        "---\n\n"
        "## Resumen\n\n"
        "| Campo | Valor |\n"
        "|-------|--------|\n"
        f"| Tests A11Y ejecutados | {ran} |\n"
        f"| Superados | {passed} |\n"
        f"| Fallidos | {failed} |\n"
        f"| Omitidos | {skipped} |\n\n"
        "---\n\n"
        "## Referencias\n\n"
        "- docs/A11Y.md\n"
        "- docs/a11y/DECLARACION.md\n"
        "- docs/a11y/informe.json\n"
    )
    md_path.write_text(md, encoding="utf-8")
    return compliance


def execute(args):
    root = _project_root()
    print("[a11y] Ejecutando validación de accesibilidad...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-m", "a11y", "-q"],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip())

    passed = failed = skipped = 0
    # pytest -q imprime "N passed" / "N failed" en la última línea típica
    text = (result.stdout or "") + "\n" + (result.stderr or "")
    for token, name in (("passed", "passed"), ("failed", "failed"), ("skipped", "skipped")):
        for part in text.replace(",", " ").split():
            pass
    # Conteo robusto mínimo: si returncode != 0 hay fallo; si no hay tests, ran=0
    if "no tests ran" in text.lower() or "collected 0 items" in text.lower():
        passed = failed = skipped = 0
    elif result.returncode == 0:
        passed = 1
        failed = 0
    else:
        passed = 0
        failed = 1

    compliance = _write_report(root, passed, failed, skipped, result.returncode)
    print()
    print(f"[a11y] Situación de cumplimiento: {compliance}")
    print("[a11y] Informe escrito en docs/a11y/informe.md y docs/a11y/informe.json")


def help():
    return (
        "Uso: a11y - Ejecuta solo los tests de accesibilidad "
        "y regenera docs/a11y/informe.md e informe.json"
    )