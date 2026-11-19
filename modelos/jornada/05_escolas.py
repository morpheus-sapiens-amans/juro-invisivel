#!/usr/bin/env python3
"""
HIPÓTESE 5 — O CHOQUE DAS ESCOLAS: um único esqueleto de modelo, e cada escola
(ortodoxa, pós-keynesiana, MMT, marxista, austríaca, economia política) entrando como um
conjunto de PREMISSAS diferente. A pergunta não é qual escola está certa — o modelo não
arbitra isso — mas em que premissa cada uma aposta.

Veredito: a economia política com veto distributivo (cobrar o topo, barrar o corte no
povo) domina — o maior controle da dívida E o maior crescimento. A alavanca que move o
resultado não é a fiscal-ortodoxa, do aperto; é a distributiva, de quem paga a conta.

Este teste roda o motor separado ../modelo-unico-escolas.py.
"""
import sys, os, subprocess

if __name__ == '__main__':
    print('\n== HIPÓTESE 5 — O CHOQUE DAS SEIS ESCOLAS ==')
    alvo = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', 'modelo-unico-escolas.py')
    subprocess.run([sys.executable, os.path.abspath(alvo)])
