# O neo-Fisherian com sotaque: o modelo de Dejanir Silva contra (e a favor de) a tese do corte

**Objeto.** Dejanir H. Silva (Purdue), *"Neo-Fisherian Adventures in the Tropics: Monetary Policy and Fiscal Inflation in Brazil"* (4 nov 2026, 99 pp). Um modelo de **teoria fiscal do nível de preços (FTPL) em economia aberta**, estimado em dados brasileiros, que pergunta: o que acontece quando o Banco Central se compromete de forma crível a baixar a Selic de 13,75% para 7,5%?

Este documento confronta o paper com **nossa tese** (o corte da Selic do campo Lara Resende) e com **nosso modelo** (BrasilSFC, stock-flow consistent / Minsky). Todos os números abaixo foram **reproduzidos** pelo nosso port Python do modelo dele (`dejanir_model.py`), que bate com o paper até a casa decimal.

---

## 1. O que o Dejanir prova — e por que não dá para ignorar

Diferente do neo-Fisherian de boteco ("corta a Selic que a inflação cai, fim"), o modelo dele é honesto com os dois lados:

**A favor do corte (munição pró-tese):**
- **O efeito neo-Fisherian de longo prazo é real.** Com o corte crível, a inflação cheia cai de ~6,1% a.a. para ~0,3% no longo prazo (t24). A identidade de Fisher opera: Selic nominal menor → inflação menor no equilíbrio. Isso valida a intuição central de Lara Resende de que juro alto *permanente* convive com inflação alta, não baixa.
- **A composição da dívida brasileira AMORTECE o choque.** O Brasil é pós-fixado-pesado (LFT ≈ 33% da dívida). Isso é uma bênção aqui: no portfólio atual (set/2026, LFT-pesado) o surto de inflação de impacto é de só **6,7%**; no portfólio prefixado-longo de set/2014 seria **11,1%**. Dívida flutuante limita a revalorização dos títulos quando o juro cai. — *Isto conversa direto com nosso "revogar E ancorar": a estrutura da dívida é alavanca, não detalhe.*
- **Dá para domar o pedágio de transição.** Uma venda esterilizada de reservas de 1% do PIB (~US$26 bi, ordem de grandeza das intervenções reais de 2024) corta o surto de impacto de **+3,3pp para +0,3pp**. O Brasil tem reservas para fazer isso. — *Isto é a tese das reservas do Laércio, confirmada num modelo ortodoxo.*

**Contra o atalho (o que desmonta o "de graça"):**
- **O juro REAL de longo prazo não se mexe.** No benchmark, o juro real da Selic sai de 7,27% no impacto e volta a 7,17% em t24 — o pré-plano. **Cortar a Selic nominal não baixa o juro real estrutural.** O problema do "Brasil paga o juro real mais alto do mundo" sobrevive intacto ao corte.
- **O nó real é risco-país + fiscal distributivo.** Só duas coisas baixam o juro real de longo prazo no modelo dele (Figura 12): (a) reduzir o **prêmio de risco cambial** (metade da variância cambial leva 7,25%→5,25%); (b) **consolidação fiscal que divide o alívio tributário com famílias hand-to-mouth** (tirar 1% do PIB de dívida leva 7,25%→6,23%). Nenhuma das duas é "só cortar a Selic".
- **Há um surto de transição.** Revalorização da dívida + depreciação cambial produzem um salto de inflação no impacto. E se o governo *gastar* a economia de juros, o surto explode de 9,4% para **23,5%**. A disciplina fiscal não é opcional no plano — é o que separa um pouso suave de um susto.

---

## 2. Confronto com o BrasilSFC: onde convergimos e onde divergimos

Rodamos o **mesmo choque** (corte 13,75%→7,5%) nos dois modelos (`cross_run.py`).

### Convergências (os dois modelos, metodologias opostas, concordam)
1. **A dívida e sua composição são o centro de gravidade.** Nosso modelo tem as 3 pernas (47% LFT / 26% pré / 27% IPCA); o dele tem o mesmo mecanismo de composição. Ambos dizem: *como* o governo se endivida decide o repasse do juro à inflação.
2. **O câmbio/risco-país é o canal crítico.** No nosso, o carry e o prêmio endógeno movem `e`; no dele, o wedge UIP e os arbitradores movem o câmbio real. Os dois põem o dólar no caminho crítico entre Selic e preços.
3. **Cortar a Selic nominal não entrega juro real baixo sozinho.** Esta é a conclusão compartilhada mais importante — e a mais inconveniente para a versão ingênua da tese.

### A divergência central: **regime único vs. flip de regime**
O modelo do Dejanir vive **sempre no regime "normal"**: um corte da Selic *sempre* deprecia o câmbio no impacto e produz surto de inflação. Não há inversão.

Nosso BrasilSFC tem **duas folhas**. Abaixo do limiar de dominância (b < 0,90) ele concorda com o Dejanir — corte deprecia, pressiona preços (no cross-run: inflação +0,01pp, câmbio +0,006; mesmo *sinal*, magnitude menor porque não temos revalorização forward-looking nem pass-through tão forte). **Acima do limiar** (b > 0,90, `phi_endog`), o sinal **inverte**: o corte *aprecia* o câmbio (−0,054) e *baixa* a inflação (−0,08pp), porque aliviar o serviço da dívida melhora a percepção de sustentabilidade. **Esse canal de dominância fiscal — o coração da tese ALR — simplesmente não existe no modelo do Dejanir.**

Ou seja: o Dejanir é um teste adversarial forte da nossa tese. Ele concede o longo prazo neo-Fisherian e a eficácia das reservas, mas **nega o mecanismo de dominância** pelo qual cortar apreciaria o Real. Para nós, o modelo dele é o "caso normal" da nossa Figura de bifurcação — o ramo que vale enquanto a dívida não cruza o limiar.

### O que cada um tem que o outro não tem
- **Nós temos, ele não:** flip de regime endógeno (bifurcação 2034), dívida privada endógena (Minsky), ciclo de Goodwin não-linear, as duas peças do "pacote do mal" (teto EC95 vs arcabouço LC200).
- **Ele tem, nós não:** FTPL propriamente dita (preço ajusta para igualar dívida real ao VP dos superávits), revalorização forward-looking dos títulos no impacto (o salto de dívida de +3,4% que não aparece no nosso), estimação bayesiana com decomposição histórica (os 38% da inflação vindos de choques fiscais em 5 anos), e o microfundamento do prêmio de risco cambial (arbitradores com aversão a risco).

---

## 3. Veredito para o roteiro "O Juro Invisível"

O paper do Dejanir é o **melhor presente possível** para a tese — porque é um adversário ortodoxo que concede o essencial:

> *Cortar a Selic não dispara uma hiperinflação. No longo prazo, até baixa a inflação. E o Brasil tem a composição de dívida e as reservas para administrar a transição.*

Mas ele também é a **vacina contra o exagero**:

> *O juro real alto não é teimosia do Banco Central — é prêmio de risco-país e fisco. Cortar a Selic nominal não o resolve. E se o governo gastar a economia de juros, o tiro sai pela culatra.*

A síntese para a narrativa (dosando a carga conforme o público):
- **Versão equilibrada / técnica:** usar o Dejanir como "até a ortodoxia de Purdue admite" — o longo prazo neo-Fisherian, as reservas, a composição. E ser honesto sobre o juro real estrutural: o corte é necessário mas não suficiente; o nó é risco-país + ajuste fiscal *progressivo* (hand-to-mouth), não austeridade cega.
- **Versão mobilização:** o pivô é o "ajuste fiscal com hand-to-mouth" da Figura 12 — *a própria FTPL de Purdue diz que dividir o alívio com os de baixo baixa o juro real*. Isso é munição para a proposta própria do Laércio contra o ajuste regressivo.

O Dejanir não prova a tese inteira. Ele prova **metade dela com força total** e marca onde a outra metade (a dominância) precisa de defesa — que é exatamente onde nosso BrasilSFC entra.

---

*Arquivos relacionados neste repositório: [`dejanir-resumo-tecnico.md`](dejanir-resumo-tecnico.md) (dissecação do paper), [`nosso-modelo-mapa.md`](nosso-modelo-mapa.md) (nosso SFC), [`../modelos/dejanir_model.py`](../modelos/dejanir_model.py) (port validado), [`../modelos/cross_run.py`](../modelos/cross_run.py) (comparação executável).*

---

**O paper original de Dejanir Silva** não está incluído aqui (é obra dele, com direitos
próprios). Acesse na página do autor: <https://sites.google.com/site/dejanirhsilva/research>
("Neo-Fisherian Adventures in the Tropics: Monetary Policy and Fiscal Inflation in
Brazil", Purdue University, 2026). As simulações interativas da Seção 5 dele estão em
<https://dejanirsilva.github.io/neofisherian_adventures/>.
