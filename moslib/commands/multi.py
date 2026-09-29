"""Lote: acumula con input(). Parseo solo al :e."""

from moslib.core.multi_run import lanzar


def _meta(line: str) -> str:
    s = line.strip().replace(chr(0xFEFF), "")
    if s.startswith(";"):
        return ":" + s[1:]
    return s


def execute(args):
    print("[multi] Pega el bloque.")
    print("[multi] Luego una linea solo con :e  (o :q).")
    lote = []
    while True:
        try:
            line = input()
        except (EOFError, KeyboardInterrupt):
            print("[multi] Cancelado.")
            return 1
        line = line.replace(chr(13), "")
        for piece in line.split(chr(10)):
            meta = _meta(piece).lower()
            if meta == ":q":
                print("[multi] Cancelado.")
                return 1
            if meta in (":e", ":w"):
                return lanzar(lote)
            lote.append(piece)


def help():
    return "Uso: multi o ./write.sh. :e ejecuta, :q cancela. Sumario ok/!!!."


def sinopsis():
    return ["multi", "m"]
