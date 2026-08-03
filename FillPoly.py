import pygame

# Classe que armazena as coordenadas de um ponto
class Ponto:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

# Classe que representa um polígono formado por uma lista de pontos
class Poligono:
    def __init__(self, pontos: list[Ponto], cor:bool = False):
        self.pontos = pontos
        self.cor = cor
        self.selecionado = False # Indica se o polígono está selecionado

    def desenhar_arestas(self, tela):

        # Verifica se terá arestas para desenhar
        if self.selecionado:
            aresta_cor = VERMELHO
        elif self.cor:
            aresta_cor = BRANCO
        else:
            aresta_cor = PRETO

        # Descobre os limites do polígono para desenhar as arestas
        y_min = min(ponto.y for ponto in self.pontos)
        y_max = max(ponto.y for ponto in self.pontos)

        # Calcula o número de scanlines (linhas horizontais)
        Ns = y_max - y_min # a de baixo a gente não conta

        # Calculado o coeficiente angular da reta dos pontos
        for i in range(len(self.pontos)):
            if (self.pontos[i].y < self.pontos[(i + 1) % len(self.pontos)].y):
                ponto1 = self.pontos[i]
                ponto2 = self.pontos[(i + 1) % len(self.pontos)] # O próximo ponto, voltando ao início se necessário
            else:
                ponto2 = self.pontos[i]
                ponto1 = self.pontos[(i + 1) % len(self.pontos)] # O próximo ponto, voltando ao início se necessário
            
            if ponto1.y != ponto2.y:  # Evita divisão por zero
                Tx = (ponto2.x - ponto1.x) / (ponto2.y - ponto1.y)  # Coeficiente angular

                x = ponto1.x # Inicializa x com a coordenada x do ponto1
                
                # Desenha a linha entre os dois pontos
                for y in range(ponto1.y, ponto2.y):
                    tela.set_at((int(x), y), aresta_cor)  # Desenha um pixel na posição calculada
                    x += Tx # Atualiza a coordenada x para a próxima scanline


# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 122, 204)
AZUL_CLARO = (51, 153, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)
CINZA = (128, 128, 128)


class PainelUI:
    def __init__(self, x, y, largura, altura, cor_fundo=(BRANCO)):
        '''Inicializa o painel de UI com suas propriedades.
        
        Parâmetros:
            x, y (int): Posição horizontal e vertical do painel.
            largura (int): Dimensão de largura do painel.
            altura (int): Dimensão de altura do painel.
            cor_fundo (tuple): Cor de fundo do painel em formato RGB.
        '''

        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_fundo = cor_fundo

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor_fundo, self.rect)

    def foi_clicado(self, event):
        # Verifica se o evento foi um clique esquerdo E se ocorreu dentro do painel
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class AreaDesenho:
    def __init__(self, x, y, largura, altura, cor_fundo=(PRETO)):
        '''Inicializa a área de desenho com suas propriedades.
        
        Parâmetros:
            x, y (int): Posição horizontal e vertical da área de desenho.
            largura (int): Dimensão de largura da área de desenho.
            altura (int): Dimensão de altura da área de desenho.
            cor_fundo (tuple): Cor de fundo da área de desenho em formato RGB.
        '''

        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_fundo = cor_fundo

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor_fundo, self.rect)

    def foi_clicado(self, event):
        # Verifica se o evento foi um clique esquerdo E se ocorreu dentro da área de desenho
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or event.button == 3:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Botao:
    def __init__(self, x, y, largura, altura, texto, tam_fonte = 36, cor_fonte=BRANCO, cor=AZUL, cor_hover=AZUL_CLARO):
        """Inicializa o botão com suas propriedades.

        Parâmetros:
            x, y (int): Posição horizontal e vertical do botão.
            largura (int): Dimensão de largura do botão.
            altura (int): Dimensão de altura do botão.
            texto (str): Texto a ser exibido no botão.
            tam_fonte (int): Tamanho da fonte do texto.
            cor_fonte (tuple): Cor do texto em formato RGB.
            cor (tuple): Cor padrão do fundo do botão.
            cor_hover (tuple): Cor do botão quando o mouse está sobre ele.
        """

        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.fonte = pygame.font.Font(None, tam_fonte)
        self.cor_fonte = cor_fonte
        self.cor = cor
        self.cor_hover = cor_hover

    def desenhar(self, tela):
        # Captura a posição atual do mouse para o efeito de "hover" (passar o mouse por cima)
        mouse_pos = pygame.mouse.get_pos()
        
        # Muda a cor se o mouse estiver sobre o botão
        if self.rect.collidepoint(mouse_pos):
            cor_atual = self.cor_hover
        else:
            cor_atual = self.cor
            
        # Desenha o retângulo do botão
        pygame.draw.rect(tela, cor_atual, self.rect, border_radius=8) # border_radius arredonda os cantos
        
        # Renderiza e centraliza o texto dentro do botão
        superficie_texto = self.fonte.render(self.texto, True, self.cor_fonte)
        rect_texto = superficie_texto.get_rect(center=self.rect.center)
        tela.blit(superficie_texto, rect_texto)

    def foi_clicado(self, event):
        # Verifica se o evento foi um clique esquerdo E se ocorreu dentro do botão
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

pygame.init()


tela = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Divisão de Áreas")

painel_ui = PainelUI(850, 0, 350, 600, BRANCO)
area_desenho = AreaDesenho(0, 0, 850, 600, PRETO)

botao_arestas = Botao(900, 50, 250, 50, "Exibe Arestas", tam_fonte=30, cor=AZUL, cor_hover=AZUL_CLARO)

# Criar estruturas que irão armazenar os polígonos e pontos desenhados
Pontos = [] # Lista para armazenar os pontos clicados pelo mouse
Poligonos = [] # Lista para armazenar os polígonos desenhados
Botoes_Poligonos = [] # Lista para armazenar os botões dos polígonos desenhados 

rodando = True
while rodando:
    # 1. Limpa a tela
    tela.fill(PRETO)

    # 2. Processa os eventos de input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        # Verifica se ocorreu um clique do mouse
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Verifica se o clique foi na UI
            if (painel_ui.foi_clicado(event)):
                print("Painel de UI foi clicado!")

                if (botao_arestas.foi_clicado(event)):
                    print("Botão 'Exibe Arestas' foi clicado!")
                    tem_aresta = any(poligono.cor for poligono in Poligonos)  # Verifica se algum polígono está com arestas exibidas
                    if (tem_aresta):
                        print("Desativando exibição das arestas dos polígonos.")
                        for poligono in Poligonos:
                            poligono.cor = False # Alterna a exibição das arestas do polígono
                    else:
                        print("Ativando exibição das arestas dos polígonos.")
                        for poligono in Poligonos:
                            poligono.cor = True # Alterna a exibição das arestas do polígono

                for i, botao in enumerate(Botoes_Poligonos):
                    if botao.foi_clicado(event):
                        print(f"Polígono {i + 1} foi selecionado!")

                        # desmarca todos os polígonos
                        for p in Poligonos:
                            p.selecionado = False

                        # Marca apenas o polígono correspondente ao botão clicado
                        Poligonos[i].selecionado = True


            # Verifica se o clique foi na área de desenho
            if (area_desenho.foi_clicado(event)):
                print("Área de desenho foi clicada!")

                # botão esquerdo = armazena o ponto.
                if event.button == 1:
                    PontosAux = Ponto(event.pos[0], event.pos[1])
                    Pontos.append(PontosAux)

                # Botão direito = armazena o polígono formado pelos pontos clicados.
                elif event.button == 3:
                    if len(Pontos) >= 3: # Verifica se há pelo menos 3 pontos para formar um polígono
                        tem_aresta = any(poligono.cor for poligono in Poligonos)  # Verifica se algum polígono está com arestas exibidas

                        PoligonosAux = Poligono(Pontos, tem_aresta) # Cria um novo polígono com os pontos armazenados
                        Poligonos.append(PoligonosAux)
                        Pontos = []  # Limpa a lista de pontos após criar o polígono
                        print("Polígono criado com sucesso!")

                        # Criar botão dinâmico
                        qtd = len(Poligonos)
                        # a posição y aumenta em cada botão criado, para que eles não se sobreponham
                        y_botao = 320 + (qtd - 1) * 60

                        novo_botao = Botao(875, y_botao, 305, 50, f"Polígono {qtd}", tam_fonte=28, cor=AZUL, cor_hover=AZUL_CLARO)
                        Botoes_Poligonos.append(novo_botao)

                    else:
                        print("É necessário pelo menos 3 pontos para formar um polígono.")

    # 3. FASE DE DESENHO CONTÍNUO (renderiza tudo que existe a cada frame)
    area_desenho.desenhar(tela)
    painel_ui.desenhar(tela)

    # Desenhar area para seleção de cores
    pygame.draw.rect(tela, (200, 200, 200), pygame.Rect(875, 150, 305, 150))

    # Desenha os botões na tela
    botao_arestas.desenhar(tela)

    # Desenha os botões dos polígonos
    for botao in Botoes_Poligonos:
        botao.desenhar(tela)

    # Desenha os pontos que estão sendo clicados e ainda não viraram polígonos
    for p in Pontos:
        tela.set_at((p.x, p.y), BRANCO) # Desenha um pixel branco na posição do ponto

    # Desenha as arestas dos polígonos salvos
    for poligono in Poligonos:
        poligono.desenhar_arestas(tela)

    # 4. Atualiza a tela
    pygame.display.flip()
