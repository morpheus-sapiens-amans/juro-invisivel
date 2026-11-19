"""
cross_run.py — roda o MESMO choque de política (corte da Selic 13,75% -> 7,5%)
nos dois modelos e tabula lado a lado:

  (1) dejanir_model.solve()  — FTPL economia aberta, forward-looking, trajetória anunciada.
  (2) brasil_sfc.simula()    — nosso SFC/Minsky, Selic como botão constante, regime phi.

Os modelos NÃO são comensuráveis unidade-a-unidade (Dejanir reporta desvios anualizados
em relação ao estado estacionário; o nosso reporta níveis). A comparação é de SINAL e
MECANISMO, mais o delta interno de cada modelo (cortar vs não-cortar).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dejanir_model as dj
import brasil_sfc as sfc


def bloco_dejanir():
    print("=" * 74)
    print("(1) MODELO DEJANIR (FTPL aberto) — corte Selic 13,75% -> 7,5% em 4 trimestres")
    print("=" * 74)
    bench = dj.solve(dj.PRESETS["benchmark"])
    sale = dj.solve(dj.PRESETS["sale"])
    pre = 100 * (1.1375 / (1.01 * math.exp(0.06)) - 1)
    print(f"Inflação de regime pré-plano: {pre:.2f}% a.a.")
    print(f"{'':20s}{'impacto(t0)':>12s}{'t4':>8s}{'t8':>8s}{'longo prazo(t24)':>18s}")
    for nome, path in [("benchmark s/ FX", bench), ("com venda reservas", sale)]:
        print(f"{nome:20s}"
              f"{path[0]['inflation']:>11.2f}%{path[4]['inflation']:>7.2f}%"
              f"{path[8]['inflation']:>7.2f}%{path[24]['inflation']:>16.2f}%")
    print("\nLeituras-chave do modelo do Dejanir:")
    print(f"  • Juro REAL da Selic: {bench[0]['real']:.2f}% (impacto) -> {bench[24]['real']:.2f}% (t24).")
    print(f"    O real volta ao pré-plano (~7,25%): o corte NÃO baixa o juro real de longo prazo.")
    print(f"  • Câmbio real deprecia no impacto (+{bench[0]['fx']:.2f}% log) -> some no longo prazo.")
    print(f"  • Dívida real salta +{bench[0]['debt']:.2f}% no impacto (revalorização dos títulos).")
    return bench


def bloco_nosso():
    print("\n" + "=" * 74)
    print("(2) NOSSO BrasilSFC (Minsky/SFC) — Selic 13,75% vs 7,5%, dois regimes")
    print("=" * 74)
    T = 20.0
    cfgs = [
        ("NORMAL  Selic 13,75%", dict(Selic=0.1375, phi_endog=False, b0=0.78)),
        ("NORMAL  Selic  7,50%", dict(Selic=0.075,  phi_endog=False, b0=0.78)),
        ("DOMINÂNCIA Selic 13,75% (b0=1.00)", dict(Selic=0.1375, phi_endog=True, b0=1.00)),
        ("DOMINÂNCIA Selic  7,50% (b0=1.00)", dict(Selic=0.075,  phi_endog=True, b0=1.00)),
    ]
    out = {}
    print(f"{'cenário':36s}{'infl t=2a':>10s}{'câmbio':>9s}{'b (dív/PIB)':>12s}{'r-g':>8s}")
    for nome, kw in cfgs:
        h = sfc.simula(T=T, every=1.0, **kw)
        # snapshot ~2 anos após o choque
        s2 = next(r for r in h if r["t"] >= 2.0)
        sL = h[-1]
        out[nome] = (s2, sL)
        print(f"{nome:36s}{100*s2['infl']:>9.2f}%{s2['cambio']:>9.3f}{s2['b']:>12.3f}{s2['rg']:>+8.3f}")
    return out


def confronto(bench, out):
    print("\n" + "=" * 74)
    print("CONFRONTO — o que cada modelo diz sobre CORTAR a Selic")
    print("=" * 74)
    # deltas internos: cortar menos não-cortar
    dj_impact = bench[0]["inflation"]
    nn = out["NORMAL  Selic 13,75%"][0]; nc = out["NORMAL  Selic  7,50%"][0]
    dn = out["DOMINÂNCIA Selic 13,75% (b0=1.00)"][0]; dc = out["DOMINÂNCIA Selic  7,50% (b0=1.00)"][0]
    print(f"""
  DEJANIR (único regime, 'normal'):
    corte -> depreciação + revalorização da dívida -> SURTO de inflação no impacto
    (+3,3pp), domado por venda de reservas. Longo prazo: inflação CAI (neo-Fisher),
    juro real INALTERADO. Baixar o juro real exige risco-país menor OU ajuste fiscal
    com hand-to-mouth — NUNCA o corte nominal sozinho.

  NOSSO SFC, regime NORMAL (b<0,90):
    corte 13,75->7,5 muda inflação em {100*(nc['infl']-nn['infl']):+.2f}pp e câmbio em {nc['cambio']-nn['cambio']:+.3f}.
    MESMO SINAL do Dejanir no impacto: cortar deprecia e pressiona preços via pass-through.

  NOSSO SFC, regime DOMINÂNCIA (b>0,90, phi_endog):
    corte 13,75->7,5 muda inflação em {100*(dc['infl']-dn['infl']):+.2f}pp e câmbio em {dc['cambio']-dn['cambio']:+.3f}.
    Aqui o sinal PODE inverter (corte APRECIA): é a tese ALR de dominância fiscal.
    >>> Este regime NÃO existe no modelo do Dejanir: ele é sempre 'normal'. <<<

  CONVERGÊNCIA:  ambos veem a dívida alta/composição como o nó; ambos põem o câmbio/
                 risco-país no centro; ambos dizem que cortar a Selic não baixa o juro
                 real estrutural por si só.
  DIVERGÊNCIA:   o Dejanir não tem flip de regime (corte sempre deprecia no impacto) nem
                 dívida privada endógena; nós não temos FTPL nem revalorização forward-
                 looking dos títulos (o salto de dívida de impacto dele não aparece aqui).
""")


if __name__ == "__main__":
    bench = bloco_dejanir()
    out = bloco_nosso()
    confronto(bench, out)
