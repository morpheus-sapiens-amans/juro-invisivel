#!/usr/bin/env python3
"""
teste_regime.py — O CORAÇÃO DO ARTIGO: o câmbio responde à Selic com SINAL OPOSTO
conforme o regime fiscal (phi endógeno). Gera modelos-saida/00_teste_regime.png.

  Regime NORMAL (dívida baixa):    Selic alta APRECIA o Real (convencional).
  Dominância fiscal (dívida alta): Selic alta DEPRECIA o Real (o juro se autossabota).

A inversão é a tese do André Lara Resende, agora SAINDO do modelo stock-flow.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from brasil_sfc import simula, PARS

T = 8.0                                   # horizonte curto: o regime não migra no meio da rodada
SELICS = np.array([0.16, 0.14, 0.12, 0.10, 0.08, 0.06])
B_DOM = PARS['b_dom']                      # limiar de dominância (0.90)


def cambio_fim(sel, b0, tr=0.0):
    return simula(sel, phi_endog=True, b0=b0, T=T, tax_rich=tr)[-1]['cambio']


# --- Painel A: câmbio × Selic, uma curva por regime ---
camb_normal = [cambio_fim(s, 0.45, tr=0.02) for s in SELICS]   # dívida baixa e estável
camb_domin = [cambio_fim(s, 1.25) for s in SELICS]             # dívida alta (dominância)

# --- Painel B: Δcâmbio de um corte de 6 p.p. (16%→10%) × nível de dívida ---
B0S = np.linspace(0.40, 1.60, 25)
d_camb = []
for b0 in B0S:
    tr = 0.02 if b0 < B_DOM else 0.0       # economia saudável segura o primário; dominância não
    alto = cambio_fim(0.16, b0, tr)
    corte = cambio_fim(0.10, b0, tr)
    d_camb.append(corte - alto)            # >0 deprecia no corte (normal); <0 aprecia (dominância)
d_camb = np.array(d_camb)

plt.rcParams.update({'font.size': 11, 'axes.grid': True, 'grid.alpha': 0.25})
fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 5.2))

# Painel A
axA.plot(SELICS * 100, camb_normal, 'o-', color='#1b7837', lw=2.4, ms=7,
         label='Regime normal (dívida ~45% do PIB)')
axA.plot(SELICS * 100, camb_domin, 's-', color='#b2182b', lw=2.4, ms=7,
         label='Dominância fiscal (dívida ~125% do PIB)')
axA.set_xlabel('Selic (% a.a.)   (→ cortar a Selic)')
axA.set_ylabel('Câmbio (R$/US$, índice; ↑ = Real mais fraco)')
axA.set_title('A. A mesma Selic, efeito OPOSTO no câmbio', fontweight='bold', fontsize=12)
axA.invert_xaxis()                         # ler da esquerda p/ direita = cortar a Selic
axA.annotate('normal:\ncorte DEPRECIA', xy=(6.4, camb_normal[-1]), xytext=(9, 1.22),
             fontsize=9.5, color='#1b7837', ha='center',
             arrowprops=dict(arrowstyle='->', color='#1b7837'))
axA.annotate('dominância:\ncorte APRECIA', xy=(6.4, camb_domin[-1]), xytext=(9.5, 1.95),
             fontsize=9.5, color='#b2182b', ha='center',
             arrowprops=dict(arrowstyle='->', color='#b2182b'))
axA.legend(loc='upper left', fontsize=9.5, framealpha=0.95)

# Painel B
axB.axhline(0, color='#333', lw=1)
axB.axvline(B_DOM * 100, color='#555', ls='--', lw=1.2)
axB.fill_between(B0S * 100, d_camb, 0, where=(d_camb >= 0), color='#1b7837', alpha=0.18)
axB.fill_between(B0S * 100, d_camb, 0, where=(d_camb < 0), color='#b2182b', alpha=0.18)
axB.plot(B0S * 100, d_camb, '-', color='#2166ac', lw=2.6)
axB.set_xlabel('Dívida/PIB inicial (%)')
axB.set_ylabel('Δ câmbio de um corte de 6 p.p. na Selic')
axB.set_title('B. O regime vira o sinal (limiar de dominância)', fontweight='bold', fontsize=12)
axB.text(52, max(d_camb) * 0.42, 'corte\nDEPRECIA\n(regime normal)', ha='center', va='top',
         fontsize=9.5, color='#1b7837', fontweight='bold')
axB.text(135, min(d_camb) * 0.55, 'corte\nAPRECIA\n(dominância)', ha='center',
         fontsize=9.5, color='#b2182b', fontweight='bold')
axB.text(B_DOM * 100 + 1, max(d_camb) * 0.9, f'  limiar b_dom ≈ {B_DOM*100:.0f}%',
         fontsize=9, color='#555', rotation=90, va='top')

fig.suptitle('TESTE DE REGIME — o câmbio e a Selic: o sinal depende da saúde fiscal (phi endógeno)',
             fontsize=13.5, fontweight='bold')
fig.text(0.5, 0.005,
         'Modelo SFC Brasil (Minsky/Godley) · phi endógeno à dívida · '
         'tese ALR "Eu Acuso" · mecanismo, não previsão',
         ha='center', fontsize=8.5, color='#666')
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
out = 'saida/00_teste_regime.png'
fig.savefig(out, dpi=140)
print('salvo:', out)
