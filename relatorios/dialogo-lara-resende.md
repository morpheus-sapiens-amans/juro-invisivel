# Diálogo com Lara Resende: a Selic como ré

**Objeto.** André Lara Resende (ALR) e a tese do seu *"Eu Acuso"*: a de que o vilão fiscal
do Brasil não é o gasto social, mas o **juro**. Este documento explica a posição dele na
terceira pessoa, mostra onde o nosso trabalho **constrói com ele**, e onde vai **além** —
e termina apontando onde um adversário acadêmico (Dejanir Silva) aperta. Não é panfleto:
é a tese do ALR levada a sério, inclusive no que ela tem de disputado.

---

## 1. A mesa que ele vira

A narrativa dominante na grande mídia e no mercado tem a forma de uma ameaça: *"o Brasil
gasta demais; se não cortar despesa — inclusive saúde e educação —, a dívida explode."*
Nessa visão, o juro alto é **remédio** (contém demanda, ancora a inflação) e só poderá cair
quando o governo "provar" que é austero. O gasto público é o réu; o juro é o juiz.

**Lara Resende inverte a acusação.** Ele olha os números oficiais e mostra que o déficit
**primário** do Brasil é pequeno — dos menores do mundo. O rombo gigante é o déficit
**nominal**, e a diferença entre os dois é **quase toda conta de juros**. A conclusão dele:
*o vilão não é a escola nem o hospital — é a própria Selic, fixada pelo Banco Central, que
infla a dívida que diz combater.* O juro deixa de ser juiz e vira **réu**. Daí o título
"Eu Acuso".

Em uma linha:
- **Mídia/mercado:** a dívida explode **por causa do gasto** → corte gasto.
- **Lara Resende:** a dívida explode **por causa do juro** → baixe o juro.

---

## 2. Onde construímos COM ele (o mecanismo na tela)

A tese do ALR não é um palpite: tem um mecanismo, e dá para *mostrar* esse mecanismo
rodando. É isso que o nosso modelo faz.

- **O juro infla a dívida — visível.** No modelo de Minsky/Keen (rode
  [`../modelos/keen_model.py`](../modelos/keen_model.py)), com a mesma economia e a mesma
  condição inicial, só mexendo no juro, a dívida privada oscila com amplitude crescente até
  explodir — e **quanto maior o juro, mais rápido o colapso** (≈130 anos a 3%, ≈73 a 6%,
  ≈53 a 9%). O juro não muda *se* quebra; muda *quão rápido*.
- **O gasto público não é o vilão — é o freio.** No mesmo juro alto, *sem* governo a
  economia colapsa; *com* déficit público contracíclico ela se estabiliza. **Mas** há um
  limite honesto: se o juro for alto demais, nem o governo segura. O déficit estabiliza —
  **é o juro que decide se o remédio ainda funciona.**
- **A Selic como ré, em números.** Rode
  [`../modelos/tese_lara_resende.py`](../modelos/tese_lara_resende.py): baixar a Selic
  reduz o motor da dívida (a diferença entre juro e crescimento) e a trajetória de
  dívida/PIB termina mais baixa. Aritmética, não ideologia.

---

## 3. As três camadas (onde a tese é sólida e onde é aposta)

A honestidade do argumento está em separar três camadas — você pode **cravar as duas
primeiras sem comprar inteira a terceira**:

| Camada | Afirmação | Força |
|---|---|---|
| (a) Diagnóstico | o rombo é juro, não gasto social | **Sólido** |
| (b) Institucional | há teto constitucional pro gasto social e **nenhum** pro juro | **Forte** |
| (c) Solução | baixar a Selic sem detonar o câmbio | **Corajosa e disputada** |

A camada (c) é onde a tese ganha ou perde — e é também onde o ALR, na versão forte, diz que
o juro real alto é em larga medida **convenção/escolha**, não necessidade. Aqui é preciso
cuidado (ver seção 5).

---

## 4. Onde o nosso trabalho vai ALÉM do Lara Resende

O ALR acusa o juro e pede o corte. O nosso trabalho aceita o diagnóstico e **avança para a
pergunta que ele deixa em aberto: como cortar sem detonar o câmbio, e quem paga a conta.**

- **O câmbio, que faltava.** A crítica mais dura ao "só baixar a Selic" sempre foi o setor
  externo (fuga de capital, dólar). O nosso modelo **incorpora** esse bloco — câmbio,
  reservas, prêmio de risco, teste de regime. É exatamente aí que a tese é testada.
- **A proposta progressiva (o "topo paga").** Em vez de só cortar a Selic, o ajuste pode
  ser feito pelo **topo** (tributar o andar de cima, preservar o piso social), "revogar E
  ancorar" o teto/arcabouço, e reindustrializar via investimento público. Ver
  [`O-Juro-Invisivel.pdf`](O-Juro-Invisivel.pdf).
- **Reservas/ouro = ferramenta de transição**, não solução estrutural do juro real (as
  contas do próprio modelo mostram isso).

---

## 5. Onde o Dejanir aperta (e por que isso fortalece a proposta)

O paper de **Dejanir Silva** (Purdue, FTPL de economia aberta, estimado) é o melhor
adversário da tese — e ele **concede metade**: cortar a Selic não dispara hiperinflação, e
no longo prazo a inflação até cai. Mas ele crava um ponto contra a versão forte do ALR:
**o corte nominal não baixa o juro REAL estrutural** — ele volta ao nível pré-plano. O juro
real alto está preso ao prêmio de risco cambial e ao fisco, não à vontade do Banco Central.

A reviravolta: o Dejanir mostra que o que *de fato* baixa o juro real de longo prazo é
reduzir o risco cambial **ou** uma consolidação fiscal que **divide o alívio com os de
baixo (hand-to-mouth)** — ou seja, exatamente o "topo paga". A literatura ortodoxa
*enfraquece* a bandeira do "só cortar a Selic" e *fortalece* a proposta progressiva.

O confronto completo, com os números, está em
[`confronto-dejanir-silva.md`](confronto-dejanir-silva.md).

---

## Como interrogar você mesmo

- Rode [`../modelos/tese_lara_resende.py`](../modelos/tese_lara_resende.py) (a Selic como ré,
  nos dois regimes) e [`../modelos/keen_model.py`](../modelos/keen_model.py) (o juro→colapso).
- Abra o `dashboard/index.html` e passeie pelas abas "Bifurcação 2034" e "Neo-Fisher ·
  Dejanir".
- Mude os parâmetros. Discorde com base nas suas próprias contas.

---
*Aviso de método: os modelos mostram o **mecanismo qualitativo**, não previsão calibrada do
Brasil. A tese do ALR é levada a sério aqui — inclusive onde ela é disputada.*
