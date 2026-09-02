# 08 – Apps

**Versión del documento:** 1.0  
**Estado:** Normativo (campaña 07, frente A)  
**Baseline:** v0.2.5  
**Documentos relacionados:** docs/specs/01-SSS-System-Specification.md, docs/specs/04-SEC-Security-Policy.md, docs/A11Y.md, docs/INCENTIVOS.md, docs/plans/2026-09-01-02-campana-07-soporte-apps-tareas-ia.md

---

## Propósito

Definir qué es una **app** en MetsuOS, cómo se relaciona con el núcleo y qué debe cumplir para cargarse.

No describe la suite de desarrollo (08), ni la malla (10), ni DepManager.

---

## Qué es y qué no es

Una app es un paquete con **identidad propia**, **repo propio** (o árbol equivalente) y **uno o más comandos** que se ejecutan dentro de MOSh.

No es un archivo suelto en `moslib/commands/`.  
No sustituye el núcleo.  
No puede importar fuera de stdlib + moslib + su mini-moslib declarado.

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
| acceso | sí | quién instala/usa (mínimo: local-owner) |
| docs | sí | man/specs propios sujetos a A11Y/SEC/SSS |

Ampliar campos en versiones posteriores de este spec. No renombrar estos.

---

## Ciclo de vida (07)

| Acción | 07 implementa |
|--------|----------------|
| Instalar desde path local | sí |
| Listar instaladas | sí |
| Ver metadatos | sí |
| Quitar | sí |
| Tienda remota / firmas de autor | no (spec reserva el campo acceso) |

Directorio de instalación: se fija en ICD al implementar. Candidatos: `rootfs/home/<usuario>/.mos/apps/` (usuario) y un prefijo de sistema no versionado. No mezclar con `moslib/commands/`.

---

## Carga y normas férreas

El núcleo descubre apps instaladas y carga sus comandos con **la misma** validación que un comando de sistema:

- `execute(args)` y `help()` → str
- AST: solo stdlib + moslib (+ mini-moslib de esa app, si el loader lo admite de forma explícita)
- Nombre de comando de app no pisa un comando de sistema
- Prefijo recomendado: `app_<id>_` o namespace de la app; se concreta en ICD
- A11Y: si la app no cumple el mínimo de docs/A11Y.md (help usable, texto lineal, no solo-color), **no se acepta en desarrollo y no se ejecuta**
- SEC: import ilegal → no carga; tests de arranque deben ver las apps instaladas del usuario actual o un inventario declarado

Mini-moslib: el resto del sistema **no** importa esa mini-lib. Solo comandos de esa app. Subida al moslib central = PR / campaña, no un copy silencioso.

---

## Acceso (mínimo 07)

| Valor | Significado |
|-------|-------------|
| local-owner | Solo el usuario anfitrión de este clone |
| system | Reservado; no implementar tienda en 07 |

Quién “tiene la app” lo decide el desarrollador de la app en metadatos; el núcleo en 07 solo respeta local-owner.

---

## Criterios de aceptación del frente A

1. Spec publicado (este archivo).
2. Fixture de app de prueba instala, lista, ejecuta un comando legal, se desinstala.
3. Fixture con import ilegal no carga.
4. Fixture que pisa un comando de sistema no carga.
5. Sin A11Y mínima no se acepta ni se ejecuta.

---

## Autoridad

Normativo para apps. Choca con SEC/A11Y/SSS → ganan esas y se versiona este archivo.