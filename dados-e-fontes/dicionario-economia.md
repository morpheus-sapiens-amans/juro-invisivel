# Dicionário de bolso — ajuste fiscal, Selic e dívida

> Referência rápida pros termos que aparecem no projeto. Feito pra ler no meio de outra
> sessão, quando cai uma palavra e o entendimento trava. Cada verbo está em **português
> de gente**, com uma nota *[no projeto]* quando o sentido aqui é específico.
>
> Se você só tem 30 segundos, leia a **equação da dívida** aqui embaixo. Quase tudo neste
> dicionário é uma peça dela.

---

## A equação que organiza tudo

```
variação da dívida/PIB  =  (r − g)·dívida  −  superávit primário
                            juro  cresc.        (receita − gasto, fora juros)
```

A dívida/PIB sobe ou desce por **três botões**, e só três:
- **`r` (juro)** — quanto a dívida custa. O maior termo no Brasil.
- **`g` (crescimento)** — o denominador. Crescer dilui a dívida.
- **primário** — arrecadar mais do que se gasta (fora juros).

O projeto deu **apelidos** pros botões (é o que aparece em frases como *"âncora de dívida +
cobrança do topo + fricção cambial"*):

| Botão técnico | Apelido no projeto | O que é |
|---|---|---|
| mexer no `r` | **fricção cambial / reservas** | baixar o juro sem o câmbio disparar — segurado por reservas/ouro |
| mexer no `r` | **âncora de dívida** | trocar o teto de gasto por uma regra que mira a dívida/PIB |
| melhorar o primário | **cobrança do topo** | arrecadar do andar de cima (dividendos, lucro, fortunas), não cortar gasto |
| levantar o `g` | **crescimento / denominador** | investimento + indústria puxam o PIB e diluem a dívida |

---

## Os números da dívida (déficit, primário, nominal)

- **Déficit primário** — a conta do governo **sem contar os juros**: receita menos gasto
  "de verdade" (saúde, educação, servidores, investimento). *[no projeto]* O argumento
  central do Lara Resende: o primário do Brasil é **pequeno** (~0,43% do PIB em 2025), dos
  menores do mundo. Ou seja, o gasto não-juros está quase no lugar.
- **Superávit primário** — o contrário: sobra antes dos juros. Entra na equação com sinal de
  menos (superávit *reduz* a dívida).
- **Déficit nominal** — a conta **com os juros** incluídos. No Brasil é gigante (~8–10% do
  PIB). *[no projeto]* A diferença entre o nominal e o primário é **quase toda conta de
  juros** — é essa diferença que vira a tese "o vilão é o juro, não o gasto".
- **Dívida/PIB** — o estoque da dívida dividido pelo tamanho da economia. É a régua que todo
  mundo olha (em vez do valor absoluto), porque uma economia maior aguenta mais dívida.
- **Bola de neve** — quando `r` é maior que `g` por muito tempo: o juro faz a dívida crescer
  mais rápido que a economia, e ela "rola" sozinha ladeira abaixo, mesmo sem gasto novo.

---

## Juros e o Banco Central

- **Selic** — a taxa básica de juros, definida pelo Banco Central. É o `r` da equação na
  prática. *[no projeto]* É a ré do argumento: alta demais, ela mesma infla a dívida que
  diz combater.
- **Prêmio de risco** — o juro **extra** que o mercado cobra além da Selic, por medo de não
  receber (risco fiscal, político, de credibilidade). Juro de mercado = Selic + prêmio de
  risco + prêmio de prazo.
- **Prêmio de prazo** — pedaço do prêmio que cobra pela **incerteza do tempo**: emprestar por
  10 anos é mais arriscado que por 1, então exige-se juro maior.
- **Credibilidade** — a crença do mercado de que a dívida será honrada e a regra, cumprida. Não
  é verbete solto: vive dentro do **prêmio de risco** (menos credibilidade → prêmio maior → juro
  maior) e da **âncora** (a regra crível *compra* credibilidade). *[no projeto]* é o elo que o
  Jones **não engaja** — ele trata o ajuste como pura escolha de classe e ignora o canal "sem
  âncora → prêmio sobe → Selic sobe", que é exatamente o que o modelo SFC testa.
- **Regra de Taylor** — a "fórmula" clássica de como um BC deveria mexer o juro: sobe o juro
  quando a inflação passa da meta, desce quando a economia esfria. *[no projeto]* aparece
  como o "piloto automático" do BC que o modelo pode ligar ou desligar.
- **Dominância fiscal** — o regime em que a política fiscal manda na monetária: a dívida está
  tão frágil que **subir o juro piora tudo** (encarece a dívida e assusta mais do que
  ancora). Nesse regime, cortar o juro pode até **fortalecer** o câmbio — o oposto do normal.
  *[no projeto]* É a pergunta que decide o debate; a decisão foi **não cravar** que o Brasil
  está em dominância (seria atacável), só listar os sintomas e propor um teste.
- **Teste de regime (phi endógeno)** — o experimento do modelo: a **mesma** Selic produz
  efeito **oposto** no câmbio dependendo da saúde fiscal. "phi endógeno" = a sensibilidade do
  câmbio deixa de ser fixa e passa a **reagir** ao estado da dívida. É o coração do modelo.
- **Corte gradual (gradualismo)** — baixar a Selic aos poucos, não de choque. *[no projeto]* é
  tratado como o **teste falseável** da tese: corta 2 pontos; se o Real **aprecia**, confirma
  dominância fiscal.

---

## A dívida por dentro (indexação, carrego, reservas)

- **LFT** — título público **pós-fixado**, cujo rendimento acompanha a Selic. *[no projeto]*
  ~metade (≈47%–74% dependendo do recorte) da dívida é indexada assim: por isso subir a Selic
  bate **na hora** no déficit.
- **Indexação / desindexação** — "indexar" é atrelar um valor a um índice (Selic, inflação).
  **Desindexar** a dívida = trocar LFT por título **prefixado**, cortando o fio direto
  Selic→déficit. *[no projeto]* é a reforma "técnica, chata e talvez a mais potente".
- **`theta` / `theta_pre`** — os parâmetros do modelo que medem a fatia indexada vs. prefixada
  da dívida. Mexer neles = simular a desindexação.
- **Prefixado** — título com juro **travado** na emissão. Não reage à Selic depois — por isso
  blinda o déficit de altas de juro.
- **Compromissadas** — operações de curtíssimo prazo em que o BC toma dinheiro emprestado dos
  bancos pagando Selic (pra "enxugar" liquidez). *[no projeto]* entram como **sintoma** de
  fragilidade: é dívida que rende Selic todo dia.
- **Carrego (custo de carregamento / quase-fiscal)** — o custo de o país **carregar** reservas:
  você guarda dólar que rende pouco e paga Selic (alta) pra financiar isso — a diferença é
  prejuízo. *[no projeto]* achado contraintuitivo: **cortar a Selic melhora o carrego** (baixa
  o custo de carregar as reservas).
- **Reservas internacionais** — o "colchão" de dólares/ativos do país pra defender o Real.
  *[no projeto]* no modelo, reserva formada = Real defendido na janela do corte de juro —
  mas drena com o tempo, não é blindagem eterna.
- **Ouro** — reserva que **não depende do dólar nem do Tesouro dos EUA**. *[no projeto]* é a
  sua tese fina: diversificar a reserva pra ter autonomia cambial.
- **Carry / carry trade** — estrangeiro traz dólar pra ganhar a Selic alta (câmbio
  "defendido" pelo juro). *[no projeto]* o problema: esse Real forte é **pago com dívida** —
  tira-se o carry (baixa o juro) e o câmbio pressiona.
- **Fricção cambial** — o atrito/pressão no câmbio quando capital quer sair. É o custo de
  baixar o juro "a fórceps" sem reservas.

---

## O ajuste e quem paga

- **Austeridade** — a política de equilibrar as contas **cortando gasto**. Mexe só no 3º botão.
- **Austeridade autoderrotante (autodestrutiva)** — quando cortar gasto derruba o crescimento
  (`g`) mais do que melhora o primário, e a dívida/PIB **sobe** apesar do corte. *[no projeto]*
  o modelo mostra que **não vale pra ajuste pequeno** (0,45%) com desemprego baixo; a autoderrota
  exige multiplicador >1,5 e recessão profunda. Então a crítica foi **reformulada** como
  "composição do ajuste / quem paga".
- **Composição do ajuste** — **como** se ajusta importa, não só quanto. Cortar investimento
  custa muito mais produto do que ajustar pela receita. *[no projeto]* resultado pós-keynesiano
  mais robusto: cortar investimento custa **4 a 6×** mais produto que ajustar por receita.
- **Multiplicador (fiscal)** — quanto de PIB se perde (ou ganha) por real cortado (ou gasto).
  Multiplicador 1,5 = cada R$1 cortado tira R$1,50 de produto. Quanto maior, mais a austeridade
  se autossabota.
- **Crowding-in / crowding-out** — *out*: o Estado "expulsa" o investimento privado (disputa
  poupança, sobe juro) — tese austríaca. *in*: o investimento público **puxa** o privado junto
  (obra atrai fornecedor) — tese do lado keynesiano. *[no projeto]* o crowding-in é um dos
  canais pra levantar o `g`.
- **Reforma tributária progressiva** — arrecadar mais de quem ganha mais. *[no projeto]* a
  "cobrança do topo": hoje o Brasil taxa pesado o **consumo** (pobre paga mais) e **isenta
  dividendos**; taxar lucro/dividendo/fortuna melhora o primário **sem cortar gasto**.
- **Parcela salarial (ω, ômega)** — a fatia do PIB que vai pros salários (o resto é lucro).
  *[no projeto]* o teto "cresce" **reprimindo** essa parcela (ω baixo, 0,77) — crescimento por
  repressão salarial. É o "caráter de classe" do ajuste.
- **Bolsa-rentista** — apelido crítico: o gasto com juros é uma "transferência" pra quem detém
  a dívida (rentistas). Contraste direto com os programas sociais que se quer cortar.
- **Gasto primário × gasto financeiro** — os dois ramos do gasto público. **Primário**: saúde,
  educação, C&T, meio ambiente, infraestrutura, previdência, funcionalismo — o que vai pro povo.
  **Financeiro**: juros e serviço da dívida. *[no projeto]* o nervo do argumento do Jones: o
  arcabouço (LC 200) **deixa livre o financeiro** e **põe teto no primário** — cresce reprimindo
  o social, não o rentista. É o "caráter de classe" do teto (liga a **bolsa-rentista** e a ω).
- **Gastos tributários (renúncia fiscal)** — o que o Estado **deixa de arrecadar** por isentar
  ou incentivar: crédito presumido, alíquota zero, isenção, incentivo tributário, equalização de
  financiamento à exportação. *[no projeto]* é o "aceno ao andar de cima" do pacote (mexer aqui =
  cobrança do topo) — mas o Jones prevê que **essa metade é desidratada no Congresso** enquanto o
  corte no primário passa.

---

## As regras fiscais (o enredo institucional)

- **Teto de gastos (EC 95/2016, Temer)** — emenda que **congelou o gasto primário real** por
  20 anos (só corrige pela inflação). Instituiu a lógica "ajuste = cortar gasto".
- **Arcabouço fiscal (LC 200/2023, Haddad)** — substituiu o teto por regra menos rígida: o
  gasto pode crescer 0,6%–2,5% real, atrelado à receita. Menos apertado, mas mantém a lógica
  do gasto como variável de ajuste.
- **PLP 299/2026** — o projeto em tramitação **agora** que **aperta** o arcabouço (crescimento
  real da despesa cai de 2,5%→2%) e muda a **base de cálculo** dos pisos de saúde/educação. É
  o "teto voltando pela janela" — e o caso vivo do roteiro.
- **Base de cálculo (dos pisos)** — a conta **sobre a qual** incidem os percentuais mínimos
  (saúde 15% da RCL, educação 18%). *[no projeto]* a "manobra fina": não mudam o percentual
  (seria corte explícito), mudam a base — tiram receita de petróleo da conta, e o piso encolhe
  "sem corte nominal".
- **Âncora (fiscal)** — qualquer regra crível que diga ao mercado "a dívida não vai explodir".
  *[no projeto]* a chave do argumento: **"revogar o teto" sem âncora assusta o mercado** (no
  modelo, a dívida chega a 3,7×); a saída é **revogar E ancorar** numa regra de **dívida/PIB**
  (controla melhor que o teto *e* preserva o social).
- **Regra de dívida** — âncora que mira diretamente a **dívida/PIB** (em vez de limitar o
  gasto). Permite mexer nos três botões — inclusive juro e crescimento — não só cortar.
- **Regra de ouro** — norma que proíbe o governo de se endividar pra pagar despesa corrente
  (só pra investimento). (Não confundir com o ouro-reserva acima.)
- **Receita Corrente Líquida (RCL)** — a base de arrecadação "de verdade" da União (impostos,
  contribuições, royalties), líquida de transferências. É **sobre ela** que incidem os pisos.
  *[no projeto]* quem controla a *definição* da RCL controla o tamanho do piso **sem tocar no
  percentual** — o coração da manobra do PLP 299.
- **Piso constitucional (saúde/educação)** — o mínimo que a União é **obrigada** a gastar: 15%
  da RCL em saúde, 18% em educação. *[no projeto]* alvo da manobra fina — não mudam o %, encolhem
  a base.
- **Receitas extraordinárias / royalties do petróleo** — arrecadação **volátil** (preço do
  barril, leilões) que entra na RCL. *[no projeto]* o PLP 299 as **tira da base de cálculo** do
  piso da saúde → −10 bi no SUS em 2027. Tensão honesta: o governo diz "não se indexa gasto
  permanente a receita cíclica" (o Jones admite a lógica); a crítica é muda-se a Constituição por
  PLP, sem PEC, e abre precedente.
- **Contingenciamento** — **congelar/bloquear** temporariamente despesa primária já autorizada
  quando a arrecadação frustra a meta. *[no projeto]* o PLP amplia o poder de contingenciar
  (preservadas obrigações constitucionais) **sem dizer quais** programas caem.
- **Lei Kandir (LC 87/1996)** — isenta de ICMS a exportação de primários e semielaborados (soja,
  minério, carne). *[no projeto]* esvaziou a arrecadação dos estados e incentiva a economia
  primário-exportadora; criou uma **compensação** da União aos estados — que o PLP 299 corta
  (4→1 bi/ano). Posição do Jones: **revogar** a Kandir, mas cortar a compensação aperta a
  austeridade estadual.
- **Lei 15.077/2024** — proíbe aumento **real** do salário mínimo acima de 2,5% da inflação.
  *[no projeto]* o PLP 299 aperta pra 2% → teto de ~8% de ganho real em 4 anos. Exemplo de lei
  antipopular aprovada "sem Lula nunca ter defendido em público".

---

## As seis escolas (os personagens do debate)

Cada uma responde diferente à pergunta "o ajuste derruba o juro?". *[no projeto]* o modelo
roda com os parâmetros de cada uma e mostra que a divergência inteira mora em 2–3 números
não medidos no Brasil.

- **Ortodoxia** — a dívida encarece o juro; ajuste crível barateia. Vê a restrição no tempo e
  o papel das **expectativas**. Ponto cego: **distribuição** (não diz quem paga).
- **Austríacos / escolha pública** — como a ortodoxia, e mais forte (o Estado disputa
  poupança). Enxergam que **a regra importa mais que o pacote**.
- **Pós-keynesianos** — o ajuste quase não mexe no juro; o que importa é a **composição**
  (cortar investimento é caríssimo).
- **MMT (Teoria Monetária Moderna)** — o juro é decisão política do BC, não imposição do
  mercado; o Estado emissor da própria moeda não "quebra" como empresa. Ponto cego:
  **restrição externa** (país periférico, câmbio).
- **Marxista** — foco em **quem recebe os juros e quem perde no corte** (classe). Ponto cego:
  o que fazer com a trajetória da dívida.
- **Economia política (da conciliação)** — meio ajuste rende quase nada; entregar 50% do
  anunciado deixa a dívida quase como se nada tivesse sido feito.

- **Expectativas** — o que agentes *acham* que vai acontecer. Pra ortodoxia, movem o juro hoje
  (um ajuste "crível" derruba o prêmio mesmo antes de aparecer nos números). Pros heterodoxos,
  pesam menos que a renda e a liquidez reais.
- **Restrição externa** — o limite que o **setor externo** impõe a um país periférico: pra
  crescer, importa mais, gasta dólar, pressiona o câmbio. *[no projeto]* é justamente o que o
  modelo (economia fechada) ainda **não tem** — o próximo bloco a construir.

---

## O modelo e o método

- **SFC (stock-flow consistent)** — modelo "contabilidade-consistente": toda saída de um setor
  é entrada de outro, nada some no meio. *[no projeto]* é o `BrasilSFC.mky` (Minsky/Keen).
- **Minsky** — o software (do Steve Keen) que desenha e roda esses modelos. `.mky` é o arquivo.
- **Modelo de mecanismo vs. previsão** — *[no projeto]* aviso de método repetido: o modelo
  mostra **direção e trade-off** (qualitativo), **não** número calibrado do Brasil. Essa
  honestidade **é o escudo** contra o crítico.
- **Ciclo de Goodwin** — modelo clássico do sobe-e-desce entre salário e lucro (como predador-
  presa). *[no projeto]* aparece como alerta: se a parcela salarial (ω) passa de 1 no modelo,
  é **overshoot do ciclo** (salário > produto, impossível), não um resultado válido.
- **Falseável** — afirmação que pode ser **testada e desmentida** por evidência. *[no projeto]*
  padrão de qualidade: a tese é formulada pra poder ser provada errada (ex.: "corte 2 p.p.; se
  o Real não apreciar, a tese caiu").
- **[FATO] vs. [JUÍZO]** — a regra de ouro do projeto: separar **aritmética/fonte primária**
  (FATO) da **parte corajosa e disputável** (JUÍZO). A força do argumento está em **não
  misturar** os dois.
- **Robusto (em direção / em nível)** — *[no projeto]* classificação dos resultados: "robusto
  em direção" = o sinal é confiável (a dívida *sobe*); "o nível exato" (371%) depende de
  parâmetros e é só condicional.
- **Estudo de evento** — método pra testar se o mercado reage ao fiscal: olhar juros futuros e
  câmbio **nos dias de anúncio**. *[no projeto]* o teste que decidiria a pergunta ortodoxa.
- **Materialismo histórico dialético (MHD)** — o método declarado do Jones: ler a política pela
  **estrutura de classe** e prever o desfecho a partir de quem ganha/perde. *[no projeto]* no
  vídeo do PLP 299 ele o usa como **previsão falseável** — "a arrecadação do topo será derrubada
  e o corte no primário passará" — e cobra o acerto como prova do método.
- **Eufemismo fiscal / linguagem esópica** — trocar a palavra que dói pela que anestesia:
  "economia" por **corte**, "qualificar o gasto" por **cortar saúde**, "impacto" por **perda**.
  *[no projeto]* é a "forma" na dupla substância×forma — e, nota pro roteiro, o alvo natural de
  uma **virada** no método tese-e-ataque (devolver o número cru que o eufemismo esconde: "corta
  10 bi do SUS").

---

*Faltou alguma palavra? Me fala numa sessão que eu atualizo este arquivo — ele é vivo.*
