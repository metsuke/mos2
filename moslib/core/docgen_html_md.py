"""Markdown → HTML (cuerpo)."""

from __future__ import annotations

import html
import re

from moslib.core.docgen_html import estructurar_listas_de_opciones


def _inline(texto: str) -> str:
    texto = html.escape(texto)
    texto = re.sub(r"`([^`]+)`", r"<code>\1</code>", texto)
    texto = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", texto)
    texto = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", texto)
    return texto


def markdown_a_html(md: str, titulo: str) -> str:
    md = estructurar_listas_de_opciones(md)
    lineas = md.splitlines()
    cuerpo = []
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        if linea.startswith("```"):
            bloque = []
            i += 1
            while i < len(lineas) and not lineas[i].startswith("```"):
                bloque.append(html.escape(lineas[i]))
                i += 1
            i += 1
            cuerpo.append("<pre><code>" + "\n".join(bloque) + "</code></pre>")
            continue
        if linea.strip() == "---":
            cuerpo.append("<hr>")
            i += 1
            continue
        if linea.startswith("# "):
            cuerpo.append(f"<h1>{_inline(linea[2:].strip())}</h1>")
            i += 1
            continue
        if linea.startswith("## "):
            cuerpo.append(f"<h2>{_inline(linea[3:].strip())}</h2>")
            i += 1
            continue
        if linea.startswith("### "):
            cuerpo.append(f"<h3>{_inline(linea[4:].strip())}</h3>")
            i += 1
            continue
        if linea.strip().startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                celdas = [c.strip() for c in lineas[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") and "-" in c for c in celdas if c):
                    filas.append(celdas)
                i += 1
            if filas:
                thead = "".join(f"<th>{_inline(c)}</th>" for c in filas[0])
                body = ["<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in f) + "</tr>" for f in filas[1:]]
                cuerpo.append(
                    "<table><thead><tr>" + thead + "</tr></thead><tbody>" + "".join(body) + "</tbody></table>"
                )
            continue
        if linea.startswith("- ") or linea.startswith("* "):
            items = []
            while i < len(lineas) and (lineas[i].startswith("- ") or lineas[i].startswith("* ")):
                items.append(f"<li>{_inline(lineas[i][2:].strip())}</li>")
                i += 1
            cuerpo.append("<ul>" + "".join(items) + "</ul>")
            continue
        if linea.strip() == "":
            i += 1
            continue
        par = [linea]
        i += 1
        while (
            i < len(lineas)
            and lineas[i].strip()
            and not lineas[i].startswith("#")
            and not lineas[i].strip().startswith("|")
            and not lineas[i].startswith("```")
            and not lineas[i].startswith("- ")
        ):
            par.append(lineas[i])
            i += 1
        cuerpo.append("<p>" + _inline(" ".join(par)) + "</p>")
    tit = html.escape(titulo)
    return (
        '<!DOCTYPE html>\n<html lang="es"><head><meta charset="utf-8">'
        f"<title>{tit}</title>"
        "<style>"
        "body{font-family:sans-serif;max-width:52rem;margin:1.5rem auto;padding:0 1rem;line-height:1.45}"
        "table{border-collapse:collapse;width:100%;margin:1rem 0}"
        "th,td{border:1px solid #888;padding:.35rem .5rem;text-align:left;vertical-align:top}"
        "pre{background:#f4f4f4;padding:.75rem;overflow:auto}"
        "code{font-family:ui-monospace,monospace}"
        "</style></head><body>\n"
        + "\n".join(cuerpo)
        + "\n</body></html>\n"
    )
