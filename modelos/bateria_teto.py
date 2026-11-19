#!/usr/bin/env python3
"""
bateria_teto.py — A CONSEQUÊNCIA DE ABOLIR O "PACOTE DO MAL" (teto + arcabouço).
Testa a tese do Laércio: revogar o teto de gastos (EC 95) E o arcabouço (LC 200).
Gera modelos-saida/01_bateria_teto.png (4 painéis) + imprime o placar.

Selic FIXA em 15% (isola o efeito da REGRA FISCAL do efeito do juro).

Veredito honesto (não maquiado):
  1. DÍVIDA  — revogar sem âncora EXPLODE; revogar + regra de dívida controla MELHOR que o teto.
               → a tese só se sustenta como "revogar E ancorar", nunca "revogar e largar".
  2. SOCIAL  — o teto esmaga o gasto social (ajuste por composição); o pacote ancorado preserva.
  3. SALÁRIO — o teto tem a MENOR parcela salarial: ele "cresce" reprimindo salário (caráter de classe).
  4. PIB     — o teto cresce mais no agregado, MAS por repressão; o pacote troca PIB por distribuição.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from brasil_sfc import simula


def suave(t, y, win=3.0):
    """Média móvel centrada (janela 'win' anos) — mostra a TENDÊNCIA, atenua o ciclo de Goodwin."""
    y = np.asarray(y, float)
    dt = (t[1] - t[0]) if len(t) > 1 else 1.0
    k = max(1, int(win / dt))
    out = np.array([y[max(0, i - k // 2):min(len(y), i + k // 2 + 1)].mean() for i in range(len(y))])
    return t, out

S = 0.15            # Selic fixa: isola a regra fiscal
T = 20.0

CEN = [
    ('Teto de gastos (EC 95)',        dict(regime_gasto='teto'),                                  '#d6604d', '-'),
    ('Arcabouço (LC 200)',            dict(regime_gasto='arcabouco'),                             '#f4a582', '-'),
    ('Revogar SEM âncora',            dict(regime_gasto='livre'),                                 '#b2182b', '--'),
    ('Revogar + regra de dívida',     dict(regra_divida=True),                                    '#4393c3', '-'),
    ('Revogar + regra + topo + invest', dict(regra_divida=True, tax_rich=0.008, invest_pub=0.015), '#1b7837', '-'),
]

runs = [(nome, simula(S, T=T, every=0.5, **kw), cor, ls) for nome, kw, cor, ls in CEN]

plt.rcParams.update({'font.size': 10.5, 'axes.grid': True, 'grid.alpha': 0.25})
fig, ax = plt.subplots(2, 2, figsize=(14, 9))
(axD, axG), (axW, axY) = ax


def serie(h, campo, idx=False):
    t = [x['t'] for x in h]
    if idx:
        y0 = h[0][campo]
        y = [100 * x[campo] / y0 for x in h]
    else:
        y = [x[campo] for x in h]
    return suave(t, y)


for nome, h, cor, ls in runs:
    lw = 2.8 if cor == '#1b7837' else 2.0
    axD.plot(*serie(h, 'b'), ls, color=cor, lw=lw, label=nome)
    axG.plot(*serie(h, 'gsy'), ls, color=cor, lw=lw)
    axW.plot(*serie(h, 'omega'), ls, color=cor, lw=lw)
    axY.plot(*serie(h, 'Y', idx=True), ls, color=cor, lw=lw)

axD.set_title('A. Dívida / PIB — "revogar E ancorar" controla melhor que o teto',
              fontweight='bold', fontsize=11)
axD.set_ylabel('dívida / PIB'); axD.set_xlabel('anos')
axD.annotate('revogar sem âncora:\na dívida EXPLODE', xy=(T, runs[2][1][-1]['b']),
             xytext=(11, 3.2), color='#b2182b', fontsize=9.5, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#b2182b'))

axG.set_title('B. Gasto social / PIB — o teto esmaga; o pacote ancorado preserva',
              fontweight='bold', fontsize=11)
axG.set_ylabel('gasto público / PIB'); axG.set_xlabel('anos')
axG.annotate('"ajuste por composição":\no social encolhe sem corte nominal',
             xy=(T, runs[0][1][-1]['gsy']), xytext=(6, 0.19), color='#d6604d', fontsize=9,
             arrowprops=dict(arrowstyle='->', color='#d6604d'))

axW.set_title('C. Parcela salarial ω — o teto "cresce" REPRIMINDO salário (caráter de classe)',
              fontweight='bold', fontsize=11)
axW.set_ylabel('salários / PIB (ω)'); axW.set_xlabel('anos')
axW.axhline(1.0, color='#999', lw=0.8, ls=':')
axW.text(1, 1.02, 'ω>1 = profit-squeeze (segurar salário a Selic 15% → a reforma precisa do corte)',
         fontsize=7.8, color='#666')

axY.set_title('D. PIB acumulado — o teto cresce mais, mas é crescimento por repressão',
              fontweight='bold', fontsize=11)
axY.set_ylabel('PIB (índice, t0 = 100)'); axY.set_xlabel('anos')

axD.legend(loc='upper left', fontsize=9, framealpha=0.95, ncol=1)
fig.suptitle('O "PACOTE DO MAL" NO MODELO — consequência de abolir o teto de gastos + o arcabouço fiscal',
             fontsize=14, fontweight='bold')
fig.text(0.5, 0.005,
         'Modelo SFC Brasil (Minsky/Godley) · Selic fixa 15% (isola a regra fiscal) · '
         'teto=EC95, arcabouço=LC200 · curvas = tendência (média móvel 3 anos) · mecanismo, não previsão',
         ha='center', fontsize=8.5, color='#666')
fig.tight_layout(rect=[0, 0.025, 1, 0.955])
out = 'saida/01_bateria_teto.png'
fig.savefig(out, dpi=140)
print('salvo:', out)

# placar no terminal
print(f'\n{"cenário":34} | dívida | G/Y  | ω    | PIB(t0=100)')
for nome, h, _, _ in runs:
    idx = 100 * h[-1]['Y'] / h[0]['Y']
    print(f'{nome:34} |  {h[-1]["b"]:4.2f}  | {h[-1]["gsy"]:.2f} | {h[-1]["omega"]:.2f} |   {idx:5.1f}')
