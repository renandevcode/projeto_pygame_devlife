import pygame
import random

pygame.init()

janela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Meu jogo")

nave = pygame.image.load(
    "assets/img/playerShip1_orange.png"
).convert_alpha()
nave = pygame.transform.scale(nave, (60, 50))

fundo = pygame.image.load(
    "assets/img/starfield.png").convert()
fundo = pygame.transform.scale(fundo, (800, 600))

estrelas = []
for i in range(50):
    x = random.randint(0, 799)
    y = random.randint(0, 599)
    raio = random.randint(1, 3)
    estrelas.append((x, y, raio))

vidas=3
fonte=pygame.font.Font("assets/font/PressStart2P.ttf",24)

relogio=pygame.time.Clock()
fonte_fps=pygame.font.Font("assets/font/PressStart2P.ttf",16)

nave_x = 370
nave_y = 500
velocidade = 300  

imagem_meteoro = pygame.image.load(
    "assets/img/meteorBrown_med1.png").convert_alpha()
imagem_meteoro = pygame.transform.scale(imagem_meteoro, (50, 40))
meteoros = []
for i in range(5):
    meteoro = {
        "x": random.randint(0, 750),
        "y": random.randint(-600, -40),
        "velocidade": random.randint(100, 250),
    }
    meteoros.append(meteoro)

rodando = True
while rodando:
    # Converte o tempo entre quadros de milissegundos para segundos
    dt = relogio.tick(60) / 1000

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    velocidade_x = 0
    velocidade_y = 0

    if teclas[pygame.K_LEFT]:
        velocidade_x -= velocidade
    if teclas[pygame.K_RIGHT]:
        velocidade_x += velocidade
    if teclas[pygame.K_UP]:
        velocidade_y -= velocidade
    if teclas[pygame.K_DOWN]:
        velocidade_y += velocidade

    # Usa o tempo decorrido para manter o movimento independente do FPS.
    nave_x += velocidade_x * dt
    nave_y += velocidade_y * dt

    # Mantém a nave inteira dentro da janela.
    nave_x = max(0, min(nave_x, 800 - nave.get_width()))
    nave_y = max(0, min(nave_y, 600 - nave.get_height()))

    retangulo_nave = nave.get_rect(
        topleft=(round(nave_x), round(nave_y))
    )

    for meteoro in meteoros:
        meteoro["y"] += meteoro["velocidade"] * dt

        retangulo_meteoro = imagem_meteoro.get_rect(
            topleft=(round(meteoro["x"]), round(meteoro["y"]))
        )

        colidiu = retangulo_nave.colliderect(retangulo_meteoro)

        if colidiu:
            vidas -= 1
            if vidas <= 0:
                rodando = False
                break

        # Reposiciona o meteoro após uma colisão ou ao sair da tela.
        if colidiu or meteoro["y"] > 600:
            meteoro["x"] = random.randint(0, 750)
            meteoro["y"] = random.randint(-600, -40)
            meteoro["velocidade"] = random.randint(100, 250)

    janela.blit(fundo, (0, 0))
    for x,y,raio in estrelas:
        pygame.draw.circle(janela,(255,255,255),(x,y),raio)

    for meteoro in meteoros:
        janela.blit(
            imagem_meteoro,(round(meteoro["x"]), round(meteoro["y"])))
    janela.blit(nave,(round(nave_x),round(nave_y)))

    coracoes=chr(9829) * vidas
    texto_vidas=fonte.render(coracoes,True,(255,0,0))
    janela.blit(texto_vidas,(10,10))

    fps = relogio.get_fps()
    texto_fps = fonte_fps.render(f"FPS: {fps:.0f}", True, (255, 255, 255))

    posicao_fps = texto_fps.get_rect()
    # Mantém uma margem de 10 pixels das bordas direita e inferior.
    posicao_fps.bottomright = (790, 590)

    janela.blit(texto_fps, posicao_fps)
    pygame.display.update()

pygame.quit()
