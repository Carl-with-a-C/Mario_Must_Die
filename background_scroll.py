import pygame

WINDOW_SIZE = (800, 400)

screen = pygame.display.set_mode(WINDOW_SIZE)



class Foreground():
  def __init__(self):
    self.bgimage = pygame.image.load('graphics/mario_ground.png').convert_alpha()
    self.bgimage = pygame.transform.scale(self.bgimage, (800, 60))
    self.rectBGimg = self.bgimage.get_rect()

    self.bgY1 = 340
    self.bgX1 = 0

    self.bgY2 = 340
    self.bgX2 = -self.rectBGimg.width

    self.moving_speed = 5
      
  def update(self):
    self.bgX1 += self.moving_speed
    self.bgX2 += self.moving_speed
    if self.bgX1 >= self.rectBGimg.width:
        self.bgX1 = -self.rectBGimg.width
    if self.bgX2 >= self.rectBGimg.width:
        self.bgX2 = -self.rectBGimg.width
          
  def render(self):
    screen.blit(self.bgimage, (self.bgX1, self.bgY1))
    screen.blit(self.bgimage, (self.bgX2, self.bgY2))


class Background():
  def __init__(self):
    self.bgimage = pygame.image.load('graphics/mario_background.jpeg').convert_alpha()
    self.bgimage = pygame.transform.scale(self.bgimage, (800, 400))
    self.rectBGimg = self.bgimage.get_rect()

    self.bgY1 = 0
    self.bgX1 = 0

    self.bgY2 = 0
    self.bgX2 = -self.rectBGimg.width

    self.moving_speed = 0.2
      
  def update(self):
    self.bgX1 += self.moving_speed
    self.bgX2 += self.moving_speed
    if self.bgX1 >= self.rectBGimg.width:
        self.bgX1 = -self.rectBGimg.width
    if self.bgX2 >= self.rectBGimg.width:
        self.bgX2 = -self.rectBGimg.width
          
  def render(self):
    screen.blit(self.bgimage, (self.bgX1, self.bgY1))
    screen.blit(self.bgimage, (self.bgX2, self.bgY2))