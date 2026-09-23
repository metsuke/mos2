# Changelog de MetsuOS

Los cambios relevantes se listan aquí. Keep a Changelog + docs/VERSIONING.md.

---

## 0.2.8 — pendiente de pruebas humanas
### Añadido

- iarouter modelos / modelo (id con espacios)
- iarouter clave; almacén .mos con moslib.core.secreto
- Ingestión de XAI_API_KEY y OPENROUTER_API_KEY al almacén
- LAN Jan y GPT4All (localhost, cache, /24)
- iarouter share y iarouter publicar
- iarouter puente (HTTP :17337, no es P2P)
- update reiniciar
- Comando docgen
- Integridad de ficheros del repo (manifiesto + sello)
- write / multi / write.sh (lote + codecs)
- test 120 (tope 120 líneas, no bloquea arranque)
- update dev / comando dev
- docs con menú de categorías y sufijo h (HTML)
- Historial de MOSh con tope
- Locale es_ES al arranque (simulación de bloqueo)

### Documentación

- Spec 10 v1.2; man iarouter y man update
- Campaña sync-docs-028
- docs/docgen/ + man docgen
- Refundido pages 2026-09 (JSON fuente + generate; sin bump Poetry)
- IA_WRITE, integridad, tope 120 en onboarding/methodology/style

---

## 0.2.7 — 2026-09-06
### Añadido

- Apps: mini-moslib, install desde clone o repo git
- Prioridad: sistema > app sistema > app usuario > user_
- Worker de tareas en sesión MOSh
- iarouter: detectar, usar, preguntar
- Proveedores Jan, GPT4All, Grok y OpenRouter

### Seguridad

- SEC permite minimoslib solo con app_dir de esa app

---

## 0.2.6 — 2026-09-03
### Añadido

- Specs 08-APPS, 09-TASKS, 10-IA-ROUTER
- Comandos apps, tareas, hilos, iarouter (off por defecto)

---

## 0.2.5-docs.2 — 2026-08-31
### Documentación

- Plan 06 incentivos
- docs/INCENTIVOS.md

---

## 0.2.5 — 2026-08-30
### Añadido

- Comandos a11y, docs, synccheck
- Política A11Y y declaración
- INTERACTION_REVIEW

### Cambiado

- Mensajes de arranque y test en texto, sin emoji como única señal

---

## 0.2.4 — 2026-08-28
### Añadido

- update sincroniza tags con origin

---

## Notas de etiquetas
Los tags v0.2.3-docs y v0.2.4-docs se renombraron a v0.2.2-docs.2 y v0.2.2-docs.3.

---

## 0.2.3 — 2026-08-28
### Corregido

- Poetry: candidato solo si --version funciona
- .gitattributes LF

---

## 0.2.4-docs — 2026-08-28
CHANGELOG como relato; VERSIONING y DEVELOPER_GUIDE; test SemVer Poetry.

---

## 0.2.3-docs — 2026-08-27
Onboarding IA y humano; VERSIONING; hotfix SCRIPT_DIR / WSL.

---

## 0.2.2 — 2026-08-25
ENVIRONMENTS; guard WSL /mnt; Poetry portable.

---

## 0.2.1
Tests de arranque; update backup; man; ECSS-light; AST de imports.

---

## 0.2.0-alpha-user-space
Espacio personal; user_*; protección de comandos de sistema.