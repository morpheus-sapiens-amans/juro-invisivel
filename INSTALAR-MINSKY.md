# Rodar o modelo no Minsky — dar play e ver funcionando

O **Minsky** é um programa livre e de código aberto, criado pelo economista **Steve Keen**,
para montar e simular modelos econômicos de forma **visual** — você vê o modelo como um
diagrama, aperta *play*, e acompanha os gráficos em tempo real. Nosso modelo do Brasil
(`modelo-minsky/BrasilSFC-com-plots.mky`) foi feito nele.

Você **não precisa** do Minsky para usar o resto deste repositório (o dashboard e os
modelos em Python funcionam sozinhos). O Minsky é para quem quer **abrir o modelo por
dentro** e mexer nele como numa bancada.

> Por que não vem junto? O Minsky é um programa grande, com licença própria (GPL). Em vez
> de embutir, a gente entrega o **modelo** (`.mky`) e te mostra como pegar o Minsky oficial
> — assim você sempre tem a versão mais atual, direto da fonte.

## 1. Baixar e instalar o Minsky

Site oficial (instaladores para **Windows, macOS e Linux**):
- https://www.hpcoders.com.au/minsky.html
- Projeto e código-fonte: https://sourceforge.net/projects/minsky/ · https://github.com/highperformancecoder/minsky

Baixe o instalador do seu sistema e instale normalmente.

## 2. Abrir o modelo

1. Abra o Minsky.
2. Menu **File → Open** e escolha o arquivo **`modelo-minsky/BrasilSFC-com-plots.mky`**
   (a versão "com-plots" já vem com os gráficos montados; `BrasilSFC.mky` é a versão sem
   os gráficos).
3. Você vai ver o diagrama do modelo: as variáveis (dívida, câmbio, Selic, reservas…), as
   ligações entre elas e os painéis de gráfico.

## 3. Dar play

- Use os botões de **play / pause / reset** na barra do Minsky para rodar a simulação.
- Os gráficos se preenchem enquanto o modelo roda.
- Dê um duplo-clique numa variável ou parâmetro para **mudar o valor** (por exemplo, a
  Selic) e rode de novo para ver o efeito. **Essa é a graça:** é a sua bancada, faça suas
  próprias perguntas.

## Observação para quem usa Linux (Arch e afins)

Se a janela do Minsky abrir preta ou com problema de renderização no Wayland, force o X11:

```bash
minsky --ozone-platform=x11
```

## Quer reconstruir o `.mky` a partir do código?

Os scripts em `modelos/` que começam com `build_brasil_mky.py` / `cenarios_mky.py` /
`add_plots.py` geram e editam o `.mky` por código, usando a biblioteca **`pyminsky`** (as
ligações Python do Minsky). É um caminho avançado — a maioria das pessoas só precisa abrir
o `.mky` pronto e dar play.
