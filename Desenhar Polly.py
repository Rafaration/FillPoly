import pygame
import sys

class Ponto:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Poligono:
    def __init__(self, pontos: list[Ponto]):
        self.pontos = pontos

    def desenhar(self, tela):
        # Converte os pontos para uma lista de tuplas (x, y)
        pontos_tupla = [(ponto.x, ponto.y) for ponto in self.pontos]

        # Desenha o polígono na tela usando as linhas
        if len(pontos_tupla) >= 3: 
            for i in range(len(pontos_tupla)):
                pygame.draw.line(tela, (255, 0, 0), pontos_tupla[i], pontos_tupla[(i + 1) % len(pontos_tupla)], 2)
        else:
            print("É necessário pelo menos 3 pontos para formar um polígono.")


Pontos = [] # Lista para armazenar os pontos clicados pelo mouse
Poligonos = [] # Lista para armazenar os polígonos desenhados

# Inicializar o Pygame
pygame.init()

# Configurações da janela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Capturando cliques do mouse")

# Loop principal do jogo
rodando = True
while rodando:
    # Analisa a fila de eventos
    for evento in pygame.event.get():

        # fecha a janela se o usuário clicar no X
        if evento.type == pygame.QUIT:
            rodando = False

        # Verifica se ocorreu um clique do mouse
        elif evento.type == pygame.MOUSEBUTTONDOWN:

            # event.pos retorna as coordenadas (x, y) do clique do mouse
            

            # 1 = Esquerdo | 2 = Meio (Scroll) | 3 = Direito
            if evento.button == 1:
                aux = Ponto(evento.pos[0], evento.pos[1])
                Pontos.append(aux)
                pygame.draw.circle(tela, (0, 255, 0), (evento.pos[0], evento.pos[1]), 5)  # Desenha um ponto verde
                pygame.display.flip()

            elif evento.button == 2:
                tela.fill((0, 0, 0))  # Limpa a tela
                Pontos = []  # Limpa a lista de pontos
                Poligonos = []  # Limpa a lista de polígonos

            elif evento.button == 3:
                aux = Poligono(Pontos)
                Poligonos.append(aux)
                aux.desenhar(tela)
                pygame.display.flip()
                Pontos = []  # Limpa a lista de pontos para o próximo polígono

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_2: # Se a tecla '2' for pressionada
                tela.fill((0, 0, 0)) # Limpa a tela
                Poligonos.remove(Poligonos[1]) # Remove o segundo polígono da lista
                for poligono in Poligonos:
                    poligono.desenhar(tela) # Redesenha os polígonos restantes

    # Atualiza a tela
    pygame.display.flip()

pygame.quit()
sys.exit()