import math
import random
import pygame

# ============================================================
# CORES
# ============================================================

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

# Paleta exibida ao usuário para trocar a cor de preenchimento do polígono selecionado
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


# ============================================================
# MODELOS GEOMÉTRICOS (Ponto, Polígono, algoritmo fillpoly)
# ============================================================

class Ponto:
    '''Representa uma coordenada (x, y) no sistema de referência da tela (SRT).

    Parâmetros:
        x (int): Coordenada horizontal.
        y (int): Coordenada vertical.
    '''

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Poligono:
    '''Representa um polígono desenhado pelo usuário, com possíveis buracos.

    O polígono é armazenado como uma lista de contornos: o primeiro elemento
    de `contornos` é sempre o contorno externo, e os demais (se existirem)
    são os buracos. Todos os contornos entram juntos na mesma tabela de
    interseções do fillpoly, o que faz a regra par-ímpar do algoritmo
    resolver buracos e autointerseção automaticamente, sem lógica extra.

    Parâmetros:
        pontos_externos (list[Ponto]): Vértices do contorno externo, na ordem
            em que foram clicados.
        aresta (bool): Se True, as arestas do polígono são desenhadas em branco.
        cor (tuple): Cor RGB de preenchimento do polígono.
    '''

    def __init__(self, pontos_externos: list[Ponto], aresta: bool = False, cor: tuple = BRANCO):
        self.contornos = [pontos_externos]  # [0] = contorno externo; [1:] = buracos
        self.aresta = aresta
        self.selecionado = False  # Indica se o polígono está selecionado
        self.cor = cor  # Cor de preenchimento do polígono
        self.atualizar_geometria()

    def adicionar_buraco(self, pontos_buraco: list[Ponto]):
        '''Adiciona um novo contorno interno (buraco) e recalcula a geometria.'''
        self.contornos.append(pontos_buraco)
        self.atualizar_geometria()

    def atualizar_geometria(self):
        '''Recalcula os limites verticais (y_min, y_max) e a tabela de interseções.

        Precisa ser chamado sempre que um contorno for adicionado ou alterado,
        já que a tabela de interseções é cacheada em `self.tabela_intersecoes`.
        '''
        todos_pontos = [p for contorno in self.contornos for p in contorno]
        self.y_min = min(p.y for p in todos_pontos)
        self.y_max = max(p.y for p in todos_pontos)
        self.Ns = self.y_max - self.y_min
        self.tabela_intersecoes = self.calcular_tabela_intersecoes()

    def calcular_tabela_intersecoes(self):
        '''Calcula, para cada scanline do polígono, a lista de interseções x
        com as arestas de todos os contornos (externo + buracos), usando
        aritmética incremental (Tx = dx/dy).
        '''
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
                    continue  # Aresta horizontal: não é processada

                Tx = (ponto2.x - ponto1.x) / (ponto2.y - ponto1.y)
                x = ponto1.x

                # Processa de ymin até (ymax - 1), como especificado nos slides
                for y in range(ponto1.y, ponto2.y):
                    indice_scanline = y - self.y_min
                    tabela_x[indice_scanline].append(x)
                    x += Tx

        return tabela_x

    def preencher(self, tela):
        '''Preenche o interior do polígono usando o algoritmo fillpoly.'''
        tabela_x = self.tabela_intersecoes

        for indice, lista_x in enumerate(tabela_x):
            # Ordena as interseções em ordem crescente de x
            lista_x.sort()

            y = self.y_min + indice  # y real da tela para essa scanline

            # Percorre a lista aos pares: (x_ini, x_fim), (x_ini, x_fim), ...
            for j in range(0, len(lista_x) - 1, 2):
                x_ini = math.ceil(lista_x[j])    # arredonda para cima
                x_fim = math.floor(lista_x[j + 1])  # arredonda para baixo

                for x in range(x_ini, x_fim + 1):
                    tela.set_at((x, y), self.cor)

    def desenhar_arestas(self, tela):
        '''Desenha, em branco, as arestas de todos os contornos (externo + buracos),
        caso o polígono esteja selecionado ou com a exibição de arestas ativada.
        '''
        if self.selecionado or self.aresta:
            aresta_cor = BRANCO
        else:
            return

        for contorno in self.contornos:
            for i in range(len(contorno)):
                p_atual = contorno[i]
                p_prox = contorno[(i + 1) % len(contorno)]

                if p_atual.y < p_prox.y:
                    ponto1, ponto2 = p_atual, p_prox
                else:
                    ponto1, ponto2 = p_prox, p_atual

                if ponto1.y == ponto2.y:
                    continue  # Aresta horizontal: não é desenhada por aqui

                Tx = (ponto2.x - ponto1.x) / (ponto2.y - ponto1.y)
                x = ponto1.x

                for y in range(ponto1.y, ponto2.y):
                    tela.set_at((int(x), y), aresta_cor)
                    x += Tx

    def contem_ponto(self, ponto: Ponto) -> bool:
        '''Testa se `ponto` está na região interna do polígono, reaproveitando
        a mesma tabela de interseções do fillpoly (regra par-ímpar). Pontos
        dentro de um buraco retornam False automaticamente, sem lógica extra.
        '''
        tabela_x = self.tabela_intersecoes
        y_max = self.y_min + len(tabela_x) - 1

        # Se o clique foi acima ou abaixo dos limites do polígono, está fora
        if ponto.y < self.y_min or ponto.y > y_max:
            return False

        # Pega a linha exata onde o clique ocorreu
        indice = ponto.y - self.y_min
        intersecoes_x = tabela_x[indice]

        # O fillpoly precisa das interseções ordenadas para saber onde entra e sai
        intersecoes_x.sort()

        for j in range(0, len(intersecoes_x) - 1, 2):
            x_ini = intersecoes_x[j]
            x_fim = intersecoes_x[j + 1]

            if x_ini <= ponto.x <= x_fim:
                return True  # Ponto está dentro do polígono (ou fora de um buraco)

        return False  # Ponto está fora do polígono (ou dentro de um buraco)


# ============================================================
# COMPONENTES DE INTERFACE (painel, botões, área de desenho)
# ============================================================

class PainelUI:
    '''Painel lateral que agrupa os controles (botões, paleta de cores).

    Parâmetros:
        x, y (int): Posição horizontal e vertical do painel.
        largura (int): Dimensão de largura do painel.
        altura (int): Dimensão de altura do painel.
        cor_fundo (tuple): Cor de fundo do painel em formato RGB.
    '''

    def __init__(self, x, y, largura, altura, cor_fundo=BRANCO):
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
    '''Área onde o usuário desenha e seleciona polígonos com o mouse.

    Parâmetros:
        x, y (int): Posição horizontal e vertical da área de desenho.
        largura (int): Dimensão de largura da área de desenho.
        altura (int): Dimensão de altura da área de desenho.
        cor_fundo (tuple): Cor de fundo da área de desenho em formato RGB.
    '''

    def __init__(self, x, y, largura, altura, cor_fundo=PRETO):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_fundo = cor_fundo

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor_fundo, self.rect)

    def foi_clicado(self, event):
        # Verifica se o evento foi um clique esquerdo ou direito dentro da área de desenho
        if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Botao:
    '''Botão retangular clicável com texto e efeito de hover.

    Parâmetros:
        x, y (int): Posição horizontal e vertical do botão.
        largura (int): Dimensão de largura do botão.
        altura (int): Dimensão de altura do botão.
        texto (str): Texto a ser exibido no botão.
        tam_fonte (int): Tamanho da fonte do texto.
        cor_fonte (tuple): Cor do texto em formato RGB.
        cor (tuple): Cor padrão do fundo do botão.
        cor_hover (tuple): Cor do botão quando o mouse está sobre ele.
    '''

    def __init__(self, x, y, largura, altura, texto, tam_fonte=36, cor_fonte=BRANCO, cor=AZUL, cor_hover=AZUL_CLARO):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.fonte = pygame.font.Font(None, tam_fonte)
        self.cor_fonte = cor_fonte
        self.cor = cor
        self.cor_hover = cor_hover

    def desenhar(self, tela):
        # Captura a posição atual do mouse para o efeito de "hover" (passar o mouse por cima)
        mouse_pos = pygame.mouse.get_pos()

        cor_atual = self.cor_hover if self.rect.collidepoint(mouse_pos) else self.cor

        pygame.draw.rect(tela, cor_atual, self.rect, border_radius=8)

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
    '''Quadrado clicável de uma cor da paleta, usado para trocar a cor
    de preenchimento do polígono selecionado.

    Parâmetros:
        x, y (int): Posição horizontal e vertical do botão.
        tamanho (int): Dimensão do lado do botão (quadrado).
        cor (tuple): Cor do botão em formato RGB.
    '''

    def __init__(self, x, y, tamanho, cor):
        self.rect = pygame.Rect(x, y, tamanho, tamanho)
        self.cor = cor

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)
        pygame.draw.rect(tela, PRETO, self.rect, 1)  # borda para destacar o botão

        # Efeito de hover simples (borda mais grossa quando o mouse está em cima)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(tela, PRETO, self.rect, 3)

    def foi_clicado(self, event):
        # Verifica se o evento foi um clique esquerdo E se ocorreu dentro do botão
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


def selecionar_cor_aleatoria():
    '''Sorteia uma cor da paleta — usada como cor inicial de um polígono recém-criado.'''
    return random.choice(CORES)


# ============================================================
# SETUP
# ============================================================

pygame.init()

tela = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("FillPoly Monolítico")

painel_ui = PainelUI(850, 0, 350, 600, BRANCO)
area_desenho = AreaDesenho(0, 0, 850, 600, PRETO)

botao_arestas = Botao(900, 50, 250, 50, "Alternar Arestas", tam_fonte=30, cor=AZUL, cor_hover=AZUL_CLARO)
botao_remover = Botao(900, 400, 250, 50, "Remover Polígono", tam_fonte=30, cor=VERMELHO, cor_hover=VERMELHO_CLARO)

# ---- Paleta de cores ----
# Moldura cinza de fundo da paleta (desenhada no loop principal) e a grade de
# botões de cor compartilham a mesma área visual — mantidas como constantes
# nomeadas aqui para não desalinhar se alguém ajustar só uma das duas.
PALETA_X = 875
PALETA_Y = 150
PALETA_LARGURA = 305
PALETA_ALTURA = 200
MOLDURA_PALETA = (200, 200, 200)  # cor de fundo da moldura (igual ao original)

tamanho_botao = 30
espacamento = 20
colunas_paleta = 6

# Posições da grade com uma margem de 10px em relação à moldura
inicio_x = PALETA_X + 10
inicio_y = PALETA_Y + 10

botoes_cores = []
for i, cor in enumerate(CORES):
    linha = i // colunas_paleta
    coluna = i % colunas_paleta

    x = inicio_x + coluna * (tamanho_botao + espacamento)
    y = inicio_y + linha * (tamanho_botao + espacamento)

    botoes_cores.append(BotaoCor(x, y, tamanho_botao, cor))

# Estruturas que armazenam os polígonos e pontos desenhados
pontos = []          # Pontos clicados pelo mouse, ainda não fechados em um polígono
pontos_buraco = []   # Pontos clicados pelo mouse, ainda não fechados em um buraco
poligonos = []       # Polígonos já criados


# ============================================================
# LOOP PRINCIPAL
# ============================================================

rodando = True
while rodando:
    # 1. Limpa a tela
    tela.fill(PRETO)

    # 2. Processa os eventos de input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            # --- Clique na UI (painel lateral) ---
            if painel_ui.foi_clicado(event):
                print("Painel de UI foi clicado!")

                # Botão "Alternar Arestas"
                if botao_arestas.foi_clicado(event):
                    print("Botão 'Alternar Arestas' foi clicado!")
                    tem_aresta = any(poligono.aresta for poligono in poligonos)
                    if tem_aresta:
                        print("Desativando exibição das arestas dos polígonos.")
                        for poligono in poligonos:
                            poligono.aresta = False
                    else:
                        print("Ativando exibição das arestas dos polígonos.")
                        for poligono in poligonos:
                            poligono.aresta = True

                # Botões da paleta de cores
                for botao in botoes_cores:
                    if botao.foi_clicado(event):
                        print(f"Botão de cor {botao.cor} foi clicado!")
                        # Altera a cor do polígono selecionado
                        for poligono in poligonos:
                            if poligono.selecionado:
                                poligono.cor = botao.cor
                                print(f"Polígono selecionado alterado para a cor {botao.cor}.")
                                break

                # Botão "Remover Polígono"
                if botao_remover.foi_clicado(event):
                    print("Botão 'Remover Polígono' foi clicado!")
                    poligono_removido = False
                    for p in poligonos:
                        if p.selecionado:
                            poligonos.remove(p)
                            poligono_removido = True
                            print("Polígono selecionado removido com sucesso!")
                            break
                    if not poligono_removido:
                        print("Nenhum polígono selecionado para remover.")

            # --- Clique na área de desenho ---
            if area_desenho.foi_clicado(event):
                print("Área de desenho foi clicada!")

                mods = pygame.key.get_mods()
                ctrl_pressionado = mods & pygame.KMOD_CTRL
                shift_pressionado = mods & pygame.KMOD_SHIFT

                if event.button == 1:
                    # SELEÇÃO: CTRL + botão esquerdo
                    if ctrl_pressionado:
                        print("Modo de seleção ativado!")
                        ponto_clicado = Ponto(event.pos[0], event.pos[1])
                        poligono_clicado = None

                        # Identifica qual polígono foi clicado (o mais acima, topo da pilha)
                        for poligono in reversed(poligonos):
                            if poligono.contem_ponto(ponto_clicado):
                                poligono_clicado = poligono
                                break

                        if poligono_clicado:
                            # Alterna a seleção do polígono clicado, garantindo que
                            # apenas um polígono fique selecionado por vez
                            estado_anterior = poligono_clicado.selecionado
                            for p in poligonos:
                                p.selecionado = False
                            poligono_clicado.selecionado = not estado_anterior

                            estado = "selecionado" if poligono_clicado.selecionado else "deselecionado"
                            print(f"Polígono {estado}.")
                        else:
                            # Clique fora de qualquer polígono: limpa a seleção
                            for p in poligonos:
                                p.selecionado = False
                            print("Clique fora. Seleção limpa!")

                    # BURACO: SHIFT + botão esquerdo adiciona um ponto de buraco
                    elif shift_pressionado:
                        alvo = next((p for p in poligonos if p.selecionado), None)
                        if alvo:
                            pontos_buraco.append(Ponto(event.pos[0], event.pos[1]))
                            print("Ponto de buraco adicionado no polígono selecionado.")
                        else:
                            print("ERRO: selecione um polígono (CTRL+clique) antes de desenhar um buraco.")

                    # DESENHO: clique simples adiciona um vértice ao polígono em construção
                    else:
                        novo_ponto = Ponto(event.pos[0], event.pos[1])
                        pontos.append(novo_ponto)
                        print(f"Ponto adicionado: ({novo_ponto.x}, {novo_ponto.y})")

                elif event.button == 3:
                    # SHIFT + botão direito: fecha o buraco em construção
                    if shift_pressionado:
                        alvo = next((p for p in poligonos if p.selecionado), None)
                        if alvo and len(pontos_buraco) >= 3:
                            alvo.adicionar_buraco(pontos_buraco)
                            pontos_buraco = []
                            print("Buraco adicionado ao polígono selecionado.")
                        else:
                            print("O buraco precisa de pelo menos 3 pontos e um polígono selecionado.")

                    # Botão direito simples: fecha o polígono em construção
                    else:
                        if len(pontos) >= 3:
                            tem_aresta = any(poligono.aresta for poligono in poligonos)
                            novo_poligono = Poligono(pontos, tem_aresta, selecionar_cor_aleatoria())
                            poligonos.append(novo_poligono)
                            pontos = []
                            print("Polígono criado com sucesso!")
                        else:
                            print("É necessário pelo menos 3 pontos para formar um polígono.")

    # 3. FASE DE DESENHO CONTÍNUO (renderiza tudo que existe a cada frame)
    area_desenho.desenhar(tela)
    painel_ui.desenhar(tela)

    # Moldura de fundo da paleta de cores
    pygame.draw.rect(tela, MOLDURA_PALETA, pygame.Rect(PALETA_X, PALETA_Y, PALETA_LARGURA, PALETA_ALTURA))

    botao_arestas.desenhar(tela)
    botao_remover.desenhar(tela)

    for botao in botoes_cores:
        botao.desenhar(tela)

    # Polígonos já criados: preenchimento + arestas
    for poligono in poligonos:
        poligono.preencher(tela)
        poligono.desenhar_arestas(tela)

    # Pontos do polígono em construção (ainda não fechado)
    for p in pontos:
        tela.set_at((p.x, p.y), BRANCO)

    # Pontos do buraco em construção (feedback visual em vermelho)
    for p in pontos_buraco:
        tela.set_at((p.x, p.y), VERMELHO)

    # 4. Atualiza a tela
    pygame.display.flip()