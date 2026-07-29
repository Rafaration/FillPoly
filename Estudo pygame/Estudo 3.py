import pygame

# definindo cores 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Inicializa o pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))

pygame.display.set_caption('Game Loop')

# Variáveis da bola
position_x = 300
position_y = 200
velocity_x = 0.2
velocity_y = 0.2

# iniciando o loop do jogo
while True:
    # PROCESSAMENTE DE ENTRADA

    # Capturando eventos
    event = pygame.event.poll()
    # Caso o evento QUIT (clicar no x da janela) seja disparado
    if event.type == pygame.QUIT:
        # Saia do loop finalizando o programa
        break


    # ATUALIZAÇÃO DO JOGO

    # Movendo a bola
    position_x += velocity_x
    position_y += velocity_y

    # mudando a direção no eixo x nas bordas
    if position_x > 600 or position_x < 0:
        velocity_x *= -1


    # mudando a direção no eixo y nas bordas
    if position_y > 440 or position_y < 0:
        velocity_y *= -1


    # DESENHO

    # Preenchendo o funndo com preto
    screen.fill(BLACK)

    # Desenhando a bola
    pygame.draw.ellipse(screen, WHITE, (position_x, position_y, 40, 40))

    # Atualizando a tela
    pygame.display.flip()