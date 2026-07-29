import pygame
import sys

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
            x, y = evento.pos
            print(f"O mouse foi clicado na posição: X={x}, Y={y}")

            # (Opicional) Você também pode verificar QUAL botão foi clicado
            # 1 = Esquerdo | 2 = Meio (Scroll) | 3 = Direito
            if evento.button == 1:
                print('Foi um clique com o botão ESQUERDO.')
            elif evento.button == 2:
                print('Foi um clique com o botão do MEIO (Scroll).')
            elif evento.button == 3:
                print('Foi um clique com o botão DIREITO.')

    # Atualiza a tela
    pygame.display.flip()

pygame.quit()
sys.exit()