#!/usr/bin/env python3
"""
HIPÓTESE 1 — LR PURO (o "Eu Acuso"): tabelar / cortar a Selic de uma vez, e mais nada.

Veredito: NÃO se sustenta. Cortar a Selic numa economia ainda não-ancorada pressiona
o Real (phi endógeno faz o prêmio de risco reagir), e o corte isolado não doma a
trajetória da dívida — falta a âncora distributiva. LR tem a matemática certa (o rombo
é o juro) sem a saída distributiva.

Roda o motor canônico ../brasil_sfc.py (não duplica o modelo).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from brasil_sfc import simula

T = 20.0


def placar(nome, h):
    print(f'{nome:46} | dívida {h[-1]["b"]:5.2f} | câmbio {h[-1]["cambio"]:5.2f} '
          f'| G/Y {h[-1]["gsy"]:.2f}')


if __name__ == '__main__':
    print('\n== HIPÓTESE 1 — LR PURO (tabelar a Selic, sem âncora/defesas) ==')
    # status quo: Selic 15%, arcabouço de pé
    status_quo = simula(0.15, regime_gasto='arcabouco', phi_endog=True,
                        conta_carrego=True, T=T, every=0.5)
    # LR puro: tabelamento abrupto para 7,5%, SEM âncora de dívida, SEM fricção, SEM reservas
    lr_puro = simula(0.075, phi_endog=True, conta_carrego=True, T=T, every=0.5)
    placar('status quo (Selic 15%)', status_quo)
    placar('LR puro (Selic 7,5% de uma vez, sem defesas)', lr_puro)
    print('leitura: o corte isolado pressiona o câmbio e não ancora a dívida sozinho.')
