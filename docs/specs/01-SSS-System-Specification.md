# 01 – SSS · Especificación de sistema

**Versión del documento:** 1.4  
**Baseline de referencia:** v0.2.7 / árbol v0.2.8  
**Estado:** Normativo  
**Documentos relacionados:** docs/specs/00-OVERVIEW.md, docs/specs/04-SEC-Security-Policy.md, docs/specs/08-APPS.md, docs/specs/09-TASKS.md, docs/specs/10-IA-ROUTER.md, docs/A11Y.md, docs/ENVIRONMENTS.md

---

## Propósito

Qué es MetsuOS a nivel de sistema, objetivos, no-objetivos y normas no negociables.

---

## Identificación

| Campo | Valor |
|-------|-------|
| Nombre | MetsuOS |
| Nombre alternativo | MOS2 |
| Tipo | Sistema operativo simulado y modular |
| Shell | MOSh |
| Lenguaje | Python 3.10+ |
| Licencia | GPL-3.0 |
| Estado | Alpha |
| Baseline actual | v0.2.7 en Poetry; v0.2.8 en árbol pendiente de pruebas humanas |

---

## Definición

MetsuOS proporciona shell MOSh, núcleo moslib, rootfs, espacio personal por usuario anfitrión, comandos Python (sistema, app, usuario), validación AST, tests de arranque, A11Y CLI, apps (path o git), tareas e hilos locales, fachada de modelos off por defecto, docs/man/a11y/synccheck/update/red.

Se ejecuta sobre un anfitrión. No reemplaza el kernel.

## Objetivos

1. Shell modular auditable. 2. Comandos sistema/app/usuario con reglas. 3. Aislamiento .mos. 4. Política SEC. 5. Agnosticismo ENVIRONMENTS. 6. Evolución con specs y tests. 7. No excluir perfiles A11Y.

## No-objetivos

Kernel real; virtualizar hardware; sustituir usuarios del anfitrión; pip arbitrario en comandos; POSIX completo; multiplexar como OS nativo; atacante con escritura en moslib; RD 1112/2018; GUI/WCAG web; malla P2P; tienda remota firmada; arreglar Grok dentro de X.

## Normas no negociables

A11Y mandatoria. Lógica por moslib. Imports: stdlib + moslib (+ minimoslib de esa app). Usuario/app no pisan sistema. execute/help. .mos no versionado. Tests de arranque bloqueantes. Perfiles linux/macos/git-bash/wsl. iarouter off hasta política humana. Claves de IA no se imprimen.

## Comandos de sistema requeridos

| Tipo | Comando | Función |
|------|---------|---------|
| accesibilidad | a11y | Informe A11Y |
| apps | apps | Ciclo de apps |
| ayuda | docs, help, man | Documentación |
| calidad | synccheck, test, update | Calidad y sync |
| host | sysinfo, uptime, version | Anfitrión |
| ia | iarouter | Modelos |
| red | red | Red anfitrión |
| sesion | exit | Builtin |
| tareas | hilos, tareas | GTD local |
| utilidad | clear, echo | Utilidad |

## Criterios de aceptación alpha

Arranque solo con tests verdes; comandos de la tabla; rechazo SEC en sistema/app/usuario; .mos fuera de git de producto; update+tags; docs/; ENVIRONMENTS; declaración A11Y; iarouter sin red si enabled=false.

## Capacidades 0.2.6–0.2.8

Normativo en 08, 09 y 10. El código está en el árbol. Tag 0.2.8: pruebas humanas.

## Autoridad

Cambio de objetivos o normas férreas se versiona aquí antes o junto al código.
