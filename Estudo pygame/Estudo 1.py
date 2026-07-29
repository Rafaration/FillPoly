import time

import pygame

# inicializa o pygame
pygame.init()

width = 640
height = 480

# Cria a tela do jogo
screen = pygame.display.set_mode((width,height))

# Define o título da janela
pygame.display.set_caption('Olá mundo')

# Define a cor de fundo da tela
screen.fill([180, 50, 180])

# Espelha o conteúdo desenhado na screen
pygame.display.flip()

# Rodar até apertar no botão de fechar
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False