# Campaña: espacio de usuario y comandos personales

**Fecha del plan:** 2026-08-12  
**NN del día:** 01  
**Estado:** Cerrada  
**Origen:** Reconstrucción a posteriori (el plan vivió solo en el chat)

---

## Objetivo

Dar a cada usuario del sistema anfitrión un espacio personal que no se sube al repo, con comandos propios gestionables sin pisar el sistema.

## Fuera de alcance

- Instalar paquetes Python de terceros en comandos
- Sobrescribir comandos oficiales
- Gestor de paquetes Linux real

---

## Normas férreas que salieron de esta campaña

- Todo comando pasa por moslib y el contrato `execute` / `help`
- Solo imports de biblioteca estándar y moslib
- Comandos de usuario: archivo `user_*.py`
- Invocación `user_hola` siempre; `hola` solo si no existe comando de sistema
- Home = usuario real del anfitrión, no hardcodeado
- Migración si el home legacy existía en otra ruta

---

## Qué se ejecutó (resumen)

- Módulo de usuario y rutas bajo `rootfs/home/<usuario>/.mos/`
- Carga de comandos de sistema + usuario
- `help` lista sistema primero y luego usuario; indica el origen
- README y comportamiento de invocación corta

---

## Producto

| Momento | Valor |
|---------|--------|
| Inicio | Anterior a espacio de usuario |
| Cierre | Tag `v0.2.0-alpha-user-space` |

## Tags

- `v0.2.0-alpha-user-space`

---

## Notas de reconstrucción

Fechas y desglose fino de commits no se recuperan aquí con exactitud de diario. El resultado en `main` y el tag son la fuente de verdad.