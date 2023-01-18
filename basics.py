import pygame

from background_scroll import Foreground, Background
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    boo_fly1 = pygame.image.load('graphics/boo1.png').convert_alpha()
    boo_fly1 = pygame.transform.scale(boo_fly1, (60, 60))
  
    boo_fly2 = pygame.image.load('graphics/boo2.png').convert_alpha()
    boo_fly2 = pygame.transform.scale(boo_fly2, (60, 60))

    self.boo_fly = [boo_fly1, boo_fly2]
    self.boo_index = 0

    self.image = self.boo_fly[self.boo_index]
    self.rect = self.image.get_rect(midbottom = (200, 300))
    self.gravity = 0
    self.fall_angle = 0

  def player_input(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
      self.gravity = -6

  def apply_gravity(self):
    self.gravity += 1
    self.rect.y += self.gravity
    self.fall_angle = int(self.gravity * 1.8)

  def animation_state(self):
    self.boo_index += 0.1
    if self.boo_index >= len(self.boo_fly):self.boo_index = 0
    self.image = pygame.transform.rotate(self.boo_fly[int(self.boo_index)], self.fall_angle)

  def update(self):
    self.player_input()
    self.apply_gravity()
    self.animation_state()

class Mario(pygame.sprite.Sprite):
  def __init__(self, type):
    super().__init__()
    if type == 'mario':
      mario_walk1 = pygame.image.load('graphics/mario/Anibody1.png').convert_alpha()
      mario_walk1 = pygame.transform.scale(mario_walk1, (50, 64))
      mario_walk2 = pygame.image.load('graphics/mario/Anibody2.png').convert_alpha()
      mario_walk2 = pygame.transform.scale(mario_walk2, (50, 64))
      mario_walk3 = pygame.image.load('graphics/mario/Anibody3.png').convert_alpha()
      mario_walk3 = pygame.transform.scale(mario_walk3, (50, 64))

      mario_jump = pygame.image.load('graphics/Deadpool.png').convert_alpha()
      mario_jump = pygame.transform.scale(mario_jump, (50, 64))

      self.walk_frames = [mario_walk1, mario_walk3, mario_walk2, mario_walk3, mario_jump]
      self.animation_index = 0
      self.gravity = 0
      self.y_pos = 340

      self.image = self.walk_frames[int(self.animation_index)]
      self.rect = self.image.get_rect(midbottom = (randint(-400, -100), self.y_pos))

      self.movement_list = []

  def animation_state(self):
    self.animation_index += 0.1
    self.image = self.walk_frames[int(self.animation_index)]
    if self.rect.bottom < self.y_pos:
      print(self.rect.bottom)
      self.animation_index = 4
    if self.rect.bottom == self.y_pos:
      if self.animation_index >= (len(self.walk_frames)-1.1):
        self.animation_index = 0
    if (score % 10) == 0:
      self.gravity = -12

  def apply_gravity(self):
    self.gravity += 1
    self.rect.y += self.gravity
    if self.rect.bottom >= self.y_pos: self.rect.bottom = self.y_pos
      
  def update(self):
    self.animation_state()
    self.apply_gravity()
    self.rect.x += 8

  def destroy(self):
    if self.rect.x >= 900:
      self.kill()

WINDOW_SIZE = (800, 400)


def display_score():
  current_time = pygame.time.get_ticks() - start_time
  score_surf = score_font.render(f'{int(current_time/ 100)}', True, 'White')
  score_rect = score_surf.get_rect(center = (400, 50))
  screen.blit(score_surf, score_rect)
  return int(current_time / 100)

def enemy_movement(obstacle_list):
  if obstacle_list:
    for obstacle_rect in obstacle_list:
      obstacle_rect.x += 8

      screen.blit(mario_surf, obstacle_rect)
        # pygame.draw.rect(screen, 'Pink', obstacle_rect, 5)
    obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x < 900]
    return obstacle_list
  else: return []

def pipes_movement(pipes_list):
  if pipes_list:
    for pipes_rect in pipes_list:
      pipes_rect.x += 5

      if pipes_rect.bottom == 400:
        screen.blit(pipes1_surf, pipes_rect)
      elif pipes_rect.bottom == 450: 
        screen.blit(pipes2_surf, pipes_rect)
      elif pipes_rect.bottom == 500: 
        screen.blit(pipes3_surf, pipes_rect)
      elif pipes_rect.bottom == 550: 
        screen.blit(pipes4_surf, pipes_rect)

    pipes_list = [pipes for pipes in pipes_list if pipes.x < 900]
    return pipes_list
  else: return []

def collisions(player, enemies, pipes):
  if enemies or pipes:
    for enemy_rect in enemies:
      if player.colliderect(enemy_rect): return False
    for pipe_rect in pipes:
      if player.colliderect(pipe_rect):
        if player.top <= (pipe_rect.top + 220) or player.bottom >= (pipe_rect.bottom - 220): return False
  return True

def player_animation():
  global player_surf, boo_index

  boo_index += 0.1
  if boo_index >= len(boo_fly):boo_index = 0
  player_surf = pygame.transform.rotate(boo_fly[int(boo_index)], fall_angle)

# def mario_animation():
  global mario_surf, mario_index

# if player_rect.bottom < 340:
#   player_surf = mario_jump
  mario_index += 0.1
  if mario_index >= len(mario_walk):mario_index = 0
  mario_surf = mario_walk[int(mario_index)]


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Basics')
clock = pygame.time.Clock()
score_font = pygame.font.Font('font/MarioWorldPixel.ttf', 50)
game_active = False
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

mario = pygame.sprite.Group()



foreground_scroll = Foreground()
background_scroll = Background()

background_surf = pygame.image.load('graphics/mario_background.jpeg').convert()
background_surf = pygame.transform.scale(background_surf, WINDOW_SIZE)
ground_surf = pygame.image.load('graphics/mario_ground.png').convert()
ground_surf = pygame.transform.scale(ground_surf, (800, 60))
ground_rect = ground_surf.get_rect(midbottom = (400, 400))

#ENEMIES-----------
mario_walk1 = pygame.image.load('graphics/mario/Anibody1.png').convert_alpha()
mario_walk1 = pygame.transform.scale(mario_walk1, (50, 64))
mario_walk2 = pygame.image.load('graphics/mario/Anibody2.png').convert_alpha()
mario_walk2 = pygame.transform.scale(mario_walk2, (50, 64))
mario_walk3 = pygame.image.load('graphics/mario/Anibody3.png').convert_alpha()
mario_walk3 = pygame.transform.scale(mario_walk3, (50, 64))

mario_jump = pygame.image.load('graphics/Deadpool.png').convert_alpha()
mario_jump = pygame.transform.scale(mario_jump, (50, 64))

mario_walk = [mario_walk1, mario_walk3, mario_walk2, mario_walk3, mario_jump]
mario_index = 0
mario_surf = mario_walk[mario_index]
# mario_rect = mario_surf.get_rect(midbottom = (400, 340))
mario_gravity = 0

mario_rect_list = []

#OBSTACLES---------
pipes1_surf = pygame.image.load('graphics/pipes.png')
pipes1_surf = pygame.transform.scale(pipes1_surf, (85, 566))
pipes1_rect = pipes1_surf.get_rect(midbottom = (-100, 400))
pipes2_surf = pygame.image.load('graphics/pipes.png')
pipes2_surf = pygame.transform.scale(pipes2_surf, (85, 566))
pipes2_rect = pipes2_surf.get_rect(midbottom = (-100, 450))
pipes3_surf = pygame.image.load('graphics/pipes.png')
pipes3_surf = pygame.transform.scale(pipes3_surf, (85, 566))
pipes3_rect = pipes3_surf.get_rect(midbottom = (-100, 500))
pipes4_surf = pygame.image.load('graphics/pipes.png')
pipes4_surf = pygame.transform.scale(pipes4_surf, (85, 566))
pipes4_rect = pipes4_surf.get_rect(midbottom = (-100, 550))

pipes_rect_list = []
pipes_index = randint(0,4)

fall_angle = 0


#PLAYER------------
boo_fly1 = pygame.image.load('graphics/boo1.png').convert_alpha()
boo_fly1 = pygame.transform.scale(boo_fly1, (60, 60))

boo_fly2 = pygame.image.load('graphics/boo2.png').convert_alpha()
boo_fly2 = pygame.transform.scale(boo_fly2, (60, 60))

boo_fly = [boo_fly1, boo_fly2]
boo_index = 0
player_surf = boo_fly[boo_index]
player_gravity = 0

player_rect = player_surf.get_rect(midbottom = (400, 200))

#TEXT--------------
game_name = score_font.render('Mario Must Die!', True, ('White'))
game_name_rect = game_name.get_rect(center = (400, 50))

game_over = score_font.render('GAME OVER', True, ('White'))
game_over_rect = game_over.get_rect(center = (400, 50))

game_message = score_font.render('Press SPACE to GO', True, ('White'))
game_message_rect = game_message.get_rect(center = (400, 320))

#TIMERS------------------
obstacle_timer = pygame.USEREVENT + 1
pipes_timer = pygame.USEREVENT + 2
mario_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(obstacle_timer, 1500)
pygame.time.set_timer(pipes_timer, 1800)
pygame.time.set_timer(mario_animation_timer, 100)


while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    if game_active:
      if event.type == pygame.MOUSEBUTTONDOWN:
        if player_rect.collidepoint(event.pos):
          # if player_rect.bottom >= 340: (mario jump mechanic)
            player_gravity = -6
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
          # if player_rect.bottom >= 340: (mario jump mechanic)
            player_gravity = -6

# Randomisation of Enemies and Pipes-----------
      if event.type == obstacle_timer:
        mario.add(Mario('mario'))
        # if randint(0,2):
        #   mario_rect_list.append(mario_surf.get_rect(bottomright = (randint(-400, -100), 340)))
        # else:
        #   mario_rect_list.append(mario_surf.get_rect(bottomright = (randint(-400, -100), 340)))
      
      if event.type == pipes_timer:
        pipes_index = randint(0,4)
        if pipes_index == 0:
          pipes_rect_list.append(pipes1_surf.get_rect(bottomright = (randint(-250, -50), 400)))
        elif pipes_index == 1:
          pipes_rect_list.append(pipes2_surf.get_rect(bottomright = (randint(-250, -50), 450)))
        elif pipes_index == 2:
          pipes_rect_list.append(pipes3_surf.get_rect(bottomright = (randint(-250, -50), 400)))
        elif pipes_index == 3:
          pipes_rect_list.append(pipes4_surf.get_rect(bottomright = (randint(-250, -50), 550)))


      if event.type == mario_animation_timer:
        mario_index += 1
        for mario_rect in mario_rect_list:
          if mario_rect.bottom < 340:
            mario_index = 4
          if mario_rect.bottom == 340:
            if mario_index >= (len(mario_walk)-1):
              mario_index = 0
              mario_surf = mario_walk[int(mario_index)]
          if (score % 10) == 0:
            mario_gravity = -12
            
              

        
    else:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        player_rect.bottom = 200
        game_active = True
        start_time = pygame.time.get_ticks()


  

  if game_active:

    background_scroll.update()
    background_scroll.render()  
    foreground_scroll.update()
    foreground_scroll.render() 

    score = display_score()


    #PLAYER-----------------------
    fall_angle = int(player_gravity * 1.8)
    player_gravity += 0.5
    player_rect.y += player_gravity
    player_animation()
    #This creates floor (add to turn into mario jump mechanic)
    screen.blit(player_surf, player_rect)

    player.draw(screen)
    player.update()

    #ENEMY_MOVEMENT---------------
    mario_rect_list = enemy_movement(mario_rect_list)
    mario_gravity += 0.7
    for mario_rect in mario_rect_list:
      mario_rect.y += mario_gravity
      if mario_rect.bottom >= 340: mario_rect.bottom = 340

    mario.draw(screen)
    mario.update()


    #OBSTACLE_MOVMENT-------------
    pipes_rect_list = pipes_movement(pipes_rect_list)

    #COLLISION--------------------
    game_active = collisions(player_rect, mario_rect_list, pipes_rect_list)
    if player_rect.bottom >= 338:
      print(player_rect.bottom)
      game_active = False

  else:
    screen.fill('Red')
    screen.blit(player_surf, player_rect)
    score_message = score_font.render(f'You Flapped: {score}', True, 'White')
    score_message_rect = score_message.get_rect(center = (400, 320))
    mario_rect_list.clear()
    pipes_rect_list.clear()
    # player_rect.bottom = 200
    player_gravity = 0

    if score == 0:
      screen.blit(game_name, game_name_rect)
      screen.blit(game_message, game_message_rect)
      
    else: 
      screen.blit(score_message, score_message_rect)
      screen.blit(game_over, game_over_rect)



  pygame.display.update()
  clock.tick(60)


