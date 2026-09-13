# 08 – Apps

**Versión del documento:** 1.1  
**Estado:** Normativo (implementado en producto 0.2.7)  
**Baseline:** v0.2.7  
**Documentos relacionados:** docs/specs/01-SSS-System-Specification.md, docs/specs/03-ICD-Interfaces-and-Command-Contract.md, docs/specs/04-SEC-Security-Policy.md, docs/A11Y.md, docs/INCENTIVOS.md, docs/man/apps.md

---

## Propósito

Definir qué es una **app** en MetsuOS, cómo se relaciona con el núcleo y qué debe cumplir para cargarse.

No describe la suite de desarrollo completa (campaña 08 de producto), ni la malla (campaña 10), ni DepManager.

---

## Qué es y qué no es

Una app es un paquete con **identidad propia**, **repo propio** (o árbol equivalente) y **uno o más comandos** que se ejecutan dentro de MOSh.

No es un archivo suelto en `moslib/commands/`.  
No sustituye el núcleo.  
No puede importar fuera de stdlib + moslib + su mini-moslib declarado (SEC: `minimoslib` solo con `app_dir` de esa app).

---

## Metadatos estables

| Campo | Obligatorio | Notas |
|-------|-------------|-------|
| id | sí | slug estable |
| nombre | sí | visible en help |
| version | sí | SemVer |
| repo | no | URL o ruta |
| comandos | sí | lista de módulos execute/help |
| mini_moslib | no | solo lo que el núcleo aún no da |
| acceso | sí | quién instala/usa |
| docs | sí | man/specs propios sujetos a A11Y/SEC/SSS |

Ampliar campos en versiones posteriores de este spec. No renombrar estos.

---

## Ciclo de vida (producto 0.2.7)

| Acción | Estado |
|--------|--------|
| Instalar desde path local (clone) | sí |
| Instalar desde repo git | sí |
| Ámbito usuario o sistema | sí |
| Listar instaladas | sí |
| Ver metadatos | sí |
| Quitar | sí |
| Tienda remota / firmas de autor | no |

Directorios:

| Ámbito | Ubicación |
|--------|-----------|
| usuario | `rootfs/home/<usuario>/.mos/apps/` |
| sistema | prefijo de sistema no versionado como producto del núcleo |
| fuente en repo | `apps/<id>/` (ejemplo versionado: `apps/dev`) |

No mezclar comandos de app con `moslib/commands/`.

---

## Carga y normas férreas

El núcleo descubre apps instaladas y carga sus comandos con **la misma** validación que un comando de sistema:

- `execute(args)` y `help()` → str
- AST: solo stdlib + moslib (+ mini-moslib de esa app, si el loader lo admite de forma explícita)
- Nombre de comando de app no pisa un comando de sistema
- Invocación: nombre corto, `id_cmd` y `app_id_cmd`
- Prioridad de resolución (ICD): sistema > app sistema > app usuario > user_
- A11Y: help usable, texto lineal, no solo-color; si no cumple, no se acepta ni se ejecuta
- SEC: import ilegal → no carga

Mini-moslib: el resto del sistema **no** importa esa mini-lib. Solo comandos de esa app. Subida al moslib central = PR / campaña.

---

## Acceso

| Valor | Significado |
|-------|-------------|
| local-owner / usuario | Usuario anfitrión de este clone |
| system | Instalación de ámbito sistema en esta máquina |

---

## App de producto en el árbol

| Nivel 1 | Nivel 2 | Nivel 3 | Descripción |
|---------|---------|---------|-------------|
| apps/ | dev/ | app.json | Metadatos de la app de desarrollo |
| apps/ | dev/ | commands/ | Comandos de la app |
| apps/ | dev/ | man/ | Man propios |

---

## Criterios de aceptación

1. Spec publicado y alineado con el loader.
2. Tests `tests/test_apps.py`, `test_cmd_loader_apps.py`, `test_security_minimoslib.py` en verde.
3. Fixture con import ilegal no carga.
4. Fixture que pisa un comando de sistema no carga.
5. Sin A11Y mínima no se acepta ni se ejecuta.

---

## Autoridad

Normativo para apps. Choca con SEC/A11Y/SSS → ganan esas y se versiona este archivo.
