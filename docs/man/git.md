# git

## NOMBRE
git – git del anfitrión sobre la raíz del clone

## SINOPSIS

- git status
- git add <ruta>
- git --no-pager diff
- git --no-pager diff --cached --stat
- git commit -m <mensaje>

## DESCRIPCIÓN
Reenvía los argumentos a git del PATH. El cwd es siempre la raíz del clone.
No interpreta el mensaje de commit ni añade flags por su cuenta.
Para evitar el pager: git --no-pager status

## SEGURIDAD
Es el git del anfitrión. Puede escribir el repo.
No escapa del clone como cwd.
Comando de sistema. Solo stdlib y moslib.

## VÉASE TAMBIÉN
touch, code, docs