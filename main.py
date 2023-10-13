import pygame
from random import randint, choice
import time

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        playerWalk1 = pygame.image.load("graphics/playerwalk1.png").convert_alpha()
        playerWalk2 = pygame.image.load("graphics/playerwalk2.png").convert_alpha()
        self.playerWalk = [playerWalk1, playerWalk2]
        self.playerIndex = 0
        self.playerJump = pygame.image.load("graphics/playerjump.png").convert_alpha()
        
        self.image = self.playerWalk[self.playerIndex]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        
        self.jumpSound = pygame.mixer.Sound("audio/jump.mp3")
        self.jumpSound.set_volume(0.5)
    
    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jumpSound.play()
            
    def applyGravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    def animationState(self):
        if self.rect.bottom < 300:
            self.image = self.playerJump
        else:
            self.playerIndex += 0.1
            if self.playerIndex > len(self.playerWalk):
                self.playerIndex = 0
            self.image = self.playerWalk[int(self.playerIndex)]
            
    def update(self):
        self.playerInput()
        self.applyGravity()
        self.animationState()
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == "fly":
            fly1 = pygame.image.load("graphics/fly1.png").convert_alpha()
            fly2 = pygame.image.load("graphics/fly2.png").convert_alpha()
            self.frames = [fly1, fly2]
            yPos = 210
        else:
            snail1 = pygame.image.load("graphics/snail1.png").convert_alpha()
            snail2 = pygame.image.load("graphics/snail2.png").convert_alpha()
            self.frames = [snail1, snail2]
            yPos = 300 
            
        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), yPos))
        
    def animationState(self):
        self.animationIndex += 0.1 
        if self.animationIndex >= len(self.frames):
            self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()  
        
    def update(self):
        self.animationState()
        self.rect.x -= 6
        self.destroy
 
def displayScore():
    currentTime = int(pygame.time.get_ticks()/1000) - startTime
    scoreSurface = gameFont.render(f"Score:  {currentTime}", False, "Black")
    scoreRectangle = scoreSurface.get_rect(center = (400, 50))
    screen.blit(scoreSurface, scoreRectangle)
    return currentTime

def collisionSprite():
    if pygame.sprite.spritecollide(player.sprite, obstacleGroup, False):
        obstacleGroup.empty()
        return False
    else:
        return True
    
def collisions(player, obstacles):
    if obstacles:
        for obstacleRectangle in obstacles:
            if player.colliderect(obstacleRectangle):
                return False
    return True

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Pixel Pacer")
clock = pygame.time.Clock()
gameFont = pygame.font.Font("fonts/pixelated.ttf", 50)
gameActive = False
startTime = 0
score = 0
bgMusic = pygame.mixer.Sound("audio/music.wav")
bgMusic.set_volume(0.3)
bgMusic.play(loops = -1)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacleGroup = pygame.sprite.Group()

skySurface = pygame.image.load("graphics/sky.png").convert()
groundSurface = pygame.image.load("graphics/floor.png").convert()
titleSurface = gameFont.render("Pixel Pacer", False, "Black")
titleRectangle = titleSurface.get_rect(center = (400, 80))
infoSurface = gameFont.render("press Space to play", False, "Black")
infoRectangle = infoSurface.get_rect(center = (400, 320))

playerLoading = pygame.image.load("graphics/playerstand.png").convert_alpha()
playerLoading = pygame.transform.rotozoom(playerLoading, 0, 1.5)
playerLoadingRectangle = playerLoading.get_rect(center = (400, 200))

obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer, 1200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if gameActive:
            if event.type == obstacleTimer:
                obstacleGroup.add(Obstacle(choice(["snail", "fly", "snail", "snail"])))
        else:
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
                gameActive = True
                startTime = int(pygame.time.get_ticks()/1000)
                
                
    if gameActive:    
        screen.blit(skySurface, (0,0))
        screen.blit(groundSurface, (0,300))
        score = displayScore()
        player.draw(screen) 
        player.update()
        obstacleGroup.draw(screen)
        obstacleGroup.update()
        gameActive = collisionSprite()

    else:
        screen.fill("#58708c")
        screen.blit(titleSurface, titleRectangle)
        playerGravity = 0
        scoreSurface = gameFont.render(f"Your Score: {score}", False, "Black")
        scoreSurfaceRectangle = scoreSurface.get_rect(center = (400, 320))
        if score == 0:
            screen.blit(infoSurface, infoRectangle)
        else:
            screen.blit(scoreSurface, scoreSurfaceRectangle)
        screen.blit(playerLoading, playerLoadingRectangle)
        
    pygame.display.update()
    clock.tick(60)