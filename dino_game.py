import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice

pygame.init()
pygame.mixer.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal,"imagens")
diretorio_sons = os.path.join(diretorio_principal,"sons")

pygame.init()

largura = 640
altura = 480

branco = (255,255,255)

tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Dino game")

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons,"death_sound.wav"))
som_colisao.set_volume(1)

som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons , "score_sound.wav"))
som_pontuacao.set_volume(1)

#pode_tocar_o_som_do_pulo = True
colidiu = False

spritesheet = pygame.image.load(os.path.join(diretorio_imagens,"dinoSpritesheet.png")).convert_alpha()


escolha_obstaculo = choice([0,1])

pontos = 0
velocidade_jogo = 15

def exibe_mensagem(mensagem , tamanho , cor):
    fonte = pygame.font.SysFont('lucidasans',tamanho, True , False)
    msg = f'{mensagem}'
    texto_formatado = fonte.render(msg , True , cor)
    return texto_formatado

def reiniciar_jogo():
    global pontos,velocidade_jogo,colidiu,escolha_obstaculo
    dino_voador.rect.x = largura
    cacto.rect.x = largura
    colidiu = False
    pontos = 0
    velocidade_jogo = 15
    #pode_tocar_o_som_do_pulo = True
    escolha_obstaculo = choice([0, 1])
    dino.pulo = False
    dino.rect.y = altura-64-(96//2)

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, "jump_sound.wav"))
        self.som_pulo.set_volume(1)
        self.imagens_dinossauro = []
        for i in range(3):
            img = spritesheet.subsurface((i*32,0),(32,32))
            img = pygame.transform.scale(img,(32*3,32*3))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = altura-64-(96//2)
        self.rect.center = (100,self.pos_y_inicial)
        self.pulo = False

    def update(self):
        if self.index_lista > 2:
            self.index_lista = 0

        self.index_lista += 0.25
        self.image = self.imagens_dinossauro[int(self.index_lista)]

        if self.pulo == True:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 20
        else :
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 20
            else:
                self.rect.y = self.pos_y_inicial

    def pular(self):
        self.pulo = True
        self.som_pulo.play()


class Nuvem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.subsurface((7*32,0),(32,32))
        self.image = pygame.transform.scale(self.image , (3*32,3*32))
        self.rect = self.image.get_rect()
        #self.rect.center = (100,100)
        self.rect.y = randrange(50,200,50)
        self.rect.x = largura + randrange(30,300,90)
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura + randrange(30,300,90)
            self.rect.y = randrange(50, 200, 50)
        else:
            self.rect.x -= 10

class Chao(pygame.sprite.Sprite):
    def __init__(self,pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.subsurface((6*32,0),(32,32))
        self.image = pygame.transform.scale(self.image , (2*32,2*32))
        self.rect = self.image.get_rect()
        self.rect.y = altura - 64
        self.rect.x = pos_x * 64
    def update(self):
        if self.rect.topright[0] < -10:
            self.rect.x = largura + 10
        else:
            self.rect.x -= velocidade_jogo

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.subsurface((5*32,0),(32,32))
        self.image = pygame.transform.scale(self.image , (2*32,2*32))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (largura,altura-64)
        self.escolha = escolha_obstaculo
        self.rect.x = largura

    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            else:
                self.rect.x -= velocidade_jogo

class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dinossauro = []
        for i in range(3,5):
            img = spritesheet.subsurface((i*32,0), (32,32))
            img = pygame.transform.scale(img , (32*3 , 32*3))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (largura , 330)
        self.escolha = escolha_obstaculo
        self.rect.x = largura

    def update(self):
        if self.escolha == 0 :
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            else:
                self.rect.x -= velocidade_jogo


            if self.index_lista > 1:
                self.index_lista = 0
            else:
                self.index_lista += 0.25
                self.image = self.imagens_dinossauro[int(self.index_lista)]

todas_as_sprites = pygame.sprite.Group()
dino = Dino()
todas_as_sprites.add(dino)

for i in range(4):
    nuvem = Nuvem()
    todas_as_sprites.add(nuvem)

for i in range(640//10):
    chao = Chao(i)
    todas_as_sprites.add(chao)

cacto = Cacto()
todas_as_sprites.add(cacto)

grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(cacto)

dino_voador = DinoVoador()
grupo_obstaculos.add(dino_voador)
todas_as_sprites.add(dino_voador)

relogio = pygame.time.Clock()

while True:
    relogio.tick(30)
    tela.fill(branco)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and colidiu==False:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()

            if event.key == K_r and colidiu == True:
                reiniciar_jogo()

    colisoes = pygame.sprite.spritecollide(dino , grupo_obstaculos , False , pygame.sprite.collide_mask)

    todas_as_sprites.draw(tela)

    if cacto.rect.topright[0] <= 0 or dino_voador.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0,1])
        cacto.rect.x = largura
        dino_voador.rect.x = largura
        cacto.escolha = escolha_obstaculo
        dino_voador.escolha = escolha_obstaculo

    if colisoes and colidiu==False:
        som_colisao.play()
        colidiu = True
        pode_tocar_o_som_do_pulo = False

    if colidiu == True:
        if pontos%100 == 0:
            pontos+=1

        game_over = exibe_mensagem('GAME OVER',36,(0,0,0))
        tela.blit(game_over,( (largura/2) - 120 , (altura/2) ) )

        restart = exibe_mensagem('Pressione R para reiniciar',18,(0,0,0))
        tela.blit(restart , ((largura/2) - 120 , (altura/2) + 44))

    else:
        todas_as_sprites.update()
        pontos += 1
        texto_pontos = exibe_mensagem(pontos , 36 , (0,0,0))

    if pontos%100 == 0:
        som_pontuacao.play()
        if velocidade_jogo >= 30:
            velocidade_jogo += 0
        else:
            velocidade_jogo += 2


    tela.blit( texto_pontos , (520,30))
    pygame.display.flip()