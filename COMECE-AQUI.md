# Comece aqui — como conversar com este material

Você não precisa ser economista nem programador. Escolha seu nível.

## Nível 1 — só olhar (2 minutos, zero instalação)
Abra **<https://morpheus-sapiens-amans.github.io/juro-invisivel/dashboard/>** no seu
navegador — funciona até no celular. (Se você já baixou esta pasta, o mesmo painel abre
offline: dois cliques no arquivo **`dashboard/index.html`**.)
Passeie pelas abas e mexa nos sliders. Comece pela aba **"Bifurcação 2034"** (dois futuros
para a dívida) e pela aba **"Neo-Fisher · Dejanir"** (o modelo de um economista de Purdue
rodando ali, na sua tela).

## Nível 2 — conversar com uma IA sobre o material
1. Baixe a pasta inteira deste repositório para o seu computador.
2. Abra uma IA que consiga ler arquivos de uma pasta — por exemplo **Claude** (claude.ai
   ou Claude Code), **ChatGPT** (com os arquivos anexados) ou **Cursor**.
3. Aponte a IA para esta pasta e peça para ela ler o arquivo `CLAUDE.md` (ou `AGENTS.md`)
   primeiro — ele instrui a IA a ser um **tutor honesto**, não um vendedor.
4. Pergunte à vontade. Sugestões de partida:

   - *"Me explique, como se eu não soubesse nada de economia, por que o juro alto do
     Brasil é um problema."*
   - *"Qual é a tese do Laércio? E onde ele pode estar errado?"*
   - *"O que o Dejanir Silva diz que contradiz o Laércio? E onde eles concordam?"*
   - *"O que significa 'dominância fiscal' e por que isso é uma aposta e não um fato?"*
   - *"Cortar a Selic baixa o juro real? Me mostre o que os modelos dizem."*
   - *"Quem paga a conta do ajuste fiscal em cada cenário?"*

   A IA deve sempre te dizer **o que é robusto e o que é aposta**, e te mandar conferir nos
   relatórios e nos modelos. Se ela só elogiar o autor, desconfie — e peça: *"seja crítico,
   onde isto é frágil?"*

## Nível 3 — rodar os modelos você mesmo (precisa de Python)
Os modelos são as **contas de verdade** por trás de tudo. Instale o Python 3 e as
bibliotecas (`pip install numpy matplotlib`) e rode, na pasta `modelos/`:

```bash
cd modelos

# o núcleo (só precisa de numpy):
python3 brasil_sfc.py      # nosso modelo do Brasil (dívida, câmbio, juro)
python3 dejanir_model.py   # o modelo do Dejanir — reproduz os números do paper dele
python3 cross_run.py       # roda os dois no MESMO choque e compara lado a lado

# os experimentos que geram as figuras dos relatórios (precisam de matplotlib;
# salvam em modelos/saida/):
python3 teste_regime.py    # o teste de dominância fiscal (o câmbio vira de sinal?)
python3 bateria_teto.py    # teto × arcabouço × revogar: o "pacote do mal"
python3 escada_carrego.py  # a escada: alternativa direta × pacote completo
python3 bateria_jones.py   # os cenários do argumento do Jones
```

**A ideia é você mexer.** Abra qualquer arquivo, mude um parâmetro (a Selic, a meta de
primário, a composição da dívida), rode de novo e veja o que muda. Faça as suas perguntas,
tire as suas conclusões. Se os números baterem com os dos relatórios, é porque **não tem
truque** — são as mesmas contas. Se não baterem, me avise: isso é um erro e eu quero saber.

## Nível 4 — abrir o modelo no Minsky e dar play
Quer ver o modelo **por dentro**, como um diagrama que roda com gráficos em tempo real?
Esse é o **Minsky**, o programa visual do economista Steve Keen. O passo a passo (baixar o
Minsky, abrir `modelo-minsky/BrasilSFC-com-plots.mky`, apertar play, mudar parâmetros) está
em **[`INSTALAR-MINSKY.md`](INSTALAR-MINSKY.md)**. Você tem o direito de apertar o play e
ver funcionando.

## Onde está cada coisa
- Dúvida de palavra ("o que é Selic? o que é prêmio de risco?") →
  `dados-e-fontes/dicionario-economia.md`.
- O argumento completo → `relatorios/O-Juro-Invisivel.pdf`.
- O confronto com a academia → `relatorios/confronto-dejanir-silva.md`.
- De onde vêm as fontes → `dados-e-fontes/bibliografia.ris`.

---
Dúvida, crítica ou convite para colaborar:
**[laercio.avelino@gmail.com](mailto:laercio.avelino@gmail.com)**
