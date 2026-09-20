# AGENTS.md Punto de entrada para IA (MetsuOS / MOS2)

Si eres un agente o modelo y te piden estudiar este repositorio, empieza aquí y en docs/AI_ONBOARDING.md.

## Lectura mínima
1. Este archivo
2. docs/AI_ONBOARDING.md
3. docs/INCENTIVES.md
4. docs/METHODOLOGY.md
5. docs/INTERACTION_REVIEW.md
6. docs/ENVIRONMENTS.md
7. docs/VERSIONING.md
8. docs/A11Y.md y docs/a11y/DECLARATION.md
9. docs/STYLE_GUIDE.md
10. docs/specs/00-OVERVIEW.md
11. docs/plans/ si hay campaña
12. Código y resto de specs según la tarea

## Escritura segura (obligatorio en chats nuevos)
La IA no edita el disco. Entrega lotes para que el humano los pegue.

Dentro de MOS:
1. Comando m (alias de multi).
2. Línea: write <ruta-desde-la-raíz-del-clone>
3. Siguiente línea: sha256 hex de los bytes UTF-8 del fichero entero (64 caracteres).
4. Siguiente línea(s): Base64 de esos mismos bytes.
5. Línea solo con un punto (.) cierra el payload.
6. Se pueden encadenar hasta tres write si los ficheros son pequeños.
7. :e ejecuta el lote. ;e y ;q se aceptan como :e y :q. El canónico es :e.
8. write solo funciona dentro de multi. Si el hash no coincide, no se toca el destino (backup temporal y restauración).
9. Tras un write OK, write abre code sobre el fichero.

Fuera de MOS (integridad rota, tests de arranque tirando el sistema):
- ./write.sh en la raíz del clone (junto a install.sh).
- Se pega el mismo lote write/hash/b64/. y se cierra con :e.
- write.sh escribe si el hash coincide e intenta registrar integridad; si MOS/python no importan, avisa y se acepta al arrancar.

Prohibido:
- Parches o fragmentos. Fichero entero siempre.
- Inventar el hash. Se calcula sobre los bytes que van en el Base64.
- Usar raw.githubusercontent.com para leer el repo (API o clone).
- cd a la ruta del clone en las instrucciones; el humano ya está en la raíz o usa sus alias.

## Tope de tamaño y ramas
- Ningún .py de moslib (core o commands) puede superar 120 líneas. Si se pasa, se trocea en submódulos y un fachada delgada. Consulta: test 120 (no tumba el arranque; lista y total).
- No se avanza sobre main. Rama paralela aunque el cambio sea pequeño.
- git commit/push/merge/rebase sobre main desde MOS están bloqueados.
- update (a secas): solo origin/main y árbol limpio. Si el árbol está sucio, se niega.
- update dev: lista ramas remotas ≠ main, se elige por número, checkout+pull.
- dev publicar: commit automático wip de prueba en otras máquinas + push de la rama actual. Prohibido en main.
- dev consolidar: ff-only a main, push, borra la rama. Si no hay fast-forward, no borra.
- Primera vez en una máquina antigua: update a main (el huevo y la gallina de update dev).

## Integridad
- Manifiesto repo: docs/docgen/integridad.json + sello .sha256.
- Copia de trabajo en el .mos del usuario.
- Si al comprobar no hay copia local o falta el sello, el sistema copia solo el manifiesto del repo. El usuario no ejecuta recargar a mano en un arranque limpio.
- Tras generar documentación, los destinos (md y html) se registran.
- integridad aceptar <ruta> solo para un fichero que el humano acaba de generar o escribir con write.

## Documentación y docgen
- Fuente: JSON en docs/docgen/ (man/, specs/, pages/, root/, reqs/, plans/, areas.json).
- El markdown publicado se obtiene con docgen generate. No se edita el .md a mano.
- Requisitos: un JSON por REQ. Alta/cambio con docgen req add|set|rm o editando ese JSON.
- Áreas y planes: CRUD sobre JSON, luego generate.
- ingest solo primera vez o recuperación desde backup.
- :s o ;s en el chat significan siguiente paso de la campaña.
- Un lote, como mucho tres ficheros pequeños. Fichero entero. No parches.

## Normas que no se improvisan
- Comandos: execute(args) y help() -> str. sinopsis() lista opciones reales del código.
- Imports en comandos: solo biblioteca estándar y moslib.
- Tests de arranque bloqueantes salvo test 120.
- Accesibilidad de interfaz mandatoria (docs/A11Y.md).
- Sin rutas personales ni nombres de máquina en docs públicas.
- Git del anfitrión sobre la raíz del clone; no funciones exclusivas de un forge.
- No diagnosticar el repo solo con raw.githubusercontent.com.

## Contexto de sesión
Contexto: <sistema> / <entorno> / <rol>
Si falta y hace falta paths o Poetry, preguntar.

## Qué no hacer
- No inventar features ausentes en código o specs.
- No desactivar seguridad ni tests para pasar.
- No excluir A11Y por comodidad.
- No asumir Mac, Git Bash o WSL sin contexto declarado.
- No usar ingest como rutina diaria.
- No consolidar a main con árbol sucio o tests rojos.