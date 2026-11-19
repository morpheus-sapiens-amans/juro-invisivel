# O Juro Invisível
### uma conversa sensata com o ajuste fiscal brasileiro

Este repositório é uma investigação pública sobre o **juro alto e o ajuste fiscal no
Brasil** — por que o país paga um dos maiores juros reais do mundo, quem paga a conta do
ajuste, e o que diferentes escolas econômicas (e um paper acadêmico recente) dizem sobre
cortar a Selic.

Foi montado por **[Laércio Avelino](mailto:laercio.avelino@gmail.com)** com ajuda de
inteligência artificial. A ideia é simples e honesta:

> **Não acredite em mim. Interrogue os estudos.**
> Baixe, abra, mexa, rode os modelos, converse com uma IA sobre eles. Aprenda a partir das
> contas — não a partir de um ser humano falando com segurança na internet.

Eu (Laércio) sou o primeiro a dizer que não tenho formação técnica para sustentar tudo
isto sozinho. Por isso o material foi feito para **se defender sozinho**: tem relatórios,
tem modelos que qualquer um pode rodar, e tem um confronto explícito com a literatura
acadêmica — inclusive mostrando **onde eu posso estar errado**.

---

## Três jeitos de usar (do mais fácil ao mais fundo)

### 1. Só abrir o painel (não precisa instalar nada)
Abra **[`dashboard/index.html`](dashboard/index.html)** no seu navegador. Mexa nos
sliders e *veja* o juro dominar a dívida, veja o corte da Selic, veja quem paga a conta.
São 8 abas, incluindo uma que roda o modelo do economista **Dejanir Silva (Purdue)** ao
vivo.

### 2. Ler os relatórios
- **[O Juro Invisível](relatorios/O-Juro-Invisivel.pdf)** — o relatório principal (PDF).
- **[Confronto com Dejanir Silva](relatorios/confronto-dejanir-silva.md)** — onde a minha
  tese dialoga com um paper acadêmico ortodoxo, onde eles concordam, e onde eu estou
  exposto.

### 3. Conversar com o repositório (via IA)
Baixe a pasta inteira, abra com uma IA que leia arquivos (Claude, ChatGPT, Cursor…) e
pergunte. O arquivo **[`COMECE-AQUI.md`](COMECE-AQUI.md)** te ensina como, com perguntas
de partida. Há um arquivo-guia (`CLAUDE.md` / `AGENTS.md`) que instrui a IA a ser um
**tutor honesto** — explicar o raciocínio de cada autor (o meu, o do Dejanir, o da Lara
Resende, o das várias escolas) na terceira pessoa, confrontar com quem discorda, e sempre
separar *o que é robusto do que é aposta*.

### 4. Virar economista de bancada (rodar os modelos você mesmo)
Isto aqui não é só para ler — é um **laboratório**. Você pode:
- **Rodar os modelos em Python** (pasta `modelos/`): mude os parâmetros, faça as suas
  perguntas, tire as suas conclusões. Precisa de Python 3 (`pip install numpy matplotlib`).
- **Abrir o modelo no Minsky** e dar *play*, vendo o diagrama rodar com gráficos em tempo
  real — exatamente como eu faço. O passo a passo está em
  [`INSTALAR-MINSKY.md`](INSTALAR-MINSKY.md).

Você tem o direito de **apertar o play e ver funcionando**, e de discordar com base nas
suas próprias contas.

---

## O que é robusto e o que é aposta (a parte mais importante)

A honestidade é o produto. Aqui está, sem maquiagem:

**Robusto (aguenta ataque):**
- O juro real alto é **estrutural**, não teimosia passageira do Banco Central.
- Cortar a Selic **não** causa descontrole inflacionário; no longo prazo a inflação até
  cai. *Até um modelo ortodoxo de Purdue concede isto.*
- A **composição da dívida** e o **câmbio/risco-país** são o centro do problema.
- O caminho sólido para baixar o juro real é o **ajuste pelo topo** (progressivo), não o
  aperto do piso social.

**Aposta (precisa de rede, pode estar errado):**
- Que o Brasil esteja em **dominância fiscal**, onde cortar a Selic *aprecia* o Real.
  Isso é hipótese — nem o meu modelo nem o do Dejanir *provam* o regime atual.
- Que **reservas/ouro** firmem o Real estruturalmente. Pelas contas, elas são **ferramenta
  de transição**, não solução do juro real.

Leia o confronto completo em
[`relatorios/confronto-dejanir-silva.md`](relatorios/confronto-dejanir-silva.md).

---

## O que tem dentro

| Pasta | O que é |
|---|---|
| [`dashboard/`](dashboard/) | O painel interativo (abre no navegador) |
| [`relatorios/`](relatorios/) | O Juro Invisível + o confronto com o Dejanir + resumos técnicos |
| [`modelos/`](modelos/) | O laboratório em Python: o modelo do Brasil, o do Dejanir, a comparação, e os experimentos que geram as figuras |
| [`modelo-minsky/`](modelo-minsky/) | O modelo em **Minsky** (`.mky`) — abra e dê *play* (veja [`INSTALAR-MINSKY.md`](INSTALAR-MINSKY.md)) |
| [`dados-e-fontes/`](dados-e-fontes/) | Bibliografia e um dicionário de economia para leigos |

---

## Licença, crédito e colaboração

Este material é **livre para usar, copiar, remixar e usar em vídeos — inclusive
comercialmente** — com **uma condição: cite o autor** (Laércio Avelino).

- **Textos, relatórios e dados:** [CC BY 4.0](CONTENT-LICENSE.md).
- **Código (`modelos/`, dashboard):** [MIT](LICENSE).

Vai fazer um vídeo, um post, uma aula com isto? Ótimo — **me cite** e, se quiser, **me
chame pra colaborar**: [laercio.avelino@gmail.com](mailto:laercio.avelino@gmail.com).

> *Isto é um trabalho de cidadão, aberto à crítica. Achou um erro? Abra uma issue,
> me escreva, ou melhor: rode o modelo e me mostre onde a conta não fecha.*
