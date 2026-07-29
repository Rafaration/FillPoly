import pygame
import sys

pygame.init()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 122, 204)
AZUL_CLARO = (51, 153, 255)

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


# --- Configuração Inicial ---
tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Criando Botões")

# Instanciando o nosso botão
botao_iniciar = Botao(300, 250, 200, 60, "Iniciar Jogo")
botao_sair = Botao(300, 350, 200, 60, "Sair", cor=(255, 0, 0), cor_hover=(255, 100, 100))

rodando = True
while rodando:
    tela.fill(PRETO)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
            
        # 1. Checa as interações do botão
        if botao_iniciar.foi_clicado(event):
            print("Botão clicado! Iniciando sistema...")
            # Aqui você mudaria a tela do seu jogo ou iniciaria uma função
            
    # 2. Desenha o botão na tela
    botao_iniciar.desenhar(tela)
    botao_sair.desenhar(tela)

    pygame.display.flip()

pygame.quit()
sys.exit()