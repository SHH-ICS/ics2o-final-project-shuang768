import pygame, sys
from pygame.locals import QUIT
from pygame import Color, Rect
from pygame import draw
from pygame import display
from pygame import time
import random

#Pacman in Python with PyGame
#Adapted by Caitlin Ross from https://github.com/hbokmann/Pacman

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)

pacman_img = pygame.image.load('images/pacman.png')
pygame.display.set_icon(pacman_img)

#Add music
#pygame.mixer.init()
#pygame.mixer.music.load('pacman.mp3')
#pygame.mixer.music.play(-1, 0.0)


# This class represents the walls of the room
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, x, y, width, height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = pygame.sprite.RenderPlain()

    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [[0, 0, 6, 600], [0, 0, 806, 6], [0, 600, 806, 6],
             [806, 0, 6, 606], [300, 0, 6, 66], [60, 60, 186, 6],
             [360, 60, 186, 6], [60, 120, 66, 6], [60, 120, 6, 126],
             [180, 120, 246, 6], [300, 120, 6, 66], [480, 120, 66, 6],
             [540, 120, 6, 126], [120, 180, 126, 6], [120, 180, 6, 126],
             [360, 180, 126, 6], [480, 180, 6, 126], [180, 240, 6, 126],
             [180, 360, 246, 6], [420, 240, 6, 126], [240, 240, 42, 6],
             [324, 240, 42, 6], [240, 240, 6, 66], [240, 300, 126, 6],
             [360, 240, 6, 66], [0, 300, 66, 6], [540, 300, 66, 6],
             [60, 360, 66, 6], [60, 360, 6, 186], [480, 360, 66, 6],
             [540, 360, 6, 186], [120, 420, 366, 6], [120, 420, 6, 66],
             [480, 420, 6, 66], [180, 480, 246, 6], [300, 480, 6, 66],
             [120, 540, 126, 6], [360, 540, 126, 6], [600, 0, 6, 66],
             [660, 60, 96, 6], [600, 120, 6, 180], [600, 360, 6, 186],
             [660, 540, 96, 6], [600, 480, 206, 6], [660, 120, 6, 216],
             [660, 390, 6, 36], [660, 420, 96, 6], [660, 330, 66, 6],
             [720, 330, 6, 36], [720, 360, 36, 6], [720, 120, 86, 6],
             [720, 120, 6, 66], [720, 180, 36, 6], [750, 240, 6, 126],
             [660, 240, 36, 6]]

    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], Color('red'))
        wall_list.add(wall)
        all_sprites_list.add(wall)

    # return our new list
    return wall_list


def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate


# This class represents the block
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()


# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):

    # Set speed vector
    change_x = 0
    change_y = 0

    # Constructor function
    def __init__(self, x, y, filename, filename2):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set height, width
        self.sprite = []
        self.image = pygame.image.load(filename).convert()
        self.sprite.append(pygame.image.load(filename).convert())
        self.image = pygame.transform.rotate(self.image, 90).convert()
        self.sprite.append(self.image)
        self.image = pygame.transform.rotate(self.image, 90).convert()
        self.sprite.append(self.image)
        self.image = pygame.transform.rotate(self.image, 90)
        self.sprite.append(self.image)
        self.image = pygame.image.load(filename2).convert()
        self.sprite.append(self.image)
        self.current_sprites = 0
        # Make our top-left corner the passed-in location.
        self.rect = self.sprite[self.current_sprites].get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    # Find a new position for the player
    def update(self, walls, gate, direction, name):
        # Get the old position, in case we need to go back to it
        #imag=pygame.image.load(filename)
        if name == "pacman":
            self.current_sprites += 1
            #self.image=pygame.image.load(filename).convert()
            if direction == "right":
                #self.image=pygame.transform.rotate(self.image, 0).convert()
                self.image = self.sprite[0]
            elif direction == "left":
                #self.image=pygame.transform.rotate(self.image, 180).convert()
                self.image = self.sprite[2]
            elif direction == "up":
                #self.image=pygame.transform.rotate(self.image, 90).convert()
                self.image = self.sprite[1]
            elif direction == "down":
                #self.image=pygame.transform.rotate(self.image, 270).convert()
                self.image = self.sprite[3]
        #self.rect=self.image.get_rect()
            else:
                self.image = self.sprite[0]
            if self.current_sprites == 4:
                self.image = self.sprite[self.current_sprites]
                self.current_sprites = 0
        else:
            self.image = self.sprite[0]

        old_x = self.rect.left
        new_x = old_x + self.change_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left = old_x
        else:

            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top = old_y

        if gate != False:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y


#Inherits from Player
class Ghost(Player):
    # Change the speed of the ghost
    def changespeed(self, list, ghost, turn, steps, l):
        try:
            z = list[turn][2]
            if steps < z:
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps += 1
            else:
                if turn < l:
                    turn += 1
                elif ghost == "clyde":
                    turn = 2
                else:
                    turn = 1
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0, 0]


Pinky_directions = [[0, -30, 4], [15, 0, 9], [0, 15, 11], [-15, 0, 23],
                    [0, 15, 7], [15, 0, 3], [0, -15, 3], [15, 0,
                                                          19], [0, 15, 3],
                    [15, 0, 3], [0, 15, 3], [15, 0, 3], [0, -15, 15],
                    [-15, 0, 7], [0, 15, 3], [-15, 0, 19], [0, -15, 11],
                    [15, 0, 9]]

Blinky_directions = [[0, -15, 4], [15, 0, 9], [0, 15, 7], [15, 0, 7],
                     [0, 15, 15], [-15, 0, 3], [0, -15, 3], [-15, 0, 3],
                     [0, -15, 3], [-15, 0, 19], [0, 15, 3], [-15, 0, 3],
                     [0, 15, 3], [-15, 0, 3], [0, -15, 15], [15, 0, 7],
                     [0, -15, 7], [15, 0, 11], [0, -15, 3], [15, 0, 7],
                     [0, -15, 3], [-15, 0, 27], [0, 15, 11], [15, 0, 3],
                     [0, -15, 7], [15, 0, 11], [0, 15, 3], [15, 0, 1]]

Inky_directions = [
    [30, 0, 2],
    [0, -15, 4],
    [15, 0, 9],
    [0, 15, 7],
    [15, 0, 3],
    [0, -15, 3],
    [15, 0, 3],
    [0, -15, 15],
    [-15, 0, 15],
    [0, 15, 3],
    [15, 0, 29],
    [0, -15, 3],
    [-15, 0, 9],
    [0, 15, 21],
    [15, 0, 3],
    [0, 15, 1],
    [15, 0, 5],
    [0, -15, 11],
    [-15, 0, 5],
    [0, -15, 7],
    [-15, 0, 7],
    [0, 15, 11],
    [-15, 0, 3],
    [0, -15, 7],
    [-15, 0, 11],
    [0, 15, 3],
    [15, 0, 3],
    [0, 15, 7],
    [-15, 0, 11],
    [0, -15, 7],
    [15, 0, 5],
]

Clyde_directions = [[-30, 0, 2], [0, -15, 4], [15, 0, 5], [0, 15, 7],
                    [-15, 0, 11], [0, -15, 7], [-15, 0, 3], [0, 15, 7],
                    [-15, 0, 7], [0, 15, 15], [15, 0, 49], [0, -15, 3],
                    [-15, 0, 9], [0, 15, 3], [-15, 0, 3], [0, -15, 15],
                    [15, 0, 3], [0, 15, 7], [15, 0, 9], [0, -15, 15],
                    [-15, 0, 5], [0, -15, 7], [-15, 0, 27], [0, -15, 3],
                    [-15, 0, 15], [0, 15, 3], [15, 0, 7], [0, 15, 3],
                    [-15, 0, 3], [0, 15, 11], [15, 0, 3], [0, -15, 7],
                    [15, 0, 9]]
pinky_length = len(Pinky_directions) - 1
blinky_length = len(Blinky_directions) - 1
inky_length = len(Inky_directions) - 1
clyde_length = len(Clyde_directions) - 1

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 606x606 sized screen
screen = pygame.display.set_mode([811, 606])

# Set the title of the window
pygame.display.set_caption('Pacman, ics2o RST')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()

# Fill the screen with a black background
background.fill(black)

clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

pygame.display.update()
#default x and y beginning locations (to avoid duplicate calculations)
default_y = (4 * 60) + 19
defaut_x = 303 - 16

#Beginning locations for Pacman and ghosts
pacman_y = (7 * 60) + 19
pacman_x = defaut_x
pinky_y = default_y
pinky_x = defaut_x
blinky_y = (3 * 60) + 19
blinky_x = defaut_x
inky_y = default_y
inky_x = 303 - 16 - 32
clyde_y = default_y
clyde_x = 303 + (32 - 16)


def startGame(fps):
    pygame.mixer.init()
    pygame.mixer.music.load('pacman1.mp3')
    pygame.mixer.music.play(-1, 0.0)
    direction = "right"
    #Initialize lists
    all_sprites_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()
    ghost_list = pygame.sprite.RenderPlain()
    pacman_collide = pygame.sprite.RenderPlain()
    wall_list = setupRoomOne(all_sprites_list)
    gate = setupGate(all_sprites_list)

    pinky_turn = 0
    pinky_steps = 0

    blinky_turn = 0
    blinky_steps = 0

    inky_turn = 0
    inky_steps = 0

    clyde_turn = 0
    clyde_steps = 0

    # Create the player paddle object
    Pacman = Player(pacman_x, pacman_y, "images/pacman.png",
                    "images/pacman (2).png")
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)

    Blinky = Ghost(blinky_x, blinky_y, "images/Blinky.png",
                   "images/Blinky.png")
    ghost_list.add(Blinky)
    all_sprites_list.add(Blinky)

    Pinky = Ghost(pinky_x, pinky_y, "images/Pinky.png", "images/Pinky.png")
    ghost_list.add(Pinky)
    all_sprites_list.add(Pinky)

    Inky = Ghost(inky_x, inky_y, "images/Inky.png", "images/Inky.png")
    ghost_list.add(Inky)
    all_sprites_list.add(Inky)

    Clyde = Ghost(clyde_x, clyde_y, "images/Clyde.png", "images/Clyde.png")
    ghost_list.add(Clyde)
    all_sprites_list.add(Clyde)
#19,26
    # Draw the grid
    for row in range(19):
        for column in range(26):
            if (row == 7 or row == 8) and (column == 8 or column == 9
                                           or column == 10):
                continue
            else:
                block = Block(yellow, 4, 4)

                # Set a random location for the block
                block.rect.x = (30 * column + 6) + 26
                block.rect.y = (30 * row + 6) + 26

                b_collide = pygame.sprite.spritecollide(
                    block, wall_list, False)
                p_collide = pygame.sprite.spritecollide(
                    block, pacman_collide, False)

                if b_collide:
                    continue
                elif p_collide:
                    continue
                else:
                    # Add the block to the list of objects
                    block_list.add(block)
                    all_sprites_list.add(block)

                    block_list_length = len(block_list)*2

    score = 0

    done=True
    while done == True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done==False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(-30, 0)
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    Pacman.changespeed(30, 0)
                    direction = "right"
                elif event.key == pygame.K_UP:
                    Pacman.changespeed(0, -30)
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, 30)
                    direction = "down"

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(30, 0)
                elif event.key == pygame.K_RIGHT:
                    Pacman.changespeed(-30, 0)
                elif event.key == pygame.K_UP:
                    Pacman.changespeed(0, 30)
                elif event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, -30)
        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        Pacman.update(wall_list, gate, direction, "pacman")

        returned = Pinky.changespeed(Pinky_directions, False, pinky_turn,
                                     pinky_steps, pinky_length)
        pinky_turn = returned[0]
        pinky_steps = returned[1]
        Pinky.changespeed(Pinky_directions, False, pinky_turn, pinky_steps,
                          pinky_length)
        Pinky.update(wall_list, False, direction, "pinky")

        returned = Blinky.changespeed(Blinky_directions, False, blinky_turn,
                                      blinky_steps, blinky_length)
        blinky_turn = returned[0]
        blinky_steps = returned[1]
        print(returned[0], returned[1])
        Blinky.changespeed(Blinky_directions, False, blinky_turn, blinky_steps,
                           blinky_length)
        Blinky.update(wall_list, False, direction, "blinky")

        returned = Inky.changespeed(Inky_directions, False, inky_turn,
                                    inky_steps, inky_length)
        inky_turn = returned[0]
        inky_steps = returned[1]
        Inky.changespeed(Inky_directions, False, inky_turn, inky_steps,
                         inky_length)
        Inky.update(wall_list, False, direction, "inky")

        returned = Clyde.changespeed(Clyde_directions, "clyde", clyde_turn,
                                     clyde_steps, clyde_length)
        clyde_turn = returned[0]
        clyde_steps = returned[1]
        Clyde.changespeed(Clyde_directions, "clyde", clyde_turn, clyde_steps,
                          clyde_length)
        Clyde.update(wall_list, False, direction, "clyde")

        # See if the Pacman block has collided with anything.
        blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)

        # Check the list of collisions.
        if len(blocks_hit_list) > 0:
            score += len(blocks_hit_list)
        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
        if score == (block_list_length/2):
          for row in range(19):
            for column in range(26):
              if (row == 7 or row == 8) and (column == 8 or column == 9
                                             or column == 10):
                  continue
              else:
                  block = Block(blue, 4, 4)
  
                  # Set a random location for the block
                  block.rect.x = (30 * column + 6) + 26
                  block.rect.y = (30 * row + 6) + 26
  
                  b_collide = pygame.sprite.spritecollide(
                      block, wall_list, False)
                  p_collide = pygame.sprite.spritecollide(
                      block, pacman_collide, False)
  
                  if b_collide:
                      continue
                  elif p_collide:
                      continue
                  else:
                      # Add the block to the list of objects
                      block_list.add(block)
                      all_sprites_list.add(block)
  

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        screen.fill(black)

        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        ghost_list.draw(screen)

        highscore(score)
        if score>=block_list_length: 
            text = font.render("Score: " + str(block_list_length) + "/" + str(block_list_length), True, red)
            screen.blit(text, [10, 10])
            doNext("Congratulations, you won!", 285, all_sprites_list,
                   block_list, ghost_list, pacman_collide, wall_list, gate)
        text = font.render("Score: " + str(score) + "/" + str(block_list_length), True, red)
        screen.blit(text, [10, 10])
      
        
        ghost_hit_list = pygame.sprite.spritecollide(Pacman, ghost_list, False)

        if ghost_hit_list:
            pygame.mixer.music.unload()
            pygame.mixer.init()
            pygame.mixer.music.load('pacman die.mp3')
            pygame.mixer.music.play(1, 0.0)
            doNext("Game Over", 375, all_sprites_list, block_list, ghost_list,
                   pacman_collide, wall_list, gate)
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        #UPDATE THE GAME
        pygame.display.flip()
        clock.tick(fps)


def doNext(message, left, all_sprites_list, block_list, ghost_list,
           pacman_collide, wall_list, gate):
    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del block_list
                    del ghost_list
                    del pacman_collide
                    del wall_list
                    del gate
                    intro(" "," ")
        #ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        #Grey background
        w = pygame.Surface((400, 200))  # the size of your rect
        w.set_alpha(10)  # alpha level
        w.fill((128, 128, 128))  # this fills the entire surface
        screen.blit(w, (255, 200))  # (0,0) are the top-left coordinates

        #Won or lost
        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [265, 303])
        text3 = font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [265, 333])
        #ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        #UPDATE THE GAME
        pygame.display.flip()
        clock.tick(15)


def intro(text, text4):
    pygame.init()
  
    # Create an 606x606 sized screen
    screen = pygame.display.set_mode([811, 606])
    
    # Set the title of the window
    pygame.display.set_caption('Pacman')
    
    # Create a surface we can draw on
    background = pygame.Surface(screen.get_size())
    
    # Used for converting color maps and such
    background = background.convert()
    
    # Fill the screen with a black background
    background.fill(black)
    
    clock = pygame.time.Clock()
    
    pygame.font.init()
    
    pygame.display.update()
    intro=True
    while intro:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_1:
                    startGame(10)
                if event.key == pygame.K_2:
                    startGame(15)
                if event.key == pygame.K_3:
                    startGame(20)
        #ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        #Grey background
        w = pygame.Surface((400, 200))  # the size of your rect
        w.set_alpha(10)  # alpha level
        w.fill((128, 128, 128))  # this fills the entire surface
        screen.blit(w, (255, 200))  # (0,0) are the top-left coordinates

        smallfont = pygame.font.SysFont("freesansbold.ttf", 25)
        #Won or lost
        text1 = smallfont.render(text, True, white)
        screen.blit(text1, [260, 233])
        text3 = smallfont.render(text4, True, white)
        screen.blit(text3, [265, 263])
        text2 = smallfont.render("press 1 for slow, 2 for medium, 3 for fast",
                                 True, white)
        screen.blit(text2, [265, 303])
        text5 = smallfont.render("To quit, press ESCAPE.", True, white)
        screen.blit(text5, [265, 333])
        #ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        #UPDATE THE GAME
        pygame.display.flip()
        clock.tick(15)

def highscore(score):
  smallfont = pygame.font.SysFont("freesansbold.ttf", 40)
  try:
    inFile = open('highscore', 'r')
    lin= inFile.readlines()
    line=int(lin[-1])
  except ValueError:
    filehandle = open('highscore','w')
    filehandle.write("0")
    filehandle.close()
    inFile = open('highscore', 'r')
    lin= inFile.readlines()
    line=int(lin[-1])
  if score>line:
    filehandle = open('highscore','w')
    filehandle.write(str(score))
    filehandle.close()
    text=smallfont.render("highscore: "+str(score),True,Color('red'))
    screen.blit(text,[610,10])
  elif score<=line:
    text=smallfont.render("highscore: "+str(line), True, Color('red'))
    screen.blit(text,[610,10])
    
intro("welcome to pacman, your goal is to eat all target",
      "do not get hit by ghost, use arrowkey")
startGame()

pygame.quit()
