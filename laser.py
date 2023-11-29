import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height): 
        super().__init__()
        #Rendering lasers
        self.image = pygame.Surface((4,20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center = pos)
        
        #Define laser speeds
        self.speed = speed

        #Defining Screen height for destroy method
        self.height_y_constraint = screen_height

    #Ensuring Lasers are destroyed once off screen
    def destroy(self): 
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50: 
            self.kill()

    #Update method allows for laser to move
    def update(self): 
        self.rect.y += self.speed
        self.destroy()