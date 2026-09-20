# git

## NOMBRE
git — git del anfitrión sobre la raíz del clone

## SINOPSIS

- git status
- git add <ruta>
- git --no-pager diff
- git --no-pager diff --cached --stat
- git commit -m <mensaje>

## DESCRIPCIÓN
Reenvía los argumentos a git del PATH. El cwd es siempre la raíz del clone.
En main están bloqueados commit, push, merge y rebase. Usa una rama y luego dev publicar o dev consolidar.

## SEGURIDAD
Es el git del anfitrión. Puede escribir el repo. No escapa del clone como cwd.

## VÉASE TAMBIÉN
dev, update, touch, code