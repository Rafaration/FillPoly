# FillPoly

Trabalho 1 da disciplina de Computação Gráfica — Curso de Ciência da Computação, Unioeste (Campus de Cascavel).
Professor: Adair Santa Catarina.

Um programa em Python + Pygame que deixa o usuário desenhar polígonos na tela com o mouse e preenche o interior deles usando o algoritmo **fillpoly** (preenchimento por scanline, com aritmética incremental), implementado do zero, pixel a pixel, sem usar nenhuma função pronta de preenchimento de biblioteca.

## Integrantes

- Rafael Loureiro Fockink - Rafaration
- Eric Barbachã Gonçalves - ericbg404

## O que o programa faz

O usuário desenha um ou mais polígonos clicando na área preta da tela. Cada polígono pode ser regular, irregular, ter arestas que se cruzam ou ter um ou mais buracos, em todos os casos, o mesmo algoritmo de preenchimento cuida de pintar só a parte "de dentro", incluindo deixar os buracos vazios e alternar regiões preenchidas/vazias quando o polígono se cruza.

Depois de desenhado, qualquer polígono pode ser selecionado clicando em cima dele, e a partir daí o usuário pode trocar a cor de preenchimento, apagá-lo da tela, ou ligar/desligar a exibição das arestas de todos os polígonos de uma vez.

## Estrutura do repositório

```
FillPoly/
├── FillPolyMono.py       # Versão final entregue (single-file)
├── FillPoly.py            # Versão anterior de desenvolvimento
├── Areas.py                # Estudo/protótipo de área de desenho em Pygame
├── Desenhar Polly.py       # Estudo/protótipo de desenho de polígono
└── Estudo pygame/          # Exercícios de estudo do Pygame (não fazem parte da entrega)
```

O arquivo que deve ser executado para a apresentação é o **`FillPolyMono.py`** — os demais arquivos na raiz e a pasta `Estudo pygame/` são material de estudo e protótipos de etapas anteriores do desenvolvimento, mantidos no histórico do repositório para referência.

## Como executar

**Sistema operacional:** qualquer um com suporte a Python 3.10+ (Windows, Linux ou macOS).

**Interpretador:** Python 3.10 ou superior.

**Biblioteca necessária:** [Pygame](https://www.pygame.org/).

Instalação:

```bash
pip install pygame
```

Ou 

```bash
pip install pygame-ce
```

Execução:

```bash
python FillPolyMono.py
```

## Como usar

Ao abrir o programa, a tela fica dividida em duas partes: a área preta à esquerda, onde os polígonos são desenhados, e o painel branco à direita, com os controles.

**Desenhando um polígono:** clique com o botão esquerdo do mouse na área preta para ir marcando os vértices, um de cada vez. Quando tiver pelo menos três pontos marcados, clique com o botão direito para fechar o polígono, ele aparece preenchido automaticamente com uma cor sorteada.

**Selecionando um polígono:** segure `Ctrl` e clique com o botão esquerdo em cima do polígono desejado. Clicar de novo no mesmo polígono (ainda com `Ctrl`) desmarca a seleção. Só um polígono fica selecionado por vez.

**Trocando a cor:** com um polígono selecionado, clique em qualquer cor da paleta no painel lateral. A cor do polígono muda na hora.

**Desenhando um buraco:** primeiro selecione o polígono que vai receber o buraco (`Ctrl` + clique). Depois, segure `Shift` e clique com o botão esquerdo para marcar os vértices do buraco — assim como no polígono, precisa de pelo menos três pontos. Para fechar o buraco, segure `Shift` e clique com o botão direito. É possível repetir esse processo para adicionar mais de um buraco ao mesmo polígono.

**Mostrando ou escondendo as arestas:** o botão "Alternar Arestas" liga e desliga, para todos os polígonos ao mesmo tempo, o contorno branco de 1 pixel ao redor de cada forma (e de seus buracos).

**Apagando um polígono:** selecione o polígono (`Ctrl` + clique) e clique em "Remover Polígono".

## As funções do programa

### `Ponto(x, y)`

A unidade mais simples do programa: só guarda uma posição na tela. `x` e `y` são as coordenadas horizontal e vertical, em pixels.

### `Poligono(pontos_externos, aresta, cor)`

Representa um polígono desenhado. `pontos_externos` é a lista de vértices que forma o contorno de fora, `aresta` diz se o contorno deve aparecer desenhado em branco, `cor` é a cor usada para preencher o interior.

Por dentro, o polígono guarda seus contornos numa lista (`contornos`): o primeiro é sempre o de fora, e os que vêm depois são os buracos, se houver. Isso é o que permite ao mesmo algoritmo de preenchimento tratar buracos e autointerseção sem precisar de nenhuma lógica extra — é só mais um contorno entrando na mesma conta.

As funções (métodos) desse objeto são:

- **`adicionar_buraco(pontos_buraco)`** — recebe uma lista de pontos e a guarda como um novo buraco do polígono, recalculando tudo o que for necessário para o buraco aparecer corretamente.
- **`atualizar_geometria()`** — recalcula os limites verticais do polígono e a tabela de interseções usada no preenchimento. É chamada sempre que a forma do polígono muda (por exemplo, ao adicionar um buraco).
- **`calcular_tabela_intersecoes()`** — para cada linha horizontal (scanline) que o polígono ocupa, calcula em quais pontos x as arestas do polígono cruzam aquela linha. É o coração do algoritmo fillpoly.
- **`preencher(tela)`** — usa a tabela de interseções para pintar, linha por linha, os pixels que ficam dentro do polígono, na cor escolhida.
- **`desenhar_arestas(tela)`** — desenha os contornos da forma: a borda externa em branco e os buracos em preto (caso a exibição geral de arestas esteja ligada), ou destaca toda a forma em branco quando o polígono está selecionado.
- **`contem_ponto(ponto)`** — responde se um ponto clicado está dentro do polígono. É usada para descobrir qual polígono o usuário quis selecionar.

### `PainelUI(x, y, largura, altura, cor_fundo)`

O painel lateral onde ficam os botões e a paleta de cores. `x` e `y` marcam onde ele começa na tela, `largura` e `altura` definem o tamanho, e `cor_fundo` é a cor de fundo do painel.

### `AreaDesenho(x, y, largura, altura, cor_fundo)`

A área preta onde os polígonos são desenhados. Os parâmetros funcionam do mesmo jeito que no `PainelUI`: posição, tamanho e cor de fundo.

### `Botao(x, y, largura, altura, texto, tam_fonte, cor_fonte, cor, cor_hover)`

Um botão clicável com texto, como "Alternar Arestas" ou "Remover Polígono". Além de posição e tamanho, recebe o `texto` que aparece nele, o tamanho da fonte (`tam_fonte`), a cor do texto (`cor_fonte`), a cor do botão (`cor`) e a cor que ele assume quando o mouse passa por cima (`cor_hover`).

### `BotaoCor(x, y, tamanho, cor)`

Cada quadradinho colorido da paleta é um `BotaoCor`. `tamanho` define o lado do quadrado, e `cor` é a cor que ele representa — a mesma cor que será aplicada ao polígono selecionado, se o usuário clicar nele.

### `selec_cor()`

Sorteia uma cor aleatória da paleta. É usada para dar uma cor inicial a cada polígono assim que ele é criado, antes de o usuário escolher outra.

## O algoritmo

O fillpoly identifica, para cada scanline (linha horizontal), os pontos onde as arestas do polígono a cruzam, ordena essas interseções e preenche os pixels entre cada par consecutivo utilizando a Regra Ímpar-Par (Odd-Even Rule). Essa abordagem permite que buracos e autointerseções sejam renderizados naturalmente, sem a necessidade de cálculos de subtração complexos. As interseções de cada scanline são calculadas de forma incremental: a partir da interseção na scanline anterior, soma-se uma taxa fixa `Tx = dx/dy` para obter a próxima, evitando recalcular a equação da reta a cada linha.

## Nota de Transparência

Este README foi feito com o auxílio do Claude (Sonnet 5) para garantir que todos os aspectos da implementação fossem devidamente citados. Todo o texto gerado foi revisado pelos autores.