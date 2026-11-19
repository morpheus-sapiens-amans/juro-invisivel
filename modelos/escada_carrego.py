#!/usr/bin/env python3
"""
escada_carrego.py — gera DOIS PNGs que fecham a modelagem:
  02_carrego.png — o custo quase-fiscal das reservas cai quando a Selic cai (contraintuitivo).
  03_escada.png  — a escada dos Modelos 1-4 (alternativa direta → pacote-ponte) em dívida e câmbio.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from brasil_sfc import simula


def suave(t, y, win=3.0):
    """Média móvel centrada (janela 'win' anos) — tendência, atenua o ciclo de Goodwin."""
    y = np.asarray(y, float)
    dt = (t[1] - t[0]) if len(t) > 1 else 1.0
    k = max(1, int(win / dt))
    out = np.array([y[max(0, i - k // 2):min(len(y), i + k // 2 + 1)].mean() for i in range(len(y))])
    return t, out


def serie(h, campo):
    return suave([x['t'] for x in h], [x[campo] for x in h])


# ======================= 02 — CARREGO =======================
SEL = [0.15, 0.13, 0.11, 0.10, 0.09, 0.08]
carr = [sum(x['carrego'] for x in simula(s, T=20, R0=0.25, accum0=0.008, every=1.0,
            conta_carrego=True)) / 20 for s in SEL]

plt.rcParams.update({'font.size': 10.5, 'axes.grid': True, 'grid.alpha': 0.25})
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

ax1.plot([s * 100 for s in SEL], [c * 100 for c in carr], 'o-', color='#762a83', lw=2.6, ms=8)
ax1.set_xlabel('Selic (% a.a.)'); ax1.set_ylabel('carrego das reservas (% do PIB / ano)')
ax1.set_title('A. Segurar reservas a juro alto é uma conta escondida', fontweight='bold', fontsize=11)
ax1.invert_xaxis()
ax1.annotate('a 15%, o carrego\ncome ~11% do PIB/ano', xy=(15, carr[0] * 100), xytext=(12.5, 7),
             color='#762a83', fontsize=9.5, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#762a83'))
ax1.annotate('cortar a Selic →\nderrete o carrego', xy=(8.3, carr[-1] * 100), xytext=(10.5, 2),
             color='#1b7837', fontsize=9.5, arrowprops=dict(arrowstyle='->', color='#1b7837'))

for sel, cor, lab in [(0.15, '#b2182b', 'Selic 15%'), (0.10, '#1b7837', 'Selic 10%')]:
    hs = simula(sel, T=20, R0=0.25, accum0=0.008, every=0.5, conta_carrego=False)
    hc = simula(sel, T=20, R0=0.25, accum0=0.008, every=0.5, conta_carrego=True)
    ax2.plot(*serie(hs, 'b'), '--', color=cor, lw=1.8, label=f'{lab} — sem carrego')
    ax2.plot(*serie(hc, 'b'), '-', color=cor, lw=2.6, label=f'{lab} — COM carrego')
ax2.set_xlabel('anos'); ax2.set_ylabel('dívida / PIB')
ax2.set_title('B. O carrego infla a dívida — e a Selic alta infla o carrego', fontweight='bold', fontsize=11)
ax2.legend(fontsize=8.5, loc='upper left')
fig.suptitle('CARREGO DAS RESERVAS — por que cortar a Selic MELHORA o quase-fiscal (contraintuitivo)',
             fontsize=13, fontweight='bold')
fig.text(0.5, 0.005, 'Modelo SFC Brasil · reservas R0=25% do PIB · carrego=(Selic−retorno−depreciação)·R · tendência (média móvel 3 anos) · mecanismo, não previsão',
         ha='center', fontsize=8.5, color='#666')
fig.tight_layout(rect=[0, 0.03, 1, 0.94])
fig.savefig('saida/02_carrego.png', dpi=140)
print('salvo: 02_carrego.png')

# ======================= 03 — ESCADA =======================
MOD = [
    ('B0 status quo (Selic 15%, nada)',       dict(Selic=0.15),                                                                     '#777777', '--'),
    ('M1 alternativa direta (topo, s/ Selic)', dict(Selic=0.15, tax_rich=0.012, regra_divida=True),                                  '#1b7837', '-'),
    ('M2 LR puro (só Selic 10%)',             dict(Selic=0.10, conta_carrego=True),                                                 '#d6604d', '-'),
    ('M3 LR + defesas (τ + reservas)',        dict(Selic=0.10, conta_carrego=True, tau_fric=0.6, R0=0.20, accum0=0.006),            '#4393c3', '-'),
    ('M4 pacote-ponte completo',              dict(Selic=0.10, conta_carrego=True, tau_fric=0.6, R0=0.20, accum0=0.006,
                                                   invest_pub=0.015, tax_rich=0.012, regra_divida=True),                             '#2166ac', '-'),
]
runs = [(n, simula(T=20, every=0.5, phi_endog=True, b0=0.78, **kw), c, ls) for n, kw, c, ls in MOD]

fig, (axb, axe) = plt.subplots(1, 2, figsize=(14, 5.6))
for nome, h, cor, ls in runs:
    lw = 3.0 if nome.startswith('M4') or nome.startswith('M1') else 2.0
    axb.plot(*serie(h, 'b'), ls, color=cor, lw=lw, label=nome)
    axe.plot(*serie(h, 'cambio'), ls, color=cor, lw=lw)
axb.set_title('A. Dívida / PIB', fontweight='bold', fontsize=12)
axb.set_ylabel('dívida / PIB'); axb.set_xlabel('anos')
axe.set_title('B. Câmbio (↑ = Real mais fraco)', fontweight='bold', fontsize=12)
axe.set_ylabel('câmbio (R$/US$, índice)'); axe.set_xlabel('anos')
axb.legend(fontsize=8.8, loc='upper left', framealpha=0.95)
axe.annotate('status quo: juro alto\nafunda o Real (dominância)', xy=(20, runs[0][1][-1]['cambio']),
             xytext=(9, 3.1), color='#777', fontsize=9, arrowprops=dict(arrowstyle='->', color='#777'))
axe.annotate('M1 e M4: Real firme', xy=(20, runs[4][1][-1]['cambio']), xytext=(10, 1.5),
             color='#1b7837', fontsize=9, arrowprops=dict(arrowstyle='->', color='#1b7837'))
fig.suptitle('A ESCADA — da alternativa direta ao pacote-ponte (dívida × câmbio, dívida inicial 78%)',
             fontsize=13.5, fontweight='bold')
fig.text(0.5, 0.005, 'Modelo SFC Brasil · phi endógeno · b0=0,78 · tendência (média móvel 3 anos) · cada degrau credita seu autor (ver RESULTADOS-MODELOS.md) · mecanismo, não previsão',
         ha='center', fontsize=8.5, color='#666')
fig.tight_layout(rect=[0, 0.03, 1, 0.94])
fig.savefig('saida/03_escada.png', dpi=140)
print('salvo: 03_escada.png')
