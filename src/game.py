import pygame

pygame.init()

# Gera tela principal

WIDTH = 800
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame")



# Inicia assets

plataform_img = pygame.image.load("assets/img/plataforma.png")
plataform_img = pygame.transform.scale(plataform_img, (WIDTH, 100))
player_img = pygame.image.load("assets/img/quadrado.png")
player_img = pygame.transform.scale(player_img, (50, 50))
obstaculo_img = pygame.image.load("assets/img/obstaculo.png")
obstaculo_img = pygame.transform.scale(obstaculo_img, (50, 50))

## ----- Inicia estruturas de dados
# Definindo os novos tipos

class Player(pygame.sprite.Sprite):
    def __init__(self,img):
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 100
        self.speedx = 0
        self.speedy = 0
        self.on_ground = True # verifica se o jogador está no chão
    
    def update(self):
        # Atualiza a posição do jogador
        self.rect.x += self.speedx
        
        # aplica a gravidade se não estiver no chão
        if not self.on_ground:
            self.speedy += 1

        self.rect.y += self.speedy

        # Checa se o jogador está no chão
        if self.rect.bottom >= HEIGHT - 100:
            self.rect.bottom = HEIGHT - 100
            self.on_ground = True
            self.speedy = 0


        # Mantem dentro da tela horizontalmente
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0: 
            self.rect.left = 0

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self,img):
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 150
        self.speedx = -10

    def update(self):
        self.rect.x += self.speedx

        if self.rect.right < 0:
            self.rect.left = WIDTH

game = True

# variavel para ajustar a velocidade do jogo
clock = pygame.time.Clock()
FPS = 30

#cria um grupo de sprites e adiciona o jogador
all_sprites = pygame.sprite.Group()
all_obstaculos = pygame.sprite.Group()

player = Player(player_img)
all_sprites.add(player)
obstaculo = Obstaculo(obstaculo_img)
all_obstaculos.add(obstaculo)
all_sprites.add(obstaculo) #para desenhar o obstaculo na tela

# for i in range(10):
#     #player = Player(player)
#     all_sprites.add(player)

#Loop principal

while game:
    clock.tick(FPS)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        #Verifica se apertou alguma tecla
        if event.type ==pygame.KEYDOWN:
            #Dependendo da tecla, altera a velocidade
            if event.key == pygame.K_LEFT: #se a tecla for a seta para a esquerda
                player.speedx -= 8
            if event.key == pygame.K_RIGHT:#se a tecla for a seta para a direita
                player.speedx += 8
            if event.key == pygame.K_SPACE and player.on_ground:#se a tecla for a seta para cima
                player.speedy = -20 #pula
                player.on_ground = False
                
        # verifica se soltou alguma tecla
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade
            if event.key == pygame.K_LEFT:
                player.speedx += 8
            if event.key == pygame.K_RIGHT:
                player.speedx -= 8 

    #atualiza estado do jogo

    #atualiza a posição do jogador
    all_sprites.update()

    #verifica se houve colisão entre o jogador e o obstaculo
    colisao = pygame.sprite.spritecollide(player, all_obstaculos, True)
    if len(colisao) > 0:
        game = False


    #gera saidas
    window.fill((255, 255, 255)) #Preenche a tela com a cor branca
    window.blit(plataform_img, (0, 500))
    all_sprites.draw(window)  #Desenha o jogador na tela

    #atualiza a tela
    pygame.display.update()

#Finaliza o pygame
pygame.quit()