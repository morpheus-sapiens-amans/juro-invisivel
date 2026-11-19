#!/usr/bin/env python3
"""
bateria_jones.py — O PENSAMENTO DO JONES MANOEL NO SFC.
Testa a proposta marxista explicitada no "Almoço dos Irmãos" (Podcast 3 Irmãos) e no
Relatório 4 (Marxistas): o problema NÃO é o primário (déficit ≈ -0,5% do PIB), é o JURO
(≈ 9% do PIB). Logo: (1) revogar o teto de gastos, (2) atacar a taxa de juros, (3)
reindustrializar com coordenação do Estado (Kalecki/Mazzucato: sem Estado não há indústria).

O relatório marxista declara o PRÓPRIO ponto cego da escola (§8):
  "O que a escola NÃO consegue dizer: o que fazer com a trajetória da dívida. 'Baixar os
   juros' é a resposta, mas a escola não tem teoria operacional de como fazê-lo numa
   economia aberta sem os efeitos que a ortodoxia prevê (câmbio, inflação)."

É esse buraco que o SFC preenche. Esta bateria responde: o diagnóstico do Jones (o alvo é o
juro) se sustenta no modelo? E "revogar e largar" + cortar a Selic sobrevive ao contra-ataque
cambial — ou precisa do ARRANJO operacional (reservas/ouro, fricção τ, âncora de dívida) que a
proposta do Laércio acrescenta?

Selic VARIA aqui (ao contrário da bateria_teto, que a fixa): o corte do juro É a tese do Jones.
phi_endog=True em todos → o custo cambial do corte aparece honestamente (teste de dominância).
conta_carrego=True → cortar a Selic MELHORA o quase-fiscal das reservas (resultado pró-Jones).

Gera modelos-saida/11_bateria_jones.png (4 painéis) + imprime o placar.
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
    return np.array([y[max(0, i - k // 2):min(len(y), i + k // 2 + 1)].mean() for i in range(len(y))])


T = 20.0
HON = dict(phi_endog=True, conta_carrego=True)   # honestidade cambial + carrego das reservas em todos

# (nome, Selic, kwargs, cor, estilo)
# ATRIBUIÇÃO HONESTA: Jones DIAGNOSTICA o juro como a disfunção, mas seu REMÉDIO é estrutural
# (revogar teto + reindustrializar); ele NÃO propõe o corte operacional da Selic (ponto cego da
# escola, §8). O corte GRADUAL do juro é a ponte que o Laércio construiu a partir do diagnóstico
# Jones/LR — sem o tabelamento abrupto do LR. Os cenários abaixo separam o que é de cada um.
CEN = [
    ('Governo — PLP 299 (arcabouço, Selic 15%)',
        0.15, dict(regime_gasto='arcabouco'),                                    '#f4a582', '-'),
    ('Jones literal — revogar teto + reindustrializar (juro como está)',
        0.15, dict(regime_gasto='livre', invest_pub=0.02),                       '#b2182b', '--'),
    ('+ corte GRADUAL do juro (operacionaliza o diagnóstico — ponte Laércio/LR)',
        0.10, dict(regime_gasto='livre', invest_pub=0.02),                       '#5aae61', '-'),
    ('Jones operacional — + âncora de dívida, topo e fricção τ (arranjo completo)',
        0.10, dict(regra_divida=True, invest_pub=0.02, tax_rich=0.008, tau_fric=0.30), '#1b7837', '-'),
]

runs = [(nome, simula(S, T=T, every=0.5, **{**HON, **kw}), cor, ls)
        for nome, S, kw, cor, ls in CEN]

plt.rcParams.update({'font.size': 10.5, 'axes.grid': True, 'grid.alpha': 0.25})
fig, ax = plt.subplots(2, 2, figsize=(14.5, 9.5))
(axD, axE), (axG, axY) = ax


def serie(h, campo, idx=False):
    t = np.array([x['t'] for x in h])
    if idx:
        y = np.array([100 * x[campo] / h[0][campo] for x in h])
    else:
        y = np.array([x[campo] for x in h])
    return t, suave(t, y)


for nome, h, cor, ls in runs:
    lw = 2.9 if cor == '#1b7837' else 2.1
    axD.plot(*serie(h, 'b'), ls, color=cor, lw=lw, label=nome)
    axE.plot(*serie(h, 'cambio'), ls, color=cor, lw=lw)
    axG.plot(*serie(h, 'gsy'), ls, color=cor, lw=lw)
    axY.plot(*serie(h, 'Y', idx=True), ls, color=cor, lw=lw)

axD.set_title('A. Dívida / PIB — o alvo é o JURO, não o primário', fontweight='bold', fontsize=11)
axD.set_ylabel('dívida / PIB'); axD.set_xlabel('anos')
axD.annotate('Jones literal (juro intacto):\nreindustrializar sozinho não doma a dívida',
             xy=(17.5, runs[1][1][-2]['b']), xytext=(9.5, 2.55),
             color='#b2182b', fontsize=8.6, fontweight='bold', ha='center',
             arrowprops=dict(arrowstyle='->', color='#b2182b'))

axE.set_title('B. Câmbio (R$/US$, t0=1) — o CUSTO do corte (teste de dominância)',
              fontweight='bold', fontsize=11)
axE.set_ylabel('câmbio (índice)'); axE.set_xlabel('anos')
axE.axhline(1.0, color='#999', lw=0.8, ls=':')
axE.annotate('só o arranjo operacional (τ + âncora)\nsegura o Real; cortar e largar o enfraquece',
             xy=(16, runs[3][1][-3]['cambio']), xytext=(2.5, 4.3), color='#1b7837',
             fontsize=8.6, fontweight='bold', arrowprops=dict(arrowstyle='->', color='#1b7837'))

axG.set_title('C. Gasto social / PIB — cortar o juro preserva; a âncora disciplina',
              fontweight='bold', fontsize=11)
axG.set_ylabel('gasto público / PIB'); axG.set_xlabel('anos')
axG.annotate('o arcabouço esmaga o social\n(ajuste por composição)',
             xy=(13, runs[0][1][26]['gsy']), xytext=(8.5, 0.30),
             color='#d6604d', fontsize=8.3, arrowprops=dict(arrowstyle='->', color='#d6604d'))
axG.annotate('a âncora de dívida troca\nsocial por controle (a conta honesta)',
             xy=(10.5, runs[3][1][21]['gsy']), xytext=(2.5, 0.245),
             color='#1b7837', fontsize=8.3, arrowprops=dict(arrowstyle='->', color='#1b7837'))

axY.set_title('D. PIB acumulado — reindustrialização puxa o denominador',
              fontweight='bold', fontsize=11)
axY.set_ylabel('PIB (índice, t0 = 100)'); axY.set_xlabel('anos')

axD.legend(loc='upper left', fontsize=8.3, framealpha=0.95, ncol=1)
fig.suptitle('O PENSAMENTO DO JONES NO SFC — o alvo é o juro, e o que o completa é o arranjo operacional',
             fontsize=13.5, fontweight='bold')
fig.text(0.5, 0.005,
         'Modelo SFC Brasil (Minsky/Godley, economia aberta) · Selic VARIA (o corte é a tese) · '
         'phi endógeno (custo cambial honesto) + carrego das reservas · curvas = tendência (média móvel 3a) · '
         'mecanismo, não previsão',
         ha='center', fontsize=8.3, color='#666')
fig.tight_layout(rect=[0, 0.025, 1, 0.955])
out = 'saida/11_bateria_jones.png'
fig.savefig(out, dpi=140)
print('salvo:', out)

# placar no terminal
print(f'\n{"cenário":58} | Selic | dívida | câmbio | R/Y  | G/Y  | ω    | PIB(t0=100)')
print('-' * 120)
for (nome, S, kw, _, _), (_, h, _, _) in zip(CEN, runs):
    idx = 100 * h[-1]['Y'] / h[0]['Y']
    short = nome.split(' —')[0][:56]
    print(f'{short:58} | {S:4.0%} |  {h[-1]["b"]:4.2f}  |  {h[-1]["cambio"]:4.2f}  | {h[-1]["R"]:4.2f} '
          f'| {h[-1]["gsy"]:.2f} | {h[-1]["omega"]:.2f} |   {idx:5.1f}')
