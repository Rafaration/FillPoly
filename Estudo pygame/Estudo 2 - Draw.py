import time

import pygame

# definindo cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Inicializa o pygame
pygame.init()

# Define o tamanho da tela
width = 640
height = 480

# Cria a tela do jogo
screen = pygame.display.set_mode((width, height))

# Carregando a fonte
font = pygame.font.Font(None, 55)

# Define o título da janela
pygame.display.set_caption('Olá Mundo')

# Preenchendo o fundo com preto
screen.fill(BLACK)

# Desenhando na superfície
pygame.draw.line(screen, WHITE, (10, 100), (630, 100), 5)
pygame.draw.rect(screen, BLUE, (200, 210, 40, 20))
pygame.draw.ellipse(screen, RED, (300, 200, 40, 40))
pygame.draw.polygon(screen, GREEN, [(400, 200), (440, 240), (400, 240)])

# Preenche apenas um único pixel da tela
screen.set_at((320, 400), WHITE)

# atualizando a tela
pygame.display.flip()

time.sleep(5)

# preenchendo o fundo com preto
screen.fill(BLACK)

# definindo o texto
text = font.render('pygame', True, WHITE)

# copiando o texto para a superfície
screen.blit(text, (250, 200))

# atualizando a tela
pygame.display.flip()

# Rodar até apertar no botão de fechar
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False