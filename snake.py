import pygame
import random
from pygame.locals import *

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

bg_color = (64,64,64)
pixel_size = 20
border = 2
screen_width = 20
screen_height = 20

def tile_to_screen_position(tile_position,pixel_size=pixel_size):
    return (int(tile_position[0])*pixel_size,int(tile_position[1])*pixel_size)
    
def screen_position_to_tile(tile_position,pixel_size=pixel_size):
    return (int(tile_position[0])//pixel_size,int(tile_position[1])//pixel_size)
    
def collision(cel1,cel2):
    return (cel1[0] == cel2[0]) and (cel1[1] == cel2[1]) 

def snake_collision(obj,head_included=True):
    if head_included:
        first_pos = 0
    else:
        first_pos = 1

    for i in range(first_pos,len(snake)):
        if collision(obj,snake[i]):
            return True
    return False

def generate_apple_position():
    x = int (random.random()*screen_width)
    y = int (random.random()*screen_height)

    position = tile_to_screen_position((x,y))

    if not snake_collision(position):
        return position
    else:
        return generate_apple_position()

pygame.init()
clock = pygame.time.Clock()                                   
screen = pygame.display.set_mode(tile_to_screen_position((screen_width,screen_height)))
pygame.display.set_caption('PySnake')

snake = [tile_to_screen_position((screen_width//2,screen_height//2))]
snake_skin = pygame.Surface((pixel_size-border,pixel_size-border))
snake_skin.fill((0,255,0))

apple_pos = generate_apple_position()
apple = pygame.Surface((pixel_size-border,pixel_size-border))
apple.fill((255,0,0))

my_direction = LEFT

while True:
    clock.tick(10)
    already_move = False
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN and not already_move:
            if event.key == K_UP:
                if not my_direction == DOWN:
                    my_direction = UP
                    already_move = True
            if event.key == K_RIGHT:
                if not my_direction == LEFT:
                    my_direction = RIGHT
                    already_move = True
            if event.key == K_DOWN:
                if not my_direction == UP:
                    my_direction = DOWN
                    already_move = True
            if event.key == K_LEFT:
                if not my_direction == RIGHT:
                    my_direction = LEFT
                    already_move = True
                
    for i in range(len(snake)-1,0,-1):
        snake[i] = (snake[i-1][0],snake[i-1][1])
                
    if my_direction == UP:
        snake[0] = (snake[0][0],snake[0][1]-pixel_size)
        if snake[0][1] < 0:
            snake[0] = (snake[0][0],(screen_height-1)*pixel_size)        
    if my_direction == RIGHT:
        snake[0] = (snake[0][0]+pixel_size,snake[0][1])
        if snake[0][0] > (screen_width-1)*pixel_size:
            snake[0] = (0,snake[0][1])
    if my_direction == DOWN:
        snake[0] = (snake[0][0],snake[0][1]+pixel_size)
        if snake[0][1] > (screen_height-1)*pixel_size:
            snake[0] = (snake[0][0],0)
    if my_direction == LEFT:
        snake[0] = (snake[0][0]-pixel_size,snake[0][1])
        if snake[0][0] < 0:
            snake[0] = ((screen_width-1)*pixel_size,snake[0][1])

    if collision(snake[0],apple_pos):
        apple_pos = generate_apple_position()
        snake.append((-pixel_size*2,-pixel_size*2))

    if snake_collision(snake[0],False):
        break
    
    screen.fill(bg_color)

    for pos in snake:
        screen.blit(snake_skin,pos)

    screen.blit(apple,apple_pos)
    pygame.display.update()
