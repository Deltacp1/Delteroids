#jogo Espacial
#Um grupo de fogueteiros escapa de uma fortaleza estelar a bordo de sua nave danificada.
#Desvie dos obstaculos até chegar em segurança na LASC.

import pygame
import time
import random
import os
import sys


class Background:

    image = None
    margin_left = None
    margin_right = None

    def __init__(self):
        background_fig = pygame.image.load("Images/background.png")       #define a imagem pelo diretorio
        background_fig.convert()
        background_fig = pygame.transform.scale(background_fig, (800, 602))
        self.image = background_fig

        margin_left_fig = pygame.image.load("Images/margin_1.png")
        margin_left_fig.convert()
        margin_left_fig = pygame.transform.scale(margin_left_fig, (60, 602))
        self.margin_left = margin_left_fig

        margin_right_fig = pygame.image.load("Images/margin_2.png")
        margin_right_fig.convert()
        margin_right_fig = pygame.transform.scale(margin_right_fig, (60, 602))
        self.margin_right = margin_right_fig

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        screen.blit(self.margin_left, (0, 0))  #60 dps da primeira margem
        screen.blit(self.margin_right, (740, 0))  # 60 antes da segunda margem

    def move(self, screen, scr_height, movL_x, movL_y, movR_x, movR_y):

        for i in range(0, 2):
            screen.blit(self.image, (movL_x, movL_y - i * scr_height))
            screen.blit(self.margin_left, (movL_x, movL_y - i * scr_height))
            screen.blit(self.margin_right, (movR_x, movR_y - i * scr_height))

class Player:
    image = None
    x = None
    y = None
    width = None
    height = None

    def __init__(self, x, y):
        player_fig = pygame.image.load("Images/player.png")
        player_fig.convert()
        player_fig = pygame.transform.scale(player_fig, (90, 90))
        self.image = player_fig
        self.x = x
        self.y = y
        self.width = player_fig.get_width()
        self.height = player_fig.get_height()


    def draw (self, screen, x, y) :
        screen.blit(self.image, (x, y))

    def move(self, mudar_x):
        #Movimentação do player
        #alterar a coordenada x da nave de acordo coom as mudanças no event_handle() da classe Game
        self.x += mudar_x


class Hazard:
    image = None
    x = None
    y = None
    width = None
    height = None

    def __init__(self, image, x, y):
        hazard_fig = pygame.image.load(image)
        hazard_fig.convert()
        hazard_fig = pygame.transform.scale(hazard_fig, (130, 130))
        self.image = hazard_fig
        self.x = x
        self.y = y
        self.width = hazard_fig.get_width()
        self.height = hazard_fig.get_height()

    def draw (self, screen, x, y):
        screen.blit(self.image, (x, y))

    def move(self, screen, velocidade_hazard):
        self.y = self.y + velocidade_hazard / 4
        self.draw(screen, self.x, self.y)
        self.y += velocidade_hazard


class Soundtrack:
    soundtrack = None
    sound = None

    def __init__(self, soundtrack):
        if os.path.isfile(soundtrack):
            self.soundtrack = soundtrack
        else:
            print(soundtrack + "not found... ignoring", file=sys.stderr)

    def play(self):
        pygame.mixer.music.load(self.soundtrack)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)

    def set(self, soundtrack):
        if os.path.isfile(soundtrack):
            self.soundtrack = soundtrack
        else:
            print(soundtrack + "not found... ignoring", file=sys.stderr)

    def play_sound(self, sound):
        if os.path.isfile(sound):
            self.sound = sound
            pygame.mixer.music.load(self.sound)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()
        else:
            print(sound + "not found... ignoring", file=sys.stderr)


class Game:
    screen=None
    screen_size=None
    width=800
    height=600
    run=True
    background=None
    player=None
    hazard = []
    soundtrack = None


    #DIREITA =  pygame.K_d
    #ESQUERDA =  pygame.K_a
    mudar_x = 0.0

    def __init__(self, size, fullscreen):    #função que inicializa o pygame, define resolução e desabilita o mouse

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))  #tamanho da tela
        self.screen_size = self.screen.get_size()                         #tamanho tela do jogo

        pygame.mouse.set_visible(0)                                       #desabilita o mouse
        pygame.display.set_caption('Delterestelar')                          #titulo jogo
    # init()

    def handle_events(self):   #trata o evento e toma as ações necessárias

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.mudar_x = - 8
                if event.key == pygame.K_d:
                    self.mudar_x = 8

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.mudar_x = 0
    # handle_events()

    def write_message(self, message, R, G, B, x, y):
        my_font1 = pygame.font.Font("Fonts/Fonte4.ttf", 100)
        render_text = my_font1.render(message, False, (R, G, B))   # (texto opaco/transparente)
        self.screen.blit(render_text, (x, y))        #desenha

    def elements_draw(self):
        self.background.draw(self.screen)  #desenha elementos
    # elements_draw()

    #informa a quantidade de hazard q passaram e a pontuação
    def score_card(self, screen, h_passou, score):
        font = pygame.font.Font("Fonts/Fonte2.ttf", 20)
        passou = font.render("Passou: " + str(h_passou), True, (255, 255, 128))
        score = font.render("Score: " + str(score), True, (253, 231, 32))
        screen.blit(passou, (0, 50))
        screen.blit(score, (0, 100))
    #score_card()

    def play_soundtrack(self):
        #inclui trilha sonora
        if os.path.isfile('Sounds/interestelar.mp3'):
            pygame.mixer.music.load('Sounds/interestelar.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(loops=-1)               #carrega o arquivo ajeita o volume e coloca pra tocar sem parar
        else:
            print("Sounds/song.mp3 not found... ignoring", file=sys.stderr)
    #play_soundtrack()

    def play_sound(self, sound):
        #som
        if os.path.isfile(sound):
            pygame.mixer.music.load(sound)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
        else:
            print("Sound file not found... ignoring", file=sys.stderr)
    #play_sound()

    def draw_explosion(self, screen, x, y):
        explosion_fig = pygame.image.load("Images/explosion.png")
        explosion_fig.convert()
        explosion_fig = pygame.transform.scale(explosion_fig, (150, 150))
        screen.blit(explosion_fig, (x, y))
    #draw_explosion()

    def check_collision(self, player, hazard):
        # AABB Collision Detection
        if (player.x < hazard.x + hazard.width and
                player.x + player.width > hazard.x and
                player.y < hazard.y + hazard.height and
                player.y + player.height > hazard.y):
            return True
        return False


    def loop(self):   #laço principal

        score = 0
        h_passou = 0

        velocidade_background = 7                #movimento do plano de fundo
        velocidade_hazard = 7

        hzrd = 0
        h_x = random.randrange(125, 660)    #localização
        h_y = -500

        #movimento da margem esquerda
        movL_x = 0
        movL_y = 0

        # movimento da margem direita
        movR_x = 740
        movR_y = 0

        self.background = Background()            #cria plano de fundo

        self.play_soundtrack()                    #inclui trilha sonora

        #posicao player
        x = (self.width - 56) / 2
        y = self.height - 125

        self.player = Player(x, y)               #Criar o player

        #Cria os Hazards
        self.hazard.append(Hazard("Images/satelite.png", h_x, h_y))
        self.hazard.append(Hazard("Images/nave.png", h_x, h_y))
        self.hazard.append(Hazard("Images/cometaVermelho.png", h_x, h_y))
        self.hazard.append(Hazard("Images/meteoros.png", h_x, h_y))
        self.hazard.append(Hazard("Images/buracoNegro.png", h_x, h_y))

        #cria trilha sonora
        self.soundtrack = Soundtrack('Sounds/interestelar.mp3')
        self.soundtrack.play()

        clock = pygame.time.Clock()               #limita o valor do fps do jogo
        dt = 16

        while self.run:
            clock.tick(1000 / dt)                 #numero máximo de fps
            self.handle_events()                  #tratar os eventos

            self.elements_draw()  # desenha elementos

            #adiciona movimento ao background4
            self.background.move(self.screen, self.height, movL_x, movL_y, movR_x, movR_y)
            movL_y = movL_y + velocidade_background
            movR_y = movR_y + velocidade_background

            #se a imagens ultrapassar a extremidade da tela, move de volta
            if movL_y > 600 and movR_y > 600:
                movL_y -= 600
                movR_y -= 600

            self.player.move(self.mudar_x)                         #movimentção do foguete

            self.player.draw(self.screen, self.player.x, self.player.y)            #desenha o player

            self.score_card(self.screen, h_passou, score)  #mostra o score

            #restricoes de movimento
            if self.player.x > 760 - 92 or self.player.x < 40 + 5:

                self.soundtrack.play_sound('Sounds/jump2.wav')

                self.write_message("BATEU FIII", 255, 255, 255, 80, 200)
                pygame.display.update()                    #atualiza a tela
                time.sleep(3)
                self.loop()
                self.run = False

            #adicionando movimento ao hazard
            self.hazard[hzrd].move(self.screen, velocidade_hazard)

            #definindo onde hazard vai aparecer, recomeçando a posição do obstáculo e da faixa
            if self.hazard[hzrd].y > self.height:
                self.hazard[hzrd].y = 0 - self.hazard[hzrd].image.get_height()
                self.hazard[hzrd].x = random.randrange(125, 650 - self.hazard[hzrd].image.get_height())
                hzrd = random.randint(0, 4)
                h_passou = h_passou + 1                             #determina quantos objetos passaram
                score = h_passou * 10

            #aumenta a velocidade se score == 60
            if score % 60 == 0:
                velocidade_hazard += 0.03

            if self.check_collision(self.player, self.hazard[hzrd]):
                # som da colisão
                self.soundtrack.play_sound('Sounds/crash.wav')

                # imagem da explosão
                self.draw_explosion(self.screen, self.player.x - (self.player.image.get_width() / 2),
                                    self.player.y - (self.player.image.get_height() / 2))

                # mensagem game over
                self.write_message("FOI DE BERÇO!", 255, 0, 0, 80, 200)  # vermelha
                pygame.display.update()
                time.sleep(3)
                self.run = False



            pygame.display.update()  # atualiza a tela
            clock.tick(2000)  # definir taxa máxima de quadrados por segundo

    # loop()



game = Game("resolution", "fullscreen")  #instancia o objeto jogo
game.loop()                              #inicia o jogo

