#!/bin/bash
echo "🚀 Iniciando despliegue de entorno mos2..."
# Asegurar entorno local estanco
poetry config virtualenvs.in-project true
# Instalación silenciosa
poetry install
echo "✅ Entorno mos2 (MetsuOS) listo para su uso."
