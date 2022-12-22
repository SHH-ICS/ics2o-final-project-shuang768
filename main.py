import pygame, sys
from pygame.locals import QUIT
from pygame import Color, Rect
from pygame import draw
from pygame import display
from pygame import time
import random

pygame.init()
display_width=800
display_height=800
gamedisplay = display.set_mode((display_width,display_height))
gamedisplay.fill(Color("lightblue"))
image_sprite = [pygame.image.load("pacman.png"),
                pygame.image.load("pacman1.png")]

#Classify the walls
#https://github.com/shuang768/pacman-vaxman(1)
class Wall (pygame.sprite.Sprite):
  def __init__(self,x,y,width,height,color):
    pygame.sprite.Sprite.__init__(self)

    width=int(width)
    height=int(height)
    
    self.image = pygame.Surface((width,height))
    self.image.fill(Color(color))

    self.rect=self.image.get_rect()
    self.rect.top=y
    self.rect.left=x
    
#create walls
#(2)
def wall(all_sprite_list):
  wall_list=pygame.sprite.Group()
  
  walls = [ [0,0,6,600],
              [0,0,600,6]]
  
  for item in walls:
    wall=Wall(item[0],item[1],item[2],item[3],Color('blue'))
    wall_list.add(wall)
    all_sprite_list.add(wall)
         
  # return our new list
  return wall_list
class Player(pygame.sprite.Sprite):
  
    # Set speed vector
    change_x=0
    change_y=0
  
    # Constructor function
    def __init__(self,x,y, filename,filename1):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
   
        # Set height, width
        self.image = pygame.image.load(filename1)
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
          
    # Find a new position for the player
    def update(self,walls):
        # Get the old position, in case we need to go back to it
        
        old_x=self.rect.left
        new_x=old_x+self.change_x
        self.rect.left = new_x
        
        old_y=self.rect.top
        new_y=old_y+self.change_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left=old_x
        else:

            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top=old_y


fps=10
pacmanthick=20
#https://github.com/shuang768/pacman-vaxman
#music
def music():
  pygame.mixer.init()
  pygame.mixer.music.load('pacman.mp3')
  pygame.mixer.music.play(-1, 0.0)

def pacman(image_sprite,lead_x,lead_y,value,ox,oy,walls):
  image_sprite[value].rect=image_sprite[value].image.get_rect()
  image_sprite[value].rect.top=lead_y
  image_sprite[value].rect.left=lead_x
  if lead_x !=ox or lead_y!=oy:
    if value % 2==0:
      value = 0
      value+=1
  x_collide=pygame.sprite.spritecollide(image_sprite[value],walls,False)
  if x_collide:
    lead_x=ox
  else:
      player=image_sprite[value]
      y_collide = pygame.sprite.spritecollide(player, walls, False)
      if y_collide:
      # Whoops, hit a wall. Go back to the old position
        image_sprite[value].rect.top=ox
    
    
  gamedisplay.blit(image_sprite[value], (lead_x, lead_y))
  value += 1
 
def gameloop():
  music()

  all_sprites_list = pygame.sprite.RenderPlain()
 # block_list = pygame.sprite.RenderPlain()
 # ghost_list = pygame.sprite.RenderPlain()
  pacman_collide = pygame.sprite.RenderPlain()
  wall_list = wall(all_sprites_list)
 # gate = setupGate(all_sprites_list)

  clock = pygame.time.Clock()
  value = 0
  
  pacman_x=display_width/2
  pacman_y=display_height/2
    
  lead_x_change=0
  lead_y_change=0

  Pacman = Player(pacman_x, pacman_y, 'pacman.png','pacman1.png' )
  all_sprites_list.add(Pacman)
  pacman_collide.add(Pacman)
  
  exit =False
  while not exit:
      clock.tick(20)
      old_x=pacman_x
      old_y=pacman_y
    
      #https://www.geeksforgeeks.org/pygame-character-animation/
      #reference for animation
     # if value >= len(image_sprite):
     #     value = 0
     # image = image_sprite[value]

      for event in pygame.event.get():
          if event.type==pygame.QUIT:
            exit=True
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(-20,0)
              elif event.key == pygame.K_RIGHT:
                  Pacman.changespeed(20,0)
              elif event.key == pygame.K_UP:
                  Pacman.changespeed(0,-20)
              elif event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,20)

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(20,0)
              elif event.key == pygame.K_RIGHT:
                  Pacman.changespeed(-20,0)
              elif event.key == pygame.K_UP:
                  Pacman.changespeed(0,20)
              elif event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,-20)
          #if event.type == pygame.KEYDOWN:
          #  if event.key==pygame.K_LEFT:
          #    lead_x_change=-20
          #    lead_y_change=0
          #    #direction="left"
          #  elif event.key==pygame.K_RIGHT:
          #    lead_x_change=20
          #    lead_y_change=0
          #    #direction="right"
          #  elif event.key==pygame.K_UP:
          #    lead_y_change=-20
          #    lead_x_change=0
          #    #direction="up"
          #  elif event.key==pygame.K_DOWN:
          #    lead_y_change=20
          #    lead_x_change=0
          #   # direction="down"
          #if event.type==pygame.KEYUP:
          #  if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
          #    lead_x_change=0
          #  elif event.key==pygame.K_UP or event.key==pygame.K_DOWN:
          #    lead_y_change=0
   
      pacman_x+=lead_x_change
      pacman_y+=lead_y_change
      Pacman.update(wall_list)
      #pacman(image,lead_x,lead_y,value)
     # pacman(image_sprite, lead_x, lead_y,value,old_x,old_y,wall_list)
      wall_list.draw(gamedisplay)
     # gate.draw(screen)
      all_sprites_list.draw(gamedisplay)
     # ghost_list.draw(screen)
      pygame.display.update()
      clock.tick(20)
      gamedisplay.fill(Color('lightblue'))
      #value += 1
    
gameloop()