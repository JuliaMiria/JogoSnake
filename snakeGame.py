import pygame, random
import os
import sys

pygame.init()


# para todos os arquivos irem no .exe sem precisar mandar a pasta inteira
def caminhoArquivo(nome):
    if getattr(sys, 'frozen', False):
        pasta = sys._MEIPASS
    else:
        pasta = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pasta, nome)



# criar a janela
tempo = pygame.time.Clock()
largura = 800
altura = 600
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jumi Snake")
pontos = 0

# direção inicial
direcao = "direita"
# proxima direção que o jogador escolheu
proximaDirecao = "direita"

# carregando imagens e sons
imagemFundo = pygame.image.load(caminhoArquivo("fundo.png"))
imagemFundoRedimensionada = pygame.transform.scale(imagemFundo, (largura, altura))

imagemFruta = pygame.image.load(caminhoArquivo('morango.png'))
imagemFrutaRedimensionada = pygame.transform.scale(imagemFruta, (15, 15))

imagemCorpo = pygame.image.load(caminhoArquivo('corpoBloco.png'))
imagemCorpoRedimensionada = pygame.transform.scale(imagemCorpo, (30, 30))

imagemCabecaDireita = pygame.image.load(caminhoArquivo("cabeca_direita.png"))
imagemCabecaDireitaRedimensionada = pygame.transform.scale(imagemCabecaDireita, (40, 40))

imagemCabecaEsquerda = pygame.image.load(caminhoArquivo("cabeca_esquerda.png"))
imagemCabecaEsquerdaRedimensionada = pygame.transform.scale(imagemCabecaEsquerda, (40, 40))

imagemCabecaCima = pygame.image.load(caminhoArquivo("cabeca_cima.png"))
imagemCabecaCimaRedimensionada = pygame.transform.scale(imagemCabecaCima, (40, 40))

imagemCabecaBaixo = pygame.image.load(caminhoArquivo("cabeca_baixo.png"))
imagemCabecaBaixoRedimensionada = pygame.transform.scale(imagemCabecaBaixo, (40, 40))

pygame.mixer.init()
somComer = pygame.mixer.Sound(caminhoArquivo('mordida.mp3'))
somGameOver = pygame.mixer.Sound(caminhoArquivo('gameOver.mp3'))

# musica de fundo
pygame.mixer.music.load(caminhoArquivo('musica.mp3'))
pygame.mixer.music.play(-1)

# criar a cabeça da cobrinha
tamanhoCabecaX = 40
tamanhoCabecaY = 40

posicaoX = largura // 2
posicaoY = altura // 2
velocidade = 20

# cada posiçao da lista representa uma partee da cobra
cobra = [[posicaoX, posicaoY]]



def criarFruta():
    # funcao para criar a fruta na tela aleatoriamente
    # o -20 evita que a fruta fica parcialmente para fora
    x = random.randint(0, largura - 20)
    y = random.randint(0, altura -20)

    return [x, y]
posicaoFrutaX, posicaoFrutaY = criarFruta()
    
fonte = pygame.font.SysFont(None, 32)

# pontuacao
def pontuacao():
    text = fonte.render(f'Pontos: {pontos}', True, (255, 255, 255))
    janela.blit(text, (10, 10))

# desenhando a cobrinha
def desenharCobra():
    if direcao == "direita":
        cabeca = imagemCabecaDireitaRedimensionada
    elif direcao == "esquerda":
        cabeca = imagemCabecaEsquerdaRedimensionada
    elif direcao == "cima":
        cabeca = imagemCabecaCimaRedimensionada
    elif direcao == "baixo":
        cabeca = imagemCabecaBaixoRedimensionada

    # cabeca
    janela.blit(cabeca, (cobra[0][0], cobra[0][1]))
    # corpo
    for parte in cobra[1:]:
        janela.blit(imagemCorpoRedimensionada, (parte[0], parte[1]))

def moverCobra():
    # descobrir onde esta a cabeça nesse momento
    x = cobra[0][0]
    y = cobra[0][1]

    # alteramos a posicao dependendo da direcao
    if direcao == "cima":
        y -= velocidade
    elif direcao == "baixo":
        y += velocidade
    elif direcao == "esquerda":
        x -= velocidade
    elif direcao == "direita":
        x += velocidade

    novaCabeca = [x, y]
    cobra.insert(0, novaCabeca)

    if not comeuFruta:
        cobra.pop()

def verificarColissao():
    global posicaoFrutaX
    global posicaoFrutaY
    global pontos
    global comeuFruta

    cabecaX = cobra[0][0]
    cabecaY = cobra[0][1]

    # criando retangulos para verificar se os objetos estao encostando
    retanguloCabeca = pygame.Rect(cabecaX, cabecaY, 40, 40)
    retanguloFruta = pygame.Rect(posicaoFrutaX, posicaoFrutaY, 20, 20)

    if retanguloCabeca.colliderect(retanguloFruta):
        comeuFruta = True
        pontos += 1

        posicaoFrutaX, posicaoFrutaY = criarFruta()

        somComer.play()


# colisao nas paredes
def bateuParede():
        x = cobra[0][0]
        y = cobra[0][1]

        if x < 0:
            return True
        if x + 40 > largura:
            return True
        if y < 0:
            return True
        if y + 40 > altura:
            return True
        return False

# se a cobra bater no proprio corpo
def bateuProprioCorpo():
    cabeca = cobra[0]

    for parte in cobra[1:]:
        if cabeca == parte:
            return True
    return False

# tela game Over
def gameOver():
    janela.blit(imagemFundoRedimensionada, (0, 0))

    fonteGrande = pygame.font.SysFont(None, 70)

    textoGameOver = fonteGrande.render("GAME OVER", True, (255, 0, 0))

    janela.blit(textoGameOver, (largura / 3, altura / 2))

    pygame.display.update()

continuar = True
fimDeJogo = False

while continuar:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            continuar = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
               if direcao != "baixo":
                   proximaDirecao = "cima"
            elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                if direcao != "cima":
                   proximaDirecao = "baixo"
            elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                if direcao != "esquerda":
                   proximaDirecao = "direita"
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                if direcao != "direita":
                   proximaDirecao = "esquerda"
    
    if fimDeJogo:
        gameOver()
        tempo.tick(15)
        continue

    direcao = proximaDirecao

    comeuFruta = False
    verificarColissao()
    moverCobra()

    if bateuParede():
        fimDeJogo = True
        somGameOver.play()
    if bateuProprioCorpo():
        fimDeJogo = True
        somGameOver.play()
    
    janela.blit(imagemFundoRedimensionada, (0, 0))
    janela.blit(imagemFrutaRedimensionada, (posicaoFrutaX, posicaoFrutaY))
    desenharCobra()
    pontuacao()
    pygame.display.update()

    tempo.tick(10)


pygame.quit()
