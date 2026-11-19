#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo unico com chaves -- projeto "Teoria Monetaria"

Um so esqueleto (o do relatorio 1: IS, Phillips, regra de Taylor, identidade da
divida) e cada escola como um conjunto de chaves. Serve para ver em que premissa
uma escola se separa da outra. NAO diz qual esta certa.

Marcacao: [I] identidade contabil, [P] premissa em disputa, [E] dado.

As duas perguntas que separam as escolas:
  1) O ajuste derruba o juro?      chaves: th_d, th_p, kappa
  2) O juro pode cair por decisao? chaves: selic_dec, custo_juro

Uso:
    python3 modelo_unico.py                  # tabela com as seis escolas
    python3 modelo_unico.py --escola mmt     # trajetoria ano a ano de uma escola
    python3 modelo_unico.py --sliders        # janela interativa (matplotlib)
    python3 modelo_unico.py --gif saida.gif  # animacao ano a ano
"""
import argparse
import math
from dataclasses import dataclass, replace

ANO0, T = 2026, 10


@dataclass
class Par:
    # ---- condicoes iniciais [E] (BCB, set/2026; iguais as dos seis relatorios) ----
    d0: float = 82.9        # divida bruta, % PIB
    pb0: float = -0.52      # primario, % PIB
    selic0: float = 13.75
    ief0: float = 11.0      # juro implicito da divida
    pi0: float = 4.6
    u0: float = 5.2
    h0: float = 0.5         # hiato do produto
    pi_meta: float = 3.0
    # ---- cenario ----
    ajuste: float = 0.45    # % PIB, permanente (R$ 60 bi)
    gn: float = 2.0         # crescimento potencial
    rn0: float = 6.0        # juro real neutro (ou "de convencao")
    # ---- PERGUNTA 1: o ajuste derruba o juro? [P] ----
    th_d: float = 0.04      # premio por ponto de divida acima da inicial
    th_p: float = 0.25      # queda do premio por ponto do PIB de ajuste
    kappa: float = 0.0      # premio entre "mercado nao acredita" e "acredita"
    p0: float = 0.35        # crenca inicial de que o governo ajusta
    # ---- PERGUNTA 2: o juro pode cair por decisao? [P] ----
    selic_dec: float = -1.0  # >0: BC larga a regra e leva a Selic a esse valor
    anos_dec: int = 2
    custo_juro: float = 1.0  # 0 = juro baixo nao aquece nem deprecia (MMT)
    #                          1 = aquece, deprecia e desancora (ortodoxia)
    # ---- custo do ajuste [P] ----
    mult: float = 0.5       # multiplicador
    ric: float = 0.25       # compensacao privada (equivalencia ricardiana parcial)
    hist: float = 0.0       # histerese: hiato negativo vira perda permanente
    # ---- demais (relatorio 1) ----
    phi_pi: float = 2.0
    phi_y: float = 0.5
    rho_i: float = 0.4
    b1: float = 0.5
    zeta: float = 0.30      # desancoragem por ponto de premio
    gam: float = 0.6
    kap: float = 0.30
    phi_e: float = 0.06
    psi: float = 5.0        # depreciacao por ponto de premio
    c_k: float = 0.15       # perda de crescimento por ponto de juro neutro
    okun: float = 0.40
    tau: float = 0.35
    w_ief: float = 0.60
    spread: float = 2.75


def derivados(p: Par):
    """A chave custo_juro move tres parametros de uma vez."""
    c = p.custo_juro
    b2 = 0.05 + 0.25 * c                       # efeito do juro real sobre a demanda
    eta = 1.0 * c                              # cambio reage ao juro real
    a_exp = 0.5 + 0.5 * c if p.selic_dec > 0 else 0.5   # inercia das expectativas
    return b2, eta, a_exp


def simular(p: Par, com_ajuste: bool):
    b2, eta, a_exp = derivados(p)
    n = T + 1
    ks = "d pb selic ief pi pie u g hiato juros prem rn rreal crenca adj pib".split()
    v = {k: [0.0] * n for k in ks}
    v["d"][0], v["pb"][0], v["selic"][0], v["ief"][0] = p.d0, p.pb0, p.selic0, p.ief0
    v["pi"][0], v["u"][0], v["g"][0], v["hiato"][0] = p.pi0, p.u0, p.gn, p.h0
    v["pie"][0] = p.pi_meta + 0.5 * (p.pi0 - p.pi_meta)
    v["rn"][0], v["rreal"][0] = p.rn0, p.selic0 - v["pie"][0]
    v["juros"][0], v["crenca"][0], v["pib"][0] = 8.99, p.p0, 100.0
    for t in range(1, n):
        adj = p.ajuste if com_ajuste else 0.0
        v["adj"][t] = adj
        # [P] crenca do mercado: sobe se o ajuste entregue passa de ~0,27% do PIB
        alvo_c = 1.0 / (1.0 + math.exp(-(adj - 0.27) / 0.05))
        v["crenca"][t] = v["crenca"][t - 1] + 0.6 * (alvo_c - v["crenca"][t - 1])
        # [P] premio: divida (th_d), ajuste (th_p) e crenca (kappa)
        v["prem"][t] = (p.th_d * (v["d"][t - 1] - p.d0) - p.th_p * adj
                        + p.kappa * (p.p0 - v["crenca"][t]))
        v["rn"][t] = p.rn0 + v["prem"][t]
        v["pie"][t] = (p.pi_meta + a_exp * (v["pi"][t - 1] - p.pi_meta)
                       + p.zeta * max(0.0, v["prem"][t]))
        # [P] regra de Taylor, ou Selic decidida
        if p.selic_dec > 0:
            frac = min(1.0, t / max(1, p.anos_dec))
            v["selic"][t] = p.selic0 + frac * (p.selic_dec - p.selic0)
        else:
            alvo = (v["rn"][t] + p.pi_meta + p.phi_pi * (v["pie"][t] - p.pi_meta)
                    + p.phi_y * v["hiato"][t - 1])
            v["selic"][t] = p.rho_i * v["selic"][t - 1] + (1 - p.rho_i) * alvo
        v["rreal"][t] = v["selic"][t] - v["pie"][t]
        # [P] curva IS
        m_ef = p.mult * (1 - p.ric)
        v["hiato"][t] = (p.b1 * v["hiato"][t - 1] - b2 * (v["rreal"][t] - v["rn"][t])
                         - m_ef * (adj - v["adj"][t - 1]))
        # oferta: deslocamento do investimento [P] e histerese [P]
        gpot = (p.gn - p.c_k * (v["rn"][t] - p.rn0)
                + p.hist * min(0.0, v["hiato"][t - 1]))
        v["g"][t] = gpot + (v["hiato"][t] - v["hiato"][t - 1])
        v["pib"][t] = v["pib"][t - 1] * (1 + v["g"][t] / 100)
        v["u"][t] = p.u0 - p.okun * (v["hiato"][t] - p.h0)
        dep = (p.psi * (v["prem"][t] - v["prem"][t - 1])
               - eta * (v["rreal"][t] - v["rreal"][t - 1]))
        v["pi"][t] = (p.gam * v["pie"][t] + (1 - p.gam) * v["pi"][t - 1]
                      + p.kap * v["hiato"][t] + p.phi_e * dep)
        # contas publicas
        v["ief"][t] = v["ief"][t - 1] + p.w_ief * ((v["selic"][t] - p.spread) - v["ief"][t - 1])
        v["pb"][t] = p.pb0 + adj + p.tau * (v["hiato"][t] - p.h0)
        gy = (1 + v["g"][t] / 100) * (1 + v["pi"][t] / 100)
        v["juros"][t] = v["ief"][t] / 100 * v["d"][t - 1] / gy
        # [I] divida(t) = divida(t-1)/(1 + crescimento nominal) + juros - primario
        v["d"][t] = v["d"][t - 1] / gy + v["juros"][t] - v["pb"][t]
    return v


# Cada escola = o mesmo esqueleto com chaves diferentes.
ESCOLAS = {
    "ortodoxia": ("Ortodoxia", dict()),
    "pos-keynesiana": ("Pos-keynesiana", dict(
        th_d=0.02, th_p=0.0, mult=1.0, ric=0.0, hist=0.3, zeta=0.0, c_k=0.0, custo_juro=0.5)),
    "mmt": ("MMT", dict(
        th_d=0.0, th_p=0.0, mult=1.0, ric=0.0, hist=0.1, zeta=0.0, c_k=0.0, psi=0.0,
        selic_dec=7.5, custo_juro=0.0)),
    "marxista": ("Marxista", dict(
        th_d=0.0, th_p=0.0, mult=1.0, ric=0.0, zeta=0.0, c_k=0.0, custo_juro=0.5)),
    "austriaca": ("Austriaca", dict(
        th_d=0.06, th_p=0.25, mult=0.3, ric=0.5, c_k=0.30)),
    "veto": ("Economia politica (veto)", dict(
        th_d=0.0, th_p=0.0, kappa=3.0, mult=0.8, ric=0.0)),
}


def resumo(p: Par):
    a, b = simular(p, True), simular(p, False)
    med = lambda x: sum(x[1:]) / T
    return dict(dA=a["d"][-1], dB=b["d"][-1], dif=a["d"][-1] - b["d"][-1],
                piA=med(a["pi"]), piB=med(b["pi"]), selA=med(a["selic"]), selB=med(b["selic"]),
                pib=100 * (a["pib"][-1] / b["pib"][-1] - 1), uA=max(a["u"]), a=a, b=b)


def tabela():
    print(f"{'escola':26s}{'div A':>7s}{'div B':>7s}{'A-B':>7s}{'IPCA A':>8s}{'IPCA B':>8s}"
          f"{'Selic A':>8s}{'Selic B':>8s}{'PIB A/B':>9s}")
    for k, (nome, mod) in ESCOLAS.items():
        r = resumo(replace(Par(), **mod))
        print(f"{nome:26s}{r['dA']:7.1f}{r['dB']:7.1f}{r['dif']:+7.1f}{r['piA']:8.2f}{r['piB']:8.2f}"
              f"{r['selA']:8.2f}{r['selB']:8.2f}{r['pib']:+8.2f}%")
    print("\nDivida/PIB em 2036; IPCA e Selic sao medias 2027-2036; PIB A/B = PIB real de A sobre B em 2036.")


def trajetoria(p: Par):
    for nome, v in (("A: com ajuste", simular(p, True)), ("B: sem ajuste", simular(p, False))):
        print(f"\n{nome}\nano    divida   selic    ipca  cresc. desemp.  juros")
        for t in range(T + 1):
            print(f"{ANO0 + t}  {v['d'][t]:7.1f} {v['selic'][t]:7.2f} {v['pi'][t]:7.2f} "
                  f"{v['g'][t]:7.2f} {v['u'][t]:7.2f} {v['juros'][t]:6.2f}")


PAINEIS = [("d", "Divida bruta (% PIB)"), ("selic", "Selic (%)"), ("pi", "IPCA (%)"),
           ("g", "Crescimento (%)"), ("u", "Desemprego (%)"), ("juros", "Juros pagos (% PIB)")]


def figura(p, ate=T, fig=None):
    import matplotlib.pyplot as plt
    a, b = simular(p, True), simular(p, False)
    anos = [ANO0 + t for t in range(T + 1)]
    fig = fig or plt.figure(figsize=(13, 7))
    fig.clf()
    for ax, (k, tit) in zip(fig.subplots(2, 3).flat, PAINEIS):
        ax.plot(anos[:ate + 1], a[k][:ate + 1], "-", lw=2, label="A: com ajuste")
        ax.plot(anos[:ate + 1], b[k][:ate + 1], "--", lw=2, label="B: sem ajuste")
        ax.set_xlim(ANO0, ANO0 + T)
        lo, hi = min(a[k] + b[k]), max(a[k] + b[k])
        m = 0.1 * (hi - lo + 1e-9)
        ax.set_ylim(lo - m, hi + m)
        ax.set_title(tit, fontsize=10)
        ax.grid(alpha=.3)
    fig.axes[0].legend(fontsize=8)
    return fig


def sliders(p):
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider
    fig = plt.figure(figsize=(13, 9.5))
    sub = fig.subfigures(2, 1, height_ratios=[5, 1.6])
    figura(p, fig=sub[0])
    defs = [("ajuste", 0, 3, "Ajuste (% PIB)"), ("rn0", 3, 8, "Juro neutro"),
            ("th_d", 0, 0.10, "Premio por divida"), ("th_p", 0, 1, "Ajuste baixa o premio"),
            ("kappa", 0, 4, "Peso da crenca"), ("custo_juro", 0, 1, "Custo de baixar o juro"),
            ("selic_dec", -1, 14, "Selic decidida (<0 = regra)"), ("mult", 0, 2.5, "Multiplicador"),
            ("hist", 0, 1, "Histerese"), ("gn", 0.5, 3.5, "Crescimento potencial")]
    sl = {}
    for i, (k, lo, hi, rot) in enumerate(defs):
        ax = sub[1].add_axes([0.12 + 0.5 * (i % 2), 0.82 - 0.17 * (i // 2), 0.28, 0.10])
        sl[k] = Slider(ax, rot, lo, hi, valinit=getattr(p, k))

    def redesenha(_):
        figura(replace(p, **{k: s.val for k, s in sl.items()}), fig=sub[0])
        fig.canvas.draw_idle()
    for s in sl.values():
        s.on_changed(redesenha)
    plt.show()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--escola", choices=list(ESCOLAS))
    ap.add_argument("--sliders", action="store_true")
    ap.add_argument("--gif")
    a = ap.parse_args()
    p = replace(Par(), **ESCOLAS[a.escola][1]) if a.escola else Par()
    if a.sliders:
        sliders(p)
    elif a.gif:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation, PillowWriter
        fig = plt.figure(figsize=(13, 7))
        FuncAnimation(fig, lambda i: figura(p, ate=i + 1, fig=fig), frames=T,
                      interval=700).save(a.gif, writer=PillowWriter(fps=1.5))
    elif a.escola:
        trajetoria(p)
    else:
        tabela()
