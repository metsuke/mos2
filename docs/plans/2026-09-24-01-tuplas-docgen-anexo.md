# Anexo al plan 2026-09-24-01 — Prompt, planteamiento y conclusión

Documento de trabajo ligado a `docs/plans/2026-09-24-01-tuplas-docgen.md`.
No es normativo de producto; es la traza de diseño para esta campaña y para la posterior de código.

---

## A. Prompt original del diseñador (íntegro)

Durante el proceso que hemos llevado a cabo para actualizar y evolucionar los documentos que originalmente escribiamos directamente en .md, hemos aplicado - si no me equivoco - dos metodos principales, el primero es del ingesta a un .json, generacion genaralista a .md desde el y luego el metodo mediante CRUD en el que definimos los Requisitos del sistema y, desde ellos, se regenera la lista completa de requisitos con tablas.

Parecido al de los requisitos es el de la sinopsis de los comandos en man, que esencialmente es un CRUD pequeño similar a ese metodo.

La problematica que hemos enfrentado con el JSON, especialmente la dificultad de mantener la consistencia de la documentacion y el razonamiento asociado a cada uno de los elementos incluidos, modificados o eliminados de la documentacion.

En conclusion lo que creo que debemos hacer es:

1. Adoptar un metodo equivalente al CRUD de Requisitos para todos los documentos, todas las secciones de los documentos y todos los elementos dentro de los encabezado (secciones) de los documentos.

2. Para ello, en primer lugar completar el metodo de Requisitos añadiendo a cada requisito una descripcion orientada no a visualizar sino a explicar al humano porque esta ahi a efectos de desarrollo y diseño, otro elemento para IA con la explicacion equivalente en terminos que un agente IA pueda interpretar y usar con el menos esfuerzo posible y maxima eficacia, un tercer elemento con el orden numerico en que deben ser renderizados despues, un campo con la explicacion de porque ese orden y no otro, que usaran tanto humano como IA cuando precisen reorganizar. En el futuro habra dos campos en forma de lista con los elementos cuyua logica lleva a la creacion y configuracion del elemento y otro con la lista de los elementos relacionados que toman la logica del actual como fuente para deducir el requisito actual, fecha de inclucisón, fecha de modificacion. Estas relaciones entre elementos mediante ID, en esta primera fase se circunscriben a los propios requisitos mmediante algo univoco, como req/IO_REQ

3. Una vez hecho esto, el siguiente paso seria aplicar este metodo, generalizando su funcionamiento y estructura para cubrir todos y cada una de las secciones de todos y cada uno de los documentos, del siguiente modo:

3.1 La lista de documentos registrados, debe incluir campos orden, logica detras de ese orden en formato texto, logica de su existencia y formato para ia, lo mismo para humano, lista de documentos que originan la existencia de este (al estilo de las relaciones de requisitos), lista de documentos cuya existencia se ve influida o justificada pora el documento actual, fecha de nclusion , fecha de modificacion,en esencia los mismos que los requisitos (si no me equivico)

3.2 Cada documento tiene que tener una lista de secciones que serán obligatorias del documento, al estilo requisitos en cuanto a formato de tupla, por cada seccion lo mismo , orden, explicacion del orden ,etc. Llamare TUPLA en este prompt a esa estructura de campos para no repetirme. Este documento permite trazar, ordenar y razonar las secciones de cada documento, su orden y forzar su existencia con posterioridad.

3.3. Dentro de cada seccion de cada doumento, misma historia, una serie de elementos TUPLA con CRUD, con un pequeño elemento adicional, si se renderiza como parrafo, o tabla (un campo nuevo para TUPLA que quiza debemos evaluar añadir a todo), tiene que haber algun lugar donde se defina (quiza otro bloque TUPLA CRUD) los modos de render, que ahora son parrafo, tabla (si hay varios elementos tabla consecutivos en funcion del orden, se pinta una tabla con todos, de forma que las tablas sean dinamicamente definidas), quiza tambien podamos incluoir h1 a h6, imagen, grafico con mermaid y las que se te ocurran para dotar de un lenguiaje comuinicativo mas rico al sistema. El objetivo es que al renderizar directamente se recorra la lista pintando segun las indicaciones al md (de ahi luego ya renderizaremos a html o a otros formatos).

3.4 Esta estructura tambien implicaria que las listas de elementos que influyem en el actuial o en los que influye, se puedan articualr con una suerte de rutas que indiquen por ejemplo documento/seccion/elemento que influyen en o influyen a, de forma que la logica coherente entre los elementos esté garantizada.

3.5 Todo esto implica crear un nuevo codigo de gestion que generalice esta estructura, manteniendo la parte de documento / estructura documento como elementos solidos, y dentro sea una estructura recursiva en cuanto a conteniudo "redactado" pero que sea tambien especifica y "separada" para elementos como requisitos, items de sinopsis o documentos relacionados de man, etc, etc , etc. Esto debe permitirnos tener todo relacionado, generalizar el texto como tal y trazar los elementos mas espeficicos comor equisitos y similñares.

3.6 a la hora de generar, se toma toda esta estructura, se genera con ella el json y de ahi el md, o nos ahorramos los json y directamente generamos el md que se usara como "codigo fuente" del documento para convertir a otros formatos.

4. Una vez hecho todo lo anterior, lo siguiente es aplicar esta metodologia al codigo completo del sistema, como forma de hacer lo mismo con el codigo, que el trabajo con IA modifiuque el codigo teniuendo toda la informacion para trazar el sistema completo.

4.1 Para el codigo habra que crear una version de la TUPLA que nos permita definir de forma recursiva desde funciones a bucles, y todos los elementos de programación, y que usaremos de base de trabajo en la campaña posterior de MPL y MCL quye hemos diseñado en otro chat (y quye aun no esta en el repo)

4.2 de forma equivalente a docgen, habra un codegen que tome todos estos datos y genere todos y cada uno de los ficheros del codigo, el equivalente a los documentos serian las carpetas, el equivalente a los documentos de estructura de documento seria una lista de los ficheros que debe contener cada caroeta, y los ficheros de codigo serian los equivalentes a las secciones de los documentos.

4.3 Todo esto es tan grande que directamente la version final la subiria a 0.3.0.

4.4 Con estos elementos implementados tanto para documentacion como para codigo, creo que podremos generalziar la metodologia al maximo manteniendo un control absoluto de cada aspecto del sistema, aumentando exponencialmente el determinismo futuro del sistema MetsuOS, pudiendo aplicar variabilidad de elementos complejos donde realmente sea necesario y minimizando el hecho de rehacer codigo o documentos, convirtiendolos en listas de instrucciones CRUD en lote que van mutando poco a poco y de forma solida el sistema

Ahora cuadremos esto

PD: quiza debnamos crear una especificacion de la TUPLA CRUD con herencia y poliomorgismo para adaptarla correctamente a toos los niveles descritos. la propioa espfiociaccion de la tupla tendria la estructura base de la tupla xD

---

## B. Planteamiento previo (asistente, antes de las 5 preguntas)

Cuadra. El eje es el mismo: nada normativo vive en el MD; el MD es un recorrido ordenado de tuplas. Lo que habíamos llamado «plantilla + reqs + código» es exactamente el caso particular de tipos de tupla (narrativa, requisito, sinopsis-desde-código).

### B.1 Tupla base (especificación que se describe a sí misma)

Campos comunes a todo nodo (`schema: metsuos-tupla-1`):

- id — único en su espacio
- tipo — discriminador: doc, seccion, elemento, req, sinopsis, man-see-also, render-modo, indice, …
- titulo — corto, humano
- cuerpo — texto que se pinta si el modo lo usa
- para_humano — por qué existe (diseño / historia)
- para_ia — misma razón, densa, accionable
- orden — entero de render en el padre
- orden_por_que — por qué ese número
- influye_de — lista de ids (quién justifica este nodo)
- influye_a — lista de ids (quién depende de este)
- creado / modificado — ISO
- render — id de modo (parrafo, tabla, h2, mermaid, …)
- activo — si false, no se pinta ni genera

Herencia = tipo añade campos, no otra tabla paralela:

- req += prioridad, verificacion, area
- sinopsis += desde: codigo, comando
- seccion += obligatoria
- doc += destino_md, categoria
- render-modo += agrupa_consecutivos (tablas), tag_md

Polimorfismo = el generador solo pregunta tipo + render. El CRUD es el mismo: add|set|rm|list sobre un almacén único.

La especificación de la tupla es un documento más hecho de tuplas (meta-circular).

### B.2 Relaciones

Ruta única. Fase 1: solo req/* ↔ req/*. El esquema admite el resto.

### B.3 Árbol

indice → documento → secciones obligatorias → elementos.

Render: ordenar hijos por orden; N render=tabla consecutivos = una tabla.

### B.4 JSON intermedio vs MD fuente

No usar el MD como fuente. Flujo: almacén (un JSON por tupla) → generate recorre → MD → HTML.

Un JSON «del documento entero» puede ser snapshot de generate, no fuente.

### B.5 Código / codegen

Fuera de esta campaña. 0.3.0: primero doc-tuplas; codegen cuando la tupla esté estable.

### B.6 Orden propuesto entonces

A schema+CRUD; B migrar reqs; C render-modo; D piloto; E resto docs; F quitar umbral 50 %.

### B.7 Preguntas que se hicieron

1. Un fichero JSON por tupla vs un JSON por documento.
2. cuerpo vacío si desde=codigo.
3. influye_* bidireccionales automáticas.
4. Piloto 02-srs o ia-write.

---

## C. Conclusión con preguntas y respuestas (íntegra)

Respuestas del diseñador (2026-09-24):

1. Sin duda un archivo por tupla, y estructura de carpetas de forma equivalente a las rutas que se van a usar.
2. Textos que se generen desde un código fuente: en lugar de cuerpo vacío, la referencia exacta de la función o bloque que genera ese trozo en forma de comando o lote de comandos.
3. Intuición: sí, bidireccional.
4. Si el orden (piloto ia-write) es correcto, adelante. Dentro de esto están las specs y en general TODOS los documentos a excepción —no se sabe si en el futuro cambiaría— de los planes. Incluye LICENSE: se empezará a trabajar elementos legales al ingerir la licencia COMPLETA GPL v3 como tuplas.
5. Al generar el plan, incluir el plan, el prompt, el planteamiento previo y el texto completo de la conclusión CON las preguntas y respuestas; anexo si hace falta. La fase posterior de código hará referencia a este plan.

Cierre técnico acordado:

- Cuerpo con origen en código = campo de referencia (comando/lote), no string vacío.
- Bidireccionalidad automática en el CRUD al set de relaciones.
- Excepción temporal: planes de campaña siguen siendo MD (+ metadato plan JSON actual) hasta revisión.
- LICENSE entra en fase E como corpus legal en tuplas (GPLv3 completa).
- Codegen no se implementa en esta campaña; este anexo es input de la campaña MPL/MCL.
