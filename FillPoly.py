import pygame

# Classe que armazena as coordenadas de um ponto
class Ponto:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

# Classe que representa um polígono formado por uma lista de pontos
class Poligono:
    def __init__(self, pontos: list[Ponto]):
        self.pontos = pontos

    def desenhar_arestas(self, tela):

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
                    tela.set_at((int(x), y), BRANCO)  # Desenha um pixel branco na posição calculada
                    x += Tx # Atualiza a coordenada x para a próxima scanline


# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 122, 204)
AZUL_CLARO = (51, 153, 255)

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

pygame.init()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 122, 204)
AZUL_CLARO = (51, 153, 255)

tela = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Divisão de Áreas")

painel_ui = PainelUI(850, 0, 350, 600, BRANCO)
area_desenho = AreaDesenho(0, 0, 850, 600, PRETO)

# Criar estruturas que irão armazenar os polígonos e pontos desenhados
Pontos = [] # Lista para armazenar os pontos clicados pelo mouse
Poligonos = [] # Lista para armazenar os polígonos desenhados

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
                        PoligonosAux = Poligono(Pontos)
                        Poligonos.append(PoligonosAux)
                        Pontos = []  # Limpa a lista de pontos após criar o polígono
                        print("Polígono criado com sucesso!")
                    else:
                        print("É necessário pelo menos 3 pontos para formar um polígono.")

    # 3. FASE DE DESENHO CONTÍNUO (renderiza tudo que existe a cada frame)
    area_desenho.desenhar(tela)
    painel_ui.desenhar(tela)

    # Desenha os pontos que estão sendo clicados e ainda não viraram polígonos
    for p in Pontos:
        tela.set_at((p.x, p.y), BRANCO) # Desenha um pixel branco na posição do ponto

    # Desenha as arestas dos polígonos salvos
    for poligono in Poligonos:
        poligono.desenhar_arestas(tela)

    # 4. Atualiza a tela
    pygame.display.flip()
