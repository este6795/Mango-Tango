import pygame
import sys
import obstacle
from player import Player
from alien import Alien, Extra_Alien
from laser import Laser
from random import choice, randint


#Contains all game logic
class Game: 
    def __init__(self): 

        #Player Setup
        player_sprite = Player((screen_width/2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        
        #Health and Score Setup 
        self.lives = 3
        self.live_surface = pygame.image.load('Assets/graphics/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surface.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('Assets/font/Pixeled.ttf', 20)

        #Obstacle Setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width/ self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = 40, y_start = 480)

        #Alien Setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.aliens_setup(rows = 6, cols = 8)
        self.aliens_direction = 1

        #Extra Alien Setup
        self.alien_extra = pygame.sprite.GroupSingle()
        self.alien_extra_spawn_time = randint(400, 800)

        #Background Music Setup
        music = pygame.mixer.Sound('Assets/audio/music.wav')
        music.set_volume(0.2)
        music.play(loops = -1)

        #Laser Sound
        self.laser_sound = pygame.mixer.Sound('Assets/audio/laser.wav')
        self.laser_sound.set_volume(0.5)

        #Explosion Sound
        self.explosion_sound = pygame.mixer.Sound('Assets/audio/explosion.wav')
        self.explosion_sound.set_volume(0.3)

    #Alien Creation 
    def aliens_setup(self, rows, cols, x_distance = 60, y_distance = 45, x_offset = 70, y_offset = 100): 
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)): 
                #Defining Display Distance
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                
                #Defining what Aliens go into which rows
                if row_index == 0: 
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2: 
                    alien_sprite = Alien('green', x, y)
                else: 
                    alien_sprite = Alien('red', x, y)

                #Adding Aliens to Sprite Group 
                self.aliens.add(alien_sprite)

    #Alien Direction
    def alien_position_checker(self): 
        all_aliens = self.aliens.sprites()
        for alien in all_aliens: 
            if alien.rect.right >= screen_width: 
                self.aliens_direction = - 1
                self.alien_move_down(2)
            if alien.rect.left <= 0: 
                self.aliens_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance): 
        if self.aliens: 
            for alien in self.aliens.sprites(): 
                alien.rect.y += distance

    #Alien Shoot Mechanism
    def alien_shoot(self): 
        if self.aliens.sprites(): 
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    #Extra Alien Spawn Timer
    def extra_alien_timer(self): 
        self.alien_extra_spawn_time -= 1
        if self.alien_extra_spawn_time <= 0: 
            self.alien_extra.add(Extra_Alien(choice(['right', 'left']), screen_width))
            self.alien_extra_spawn_time = randint(400, 800)

    #Obstacle Creation
    def create_obstacle(self, x_start, y_start, offset_x): 
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row): 
                if col == 'x': 
                    #Defining Display Distance
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    
                    #Adding Obstacles to Sprite Group
                    block = obstacle.Block(self.block_size, (241,79,80), x, y)
                    self.blocks.add(block)

    #Creates multiple obstacles 
    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:  
            self.create_obstacle(x_start, y_start, offset_x)

    #Collision Method
    def collision_checks(self): 

        #Player Laser Collisions
        if self.player.sprite.lasers: 
            for laser in self.player.sprite.lasers: 
                #Obstacle Collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True): 
                    laser.kill()
                    

                #Alien Collisions
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit: 
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()

                #Extra Aliens
                if pygame.sprite.spritecollide(laser, self.alien_extra, True): 
                    self.score += 500
                    laser.kill()
        
        #Alien Laser Collisions
        if self.alien_lasers: 
            for laser in self.alien_lasers:
                #Obstacle Collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True): 
                    laser.kill()

                #Player Collisions
                if pygame.sprite.spritecollide(laser, self.player, False): 
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0: 
                        self.game_over()
        
        #Alien Collisions
        if self.aliens: 
            for alien in self.aliens: 
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False): 
                    pygame.quit()
                    sys.exit()

    #Lives Method
    def display_lives(self): 
        #Check Lives Minus One
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surface.get_size()[0] + 10))
            screen.blit(self.live_surface, (x, 8)) 

    #Score Method
    def display_score(self): 
        score_surface = self.font.render(f'Score: {self.score}', False, 'white')
        score_rect = score_surface.get_rect(topleft = (10, -10))
        screen.blit(score_surface, score_rect)

    #Victory Message Display
    def victory_message(self): 
        if not self.aliens.sprites(): 
            victory_surface = self.font.render('You Won', False, 'white')
            victory_rect = victory_surface.get_rect(center = (screen_width/2, screen_height/2))
            screen.blit(victory_surface, victory_rect)

    #Game Over Display
    def game_over(self): 
        game_over_surface = self.font.render('Game Over', False, 'white')
        game_over_rect = game_over_surface.get_rect(center = (screen_width /2, screen_height/2 + 20))
        screen.blit(game_over_surface, game_over_rect)
        pygame.quit()
        sys.exit()

    #Update/Draw all sprites
    def run(self): 
        #Draw/Update Player and Laser
        self.player.update()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.collision_checks()

        #Draw Live/Score System
        self.display_lives()
        self.display_score()

        #Draw Blocks
        self.blocks.draw(screen)

        #Draw/Update Aliens
        self.aliens.draw(screen)
        self.aliens.update(self.aliens_direction)
        self.alien_position_checker()
        self.alien_lasers.update()
        self.alien_lasers.draw(screen)

        #Draw/Update Extra Alien
        self.extra_alien_timer()
        self.alien_extra.update()
        self.alien_extra.draw(screen)

        #Draw Victory Method
        self.victory_message()

#Visual Class
class CRT: 
    def __init__(self): 
        self.tv = pygame.image.load('Assets/graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))

    #CRT Lines Method
    def create_crt_lines(self): 
        line_height = 3
        line_amount = int(screen_height/ line_height)
        for line in range(line_amount): 
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos),1)

    #Visual Draw function
    def draw(self):
        self.tv.set_alpha(randint(60,90))
        self.create_crt_lines()
        screen.blit(self.tv,(0,0))

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()
    icon = pygame.image.load('Assets/graphics/yellow.png')

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 1200)

    #Game Loop
    while True: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            
            if event.type == ALIENLASER: 
                game.alien_shoot()

        
        screen.fill((30, 30, 30))
        pygame.display.set_caption('Space Invaders')
        pygame.display.set_icon(icon)
        game.run()
        crt.draw()

        pygame.display.flip()
        clock.tick(60)