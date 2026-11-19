#!/usr/bin/env python3
"""
HIPÓTESE 3 — JONES PURO ("revogar e largar"): revogar o teto + reindustrializar, com o
juro como está e NADA no lugar da âncora.

Veredito: NÃO se estabiliza. O diagnóstico está certo (o alvo é o juro, não o primário),
mas revogar sem ancorar faz a dívida e o câmbio dispararem — é o pior cenário da bateria.
O próprio campo marxista declara o ponto cego (§8): não há teoria operacional de como
baixar o juro em economia aberta. Jones tem a saída distributiva sem a matemática.

Roda o motor canônico ../brasil_sfc.py.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from brasil_sfc import simula

T = 20.0


def placar(nome, h):
    print(f'{nome:46} | dívida {h[-1]["b"]:5.2f} | câmbio {h[-1]["cambio"]:5.2f} '
          f'| G/Y {h[-1]["gsy"]:.2f}')


if __name__ == '__main__':
    print('\n== HIPÓTESE 3 — JONES PURO (revogar e largar, Selic 15%) ==')
    governo = simula(0.15, regime_gasto='arcabouco', phi_endog=True,
                     conta_carrego=True, T=T, every=0.5)
    jones_puro = simula(0.15, regime_gasto='livre', invest_pub=0.02, phi_endog=True,
                        conta_carrego=True, T=T, every=0.5)
    placar('governo (PLP 299, arcabouço)', governo)
    placar('Jones puro (revogar sem âncora)', jones_puro)
    print('leitura: revogar e largar explode dívida e câmbio — diagnóstico certo, cura incompleta.')
