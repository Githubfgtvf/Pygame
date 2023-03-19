import math
import pygame
import sys

GREY = (205, 205, 205)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Hello World")
clock = pygame.time.Clock()




class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.position = pygame.Vector2()
        self.rect.center = (self.rect.x,self.rect.y)
        self.vel = pygame.math.Vector2(0, 0)
        self.gravity = pygame.math.Vector2(0, 0.1)
        self.direction = pygame.math.Vector2(0, -1)
        
        #add the gun image to the player
        # self.gun = Gun()
        # self.gun.set_position(self.position)
        



    def update(self):
        # # Move the player down
        self.rect.y += 1

        # Apply gravity
        self.vel += self.gravity
        self.rect.move_ip(round(self.vel.x), round(self.vel.y))

        if self.rect.left < 0:
            self.rect.left = 0
            self.vel = -self.vel * 0.9  
        elif self.rect.right > 800:
            self.rect.right = 800
            self.vel = -self.vel * 0.9  

        # Check for collision with top and bottom walls
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel = -self.vel * 0.9 
        elif self.rect.bottom > 800:
            self.rect.bottom = 800
            self.vel = -self.vel * 0.9
        

    # def draw(self, screen):
    #     self.gun.draw(screen)
    #     screen.blit(self.image, self.blit_position())
    #     pygame.draw.circle(screen, (0,0,0), (self.position.x - 14 + self.offset.x, self.position.y - 10 + self.offset.y), 4)
    #     pygame.draw.circle(screen, (0,0,0), (self.position.x + 4 + self.offset.x , self.position.y - 10 + self.offset.y ), 4)
            
    # def blit_position(self):
    #     return (self.position.x - (self.image.get_width() / 2), self.position.y - (self.image.get_height() / 2))
    


        


    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def recoil(self, cursor_pos):
        direction = pygame.math.Vector2(cursor_pos[0] - self.rect.centerx, cursor_pos[1] - self.rect.centery)

        # Scale the vector to a magnitude of 10
        direction.scale_to_length(5)

        # Flip the direction
        direction = -direction

        # Reset player's velocity
        self.vel = pygame.math.Vector2(0, 0)

        # Add the recoil velocity
        self.vel += direction



class Gun(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = pygame.Vector2()
        self.image = pygame.image.load("Gunv2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()

    # def draw(self,screen):
    #     screen.blit(self.image, self.blit_position())

    # def blit_position(self):
    #     return self.position.x - (self.image.get_width() / 2), self.position.y - (self.image.get_height() / 2)
    
    # def refresh_sprite(self):
    #     self.image = pygame.image.load('data/images/Gun.png').convert_alpha()
    #     self.image = pygame.transform.scale(self.image, (200, 200))

    # def set_position(self, position):
    #     self.position = position
        

    

# put player in the middle of the screen
player = Player(320, 240)
gun = Gun()
sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(gun)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get the position of the mouse click
            target_pos = event.pos
            # apply the recoil effect
            player.recoil(target_pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, 0)
    if keys[pygame.K_RIGHT]:
        player.move(1, 0)

    if player.rect.y > 480:
        pygame.quit()
    
    mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
    screen.fill(GREY)
    sprites.update()
    sprites.draw(screen)
    pygame.display.update()
    clock.tick(60)

# TODO Fix UPDATE on GUN