#!/usr/bin/env python3
"""
HIPÓTESE 2 — OURO / RESERVAS: formar reservas (accum0 alto) para defender o Real.

Veredito: só tem relevância QUANDO a Selic cai. O "carrego" — o custo quase-fiscal de
segurar reservas (paga-se Selic para captar o que rende menos lá fora) — é alto com a
Selic alta e DERRETE quando a Selic baixa. Logo o ouro não é alavanca primária: é
complemento que só se paga dentro da sequência, depois/junto do corte do juro.

Roda o motor canônico ../brasil_sfc.py.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from brasil_sfc import simula

T = 20.0

if __name__ == '__main__':
    print('\n== HIPÓTESE 2 — OURO / RESERVAS (o carrego por nível de Selic) ==')
    for sel in (0.15, 0.13, 0.11, 0.10, 0.08):
        h = simula(sel, R0=0.25, accum0=0.008, conta_carrego=True, T=T, every=1.0)
        carr = sum(x['carrego'] for x in h) / T
        print(f'Selic {sel:4.0%} | carrego médio {carr*100:5.2f}% do PIB/ano '
              f'| dívida fim {h[-1]["b"]:5.2f}')
    print('leitura: o carrego cai com a Selic — o ouro só "paga" com o juro caindo.')
