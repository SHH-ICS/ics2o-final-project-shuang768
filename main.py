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
fps=10
#https://github.com/shuang768/pacman-vaxman
#music
def music():
  pygame.mixer.init()
  pygame.mixer.music.load('pacman.mp3')
  pygame.mixer.music.play(-1, 0.0)

def pacman(image,lead_x,lead_y,value):
  if value >= len(image_sprite):
    value = 0
    image = image_sprite[value]
  gamedisplay.blit(image, (lead_x, lead_y))
  value += 1
 

music()
clock = pygame.time.Clock()
value = 0

lead_x=display_width/2
lead_y=display_height/2
  
lead_x_change=0
lead_y_change=0
exit =False
while not exit:
    clock.tick(fps)
  
    #https://www.geeksforgeeks.org/pygame-character-animation/
    #reference for animation
    if value >= len(image_sprite):
        value = 0
    image = image_sprite[value]
  
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
          exit=True
        if event.type == pygame.KEYDOWN:
          if event.key==pygame.K_LEFT:
            lead_x_change=-20
            lead_y_change=0
            #direction="left"
          elif event.key==pygame.K_RIGHT:
            lead_x_change=20
            lead_y_change=0
            #direction="right"
          elif event.key==pygame.K_UP:
            lead_y_change=-20
            lead_x_change=0
            #direction="up"
          elif event.key==pygame.K_DOWN:
            lead_y_change=20
            lead_x_change=0
           # direction="down"
        if event.type==pygame.KEYUP:
          if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
            lead_x_change=0
          elif event.key==pygame.K_UP or event.key==pygame.K_DOWN:
            lead_y_change=0
 
    lead_x+=lead_x_change
    lead_y+=lead_y_change
    #pacman(image,lead_x,lead_y,value)
    gamedisplay.blit(image, (lead_x, lead_y))
    pygame.display.update()
    gamedisplay.fill(Color('lightblue'))
    value += 1
