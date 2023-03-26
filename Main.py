import math
import random
import pygame
from pygame import Vector2, mixer
import sys
import json
import os
import time
pygame.init()

GREY = (205, 205, 205)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hello World")


class Player():
    global dt
    def __init__(self):
        self.is_dead = False
        self.score = 0
        self.position = pygame.Vector2()
        w, h = pygame.display.get_surface().get_size()
        self.position.xy = w / 2, h / 5
        self.velocity = pygame.Vector2()
        self.rotation = pygame.Vector2()
        self.offset = pygame.Vector2()
        self.gun = Gun()
        self.drag = 100
        self.gravity_scale = 300
        self.player_sprite = pygame.image.load('Player.png').convert_alpha()
        self.font = pygame.font.Font("data/fonts/Montserrat-ExtraBold.ttf", 300)
        self.player_sprite = pygame.transform.scale(self.player_sprite, (50, 60))
        self.gun.set_position(self.position)
        self.dt = 0.02

    def move(self):
        self.gravity()
        self.wall_detection()
        self.position.x -= self.velocity.x * self.dt 
        self.position.y -= self.velocity.y * self.dt
    
    def handle_gun(self):
        self.gun.set_position(self.position)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.position.x, mouse_y - self.position.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.gun.set_rotation(angle)

        self.offset.x = min(rel_x, 4) if (self.offset.x > 0) else max(rel_x, -4)
        self.offset.y = min(rel_y, 4) if (self.offset.y > 0) else max(rel_y, -4)

    def wall_detection(self):
        if(self.position.x < 0):
            self.position.x = 0
            self.velocity = -self.velocity * 0.9
        if(self.position.x > SCREEN_WIDTH):
            self.position.x = SCREEN_WIDTH
            self.velocity = -self.velocity * 0.9

        if(self.position.y < 0):
            self.position.y = 0
            self.velocity = -self.velocity * 0.9
        if(self.position.y > SCREEN_HEIGHT):
            print("You Lost")
            print(f"Your score was {self.score}")
            self.is_dead = True

    def get_score(self):
        return self.score
        
    def gravity(self):
        self.velocity.y -= 2 #self.gravity_scale * self.dt

    def check_state(self):
        global state
        if self.is_dead:
            if not os.path.exists('data/highscore.json'):
                with open('data/highscore.json', 'w') as f:
                    json.dump({'highscore': 0}, f)
            
            with open('data/highscore.json', 'r') as f:
                data = json.load(f)
                if self.score > data['highscore']:
                    data['highscore'] = self.score
                    with open('data/highscore.json', 'w') as f:
                        json.dump(data, f)

            gameOver = GameOver(self.score)
            gameOver.draw(screen)
            pygame.display.update()
            count = 3
            while count > 0:
                print(f"Restarting in {count}")
                time.sleep(1)
                count -= 1
            gameOver.restart_game()
            


    def collision_detection(self, Coin):
        for i in range(len(Coin.refills)):
            other = Coin.refills[i]
            if(self.get_left() < other.get_right() and self.get_right() > other.get_left() and self.get_top() < other.get_bottom() and self.get_bottom() > other.get_top()):
                Coin.populate_refill()
                self.score += 1
                print(self.score)
    
    def get_right(self):
        return self.position.x + (self.player_sprite.get_width() / 2)

    def get_left(self):
        return self.position.x - (self.player_sprite.get_width() / 2)
    
    def get_top(self):
        return self.position.y - (self.player_sprite.get_height() / 2)
    
    def get_bottom(self):
        return self.position.y + (self.player_sprite.get_height() / 2)

    def draw(self, screen):
        self.gun.draw(screen)
        screen.blit(self.player_sprite, self.blit_position())

    def blit_position(self):
        return (self.position.x - (self.player_sprite.get_width() / 2), self.position.y - (self.player_sprite.get_height() / 2))

    def shoot(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.position.x, mouse_y - self.position.y
        vector = pygame.Vector2()
        vector.xy = rel_x, rel_y
        mag = vector.magnitude()
        vector.xy /= mag
        self.velocity.y = 0
        self.velocity.x = 0
        self.add_force(vector, 500)

    def add_force(self, vector, magnitude):
        self.velocity.x += vector.x * magnitude
        self.velocity.y += vector.y * magnitude

    def display_score(self):
        text = self.font.render(str(self.score), False, (200,200,200))
        screen.blit(text, (285,200))

class Gun():
    def __init__(self):
        self.gun_sprite = None
        self.position = pygame.Vector2()
        self.is_flipped = False
        self.position = pygame.Vector2()
        self.refresh_sprite()


    def refresh_sprite(self):
        self.gun_sprite = pygame.image.load('data/images/Gun.png').convert_alpha()
        self.gun_sprite = pygame.transform.scale(self.gun_sprite, (200, 200))

    def draw(self, screen):
        screen.blit(self.gun_sprite, self.blit_position())

    def set_position(self, position):
        self.position = position
    
    def set_rotation(self, degrees):
        self.refresh_sprite()
        self.gun_sprite = pygame.transform.rotate(self.gun_sprite, degrees)
          
    def blit_position(self):
        return self.position.x - (self.gun_sprite.get_width() / 2), self.position.y - (self.gun_sprite.get_height() / 2)
    

class Coin:
    def __init__(self, position):
        self.position = Vector2()
        self.position.x = position.x
        self.position.y = position.y
        self.gun_sprite = pygame.image.load('data/images/coin.png').convert_alpha()
        self.gun_sprite = pygame.transform.scale(self.gun_sprite, (30, 40))

    def draw(self, screen):
        screen.blit(self.gun_sprite, self.position)
    
    def get_right(self):
        return self.position.x + 30

    def get_left(self):
        return self.position.x 
    
    def get_top(self):
        return self.position.y
    
    def get_bottom(self):
        return self.position.y + 40

class LevelBuilder:
    def __init__(self):
        self.refills = []
    def populate_refill(self):
        self.refills = []
        sound = mixer.Sound("data/audio/coincollect.mp3")
        sound.set_volume(0.1)
        sound.play()
        for _ in range(2):
            pos = Vector2()
            pos.x = random.randint(100, 700)
            pos.y = random.randint(100, 500)
            refill = Coin(pos)
            self.refills.append(refill)
        
            
    def draw(self, screen):
        for i in range(len(self.refills)):
            self.refills[i].draw(screen) 
    


class Menu():
    def __init__(self):
        mixer.music.load("data/audio/RainingVillage.mp3")
        mixer.music.set_volume(0.9)
        mixer.music.play(-1)
        self.font = pygame.font.Font("data/fonts/Montserrat-ExtraBold.ttf", 25)
        self.title_font = pygame.font.Font("data/fonts/Montserrat-ExtraBold.ttf", 50)
        self.title = self.title_font.render('Coin Collector', True, (75,75,75))
        self.play_button = pygame.Rect(300, 300, 100, 50)
        self.play_text = self.font.render('Play', True, (75,75,75))
        self.quit_button = pygame.Rect(300, 400, 100, 50)
        self.quit_text = self.font.render('Quit', True, (75,75,75))
        self.background = pygame.image.load('data/images/Menu.jpg').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_rect = self.background.get_rect()
        self.background_rect.center = (400, 300)
        self.highscore = 0
        with open('data/highscore.json', 'r') as f:
            data = json.load(f)
            self.highscore = data['highscore']
        self.highscore_text = self.font.render('Highscore: ' + str(self.highscore), True, (75,75,75))

    def draw(self, screen):
        pygame.draw.rect(screen, (100,100,100), self.play_button)
        pygame.draw.rect(screen, (100,100,100), self.quit_button)
        screen.blit(self.background, self.background_rect)
        screen.blit(self.title, (200, 100))
        screen.blit(self.play_text, (350, 310))
        screen.blit(self.quit_text, (350, 410))
        screen.blit(self.highscore_text, (300, 500))

    def check_click(self, position):
        if self.play_button.collidepoint(position):
            return 'play'
        elif self.quit_button.collidepoint(position):
            return 'quit'
        else:
            return None
        

class GameOver():
    def __init__(self, score):
        self.score = score
        self.font = pygame.font.Font("data/fonts/Montserrat-ExtraBold.ttf", 25)
        self.title_font = pygame.font.Font("data/fonts/Montserrat-ExtraBold.ttf", 50)
        self.title = self.title_font.render('Game Over', True, (75,75,75))
        self.score_text = self.font.render('Score: ' + str(self.score), True, (75,75,75))
        self.background = pygame.image.load('data/images/Menu.jpg').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_rect = self.background.get_rect()
        self.background_rect.center = (400, 300)
        self.highscore = 0
        with open('data/highscore.json', 'r') as f:
            data = json.load(f)
            self.highscore = data['highscore']
        self.highscore_text = self.font.render('Highscore: ' + str(self.highscore), True, (75,75,75))

    def draw(self, screen):
        screen.blit(self.background, self.background_rect)
        screen.blit(self.title, (250, 100))
        screen.blit(self.score_text, (348, 235))
        screen.blit(self.highscore_text, (315, 325))


    def restart_game(self):
        game = Game()
        game.run()
        

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.gun = Gun()
        self.level_builder = LevelBuilder()
        self.level_builder.populate_refill()
        self.menu = Menu()
        self.game_over = GameOver(score=0)
        self.state = 'menu'
        self.background = pygame.image.load('data/images/SnowMap.jpg').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_rect = self.background.get_rect()
        self.background_rect.center = (400, 300)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cursor_pos = pygame.mouse.get_pos()
                    if self.state == 'menu':
                        result = self.menu.check_click(cursor_pos)
                        if result == 'play':
                            self.state = 'play'
                            mixer.music.load("data/audio/BackgroundMusic.mp3")
                            mixer.music.set_volume(0.9)
                            mixer.music.play(-1)
                        elif result == 'quit':
                            pygame.quit()
                            sys.exit()
                    elif self.state == 'game_over':
                        result = self.game_over.check_click(cursor_pos)
                        if result == 'play':
                            self.state = 'play'
                            self.player = Player()
                            self.gun = Gun()
                            self.level_builder = LevelBuilder()
                            self.level_builder.populate_refill()
                        elif result == 'quit':
                            pygame.quit()
                            sys.exit()
                    elif self.state == 'play':
                        self.player.shoot()

            self.screen.fill(GREY)
            self.screen.blit(self.background, self.background_rect)
            if self.state == 'menu':
                self.menu.draw(self.screen)
            elif self.state == 'play':
                self.player.move()
                self.player.handle_gun()
                self.player.check_state()
                self.player.display_score()
                self.player.draw(self.screen)
                self.player.check_state()
                self.level_builder.draw(self.screen)

                self.player.collision_detection(self.level_builder)
            elif self.state == 'game_over':
                self.game_over.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)




if __name__ == '__main__':
    mixer.init()
    game = Game()
    game.run()