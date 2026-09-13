# 02 – SRS · Requisitos software

**Versión del documento:** 1.3  
**Baseline de referencia:** v0.2.7 / árbol v0.2.8  
**Estado:** Normativo

Formato REQ-AREA-NNN. Áreas: SYS, CMD, USER, SEC, BOOT, TEST, DOC, UPD, PLAT, A11Y, APP, TASK, IA.

Los requisitos de la v1.2 (SYS, CMD-001 a CMD-015, USER, SEC, BOOT, TEST-001 a TEST-009, UPD-001 a UPD-006, DOC-001 a DOC-011, PLAT, A11Y) siguen Must.

## Ampliación CMD / UPD

| ID | Requisito | Prioridad | Verificación |
|----|-----------|-----------|--------------|
| REQ-CMD-016 | Baseline actual incluye a11y, docs, synccheck, apps, tareas, hilos, iarouter, red | Must | Inspection / Demo |
| REQ-CMD-017 | help y man cubren comandos de app cargados | Must | Demo / Test |
| REQ-CMD-018 | Prioridad: sistema > app sistema > app usuario > user_completo > user_corto | Must | Test |
| REQ-CMD-019 | Comando red de diagnóstico de anfitrión, no malla P2P | Must | Demo / Inspection |
| REQ-UPD-007 | update reiniciar: módulos de sesión no se sustituyen solos | Must | Demo / Inspection |

## APP

REQ-APP-001 metadatos de app. REQ-APP-002 comando apps install/list/show/remove. REQ-APP-003 ámbito usuario o sistema. REQ-APP-004 misma puerta AST. REQ-APP-005 minimoslib solo con app_dir. REQ-APP-006 no pisa sistema. REQ-APP-007 A11Y mínima o no se ejecuta. REQ-APP-008 fuente en apps/<id>/ (Should).

## TASK

REQ-TASK-001 moslib.core.tasks. REQ-TASK-002 comando tareas. REQ-TASK-003 comando hilos. REQ-TASK-004 bloqueada_a11y_sec no ejecuta. REQ-TASK-005 clase sistema reencola. REQ-TASK-006 worker local de sesión, no P2P.

## IA

REQ-IA-001 fachada en moslib, sin HTTP en el comando. REQ-IA-002 enabled=false sin red. REQ-IA-003 jan, gpt4all, grok, openrouter. REQ-IA-004 solo preguntar/complete envía. REQ-IA-005 claves .mos no se imprimen. REQ-IA-006 ingesta XAI_API_KEY y OPENROUTER_API_KEY. REQ-IA-007 rechazo .mos no allowlist. REQ-IA-008 share ≠ publicar. REQ-IA-009 puente :17337 off, no P2P. REQ-IA-010 modelo con espacios. REQ-IA-011 error usable, shell vivo.

Un Must violado no entra en main sin actualizar este SRS.
