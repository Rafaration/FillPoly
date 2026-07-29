import pygame
import sys

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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

rodando = True
while rodando:
    tela.fill(PRETO)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if (painel_ui.foi_clicado(event)):
            print("Painel de UI foi clicado!")

        if (area_desenho.foi_clicado(event)):
            print("Área de desenho foi clicada!")

    painel_ui.desenhar(tela)
    area_desenho.desenhar(tela)

    pygame.display.flip()


    

