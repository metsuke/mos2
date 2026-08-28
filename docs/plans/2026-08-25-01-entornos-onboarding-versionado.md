# Campaña: entornos, onboarding y versionado

**Fecha del plan:** 2026-08-25  
**NN del día:** 01  
**Estado:** Cerrada  
**Origen:** Reconstrucción a posteriori

---

## Objetivo

Hacer el lanzador portable entre Mac, Git Bash y WSL; documentar perfiles anónimos; onboarding para IA y humanos; política de versiones y CHANGELOG.

## Fuera de alcance

- Rutas o nombres de máquina personales en el repo
- Mover clones WSL en silencio
- CI externa

---

## Qué se ejecutó (resumen)

- `resolve_poetry` en `mos2.sh` e `install.sh`
- Git Bash: priorizar `py -m poetry` (Permission denied en `poetry.exe`)
- `docs/ENVIRONMENTS.md` y protocolo `Contexto: sistema / entorno / rol`
- Guard WSL: no ejecutar desde `/mnt/<letra>/`; `SCRIPT_DIR` antes del check
- `docs/VERSIONING.md`, `AGENTS.md`, onboarding IA/humano, `DEVELOPER_GUIDE.md`
- README / METHODOLOGY / OVERVIEW enlazados
- `CHANGELOG.md` y test SemVer de `pyproject.toml`

---

## Producto

| Momento | Valor |
|---------|--------|
| Inicio | `v0.2.1` |
| Cierre código | `v0.2.2` (Poetry portable + guard WSL) |
| Cierre docs | `v0.2.3-docs`, `v0.2.4-docs` |

## Tags

- `v0.2.2`
- `v0.2.2-docs`
- `v0.2.3-docs`
- `v0.2.4-docs`

---

## Notas de reconstrucción

En el chat esto fueron “bloques 0 / 0.1 / 1 / 2”. Aquí es una sola campaña porque el hilo era el mismo: poder trabajar en varios entornos y no perder el contexto entre chats.