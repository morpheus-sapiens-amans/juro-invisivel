# Resumo Técnico — *Neo-Fisherian Adventures in the Tropics: Monetary Policy and Fiscal Inflation in Brazil* (Dejanir H. Silva)

> Modelo DSGE Novo-Keynesiano de economia pequena e aberta, com teoria fiscal do nível de preços (FTPL), arbitragem de câmbio limitada e composição realista da dívida brasileira (LFT / LTN-NTN-F / NTN-B). Estimação bayesiana 2007Q1–2026Q2. A Seção 5 simula um "plano neo-Fisheriano": cortar a Selic de 13,75% para 7,5% e deixar o resto se ajustar.
>
> Tese central: a inflação no Brasil é, em parcela relevante, **fiscal** (choques "unbacked"), e **um corte de Selic pode ser desinflacionário no longo prazo** se houver compromisso crível — mas gera **surto de inflação no impacto** cuja magnitude depende de (i) duração/composição da dívida, (ii) intervenção cambial, (iii) credibilidade, (iv) se o governo gasta ou não a economia de juros.

---

## 1. Estrutura do modelo (Seções 3.1–3.3)

### Famílias
- Representativas (no baseline **não há hand-to-mouth**; eles só aparecem na Seção 6.2, ver abaixo). Consomem bem **tradable** `C_T` e **nontradable** `C_NT` num agregador **Cobb-Douglas** com peso `α` no tradable. Ofertam trabalho `L`, recebem endowment `Y_T` do bem tradable.
- Utilidade log no consumo, desutilidade convexa do trabalho.
- **Preferências de Uzawa** (Schmitt-Grohé–Uribe 2003): o fator de desconto de um período `β_t = β(C_t^agg)` é **fracamente decrescente no consumo agregado** (`β'(C) ≤ 0`). Isso é o que impede que a taxa real de longo prazo seja fixada só pelas preferências — condições financeiras afetam a taxa real via consumo. É o mecanismo-chave que permite taxa real doméstica alta e endógena.
- Famílias só negociam **dívida pública doméstica** (sem acesso a ativos externos).
- Restrição orçamentária nominal (eq. 1): `P_t C_t + T_t + W^H_t = W_t L_t + D_t + E_t P*_t Y_T,t + V^H_t`.
- Lei de um preço no tradable: `P_T,t = E_t P*_t` (E = preço da moeda estrangeira; depreciação eleva preço do tradable em moeda doméstica). Câmbio real `Q_t = E_t P*_t / P_t`.

### Firmas / Curva de Phillips
- Contínuo de firmas monopolisticamente competitivas produzindo nontradables, `Y_N(j) = Z_t L(j)`. Custo marginal nominal `MC = W/Z`.
- Rigidez à la Calvo (probabilidade `ξ` de manter o preço) **com fração backward-looking** à la Galí-Gertler (1999): dos que reajustam, `1−ϑ` otimizam e `ϑ` seguem regra retrospectiva → **Curva de Phillips híbrida**:
  - `π_N,t = γ_b π_N,t−1 + γ_f E_t π_N,t+1 + κ y_N,t`
  - Identidade do CPI: `π_t = π_N,t + [α/(1−α)] Δq_t` (o termo de câmbio real entra direto na inflação cheia via preços tradable).
- Firmas descontam lucros com fator próprio `β_F`. **`β_F = 1` ⇒ neutralidade de longo prazo** (mudança permanente de inflação deixa produto nontradable inalterado). Curva vertical no longo prazo se `γ_b + γ_f = 1`.

### Bloco externo / UIP / Arbitradores
- Dois tipos de investidores estrangeiros, ambos só detêm **bônus nominais curtos**:
  - **Arbitradores** (sem capital; financiam posição comprada tomando no exterior). Demanda responde ao prêmio de risco cambial com inclinação `1/Γ_t`, onde `Γ_t = γ_I Var_t(X*_{t+1})` (aversão a risco × variância condicional do payoff cambial). `X*_{t+1}` = payoff excedente ("currency risk premium"). Com arbitradores neutros ao risco, recai-se na **UIP usual**.
  - **Noise traders** ("hot money"): `H^N_t = H̄^N + ε^N_t`, choque exógeno de demanda.
- Condição de arbitragem linearizada (eq. 2): `uip_t = Γ_X (f_t − a_t − h^N_t)`, com `Γ_X = β̄ R̄* Γ C̄_T`. **Mais reservas `f` ⇒ mais posição que os arbitradores têm de absorver ⇒ wedge UIP maior.** Vender reservas estreita o wedge.
- Euler tradable + câmbio (eq. 3): `E_t Δc_T,t+1 = r*_t + uip_t − ζ c_t`; `Δe_t = π_t + Δq_t`.
- Riqueza externa / recurso externo (eq. 4): `a_t = R̄* f_{t−1} − R̄(f_{t−1}−a_{t−1}) + R̄* ℓ_F r*_{t−1} − R̄ ℓ_H (i_{t−1} − Δe_t) − c_T,t`, onde `ℓ_F = F̄/C̄_T` (reservas) e `ℓ_H = H̄/C̄_T` (bônus domésticos em mãos externas) medem a **força dos efeitos de revalorização**. Reservas são caras: rendem `R̄*` mas os bônus domésticos em mãos de estrangeiros rendem `R̄` (maior).

### Determinação da taxa real de longo prazo (Seção 3.2, Fig. 4, Prop. 1)
- Equilíbrio no mercado de bônus curtos: interseção do **schedule das famílias** (oferta residual de bônus) com a **demanda dos arbitradores**. Determina conjuntamente a taxa real doméstica e as posições externas.
- **Prop. 1**: a taxa real doméstica sobe com (i) a inclinação `Γ` (arbitragem mais limitada), (ii) a taxa real externa `R̄*`, (iii) o endowment tradable `Ȳ_T`; cai com as posições de noise traders `H̄^N`; sobe quando as famílias ficam menos pacientes. → Explica por que Brasil tem juro real alto *e* baixa participação estrangeira (demanda de arbitradores íngreme).

### Governo / Dívida / Banco Central
- Governo emite **três tipos de bônus**, mapeando a dívida federal doméstica brasileira:
  1. **Nominal curto** `B_S` (1 período) → **LFTs / Selic / pós-fixado** (reset frequente do custo).
  2. **Nominal longo** `B_N`, preço `Q_N`, cupons decaindo a `θ_N` → **LTN / NTN-F (prefixado)**.
  3. **Indexado longo** `B_R`, cupons em unidades de consumo decaindo a `θ_R` → **NTN-B (indexado ao IPCA)**.
  `θ_N, θ_R` governam a duração.
- Banco Central detém **reservas em moeda estrangeira** (`F*`), cujo poder de compra doméstico sobe com depreciação real.
- Regra de Taylor: `I_t = Ī Π_t^{φ_π} exp(u^M_t)`. `φ_π > 1` = regime "monetary-led" (ativo); `φ_π ≤ 1` = "fiscally-led" (passivo).
- Orçamento consolidado nominal: `V_t = P_t S_t + W_t` (`S` = superávit primário real; `V` = passivo líquido herdado; `W` = valor de mercado da dívida líquida carregada).
- Restrição de fluxo linearizada (eq. 5): `β̄ v_{t+1} = v_t − s_t + r_{G,t+1}`, com `r_{G,t+1}` = custo efetivo de financiamento da dívida líquida.

---

## 2. Teoria Fiscal do Nível de Preços aplicada (Seção 3.4)

### Choques fiscais "backed" vs "unbacked"
- O superávit primário segue um processo MA: `S_t = S̄ − W Σ_j (ψ^B_j ε^B_{t−j} + ψ^U_j ε^U_{t−j})`.
- **Backed** (`ε^B`): o valor presente dos superávits futuros compensa *exatamente* o déficit inicial → `Σ Ī^{−j} ψ^B_j = 0`. **Não afeta inflação.**
- **Unbacked** (`ε^U`): o valor presente dos superávits *cai* → `Σ Ī^{−j} ψ^U_j > 0`. **É o único que move a inflação.**
- Permite resposta em "S" (déficit inicial seguido de superávits, à la Cochrane 2023), mas no agregado descoberto.

### Benchmark da inflação-tendência (trend inflation)
- Com `φ_π = 1` e Phillips forward-looking neutra (`γ_b=0, γ_f=1`), e isolando o canal fiscal (`ℓ_H=0`), a solução admite `c_t = c_T,t = 0` — consumo e taxa real ficam no steady state, câmbio real fixo — e **a inflação muda permanentemente**. É uma FTPL de *tendência*.
- O choque descoberto bate na **revalorização da dívida nominal herdada**: a notícia sobre superávits (`−Ψ_U(β̄) ε^U_t`) tem de ser igualada à desvalorização da dívida nominal via inflação corrente e preços dos bônus longos.

### Proposição 2 (resultado central da FTPL) — a inflação é um random walk dirigido pela notícia fiscal descoberta:

```
π_t − π_{t−1} = [ β̄ Ψ_U(β̄) / ( (1+ρ_G)(ω̄_S + ω̄_N/(1−β̄ θ_N)) ) ] · ε^U_t
```

Interpretação dos determinantes da volatilidade da inflação:
- **Sobe** com menor backing fiscal; **sobe** quando dívida indexada substitui nominal.
- **Cai** quando dívida nominal curta é trocada por nominal longa; **cai** com maior duração da dívida nominal; **cai** quando reservas sobem via emissão doméstica (amplia o portfólio nominal que absorve a revalorização).
- Corolário prático: **mais LFT (pós) ⇒ resposta inflacionária maior**; dívida longa prefixada funciona como "amortecedor".

### Proposição 3 (tendência + ciclo, Phillips híbrida)
- `π_t = π_t^trend + π_t^cyc`, com `π_t^cyc = −c_t + ζ Σ_j E_t c_{t+j}` e `Δπ_t^trend = K_H ε^U_t`.
- Com paciência constante (`ζ=0`), `π_t^cyc = −c_t`.
- A Fig. 5 mostra: portfólio **set/2026** (mais LFT, menos reservas/dívida) responde mais forte que **set/2014** (mais nominal longo, mais reservas).

---

## 3. Estimação (Seção 4)

### Dados
- Amostra **2007Q1–2026Q2**. Observáveis: IPCA cheio, serviços e administrados; Selic; câmbio; crescimento do consumo; PIB destendido (proxy ruidosa do hiato); dívida líquida; superávit primário; taxa curta dos EUA; holdings de não-residentes; previsões Focus de câmbio e de superávit.
- Pesos IPCA: tradable 30,87% / nontradable 44,04% / administrados 25,09% (BCB 2019, Tab. 6).

### Método
- **Bayesiano** com verossimilhança gaussiana do modelo linearizado; retém só soluções determinadas; infere a história dos choques estruturais por draw. Incerteza reportada reflete parâmetros *e* histórias de choques.
- **Dois blocos de regime**: unbacked enfrenta política monetária passiva e sem ajuste fiscal à dívida; backed enfrenta política ativa + regra fiscal que estabiliza a dívida. Backing parcial do cost-push: **20% ao bloco fiscal-led, 80% ao monetary-led** (Smets-Wouters 2024). Regra fiscal à la Bohn (1998): primário responde à dívida líquida herdada e ao produto.
- Priors/restrições: resposta de inflação **> 1** no bloco monetary-led, **uniforme (0,1)** no fiscally-led. Persistência trimestral limitada a 0,99 para cost-push, unbacked e prêmio cambial.

### Posteriores selecionados (Tab. 3)
| Parâmetro | Mediana | IC 95% |
|---|---|---|
| Resposta de inflação, bloco monetary-led | 1,012 | [1,010; 1,018] |
| Resposta de inflação, bloco fiscally-led | 0,943 | [0,920; 0,961] |
| Suavização da taxa de juros | 0,640 | [0,567; 0,697] |
| Inclinação da Phillips (`κ`) | 0,017 | [0,010; 0,023] |
| Peso da inflação defasada (`γ_b`) | 0,059 | [0,004; 0,223] |
| Resposta do superávit à dívida | 0,0154 | [0,0144; 0,0194] |
| Persistência do choque fiscal unbacked | 0,971 | [0,916; 0,989] |
| SD inovação fiscal backed (% da dívida líq.) | 0,840 | [0,525; 1,120] |
| SD inovação fiscal unbacked (% da dívida líq.) | 0,023 | [0,012; 0,059] |
| Persistência cost-push | 0,9897 | [0,9883; 0,9900] |
| Persistência do prêmio cambial | 0,976 | [0,953; 0,988] |

> Nota: Phillips é **bem achatada** (`κ≈0,017`) e quase totalmente forward-looking (`γ_b≈0,06`). Isso é o que limita o surto de inflação nos experimentos.

### Decomposição histórica (resultado-chave)
- Choques fiscais **unbacked** respondem por **≈38% da variação da inflação cheia no horizonte de 5 anos**.
- Trajetória por horizonte: **≈4% em 1 trimestre → ≈7% em 1 ano → ≈38% em 5 anos**.
- Omitindo as janelas que terminam na pandemia (2020–2021): a parcela de 5 anos sobe para **≈49%** (e para ~40% sob a especificação de full-backing, ~32% sob full-backing com todas as janelas).
- Padrão: a parcela fiscal **cresce com o horizonte** (coerente com o mecanismo de tendência da Seção 3.4). Em 5 anos, unbacked é a **segunda maior** contribuição (atrás do natural-rate).

### Identificação (Seção 4.3, Fig. 6)
- Choque backed: dívida sobe para financiar o buraco e volta ao normal; inflação de serviços **não muda**.
- Choque unbacked: inflação sobe, erode o valor real dos passivos nominais, yields nominais maiores baixam preços dos bônus longos → **dívida líquida real CAI apesar do déficit**. Câmbio real **deprecia** no impacto (cost-push aprecia). As previsões Focus ajudam a separar backed de unbacked.

---

## 4. Experimentos (Seção 5) — O NÚCLEO

**Setup comum:** começa no steady state com Selic nominal **13,75%** (taxa real steady-state). BC anuncia baixar a Selic para **7,5% em 4 passos trimestrais** e manter. Famílias/firmas creem; governo mantém primário no caminho "sem plano". Compara-se com economia que mantém 13,75%. Pela relação de Fisher, Selic permanente de 7,5% ⇒ **inflação de longo prazo ≈ 0,24%**.

### 4a. Plano neo-Fisheriano base (Fig. 8)
- **Inflação cheia anualizada sobe de 6,1% → 9,4% no impacto** (4 cortes).
- Selic real começa perto de **7,25%** (nível pré-plano) e **cai para 5,1%** até o último corte; depois volta ao pré-plano à medida que a inflação esperada cai.
- **Surto no impacto existe** apesar da grande fatia de LFT, porque a revalorização dos nominais longos é forte o bastante (lógica de Cochrane 2001: subir/baixar nominal pode mexer na inflação via duração do portfólio).
- Espalhar os cortes em **8 ou 12 trimestres suaviza** o surto inicial e a queda do juro real.
- **Dívida pública real sobe 3,4%** do valor steady-state no impacto (ganho nos preços dos bônus domina a erosão inflacionária), depois volta ao pré-plano.
- Câmbio real **deprecia** no impacto em todos os casos; o wedge UIP se **estreita** porque a depreciação nominal reduz o valor em moeda estrangeira dos bônus curtos em mãos externas → arbitradores têm menos a absorver.

**Decomposição da inflação de impacto (Tab. 4, em pontos % log anualizados, caso 4 cortes):**
- Painel A (no anúncio): depreciação real **+4,19**; hiato de consumo corrente **+0,46**; inflação nontradable esperada próx. trimestre **−1,58** → impacto **+3,07**.
- Painel B (Phillips resolvida pra frente): depreciação real **+4,19**; caminho esperado do hiato **+4,17**; inflação de longo prazo **−5,30** → impacto **+3,07**.
- **A depreciação real é o canal dominante**; o hiato contribui pouco (Phillips achatada). Decomposição UIP: queda das taxas reais esperadas contribui **3,78 log pp** de depreciação; estreitamento do wedge compensa **0,64 log pp (≈17%)** → depreciação real líquida **3,14 log pp**.

### 4b. Intervenção cambial (Fig. 9, Seção 5.2)
- Venda esterilizada **temporária** de reservas = **1% do PIB** no anúncio, recompra 4 trimestres depois (≈ **US$ 26 bi** a valores set/2026; comparável aos US$ 21,6 bi de intervenções spot do BC em dez/2024).
- Reduz a exposição cambial que os arbitradores absorvem → estreita o wedge UIP → limita a depreciação real.
- **Inflação: começa em 6,1%, vai a 9,4% SEM intervenção, e só a 6,4% COM intervenção** — quase elimina o surto. O juro real cai um pouco *mais* no impacto.
- Parte do alívio se desfaz na recompra (câmbio deprecia além do caminho sem intervenção).
- FX swaps tradicionais podem replicar a venda mantendo reservas brutas (Apêndice B.4).

### 4c. Composição da dívida (Fig. 10, Seção 5.3)
- Mesmo corte de Selic **sobe ou baixa o juro real no impacto conforme a composição**:
  - Portfólio **set/2014** (duração maior, mais nominal longo): surto maior, **inflação de impacto 11,1%**, juro real **cai** no impacto.
  - Portfólio **set/2026** (LFT-pesado, menos reservas/dívida): surto menor, **inflação de impacto 6,7%**, juro real **sobe** no impacto.
- Yields menores elevam mais o valor de mercado em portfólio de maior duração → exige maior alta do nível de preços para compensar em termos reais → maior depreciação real adiciona à inflação cheia via tradable.
- → **O perfil pós-fixado atual (LFT) favorece o plano**: limita o surto inicial.

### 4d. Credibilidade imperfeita + gastar a economia de juros (Fig. 11, Seção 5.4)
- **Risco de reversão**: a partir do tri 4, agentes atribuem **50% de probabilidade por trimestre** de alta permanente da Selic para **17,5%** (condicional a ainda estar baixa). Com juro real steady-state 7,25%, reversão a 17,5% implica **inflação de longo prazo de 9,56%** (vs 0,24% sob credibilidade plena).
  - Efeito: risco de reversão **suaviza o surto inicial** (corte parece menor ao longo do caminho esperado) — **inflação de impacto cai de 9,4% → 5,1%** — mas desanora expectativas de longo prazo.
- **Gastar a economia de juros** (crível): governo reduz o primário pela economia de financiamento, `s_t = χ_G r_t`, `χ_G = 1 + (1 − R̄*/R̄) ρ_G`. Isso anula a melhora de backing.
  - **Inflação de impacto sobe de 9,4% (retém) → 23,5% (gasta).**
- **Gastar SOB risco de reversão**: o risco de hike tempera o easing esperado → **inflação de impacto 6,9%** (vs 23,5% quando o caminho baixo é plenamente crível). Mas o surto vem **depois**: por volta do **tri 8, inflação chega a 11,8% com gasto vs 4,4% com retenção**, sob o mesmo risco de reversão.
  - Mensagem: um impacto modesto pode dar lugar a um surto maior *lá na frente*.

### 4e. Baixar o juro real de LONGO prazo — as 2 vias (Seção 6, Fig. 12)
A neutralidade de longo prazo devolve o juro real ao pré-plano; para baixá-lo de forma duradoura é preciso mudar o que o determina:
- **Via 1 — reduzir o risco cambial (Fig. 12a):** a inclinação `Γ_t = γ_I Var_t(X*_{t+1})`. Mudanças no *componente sistemático* de política (backing fiscal mais forte, estabilização mais eficaz) que tornem a depreciação mais previsível **achatam o schedule dos arbitradores**. Ilustração: **halving** da variância condicional do payoff cambial reduz a taxa real anual de **7,25% → 5,25%**.
- **Via 2 — consolidação fiscal com famílias não-Ricardianas (Fig. 12b):** no modelo representativo, aposentar dívida *não* muda o juro real (corte de imposto compensa a renda de juros perdida). Com modelo de **dois agentes** (savers + **hand-to-mouth** que recebem fração `λ` do alívio tributário recorrente), a dívida doméstica é "net wealth" para os savers.
  - **Proposição 4**: retirar dívida `ΔD` desloca o schedule das famílias por `λ ΔD`; com `λ > 0`, aposentar dívida **baixa a taxa real de longo prazo**.
  - Ilustração: com **1/3 das famílias hand-to-mouth** e alívio igual por família, retirar dívida de **1% do PIB** baixa o juro real anual de **7,25% → 6,23%**.

---

## 5. Calibração (Tabela 2 / Online Appendix E)

| Input | Valor | Base |
|---|---|---|
| Taxa real doméstica, anual | **7,25%** | Implícita no alvo de UIP |
| Taxa real externa, anual | **1,0%** | Calibração externa |
| Wedge UIP steady-state | **6%** | Gap anual de retorno log (Tab. 1) |
| Crescimento real de tendência, anual | **2,1%** | Balanced-growth |
| **Fator de desconto fiscal, trimestral** | **0,988** | Crescimento trim. / retorno real doméstico |
| Share de gasto tradable (`α`) | **30,87%** | Share tradable do IPCA |
| **Inclinação de Uzawa (ζ)** | **0,02** | Grid de verossimilhança (Apêndice D.6) |
| Dívida pública líquida / PIB anual | **44,0%** | Média 2007Q1–2023Q2 |
| Share dívida nominal curta (LFT) | **33,4%** | LFTs no portfólio modelado |
| Share dívida nominal longa (prefixada) | **38,0%** | LTN/NTN-F |
| Share dívida indexada (NTN-B) | **28,6%** | IPCA-linked |
| Duração dívida nominal | **7,8** trimestres | Fluxos nominais |
| Duração dívida indexada | **29,6** trimestres | Fluxos indexados |
| Reservas brutas / dívida líquida | **40,4%** | Média 2007Q1–2023Q2 |
| Holdings de não-residentes | **1,07** | Média (unidades de consumo tradable trim.) |
| Holdings steady-state de noise traders | **0,91** | Total menos posição de arbitradores |
| **Inclinação UIP normalizada (`Γ_X`)** | **0,091** | Alvo FX swap de 2% de depreciação no impacto |
| Debt feedback fiscal-led | 0 | Por designação de regime |
| Persistência choque backed | 0,50 | Cochrane (2020) |
| Persistência do balanço de repagamento | 0,81 | ~8 trimestres (descontado) |
| Persistência do consumo natural | 0,70 | Grid de persistência |
| Resposta do superávit ao produto | 0,36 | Comum a ambos os blocos |
| Peso CPI administrados | 25,09% | Share administrados IPCA |
| Persistência gap administrados | 0,27 | AR(1) |
| SD inovação gap administrados | 1,87 | Resíduo AR(1) |
| Persistência taxa curta EUA | 0,94 | AR(1) |
| SD inovação taxa curta EUA | 0,12 | Resíduo |
| Persistência foreign-demand | 0,70 | Fixada no fit do bloco externo |

> Notas: shares do portfólio usam estoques do Tesouro 2007Q1–2023Q2, normalizados sobre as classes modeladas; amostra de duração 2017Q3–2023Q2. Persistências e inovações são **trimestrais**.

---

## 6. Limitações e ressalvas admitidas pelo autor

- **Neutralidade de longo prazo é imposta** (`β_F=1`, `γ_b+γ_f=1`): o plano neo-Fisheriano *por construção* devolve o juro real ao pré-plano — a desinflação duradoura depende dessa hipótese e, para o juro real cair de vez, precisa de uma das vias da Seção 6.
- **Backing parcial do cost-push é uma escolha de calibração** (20/80, motivada por Smets-Wouters 2024); há formulação alternativa (Bianchi et al. 2023) com cost-push 100% monetary-led, reestimada.
- A parcela fiscal de 38% é **sensível à janela**: sobe a ~49% sem pandemia; varia entre ~32% e ~40% conforme a especificação de backing.
- **PIB destendido é proxy ruidosa do hiato**; serviços é proxy ruidosa do nontradable.
- Hand-to-mouth **não está no baseline estimado** — entra só como ilustração de dois agentes na Seção 6.2 (resultado qualitativo via Proposição 4, com `λ` e share de 1/3 calibrados ad hoc).
- Os experimentos da Seção 5 assumem **anúncio perfeitamente crível** no baseline; a credibilidade imperfeita é tratada como cenário (50% de reversão), não estimada.
- CIP vale no setting (posições totalmente hedgeadas não têm risco cambial); forwards no Apêndice D.6.
- O resultado de que mais reservas *dampen* a inflação depende de elas serem financiadas por emissão doméstica; dívida em moeda estrangeira *amplificaria* a resposta.

---

### Referências-âncora do arcabouço
Cochrane (2001, 2023) — FTPL e duração da dívida; Bianchi-Faccini-Melosi (2023) e Smets-Wouters (2024) — backed/unbacked; Itskhoki-Mukhin (2021) e Froot-Ramadorai (2005) — arbitragem cambial/UIP; Schmitt-Grohé–Uribe (2003) — Uzawa; Galí-Gertler (1999) — Phillips híbrida; Bohn (1998) — regra fiscal; Blanchard (1985) — caso de economia pequena aberta.
