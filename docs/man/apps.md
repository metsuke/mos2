# apps

## NOMBRE
apps – instala, lista y quita apps locales

## SINOPSIS
apps
apps list
apps show ID
apps install RUTA
apps remove ID

## DESCRIPCIÓN
Gestiona paquetes de app en el espacio del usuario (.mos/apps).
Instalar valida app.json, que los comandos no pisen el sistema y la política de imports.
Sin cumplir SEC/A11Y de los módulos de comando, no se acepta.

## EJEMPLOS
apps list
apps install /ruta/a/mi-app

## SEGURIDAD
Comando de sistema. stdlib + moslib.