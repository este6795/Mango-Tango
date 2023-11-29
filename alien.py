import pygame

class Alien(pygame.sprite.Sprite): 
    def __init__(self, color, x, y): 
        super().__init__()
        #Defining a file path for ALL enemies 
        file_path = 'Assets/graphics/' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))

        #Giving Score Values to Aliens
        if color == 'red': 
            self.value = 100
        elif color == 'green': 
            self.value = 200
        else: 
            self.value = 300

    def update(self, direction): 
        self.rect.x += direction

class Extra_Alien(pygame.sprite.Sprite): 
    def __init__(self, side, screen_width): 
        super().__init__()
        #Rendering Alien
        self.image = pygame.image.load('Assets/graphics/extra.png').convert_alpha()
        
        #Defining which Side Alien Spawns on
        if side == 'right': 
            x = screen_width + 50
            self.speed = -3
        else: 
            x = -50
            self.speed = 3
        
        #Creating Rectangle Around Alien
        self.rect = self.image.get_rect(topleft = (x, 80))

    #Creating Speed of Alien
    def update(self): 
        self.rect.x += self.speed