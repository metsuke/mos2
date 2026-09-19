"""HTML de lectura ágil y listas en SINOPSIS/EJEMPLOS/USO."""

from __future__ import annotations

from pathlib import Path

from moslib.core import docgen as motor

SECCIONES_LISTA = {
    "sinopsis",
    "synopsis",
    "ejemplos",
    "examples",
    "uso",
    "comandos",
}


def html_dir() -> Path:
    d = motor.get_docgen_dir() / "html"
    d.mkdir(parents=True, exist_ok=True)
    return d


def html_path_for(doc_id: str) -> Path:
    return html_dir() / f"{doc_id}.html"


def _clave_seccion(titulo: str) -> str:
    raw = titulo.strip().lower()
    return (
        raw.replace("ó", "o")
        .replace("í", "i")
        .replace("á", "a")
        .replace("é", "e")
        .replace("ú", "u")
    )


def estructurar_listas_de_opciones(md: str) -> str:
    lineas = md.splitlines()
    out = []
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        if linea.startswith("## "):
            out.append(linea)
            clave = _clave_seccion(linea[3:])
            i += 1
            bloque = []
            while i < len(lineas) and not lineas[i].startswith("#"):
                bloque.append(lineas[i])
                i += 1
            if clave in SECCIONES_LISTA:
                out.append("")
                for fila in bloque:
                    texto = fila.strip()
                    if not texto or texto == "---":
                        continue
                    if texto.startswith("- ") or texto.startswith("* "):
                        out.append(texto)
                    else:
                        out.append("- " + texto)
                out.append("")
            else:
                out.extend(bloque)
            continue
        out.append(linea)
        i += 1
    return "\n".join(out)


def markdown_a_html(md: str, titulo: str) -> str:
    from moslib.core.docgen_html_md import markdown_a_html as _conv

    return _conv(md, titulo)


def escribir_html(doc_id: str, markdown: str) -> Path:
    dest = html_path_for(doc_id)
    dest.write_text(markdown_a_html(markdown, doc_id), encoding="utf-8")
    return dest
