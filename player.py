import pygame
from laser import Laser

class Player(pygame.sprite.Sprite): 
    #Main class for Player Sprite 
    def __init__(self, pos, constraint, speed): 
        super().__init__()
       
        #Rendering Player image
        self.image = pygame.image.load('Assets/graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        
        #Defining Movement constraints and speed
        self.speed = speed
        self.max_x_constraint = constraint
        
        #Defining Laser Parameters
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600
        self.lasers = pygame.sprite.Group()

        #Player Laser Sounds
        self.laser_sound = pygame.mixer.Sound('Assets/audio/laser.wav')
        self.laser_sound.set_volume(0.5)

    #Handling Movement
    def get_input(self): 
        keys = pygame.key.get_pressed()

        #Movement
        if keys[pygame.K_RIGHT]: 
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]: 
            self.rect.x -= self.speed

        #Firing Mechanism
        if keys[pygame.K_SPACE] and self.ready: 
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()

    #Constraining Player to Screen
    def constraint(self): 
        if self.rect.left <= 0: 
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint: 
            self.rect.right = self.max_x_constraint

    #Firing Mechanism Method
    def recharge(self): 
        if not self.ready: 
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown: 
                self.ready = True 

    def shoot_laser(self): 
       new_laser = Laser(self.rect.center, -8, self.rect.bottom)
       self.lasers.add(new_laser)

    #Update method
    def update(self): 
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()