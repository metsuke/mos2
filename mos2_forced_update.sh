# Por si la hemos liado y no queremos usar 
#  el update de mos2 con backup.
git fetch origin
git reset --hard origin/main
git clean -fd