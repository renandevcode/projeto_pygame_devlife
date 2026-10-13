import pygame
import random

pygame.init()

janela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Meu jogo")

nave = pygame.image.load(
    "assets/img/playerShip1_orange.png"
).convert_alpha()
nave = pygame.transform.scale(nave, (60, 50))

fundo = pygame.image.load("assets/img/starfield.png").convert()
fundo = pygame.transform.scale(fundo, (800, 600))

estrelas = []
for i in range(50):
    x = random.randint(0, 799)
    y = random.randint(0, 599)
    raio = random.randint(1, 3)
    estrelas.append((x, y, raio))

vidas=3
fonte=pygame.font.Font("assets/font/PressStart2P.ttf",24)

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    janela.blit(fundo, (0, 0))
    for x,y,raio in estrelas:
        pygame.draw.circle(janela,(255,255,255),(x,y),raio)

    janela.blit(nave,(370,500))

    coracoes=chr(9829) * vidas
    texto_vidas=fonte.render(coracoes,True,(255,0,0))
    janela.blit(texto_vidas,(10,10))
    pygame.display.update()

pygame.quit()
