#!/usr/bin/env python3
"""
HIPÓTESE 4 — LR + JONES (o arranjo operacional): revogar E ancorar na trajetória da
dívida (de Jones), corte GRADUAL da Selic com defesas cambiais (de LR), cobrança do topo
e fricção. A ponte é o corte gradual + a âncora distributiva.

Veredito: FUNCIONA. Controla dívida E câmbio ao mesmo tempo e supera o pacote do governo
nos dois, preservando o social de forma sustentável. A alternativa direta (cobrar o topo)
não é alternativa ao corte da Selic — é a precondição que o torna seguro. Ancora-se
primeiro, corta-se depois.

Nota de honestidade: ω (parcela salarial) sofre overshoot de Goodwin nos cenários
ancorados; lê-se DIREÇÃO e ordem de grandeza, não o nível exato. Horizonte confiável
~25-30 anos. Roda o motor canônico ../brasil_sfc.py.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from brasil_sfc import simula

T = 20.0


def placar(nome, h):
    print(f'{nome:46} | dívida {h[-1]["b"]:5.2f} | câmbio {h[-1]["cambio"]:5.2f} '
          f'| G/Y {h[-1]["gsy"]:.2f}')


if __name__ == '__main__':
    print('\n== HIPÓTESE 4 — LR + JONES (revogar + ancorar + corte gradual) ==')
    governo = simula(0.15, regime_gasto='arcabouco', phi_endog=True,
                     conta_carrego=True, T=T, every=0.5)
    jones_puro = simula(0.15, regime_gasto='livre', invest_pub=0.02, phi_endog=True,
                        conta_carrego=True, T=T, every=0.5)
    lr_jones = simula(0.10, regra_divida=True, invest_pub=0.02, tax_rich=0.008,
                      tau_fric=0.30, phi_endog=True, conta_carrego=True, T=T, every=0.5)
    placar('governo (PLP 299, Selic 15%)', governo)
    placar('Jones puro (revogar e largar)', jones_puro)
    placar('LR+Jones operacional (Selic 10%)', lr_jones)
    print('leitura: só a sequência (ancora, depois corta) controla dívida E câmbio.')
