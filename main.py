# Import necessary libraries
import pygame
from random import randint, choice
import time

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load player images and set initial properties
        playerWalk1 = pygame.image.load("graphics/playerwalk1.png").convert_alpha()
        playerWalk2 = pygame.image.load("graphics/playerwalk2.png").convert_alpha()
        self.playerWalk = [playerWalk1, playerWalk2]
        self.playerIndex = 0
        self.playerJump = pygame.image.load("graphics/playerjump.png").convert_alpha()
        
        # Set initial image and position
        self.image = self.playerWalk[self.playerIndex]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        
        # Load and set up jump sound
        self.jumpSound = pygame.mixer.Sound("audio/jump.mp3")
        self.jumpSound.set_volume(0.5)
    
    # Handle player input
    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            # Apply upward force to simulate jumping
            self.gravity = -20
            # Play jump sound
            self.jumpSound.play()
            
    # Apply gravity to the player
    def applyGravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        # Keep the player on the ground
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    # Manage player animation state
    def animationState(self):
        if self.rect.bottom < 300:
            # If player is in the air, show jump image
            self.image = self.playerJump
        else:
            # Animate walking by cycling through images
            self.playerIndex += 0.1
            if self.playerIndex > len(self.playerWalk):
                self.playerIndex = 0
            self.image = self.playerWalk[int(self.playerIndex)]
            
    # Update the player's state
    def update(self):
        self.playerInput()
        self.applyGravity()
        self.animationState()

# Define the Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        # Load obstacle images based on type
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
            
        # Set initial animation frame and position
        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), yPos))
        
    # Manage obstacle animation state
    def animationState(self):
        self.animationIndex += 0.1 
        if self.animationIndex >= len(self.frames):
            self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]
        
    # Remove obstacle if it goes off the screen
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()  
        
    # Update the obstacle's state
    def update(self):
        self.animationState()
        # Move obstacle horizontally
        self.rect.x -= 6
        # Remove obstacle if it's off the screen
        self.destroy

# Display the current score
def displayScore():
    # Calculate and display the score
    currentTime = int(pygame.time.get_ticks() / 1000) - startTime
    scoreSurface = gameFont.render(f"Score:  {currentTime}", False, "Black")
    scoreRectangle = scoreSurface.get_rect(center=(400, 50))
    screen.blit(scoreSurface, scoreRectangle)
    return currentTime

# Check for collisions between player and obstacles
def collisionSprite():
    # Check for collisions and clear obstacles on collision
    if pygame.sprite.spritecollide(player.sprite, obstacleGroup, False):
        obstacleGroup.empty()
        return False
    else:
        return True
    
# Check for collisions between player and obstacles
def collisions(player, obstacles):
    # Check for collisions between player and obstacles
    if obstacles:
        for obstacleRectangle in obstacles:
            if player.colliderect(obstacleRectangle):
                return False
    return True

# Initialize Pygame
pygame.init()
# Set up the game window
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Pixel Pacer")
# Set up the game clock
clock = pygame.time.Clock()
# Load the game font
gameFont = pygame.font.Font("fonts/pixelated.ttf", 50)
# Set the initial game state
gameActive = False
# Initialize start time and score
startTime = 0
score = 0

# Load and play background music
bgMusic = pygame.mixer.Sound("audio/music.wav")
bgMusic.set_volume(0.3)
bgMusic.play(loops=-1)

# Create player and obstacle groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacleGroup = pygame.sprite.Group()

# Load background and title images
skySurface = pygame.image.load("graphics/sky.png").convert()
groundSurface = pygame.image.load("graphics/floor.png").convert()
titleSurface = gameFont.render("Pixel Pacer", False, "Black")
titleRectangle = titleSurface.get_rect(center=(400, 80))
infoSurface = gameFont.render("press Space to play", False, "Black")
infoRectangle = infoSurface.get_rect(center=(400, 320))

# Set up player loading animation
playerLoading = pygame.image.load("graphics/playerstand.png").convert_alpha()
playerLoading = pygame.transform.rotozoom(playerLoading, 0, 1.5)
playerLoadingRectangle = playerLoading.get_rect(center=(400, 200))

# Set up obstacle spawn timer
obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer, 1200)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if gameActive:
            if event.type == obstacleTimer:
                # Add a new obstacle to the group at regular intervals
                obstacleGroup.add(Obstacle(choice(["snail", "fly", "snail", "snail"])))
        else:
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
                # Start the game when the space key is pressed
                gameActive = True
                startTime = int(pygame.time.get_ticks() / 1000)
                
    if gameActive:    
        # Draw game elements during active gameplay
        screen.blit(skySurface, (0, 0))
        screen.blit(groundSurface, (0, 300))
        score = displayScore()
        player.draw(screen) 
        player.update()
        obstacleGroup.draw(screen)
        obstacleGroup.update()
        gameActive = collisionSprite()

    else:
        # Draw title screen and player loading animation
        screen.fill("#58708c")
        screen.blit(titleSurface, titleRectangle)
        playerGravity = 0
        scoreSurface = gameFont.render(f"Your Score: {score}", False, "Black")
        scoreSurfaceRectangle = scoreSurface.get_rect(center=(400, 320))
        if score == 0:
            screen.blit(infoSurface, infoRectangle)
        else:
            screen.blit(scoreSurface, scoreSurfaceRectangle)
        screen.blit(playerLoading, playerLoadingRectangle)
        
    pygame.display.update()
    clock.tick(60)
