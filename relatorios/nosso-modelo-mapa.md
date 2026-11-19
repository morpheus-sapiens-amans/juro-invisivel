# MAPA DO NOSSO MODELO (BrasilSFC) — para comparação com o FTPL/DSGE do Dejanir

Mapa conciso do modelo próprio, um stock-flow consistent (SFC) heterodoxo tipo
Godley-Lavoie-Minsky, construído sobre o núcleo `MinskyGovernmentNonlinear` do
Steve Keen (Goodwin não-linear + governo contracíclico) e estendido com quatro
blocos novos (BC/Selic, dívida pública, fiscal/teto, externo/câmbio).

Arquivos-fonte (o núcleo está em [`../modelos/brasil_sfc.py`](../modelos/brasil_sfc.py)):
- `brasil_sfc.py` — modelo central e canônico (função `simula`, dicionário `PARS`).
- `cambio.py` — bloco de câmbio **standalone** (reduzido, ilustrativo, curto prazo).
- `selic_fases.py` — Selic em fases/degraus (A/B/C), economia FECHADA.
- `teste_regime.py` — teste de regime (phi endógeno): o sinal câmbio×Selic.
- `bateria_teto.py` — bateria do teto/arcabouço (o "pacote do mal").

> **Natureza do modelo:** o objetivo declarado é **MECANISMO, não previsão
> calibrada**. É um sistema de EDOs integrado por Euler/RK4 em tempo contínuo
> (dt≈0,01, Euler em `brasil_sfc.py`; RK4 em `selic_fases.py`). Calibração "ao
> Brasil" (Copom nov/2025 Selic 15%, RMD set/2025, IBGE 2025, elasticidades IPEA,
> Lobo & Oreiro 2012) é ilustrativa, não econométrica.

---

## 1. Variáveis de estado e estoques

O núcleo de `brasil_sfc.py` carrega **9 estados** integrados no tempo:

| Estado | Símbolo | O que é |
|---|---|---|
| Capital | `K` | estoque de capital (núcleo real de Goodwin/Keen) |
| Produtividade do trabalho | `a` | cresce à `prod_gr` (tendência) |
| População/força de trabalho | `N` | cresce à `pop_gr` |
| Salário (taxa) | `w` | dinâmica de Phillips sobre o emprego λ |
| Dívida privada | `D_priv` | endividamento das firmas (canal Minsky) |
| **Dívida pública/PIB** | `b` | razão `B_gov/PIB`, estado-chave do bloco fiscal |
| Reservas/PIB | `R` | reservas internacionais que se formam e defendem o Real |
| Dívida externa/PIB | `D_ext` | passivo externo |
| Câmbio | `e` | taxa de câmbio nominal (Real/dólar), nível |

Variáveis derivadas a cada passo: PIB `Y=K/v`; emprego `L=Y/a`; taxa de emprego
`λ=L/N` (a "tensão" que move salário e gasto); massa salarial `Wages=w·L`; parcela
salarial `ω` (omega); inflação; primário `pb`; gasto `G`; carrego quase-fiscal.

**Composição da dívida pública (3 pernas)** — é o diferencial que faz a Selic
entrar na dinâmica: `theta=0,47` indexada à Selic (LFT), `theta_pre=0,26`
pré-fixada + câmbio, `theta_ipca=0,27` indexada ao IPCA. O juro efetivo da dívida
é `r_gov = θ·Selic + (1−θ)·r_pre` (mais a perna IPCA), que fecha o loop ALR "o
juro infla o déficit".

> Observação: `cambio.py`, `selic_fases.py` e `teste_regime.py` são satélites.
> `selic_fases.py` roda um sub-sistema fechado de **3 estados** (ω, λ, d) só para
> as fases da Selic; `cambio.py` é um modelo de câmbio reduzido à parte (não SFC).

---

## 2. Como a Selic entra

A **Selic é o botão de política** — argumento exógeno de `simula(Selic, ...)`.
Ela não é uma regra de Taylor endógena; é escolhida pelo analista. Seus canais:

1. **→ Dívida** (canal central ALR): via `r_gov = θ·Selic + (1−θ)·r_pre`, a Selic
   entra na equação-padrão `db/dt = (r_gov − g_nom)·b − pb`. Selic alta encarece o
   serviço da dívida indexada (47% em LFT) → infla o déficit → `b` sobe.
2. **→ Carrego quase-fiscal** (`conta_carrego`): paga-se Selic sobre as reservas;
   custo do carry = `Selic − ret_reservas − depreciação`. Cortar a Selic **melhora**
   o quase-fiscal (resultado contraintuitivo — acumular reserva/ouro não "firma o
   Real" porque custa Selic carregar).
3. **→ Câmbio** (dois canais, ver §3 e §5): via carry/UIP (`phi_carry`) e via
   sustentabilidade (`phi_sust`), com sinal que depende do regime.
4. **→ Inflação**: indiretamente, pelo câmbio (pass-through da depreciação) e pela
   demanda; **não há canal direto Selic→inflação do tipo curva IS + Phillips
   neokeynesiana** (ver §4). A Selic no modelo não "controla inflação" por demanda
   de forma microfundada — é quase neutra/perversa sobre preços, por desenho (é a
   tese).

Em `selic_fases.py` a Selic é tratada como **juro real** ≈ Selic nominal − 4%, e
comparam-se 3 trajetórias: A (status quo alto), B (fases/degraus com checkpoints —
a "escada" do Laércio), C (choque de corte único, que o LR evita).

---

## 3. Como o câmbio é modelado

Há **duas modelagens de câmbio**, e isso importa para a comparação:

**(a) `cambio.py` (satélite, curto prazo, NÃO-SFC, ilustrativo):**
- **Correção de erro**: o câmbio `e` persegue um equilíbrio `e*`, com
  `e* = 1 + GAMMA·max(0, RREF − r)` — ou seja, juro real baixo → `e*` (dólar) sobe
  → Real deprecia. É um canal tipo UIP **reduzido/implícito** (carry), não um UIP
  microfundado com paridade de juros formal.
- **Sentimento / overshoot**: variável de expectativa `s` que amplifica cortes
  BRUSCOS (decai em ~1,2 ano) — justifica por que o LR propõe FASES e não choque.
- **Intervenção**: o BC vende RESERVAS (`PHI`, `DRAIN`) para amortecer; reservas
  se esgotam.
- **Pass-through**: `PASS=0,10` → depreciação vira inflação importada.
- ⚠️ Ressalva no próprio código: aqui reservas DEFENDEM o Real (curto prazo); o
  modelo canônico mostra que ACUMULAR reserva não firma o Real (carrego). Não
  afirmar publicamente que "ouro firma o Real".

**(b) `brasil_sfc.py` (canônico):** o câmbio `e` é estado endógeno, com
**prêmio de risco e câmbio endógenos à dívida** quando `phi_endog=True`. Dois
canais (ver §5): `phi_carry` (UIP/carry — Selic alta aprecia) e `phi_sust`
(sustentabilidade — dívida alta faz o prêmio de risco subir e depreciar). Há
pass-through para preços (`pass_through=0,15`), elasticidades de comércio IPEA
(câmbio-exportação 0,6 / importação 0,3; condição Marshall-Lerner frágil; renda-M
1,5 > renda-X 1,0 → viés Thirlwall), e fricção de fluxo `tau_fric` (IOF-derivativos/
encaje) que reduz mobilidade do carry.

**Resumo:** temos UIP/carry **reduzido** (não paridade de juros formal com
expectativa racional) e um prêmio de risco **endógeno à razão dívida/PIB** (não
microfundado em aversão a risco de agente representativo). Pass-through: sim, nos
dois.

---

## 4. Inflação: qual mecanismo?

- **Curva de Phillips: sim, mas é a de SALÁRIO (à la Goodwin/Keen), não de preços.**
  Em `brasil_sfc.py`, `dw/dt` é governada por `genexp(λ, x_e, s_e, min_e, y_e)`
  (parâmetros `x_e=0,96, s_e=2,0, min_e=−0,04`): emprego alto (λ→1) acelera salário.
  É a "curva de Phillips de barganha salarial", não a Phillips expectacional de
  preços neokeynesiana.
- **Inflação de preços**: combinação **custo + demanda + importada**, com
  `infl0=0,035` (base, meta ~3%), `k_dem=0,15` (canal demanda/hiato) e
  `pass_through=0,15` (câmbio→preços). Não há expectativa de inflação racional/
  forward-looking nem âncora de meta mecânica.
- **Canal fiscal / FTPL: NÃO.** A inflação **não** é determinada pela restrição
  orçamentária intertemporal do governo (preços ajustando para igualar o valor
  real da dívida ao valor presente dos superávits). Dívida alta age sobre
  **câmbio** (prêmio de risco → depreciação → pass-through) e sobre o **juro da
  dívida**, não diretamente sobre o nível de preços via FTPL. É um modelo de
  **demanda/custo/distribuição**, não de teoria fiscal do nível de preços.

---

## 5. As "6 alavancas" e o teste de regime (phi)

**As 6 alavancas** (parâmetros de `simula`, todas default-OFF → o modelo reproduz
os cenários-base A/B/B±/C; cada uma credita um autor):

| # | Alavanca | Parâmetro(s) | Mecanismo | Crédito |
|---|---|---|---|---|
| 1 | `tax_rich` | 0,0035 / 0,008 / 0,013 | primário extra do topo (tributar ricos) | Lindbergh/Melchionna/PSOL |
| 2 | `invest_pub` | +`mult_pub=1,5` | investimento público entra em G E forma capital (multiplicador) | Laércio (portos+know-how)/IPEA |
| 3 | `tau_fric` | 0..1 | fricção de fluxo (IOF-derivativos/encaje) reduz mobilidade do carry (κ) e repasse ao câmbio (φ) | Kobori/Chamon-Garcia |
| 4 | `phi_endog` | `b_dom`,`risk_b`,`phi_carry`,`phi_sust` | prêmio de risco e câmbio endógenos à dívida → **teste de regime** | o coração do artigo |
| 5 | `conta_carrego` | `ret_reservas=0,04` | soma custo quase-fiscal do carry das reservas ao déficit (cortar Selic melhora o quase-fiscal) | Modelo 2/3 |
| 6 | `regra_divida` | `b_alvo=0,78`,`pb_star`,`phi_pb=0,30`,`banda=0,05` | troca o teto-clamp por regra de dívida com banda (âncora europeia 2024); social vira endógeno à saúde da dívida | Modelo 4 |

(Há ainda `regime_gasto` — teto/arcabouço/livre — que é o eixo da `bateria_teto.py`,
distinguindo as duas peças do "pacote do mal": EC 95 e LC 200.)

**O teste de regime (phi endógeno)** — `teste_regime.py`, o coração do artigo:
com `phi_endog=True`, o prêmio de risco liga acima de um limiar de dívida
`b_dom=0,90`. O sinal da resposta câmbio↔Selic **inverte** conforme o regime:

- **Regime NORMAL (dívida baixa, b<b_dom):** domina o canal carry/UIP
  (`phi_carry=0,40`). Selic alta APRECIA o Real (convencional). → logo, **cortar a
  Selic DEPRECIA**.
- **Dominância fiscal (dívida alta, b>b_dom):** domina o canal sustentabilidade
  (`phi_sust=0,90`): dívida alta → prêmio de risco (`risk_b=0,06` sobre o excesso)
  → Selic alta DEPRECIA o Real (o juro se autossabota). → logo, **cortar a Selic
  APRECIA**.

Essa inversão de sinal (a tese ALR "Eu Acuso", agora saindo do SFC) é o resultado
central. `teste_regime.py` plota câmbio×Selic por regime (Painel A) e o Δcâmbio de
um corte de 6 p.p. contra o nível de dívida, mostrando o limiar onde o sinal vira
(Painel B).

---

## 6. O que NOSSO modelo tem que o FTPL não tem — e vice-versa

**Nosso SFC (BrasilSFC) TEM, e o FTPL/DSGE do Dejanir tipicamente não:**
- **Dinâmica Minsky / endividamento privado endógeno** (`D_priv`): ciclos de
  fragilidade financeira do setor privado, ausentes de um FTPL de agente
  representativo.
- **Ciclo de Goodwin não-linear** (distribuição ω×emprego λ como motor endógeno de
  flutuação) — luta de classes salário/lucro, não ciclo de choques estocásticos.
- **Consistência de estoques e fluxos (SFC)**: toda emissão/pagamento tem
  contraparte de balanço; nada "vaza". O FTPL impõe apenas a restrição
  intertemporal do governo, não a matriz completa de balanços setoriais.
- **Composição da dívida em 3 pernas** (LFT/pré/IPCA) fazendo a Selic entrar
  mecanicamente no déficit (loop ALR) — o FTPL trabalha com dívida de valor real
  genérico.
- **Setor externo com câmbio, reservas, carrego quase-fiscal e Marshall-Lerner/
  Thirlwall** — economia aberta estrutural, não via UIP de equilíbrio.
- **Teste de regime com inversão de sinal** (normal↔dominância) por limiar de
  dívida — o regime não é imposto, emerge do nível de `b`.

**O FTPL/DSGE do Dejanir TEM, e o nosso não:**
- **Determinação do nível de preços pela restrição fiscal (FTPL propriamente):** a
  equação em que P ajusta para igualar dívida real = VP dos superávits. No nosso,
  inflação é custo/demanda/importada — não há esse canal.
- **Microfundamentação com otimização intertemporal e expectativas racionais/
  forward-looking** (famílias/firmas maximizando, Euler de consumo). O nosso é de
  regras comportamentais e agregados (não há agente otimizador; expectativas são
  adaptativas/"sentimento" no câmbio).
- **Prêmio de risco cambial microfundado** (UIP formal + paridade de juros com
  aversão a risco derivada de preferências). O nosso tem carry/prêmio **reduzido** e
  endógeno à dívida, não microfundado.
- **Regra de política monetária endógena** (Taylor) e o aparato
  neofisheriano/equilíbrios de ponto fixo. No nosso a Selic é botão exógeno.
- **Fundamentação de bem-estar / análise de equilíbrio e indeterminação** (ativo×
  passivo, seleção de equilíbrio). O nosso é um sistema dinâmico determinístico,
  sem seleção de equilíbrio.

**Em uma frase:** o Dejanir tem **preços endógenos à restrição fiscal e
microfundamentação otimizadora**; nós temos **balanços completos, endividamento
privado Minskyano e um câmbio que inverte de sinal com o regime fiscal** — dois
modos opostos de dizer "a conta fiscal mexe com a macro".
