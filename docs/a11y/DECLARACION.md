# Declaración de accesibilidad de MetsuOS

**Versión del documento:** 1.0  
**Estado:** Normativo (declaración pública del producto)  
**Documentos relacionados:** docs/A11Y.md, docs/a11y/informe.md, docs/USER_MANUAL.md, docs/specs/04-SEC-Security-Policy.md

---

## Compromiso

Metsuke se ha comprometido a hacer accesible MetsuOS (MOS2), en particular el shell MOSh, los scripts de lanzamiento e instalación y la documentación en `docs/`.

Esta declaración sigue la estructura del modelo europeo de declaración de accesibilidad (Decisión de ejecución (UE) 2018/1523) y las recomendaciones del Portal de Administración Electrónica para el RD 1112/2018, **adaptada a un producto de línea de comandos**.

MetsuOS no es un sitio web ni una aplicación móvil del sector público. Esta declaración **no** afirma obligación legal ni conformidad formal con el Real Decreto 1112/2018. El referente técnico interno es WCAG 2.2 (principios) y UNE-EN 301549 / EN 301 549 / ISO 9241-171 donde aplican a software y CLI. Política: `docs/A11Y.md`.

---

## Ámbito

La presente declaración se aplica a:

- el shell interactivo MOSh
- `mos2.sh` e `install.sh`
- comandos de sistema y el contrato `execute` / `help`
- la documentación del clone bajo `docs/` (incluidos A11Y, esta declaración, el informe, specs, man y planes)
- la consulta de esa documentación mediante el comando de sistema `docs` (cuando exista en esta campaña)

No se aplica a:

- interfaces gráficas (no existen en esta baseline)
- contenidos de terceros ajenos al repositorio
- el sistema operativo anfitrión ni al lector de pantalla que use la persona
- paquetes o páginas fuera del clone

---

## Situación de cumplimiento

MetsuOS es **parcialmente conforme** con su propia política de accesibilidad (`docs/A11Y.md`) en esta baseline Alpha.

Motivos:

- la declaración y la política existen
- los tests automáticos de A11Y y el informe generado aún se están implantando en esta campaña
- hay límites de ámbito (sin GUI, sin laboratorio de lectores de pantalla)

La situación automática vigente se lee en `docs/a11y/informe.md` (y `docs/a11y/informe.json`) tras ejecutar el comando `a11y` o la batería de tests que incluye la marca A11Y. Si el informe no se ha generado todavía, la situación es la de este apartado.

Valores posibles del informe:

| Valor | Significado |
|-------|-------------|
| plenamente conforme | Tests A11Y obligatorios en verde y sin no conformidades abiertas |
| parcialmente conforme | Hay excepciones documentadas o implantación incompleta |
| no conforme | Falla un test A11Y de requisito obligatorio |

---

## Contenido no accesible

El contenido que se recoge a continuación no es accesible, o no está verificado aún, por lo siguiente.

### Falta de conformidad o implantación incompleta

- El informe automático y el comando `a11y` pueden no existir todavía en el árbol hasta cerrar el Grupo II. Hasta entonces no hay revisión automática datada.
- El comando `docs` puede no existir todavía; la documentación se consulta en el sistema de archivos.
- No hay verificación de laboratorio con lectores de pantalla de terminal en esta baseline.
- Puede haber mensajes de error o de seguridad que aún no usen prefijo estable o pista de acción (se corrige en el Bloque 2 de runtime).

### Carga desproporcionada

No aplica en esta declaración. No se invoca carga desproporcionada para dejar fuera un perfil soportado.

### Contenido que queda fuera del ámbito

- GUI, vídeo, audio y widgets visuales (el producto no los incluye)
- Contraste y zoom del emulador de terminal del anfitrión
- Documentación o software de terceros
- Sonido: MetsuOS no usa audio; el perfil sordera se declara cubierto por no dependencia de sonido

---

## Preparación de la presente declaración

- Fecha de preparación: 2026-08-29
- Método: autoevaluación del propio proyecto (inspección de documentación y, cuando existan, tests automáticos A11Y)
- Última revisión de esta declaración: 2026-08-29
- Última revisión automática del producto: ver `docs/a11y/informe.md` (si el informe indica que aún no ha habido una primera ejecución, no hay revisión automática)

La declaración se actualizará al menos cuando cambie la política A11Y, cuando se publique una baseline de producto que mueva la situación de cumplimiento, o cuando el informe automático deje de coincidir con este texto.

---

## Comunicaciones

Se pueden enviar comunicaciones sobre accesibilidad, por ejemplo:

- informar de un posible incumplimiento
- transmitir una dificultad de acceso
- pedir información en formato más usable
- formular una queja

Canal en esta baseline Alpha:

- documentar el hallazgo de forma que pueda leerse con el comando `docs` o en `docs/a11y/`
- contacto del proyecto: sitio web https://metsuke.com y repositorio público del producto (el clone local no fija un forge concreto)

No se publican correos ni rutas personales en el repositorio.

---

## Procedimiento de reclamación

Si la respuesta a una comunicación no es satisfactoria, en esta fase Alpha el procedimiento es:

1. Dejar constancia escrita del problema y del perfil afectado (teclado, lector de terminal, baja visión, daltonismo, carga cognitiva, audio N/A).
2. Pedir revisión frente a `docs/A11Y.md` y a los `REQ-A11Y-*` del SRS.
3. Si hay conflicto con seguridad, aplicar el procedimiento de `docs/A11Y.md` (prevalece A11Y para no excluir el perfil; SEC no se recorta en silencio).

No existe aún una unidad administrativa de accesibilidad ni un procedimiento de supervisión pública: el producto no es una sede del sector público.

---

## Cómo consultar esta declaración en el sistema

Cuando el comando `docs` esté implantado:

```text
docs
docs a11y/DECLARACION.md
docs A11Y.md
docs a11y/informe.md
```

Hasta entonces, los mismos paths relativos a `docs/` en el clone.

Validación automática, cuando exista el comando:

```text
a11y
```

---

## Autoridad

Esta declaración es el texto público de cumplimiento adaptado.  
La política férrea está en `docs/A11Y.md`.  
El detalle medible de la última ejecución automática está en `docs/a11y/informe.md`.