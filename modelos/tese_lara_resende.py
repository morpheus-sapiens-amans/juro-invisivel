"""
tese_lara_resende.py — a tese de André Lara Resende ("Eu Acuso"), rodável.

A TESE, em uma linha:
  A mídia/mercado diz "a dívida explode POR CAUSA DO GASTO → corte gasto".
  Lara Resende vira a mesa: "a dívida explode POR CAUSA DO JURO → baixe o juro".
  O déficit PRIMÁRIO do Brasil é pequeno; o rombo é o déficit NOMINAL, e a diferença
  entre os dois é quase toda conta de juros. Logo, o réu não é a escola nem o hospital —
  é a própria Selic, que infla a dívida que diz combater.

O QUE ESTE SCRIPT FAZ:
  Roda o nosso modelo do Brasil (brasil_sfc.py) sob diferentes níveis de Selic e mostra,
  em números, o mecanismo central do argumento: baixar a Selic desacelera a espiral da
  dívida. Faz isso nos DOIS regimes do modelo (normal e dominância fiscal), para você ver
  onde a tese é robusta e onde ela vira aposta.

HONESTIDADE (leia antes de usar como prova):
  - É um modelo de MECANISMO, não previsão calibrada do Brasil.
  - O regime de "dominância fiscal" (onde cortar a Selic APRECIA o Real) é um mecanismo
    que NÓS construímos no modelo. Dentro do modelo, o Brasil está nessa zona (ponto de
    virada ~56% de dívida, hoje ~83%). Que o mecanismo seja a descrição correta do Brasil
    real é hipótese — o modelo estimado de Dejanir Silva não o reproduz. Ver
    ../relatorios/confronto-dejanir-silva.md.
  - Para a figura clássica do "juro infla a dívida" (juro 3%/6%/9% → colapso em
    ~130/73/53 anos), rode keen_model.py (gera fig2_juro_colapso.png).

Rode:  python3 tese_lara_resende.py       (só precisa de numpy)
"""
import brasil_sfc as sfc


def roda(selic, phi_endog, b0, T=20.0):
    h = sfc.simula(Selic=selic, phi_endog=phi_endog, b0=b0, T=T, every=1.0)
    return h


def linha(nome, h):
    s0, sL = h[0], h[-1]
    # 'rg' = r_gov - g_nom (o quanto o juro supera o crescimento nominal: o motor da dívida)
    print(f"  {nome:34s} b: {s0['b']:.2f} -> {sL['b']:.2f}   "
          f"câmbio: {sL['cambio']:.2f}   infl: {100*sL['infl']:.1f}%   "
          f"(r-g): {sL['rg']:+.3f}")


if __name__ == "__main__":
    print("=" * 74)
    print("A TESE DE LARA RESENDE NO MODELO — baixar a Selic desacelera a dívida?")
    print("=" * 74)
    print("Dívida pública/PIB no início e após 20 anos, para três níveis de Selic.\n")

    print("REGIME NORMAL (dívida abaixo do limiar de dominância):")
    for selic, nome in [(0.1375, "Selic 13,75% (status quo)"),
                        (0.10, "Selic 10,00% (corte gradual)"),
                        (0.075, "Selic  7,50% (corte forte)")]:
        linha(nome, roda(selic, phi_endog=False, b0=0.78))

    print("\nREGIME DE DOMINÂNCIA FISCAL (dívida alta, b0=1.00 — a aposta da tese):")
    for selic, nome in [(0.1375, "Selic 13,75% (status quo)"),
                        (0.10, "Selic 10,00% (corte gradual)"),
                        (0.075, "Selic  7,50% (corte forte)")]:
        linha(nome, roda(selic, phi_endog=True, b0=1.00))

    print("\n" + "-" * 74)
    print("""LEITURA:
  • Em AMBOS os regimes, baixar a Selic reduz o motor da dívida (r-g) e a trajetória de
    dívida/PIB termina mais baixa. Esse é o núcleo do 'Eu Acuso': o juro é o que infla a
    dívida — é aritmética, não ideologia.
  • A DIFERENÇA está no câmbio. No regime normal, cortar a Selic tende a depreciar o Real
    (pressiona preços). No regime de dominância, cortar APRECIA o Real — este é o ponto
    mais forte e mais DISPUTADO da tese (ver a ressalva de honestidade no topo do arquivo).

ONDE A TESE É SÓLIDA x ONDE É APOSTA (as três camadas):
  (a) DIAGNÓSTICO  — o rombo é juro, não gasto social .......... SÓLIDO
  (b) INSTITUCIONAL— há teto pro gasto social e nenhum pro juro . FORTE
  (c) SOLUÇÃO      — baixar a Selic sem detonar o câmbio ........ CORAJOSA e DISPUTADA
  Dá pra cravar (a) e (b) sem comprar inteira a (c).

  Mude os parâmetros acima (b0, Selic, phi_endog) e rode de novo. É a sua bancada.""")
