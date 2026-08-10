import math
import random
import pygame

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 122, 204)
AZUL_CLARO = (51, 153, 255)
AZUL_ESCURO = (0, 82, 138)
VERMELHO = (255, 0, 0)
VERMELHO_CLARO = (255, 102, 102)
VERMELHO_ESCURO = (153, 0, 0)
VERDE = (0, 255, 0)
VERDE_CLARO = (102, 255, 102)
VERDE_ESCURO = (0, 153, 0)
AMARELO = (255, 255, 0)
AMARELO_CLARO = (255, 255, 153)
AMARELO_ESCURO = (204, 204, 0)
ROXO = (128, 0, 128)
ROXO_CLARO = (178, 102, 255)
ROXO_ESCURO = (77, 0, 77)
LARANJA = (255, 165, 0)
LARANJA_CLARO = (255, 200, 102)
LARANJA_ESCURO = (204, 102, 0)
CINZA = (128, 128, 128)
CINZA_CLARO = (192, 192, 192)
CINZA_ESCURO = (64, 64, 64)

CORES = [
    BRANCO,
    AZUL,
    AZUL_CLARO,
    AZUL_ESCURO,
    VERMELHO,
    VERMELHO_CLARO,
    VERMELHO_ESCURO,
    VERDE,
    VERDE_CLARO,
    VERDE_ESCURO,
    AMARELO,
    AMARELO_CLARO,
    AMARELO_ESCURO,
    ROXO,
    ROXO_CLARO,
    ROXO_ESCURO,
    LARANJA,
    LARANJA_CLARO,
    LARANJA_ESCURO,
    CINZA,
    CINZA_CLARO,
    CINZA_ESCURO,
]

# Classe que armazena as coordenadas de um ponto
class Ponto:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

# Classe que representa um polígono formado por uma lista de pontos
class Poligono:
    def __init__(self, pontos_externos: list[Ponto], aresta:bool = False, cor:tuple = BRANCO):
        # O primeiro elemento é a borda externa. Os próximos serão os buracos
        self.contornos = [pontos_externos]
        self.aresta = aresta
        self.selecionado = False # Indica se o polígono está selecionado
        self.cor = cor # Cor do polígono
        self.atualizar_geometria() 

    def adicionar_buraco(self, pontos_buraco: list[Ponto]):
        '''Adiciona um novo contorno interno (buraco) e recalcula a matemática'''
        self.contornos.append(pontos_buraco)
        self.atualizar_geometria()

    def atualizar_geometria(self):
        '''Recalcula os limites e atabela de interseções'''
        todos_pontos = [p for contorno in self.contornos for p in contorno]
        self.y_min = min(p.y for p in todos_pontos)
        self.y_max = max(p.y for p in todos_pontos)
        self.Ns = self.y_max - self.y_min
        self.tabela_intersecoes = self.calcular_tabela_intersecoes()

    def desenhar_arestas(self, tela):

        # Verifica se terá arestas para desenhar
        if self.selecionado:
            aresta_cor = BRANCO
        elif self.aresta:
            aresta_cor = BRANCO
        else:
            return 

        # Desenha as arestas de TODOS os contornos (externo + buracos)
        for contorno in self.contornos:
            # Calculado o coeficiente angular da reta dos pontos
            for i in range(len(contorno)):
                p_atual = contorno[i]
                p_prox = contorno[(i + 1) % len(contorno)]
                
                            
                if p_atual.y < p_prox.y:
                    ponto1, ponto2 = p_atual, p_prox
                else:
                    ponto1, ponto2 = p_prox, p_atual
                
                if ponto1.y != ponto2.y:  # Evita divisão por zero
                    Tx = (ponto2.x - ponto1.x) / (ponto2.y - ponto1.y)  # Coeficiente angular

                    x = ponto1.x # Inicializa x com a coordenada x do ponto1
                    
                    # Desenha a linha entre os dois pontos
                    for y in range(ponto1.y, ponto2.y):
                        tela.set_at((int(x), y), aresta_cor)  # Desenha um pixel na posição calculada
                        x += Tx # Atualiza a coordenada x para a próxima scanline

    # calcula a tabela de interseçoes para o algoritmo de preenchimento
    #calcula para cada scalnline do poligono a lista de intersecoes x com as arestas
    def calcular_tabela_intersecoes(self):

        # Array de Ns listas vazias, uma para cada scanline 
        tabela_x = [[] for _ in range(self.Ns)]

        # Itera sobre todos os contornos para montar a tabela unificada
        for contorno in self.contornos:
            for i in range(len(contorno)):
                p_atual = contorno[i]
                p_prox = contorno[(i + 1) % len(contorno)]

                
                if p_atual.y < p_prox.y:
                    ponto1, ponto2 = p_atual, p_prox
                else:
                    ponto1, ponto2 = p_prox, p_atual

                
                if ponto1.y == ponto2.y:
                    continue

                Tx = (ponto2.x - ponto1.x) / (ponto2.y - ponto1.y)  
                x = ponto1.x

                
                for y in range(ponto1.y, ponto2.y):
                    indice_scanline = y - self.y_min
                    tabela_x[indice_scanline].append(x)
                    x += Tx

        return tabela_x

    def preencher(self, tela):
        '''Preche o interior do poligono usando o algoritmo Fillpoly.'''

        tabela_x = self.tabela_intersecoes

        for indice, lista_x in enumerate(tabela_x):
            # Ordena as interseções em ordem crescente de x
            lista_x.sort()

            y = self.y_min + indice  # y real da tela dessa scanline

            # Percorre a lista aos pares: (x_ini, x_fim), (x_ini, x_fim), ...
            for j in range(0, len(lista_x) - 1, 2):
                x_ini = math.ceil(lista_x[j]) #arredonda para cima
                x_fim = math.floor(lista_x[j + 1]) #arredonda pra bAIXO

                for x in range(x_ini, x_fim + 1):
                    tela.set_at((x, y), self.cor)

    def contem_ponto(self, ponto: Ponto) -> bool:
        '''Verifica se o ponto está dentro do polígono utilizando a tabela de interseções.'''

        tabela_x = self.tabela_intersecoes
        y_max = self.y_min + len(tabela_x) - 1

        # Se o clique foi acima ou abaixo dos limites do polígono, está fora
        if ponto.y < self.y_min or ponto.y > y_max:
            return False

        # Pega a linha exata onde o clique ocorreu
        indice = ponto.y - self.y_min
        intersecoes_x = tabela_x[indice]

        # O FillPoly precisa das interseções ordenadas para saber onde entra e sai
        intersecoes_x.sort()

        # Verifica se o ponto em x está entre os pares de entrada e saída do polígono e não está em um buraco
        for j in range(0, len(intersecoes_x) - 1, 2):
            x_ini = intersecoes_x[j]
            x_fim = intersecoes_x[j + 1]

            if x_ini <= ponto.x <= x_fim:
                return True  # O ponto está dentro do polígono

        return False  # O ponto não está dentro do polígono

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
        if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
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

class BotaoCor:
    def __init__(self, x, y, tamanho, cor):
        """Inicializa o botão de cor com suas propriedades.

        Parâmetros:
            x, y (int): Posição horizontal e vertical do botão.
            tamanho (int): Dimensão do lado do botão (quadrado).
            cor (tuple): Cor do botão em formato RGB.
        """

        self.rect = pygame.Rect(x, y, tamanho, tamanho)
        self.cor = cor

    def desenhar(self, tela):
        # Desenha o quadrado com a cor
        pygame.draw.rect(tela, self.cor, self.rect)
        # Desenha uma borda preta ao redor do botão para destacá-lo
        pygame.draw.rect(tela, PRETO, self.rect, 1)

        # Efeito de hover simples (borda mais grossa quando mouse estiver em cima)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(tela, PRETO, self.rect, 3)

    def foi_clicado(self, event):
        # Verifica se o evento foi um clique esquerdo E se ocorreu dentro do botão
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def selec_cor ():
    return random.choice(CORES)

pygame.init()


tela = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Divisão de Áreas")

painel_ui = PainelUI(850, 0, 350, 600, BRANCO)
area_desenho = AreaDesenho(0, 0, 850, 600, PRETO)

botao_arestas = Botao(900, 50, 250, 50, "Alternar Arestas", tam_fonte=30, cor=AZUL, cor_hover=AZUL_CLARO)
botao_remover = Botao(900, 400, 250, 50, "Remover Polígono", tam_fonte=30, cor=VERMELHO, cor_hover=VERMELHO_CLARO)

# ---- SETUP DAS CORES ----
botoes_cores = []
tamanho_botao = 30
espacamento = 20

# Posições iniciais baseadas no retângulo cinza
inicio_x = 885
inicio_y = 160

for i, cor in enumerate(CORES):
    colunas = 6

    linha = i // colunas   
    coluna = i % colunas   

    x = inicio_x + coluna * (tamanho_botao + espacamento)
    y = inicio_y + linha * (tamanho_botao + espacamento)

    botoes_cores.append(BotaoCor(x, y, tamanho_botao, cor))


# Criar estruturas que irão armazenar os polígonos e pontos desenhados
Pontos = [] # Lista para armazenar os pontos clicados pelo mouse
PontosBuraco = [] 
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
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # 1. Verifica se o clique foi na UI
            if (painel_ui.foi_clicado(event)):
                print("Painel de UI foi clicado!")

                # 1. Checa o botão de exibir arestas foi clicado
                if (botao_arestas.foi_clicado(event)):
                    print("Botão 'Exibe Arestas' foi clicado!")
                    tem_aresta = any(poligono.aresta for poligono in Poligonos)  # Verifica se algum polígono está com arestas exibidas
                    if (tem_aresta):
                        print("Desativando exibição das arestas dos polígonos.")
                        for poligono in Poligonos:
                            poligono.aresta = False # Alterna a exibição das arestas do polígono
                    else:
                        print("Ativando exibição das arestas dos polígonos.")
                        for poligono in Poligonos:
                            poligono.aresta = True # Alterna a exibição das arestas do polígono

                # 2. Checa os botões da paleta de cores
                for botao in botoes_cores:
                    if botao.foi_clicado(event):
                        print(f"Botão de cor {botao.cor} foi clicado!")
                        # Altera a cor dos polígonos selecionados
                        for poligono in Poligonos:
                            if poligono.selecionado:
                                poligono.cor = botao.cor
                                print(f"Polígono selecionado alterado para a cor {botao.cor}.")
                                break

                # 3. Checa o botão de remover polígono
                if (botao_remover.foi_clicado(event)):
                    print("Botão 'Remover Polígono' foi clicado!")

                    # Remove o polígono selecionado, se houver algum
                    poligono_removido = False
                    for p in Poligonos:
                        if p.selecionado:
                            Poligonos.remove(p)
                            poligono_removido = True
                            print("Polígono selecionado removido com sucesso!")
                            break # Sai do loop após remover o polígono
                    if not poligono_removido:
                        print("Nenhum polígono selecionado para remover.")

            # 2. Verifica se o clique foi na área de desenho
            if (area_desenho.foi_clicado(event)):
                print("Área de desenho foi clicada!")

                # Checa o modificador do teclado (se o CTRL está pressionado)
                mods = pygame.key.get_mods()
                ctrl_pressionado = (mods & pygame.KMOD_CTRL)
                shift_pressionado = (mods & pygame.KMOD_SHIFT) 

                # botão esquerdo = armazena o ponto.
                if event.button == 1:
                    # SELEÇÃO: Se o CTRL + botão esquerdo
                    if ctrl_pressionado:
                        print("Modo de seleção ativado!")
                        poligono_selecionado = None

                        # 1. Identifica qual polígono foi clicado (o mais acima)
                        for poligono in reversed(Poligonos):
                            if poligono.contem_ponto(Ponto(event.pos[0], event.pos[1])):
                                poligono_selecionado = poligono
                                break # Achou o alvo, para a busca

                        # 2. Aplica a exclusividade da seleção (só um polígono pode estar selecionado)
                        if poligono_selecionado:
                                # guarda o estado atual antes de resetar tudo
                                estado_anterior = poligono_selecionado.selecionado

                                # Forçamos todos para False
                                # Isso garante que apenas o polígono clicado ficará selecionado
                                for p in Poligonos:
                                    p.selecionado = False

                                # Altera o estado APENAS do polígono clicado
                                poligono_selecionado.selecionado = not estado_anterior  # Alterna o estado do polígono clicado

                                estado = "selecionado" if poligono_selecionado.selecionado else "deselecionado"
                                print(f"Polígono {estado}.")

                        else: 
                            # se clicou fora de todos os polígonos, desmarca todos
                            for p in Poligonos:
                                p.selecionado = False
                            print("Clique fora. Seleção limpa!")

                    # 2. Inserir buraco (SHIFT)
                    elif shift_pressionado:
                        # O buracodeve pertencer a alguém
                        # Verifica se existe um, e apenas um, poligono selecionado
                        alvo = next((p for p in Poligonos if p.selecionado), None)
                        if alvo:
                            PontosBuraco.append(Ponto(event.pos[0], event.pos[1]))
                            print(f"Ponto de buraco adicionado no polígono selecionado.")
                        else:
                            print("ERRO: Você precisa selecionar um polígono (CTRL+Clique) antes de desenhar um buraco.")

                    # DESENHO: Se o CTRL não estiver pressionado, adiciona o ponto normalmente
                    else:
                        # Se não estiver pressionado o CTRL, adiciona o ponto normalmente
                        PontosAux = Ponto(event.pos[0], event.pos[1])
                        Pontos.append(PontosAux)
                        print(f"Ponto adicionado: ({PontosAux.x}, {PontosAux.y})")

                # Botão direito = armazena o polígono formado pelos pontos clicados.
                elif event.button == 3:
                    # Fehar buraco
                    if shift_pressionado:
                        alvo = next((p for p in Poligonos if p.selecionado), None)
                        if alvo and len(PontosBuraco) >= 3:
                            alvo.adicionar_buraco(PontosBuraco)
                            PontosBuraco = [] # Limpa a lista
                            print("Buraco cravado no polígono")
                        else:
                            print("Sua geometria de buraco precisa de pelo menos 3 pontos e um polígono selecionado")

                    # Fechar polígono normal
                    else:
                        if len(Pontos) >= 3: # Verifica se há pelo menos 3 pontos para formar um polígono
                            tem_aresta = any(poligono.aresta for poligono in Poligonos)  # Verifica se algum polígono está com arestas exibidas

                            PoligonosAux = Poligono(Pontos, tem_aresta, selec_cor()) # Cria um novo polígono com os pontos armazenados
                            Poligonos.append(PoligonosAux)
                            Pontos = []  # Limpa a lista de pontos após criar o polígono
                            print("Polígono criado com sucesso!")

                        else:
                            print("É necessário pelo menos 3 pontos para formar um polígono.")

    # 3. FASE DE DESENHO CONTÍNUO (renderiza tudo que existe a cada frame)
    area_desenho.desenhar(tela)
    painel_ui.desenhar(tela)

    # Desenhar area para seleção de cores
    pygame.draw.rect(tela, (200, 200, 200), pygame.Rect(875, 150, 305, 200))

    # Desenha os botões na tela
    botao_arestas.desenhar(tela)

    botao_remover.desenhar(tela)

    for botao in botoes_cores:
        botao.desenhar(tela)

    # Desenha os pontos que estão sendo clicados e ainda não viraram polígonos
    for p in Pontos:
        tela.set_at((p.x, p.y), BRANCO) # Desenha um pixel branco na posição do ponto

    # FeedBack visual claro: Pontos de buracs em vermelho
    for p in PontosBuraco:
        tela.set_at((p.x, p.y), VERMELHO)

    # Desenha as arestas dos polígonos salvos
    for poligono in Poligonos:
        poligono.preencher(tela)
        poligono.desenhar_arestas(tela)

    # 4. Atualiza a tela
    pygame.display.flip()
