import random
from pathlib import Path

import pygame


LARGURA = 800
ALTURA = 600
ASSETS = Path(__file__).resolve().parent / "assets"


class Nave(pygame.sprite.Sprite):
    def __init__(self, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(topleft=(370, 500))
        self.posicao = pygame.Vector2(self.rect.topleft)
        self.velocidade = 300

    def update(self, dt):
        teclas = pygame.key.get_pressed()
        velocidade_x = 0
        velocidade_y = 0

        if teclas[pygame.K_LEFT]:
            velocidade_x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            velocidade_x += self.velocidade
        if teclas[pygame.K_UP]:
            velocidade_y -= self.velocidade
        if teclas[pygame.K_DOWN]:
            velocidade_y += self.velocidade

        # Guarda casas decimais para que o movimento não dependa do FPS.
        self.posicao.x += velocidade_x * dt
        self.posicao.y += velocidade_y * dt

        # Mantém a nave inteira dentro da janela.
        self.posicao.x = max(0, min(self.posicao.x, LARGURA - self.rect.width))
        self.posicao.y = max(0, min(self.posicao.y, ALTURA - self.rect.height))
        self.rect.topleft = (round(self.posicao.x), round(self.posicao.y))


class Meteoro(pygame.sprite.Sprite):
    def __init__(self, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect()
        self.reposicionar()

    def reposicionar(self):
        # Começa acima da janela para entrar na tela aos poucos.
        self.rect.x = random.randint(0, LARGURA - self.rect.width)
        self.posicao_y = random.randint(-ALTURA, -self.rect.height)
        self.rect.y = self.posicao_y
        self.velocidade = random.randint(100, 250)

    def update(self, dt):
        self.posicao_y += self.velocidade * dt
        self.rect.y = round(self.posicao_y)
        if self.rect.top > ALTURA:
            self.reposicionar()


class Tiro(pygame.sprite.Sprite):
    def __init__(self, imagem, posicao):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(midbottom=posicao)
        self.posicao_y = float(self.rect.y)
        self.velocidade = 500

    def update(self, dt):
        self.posicao_y -= self.velocidade * dt
        self.rect.y = round(self.posicao_y)

        # Remove tiros que já saíram completamente da janela.
        if self.rect.bottom < 0:
            self.kill()


class TelaInicial:
    def __init__(self, jogo):
        self.jogo = jogo

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            self.jogo.tela = TelaJogo(self.jogo)

    def atualizar(self, dt):
        pass

    def desenhar(self):
        self.jogo.desenhar_fundo()
        self.jogo.desenhar_texto("Meu jogo", 200)
        self.jogo.desenhar_texto("ENTER para iniciar", 300)
        self.jogo.desenhar_texto("Setas: mover | ESPACO: atirar", 370)


class TelaJogo:
    def __init__(self, jogo):
        self.jogo = jogo
        self.vidas = 3
        self.nave = Nave(jogo.imagem_nave)
        self.naves = pygame.sprite.Group(self.nave)
        self.tiros = pygame.sprite.Group()
        self.meteoros = pygame.sprite.Group()
        for _ in range(5):
            self.meteoros.add(Meteoro(jogo.imagem_meteoro))

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            tiro = Tiro(self.jogo.imagem_tiro, self.nave.rect.midtop)
            self.tiros.add(tiro)
            self.jogo.som_tiro.play()

    def atualizar(self, dt):
        self.naves.update(dt)
        self.meteoros.update(dt)
        self.tiros.update(dt)

        # Os dois True removem os tiros e os meteoros que colidiram.
        pygame.sprite.groupcollide(self.tiros, self.meteoros, True, True)

        # Cria novos meteoros acima da tela para manter a partida em andamento.
        while len(self.meteoros) < 5:
            self.meteoros.add(Meteoro(self.jogo.imagem_meteoro))

        # Mantém os sprites nos grupos para reutilizar os meteoros atingidos.
        colisoes = pygame.sprite.groupcollide(
            self.naves, self.meteoros, False, False
        )
        for meteoros_atingidos in colisoes.values():
            self.vidas = max(0, self.vidas - len(meteoros_atingidos))
            for meteoro in meteoros_atingidos:
                meteoro.reposicionar()

        if self.vidas == 0:
            self.jogo.tela = TelaGameOver(self.jogo)

    def desenhar(self):
        self.jogo.desenhar_fundo()
        self.meteoros.draw(self.jogo.janela)
        self.tiros.draw(self.jogo.janela)
        self.naves.draw(self.jogo.janela)

        coracoes = chr(9829) * self.vidas
        texto = self.jogo.fonte_vidas.render(coracoes, True, (255, 0, 0))
        self.jogo.janela.blit(texto, (10, 10))


class TelaGameOver:
    def __init__(self, jogo):
        self.jogo = jogo

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            # Uma nova tela cria uma partida com três vidas e novos meteoros.
            self.jogo.tela = TelaJogo(self.jogo)

    def atualizar(self, dt):
        pass

    def desenhar(self):
        self.jogo.desenhar_fundo()
        self.jogo.desenhar_texto("GAME OVER", 240)
        self.jogo.desenhar_texto("ENTER para recomecar", 330)


class Jogo:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Meu jogo")
        self.relogio = pygame.time.Clock()
        self.rodando = True

        self.imagem_nave = pygame.image.load(
            str(ASSETS / "img/playerShip1_orange.png")
        ).convert_alpha()
        self.imagem_nave = pygame.transform.scale(self.imagem_nave, (60, 50))
        self.imagem_meteoro = pygame.image.load(
            str(ASSETS / "img/meteorBrown_med1.png")
        ).convert_alpha()
        self.imagem_meteoro = pygame.transform.scale(self.imagem_meteoro, (50, 40))
        self.imagem_tiro = pygame.image.load(
            str(ASSETS / "img/laserRed16.png")
        ).convert_alpha()
        self.fundo = pygame.image.load(str(ASSETS / "img/starfield.png")).convert()
        self.fundo = pygame.transform.scale(self.fundo, (LARGURA, ALTURA))

        self.estrelas = []
        for _ in range(50):
            x = random.randint(0, LARGURA - 1)
            y = random.randint(0, ALTURA - 1)
            raio = random.randint(1, 3)
            self.estrelas.append((x, y, raio))

        fonte = str(ASSETS / "font/PressStart2P.ttf")
        self.fonte_vidas = pygame.font.Font(fonte, 24)
        self.fonte_texto = pygame.font.Font(fonte, 16)
        self.som_tiro = pygame.mixer.Sound(str(ASSETS / "snd/pew.wav"))
        pygame.mixer.music.load(
            str(ASSETS / "snd/tgfcoder-FrozenJam-SeamlessLoop.ogg")
        )
        # A música continua tocando durante as trocas de tela.
        pygame.mixer.music.play(-1)
        self.tela = TelaInicial(self)

    def desenhar_fundo(self):
        self.janela.blit(self.fundo, (0, 0))
        for x, y, raio in self.estrelas:
            pygame.draw.circle(self.janela, (255, 255, 255), (x, y), raio)

    def desenhar_texto(self, mensagem, y):
        texto = self.fonte_texto.render(mensagem, True, (255, 255, 255))
        posicao = texto.get_rect(center=(LARGURA // 2, y))
        self.janela.blit(texto, posicao)

    def desenhar_fps(self):
        fps = self.relogio.get_fps()
        texto = self.fonte_texto.render(f"FPS: {fps:.0f}", True, (255, 255, 255))
        # Mantém uma margem de 10 pixels das bordas direita e inferior.
        posicao = texto.get_rect(bottomright=(LARGURA - 10, ALTURA - 10))
        self.janela.blit(texto, posicao)

    def executar(self):
        try:
            while self.rodando:
                # Limita a 60 FPS e converte o tempo decorrido para segundos.
                dt = self.relogio.tick(60) / 1000
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.rodando = False
                        break
                    self.tela.tratar_evento(evento)

                if not self.rodando:
                    break

                self.tela.atualizar(dt)
                self.tela.desenhar()
                self.desenhar_fps()
                pygame.display.update()
        finally:
            pygame.quit()


if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
