#!/usr/bin/env python3
"""
cenarios_mky.py — roda o BrasilSFC.mky (o modelo nativo do Minsky) headless e compara
cenários mexendo no slider Selic. Lê as variáveis via item handle (pyminsky).
Uso: python3 cenarios_mky.py
"""
import sys
sys.path.append('/home/morpheus/src/minsky')
from pyminsky import minsky

MKY = '/home/morpheus/Documentos/tessera-talk/roteiros/ajuste fiscal/keen-ravel/models/BrasilSFC.mky'


def handles():
    h = {}
    for i in range(len(minsky.model.items())):
        it = minsky.model.items[i]
        try:
            h.setdefault(it.name(), it)
        except Exception:
            pass
    return h


def roda(Selic, teto=None, R0=None, accum=None, T=30.0, pts=(0, 5, 10, 15, 20, 25, 30)):
    minsky.load(MKY)
    H = handles()
    H['Selic'].init(str(Selic))
    if teto is not None:
        H['teto'].init(str(teto))
    if accum is not None:
        H['accum'].init(str(accum))
    if R0 is not None:
        try:
            H['R_reservas'].init(str(R0))          # a própria variável integral aceita init
        except Exception:
            pass
    minsky.reset()
    H = handles()  # re-resolve após reset
    out = []
    nextpt = list(pts)
    while minsky.t() <= T + 0.2:
        if nextpt and minsky.t() >= nextpt[0]:
            t = nextpt.pop(0)
            g = lambda n: round(H[n].value(), 3)
            out.append((t, g('b_divida'), g('r_gov') - g('g_nom'), g('e_cambio'),
                        g('R_reservas'), g('pb_ratio'), g('G_gov'), g('tax')))
        if not nextpt:
            break
        minsky.step()
    return out


def mostra(nome, rows):
    print(f"\n### {nome}")
    print("  t   b(dív/Y)  r-g    câmbio   R(nível)  pb/Y   G_gov   tax  (teto bind se G=tax)")
    for t, b, rg, e, R, pb, G, tax in rows:
        bind = "←teto" if abs(G - tax) < 0.05 else ""
        print("%4d   %6.2f  %+5.3f   %5.2f   %7.1f  %+5.3f  %5.1f  %5.1f %s"
              % (t, b, rg, e, R, pb, G, tax, bind))


if __name__ == "__main__":
    mostra("A — Selic 15% (atual, Copom nov/25)", roda(0.15))
    mostra("B — Selic 10% (corte gradual)", roda(0.10))
    mostra("B+ — Selic 10% + reservas altas (R0=25)", roda(0.10, R0=25, accum=0.010))
    mostra("B- — Selic 10% + reservas baixas (R0=8)", roda(0.10, R0=8, accum=0.0))
    mostra("C — Selic 10% + arcabouço frouxo (teto=1.06)", roda(0.10, teto=1.06))
