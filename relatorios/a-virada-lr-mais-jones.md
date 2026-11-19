# A virada: por que só LR + Jones faz o modelo fechar

Esta é a parte mais honesta — e mais importante — de todo o trabalho: **nenhuma peça,
sozinha, é a saída segura.** Nem o corte da Selic do Lara Resende, nem o "revogar o teto"
do Jones Manoel. Foi só quando as duas foram **combinadas** — ancorar pela via distributiva
*e* cortar o juro gradualmente, com defesas — que o modelo controlou dívida *e* câmbio ao
mesmo tempo.

Abaixo está a jornada auditável: cada hipótese é um script que você pode rodar
([`../modelos/jornada/`](../modelos/jornada/)), importando o mesmo motor
([`../modelos/brasil_sfc.py`](../modelos/brasil_sfc.py)). Os números são **mecanismo, não
previsão** — leia direção e ordem de grandeza. Câmbio em índice (t0 = 1).

```bash
cd modelos/jornada
python3 01_lr_puro.py     python3 02_ouro.py     python3 03_jones_puro.py
python3 04_lr_jones.py    python3 05_escolas.py
```

---

## Hipótese 1 — LR puro: cortar a Selic de uma vez

| cenário | dívida/PIB | câmbio | gasto social (G/Y) |
|---|---|---|---|
| status quo (Selic 15%) | 2,92 | 5,91 | 0,24 |
| **LR puro (Selic 7,5% de uma vez, sem defesas)** | **1,49** | **1,78** | 0,31 |

**Veredito: não se sustenta como certeza — é uma aposta.** No modelo (que *flerta* com a
dominância) cortar a Selic melhora dívida e câmbio frente ao status quo. Mas a proposta pura
(i) **aposta no regime** — o mesmo corte *deprecia* o Real se a economia não estiver em
dominância, e o modelo não prova que está; (ii) o **salto abrupto** convida o overshoot
cambial; e (iii) fica **atrás do arranjo ancorado** (dívida 1,49 vs 1,18; câmbio 1,78 vs
1,23). LR tem a matemática certa, sem a saída que a torna segura.

## Hipótese 2 — Ouro / reservas: formar reservas para defender o Real

| Selic | carrego médio (% do PIB/ano) | dívida/PIB (fim) |
|---|---|---|
| 15% | 11,43 | 6,43 |
| 11% | 4,16 | 3,12 |
| 8% | 1,07 | 1,80 |

**Veredito: só tem relevância quando a Selic cai.** O "carrego" (custo quase-fiscal de
segurar reservas: paga-se Selic para captar o que rende menos lá fora) é uma sangria de ~11%
do PIB/ano com a Selic a 15%, e **derrete** para ~1% com a Selic a 8%. O ouro não é alavanca
primária: é **complemento** que só se paga dentro da sequência, junto do corte do juro.

## Hipótese 3 — Jones puro: "revogar e largar"

| cenário | dívida/PIB | câmbio | gasto social (G/Y) |
|---|---|---|---|
| governo (PLP 299, arcabouço) | 2,92 | 5,91 | 0,24 |
| **Jones puro (revogar sem âncora, Selic 15%)** | **3,40** | **9,16** | 0,35 |

**Veredito: não se estabiliza — é o pior cenário da bateria.** O diagnóstico está certo (o
alvo é o juro, não o primário de ~0,3% do PIB), mas revogar o teto *sem pôr âncora no lugar*
faz dívida (3,40) e câmbio (9,16) dispararem. Jones tem a saída distributiva, sem a
matemática. (Detalhe em [`dialogo-jones.md`](dialogo-jones.md).)

## Hipótese 4 — LR + Jones: a síntese que funciona

| cenário | dívida/PIB | câmbio | gasto social (G/Y) |
|---|---|---|---|
| governo (PLP 299, Selic 15%) | 2,92 | 5,91 | 0,24 |
| Jones puro (revogar e largar) | 3,40 | 9,16 | 0,35 |
| **LR+Jones operacional (Selic 10% + âncora + topo + fricção)** | **1,18** | **1,23** | 0,23 |

**Veredito: funciona.** Revogar *e* ancorar na trajetória da dívida (de Jones), corte
*gradual* da Selic com defesas cambiais (de LR), cobrança do topo e fricção. Controla dívida
**e** câmbio ao mesmo tempo, e supera o pacote do governo nos dois. A chave: **a alternativa
direta (cobrar o topo) não é alternativa ao corte da Selic — é a precondição que o torna
seguro. Ancora-se primeiro, corta-se depois.**

## Hipótese 5 — O choque das seis escolas (a confirmação)

Um único esqueleto, cada escola como um conjunto de premissas (A = com a alavanca
distributiva; B = sem). Dívida/PIB em 2036:

| escola | dívida A | dívida B | A−B | PIB A/B |
|---|---|---|---|---|
| Ortodoxia | 107,5 | 115,4 | −7,9 | +0,39% |
| Pós-keynesiana | 105,3 | 110,2 | −4,9 | −0,20% |
| MMT | 85,2 | 88,5 | −3,3 | −0,03% |
| Marxista | 103,0 | 107,8 | −4,8 | 0,00% |
| Austríaca | 112,2 | 121,9 | −9,7 | +0,99% |
| **Economia política (veto)** | **87,4** | **122,2** | **−34,9** | **+4,33%** |

**Veredito: a alavanca distributiva domina.** Para quase todas as escolas, "ajustar ou não"
move pouco a dívida e quase nada o crescimento. Só a economia política com **veto
distributivo** (cobrar o topo, barrar o corte no povo) produz, ao mesmo tempo, o maior
controle da dívida (−34,9) e o maior crescimento (+4,33%). O modelo não arbitra qual escola
está certa — mostra que **o parafuso que move o resultado é o de quem paga a conta.**

---

## Síntese da jornada

Nenhuma peça, sozinha, é a saída segura. Cortar a Selic (LR) é aposta no regime e salto
abrupto; formar reservas (ouro) só paga com o juro caindo; revogar e largar (Jones) explode
tudo. **Só a sequência — ancorar pela via distributiva e cortar o juro gradualmente, com
defesas — controla dívida e câmbio ao mesmo tempo.** O choque das escolas confirma onde está
o parafuso: na alavanca distributiva, não na fiscal-ortodoxa.

**Guardrails (honestidade do método):**
- A **dominância** fiscal é construção do modelo, não prova empírica — "flerta com a
  dominância" (ver [`confronto-dejanir-silva.md`](confronto-dejanir-silva.md)).
- A parcela salarial (ω) sofre *overshoot* de Goodwin nos cenários ancorados — lê-se a
  direção, não o nível exato.
- Horizonte confiável ~25–30 anos; números relativos, não manchete.

O robusto é a espinha: **o juro domina a dívida; sem âncora ela dispara; a mesma meta pela
via do topo preserva o social e supera o corte do povo.**
