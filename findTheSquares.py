import pygame, sys, random
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Find All The Squares!")

clock = pygame.time.Clock()

WINDOW_SIZE = (900, 600)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

display = pygame.Surface((300,200))

true_scroll = [0, 0]

moving_right = False
moving_left = False
moving_up = False
moving_down = False

player = pygame.Surface((30, 30))
player.fill((0,255,0))
player_rect = player.get_rect()

class GameState:
    def __init__(self):
        self.food_to_go = 10
        self.food_list = []
        self.bg_color = ((255, 100, 100))
        self.may_reset_or_exit = False

    def set_bg_color(self, new_color):
        self.bg_color = new_color

    def game_won(self):
        self.may_reset_or_exit = True

    def reset(self):
        self.food_to_go = 10
        self.may_reset_or_exit = False

game_state = GameState()

class Food:
    def __init__(self, x, y):
        self.food = pygame.Surface((15, 15))
        self.food.fill((0, 255, 255))
        self.food_rect = (0, 0)
        self.x = x
        self.y = y

    def get_rect(self):
        self.food_rect = self.food.get_rect()
        self.food_rect.x = self.x
        self.food_rect.y = self.y


def move(rect, movement):
    rect.x += movement[0]
    rect.y += movement[1]
    return rect

def find_new_pos(rect):
    rect.x = (random.randint(0, display.get_rect().width) - rect.width)
    rect.y = (random.randint(0, display.get_rect().height) - rect.height)
    return rect

def player_got_food(player_rect, food_rect, player, state):
    hit = False
    if player_rect.colliderect(food_rect):
        food_rect = find_new_pos(food_rect)
        player.fill((random.randint(0,255), 0, 255))
        game_state.food_to_go -= 1
        hit = True
    return player, food_rect, game_state, hit

while True:
    display.fill(game_state.bg_color)

    true_scroll[0] += (player_rect.x-true_scroll[0]-130)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-100)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    
    if len(game_state.food_list) < game_state.food_to_go:
        newFood = Food(random.randint(0,300), random.randint(0,300))
        newFood.get_rect()
        game_state.food_list.append(newFood)

    for food in game_state.food_list:
        display.blit(food.food, (food.food_rect.x-true_scroll[0], food.food_rect.y-true_scroll[1]))
        player, food.food_rect, game_state, hit = player_got_food(player_rect, food.food_rect, player, game_state)
        if hit:
            game_state.food_list.remove(food)
            print("FOOD LEFT - ", game_state.food_to_go)
            game_state.set_bg_color((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        if game_state.food_to_go == 0:
            game_state.game_won()

    player_movement = [0,0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    if moving_up:
        player_movement[1] -= 2
    if moving_down:
        player_movement[1] += 2

    player_rect = move(player_rect, player_movement)

    display.blit(player, (player_rect.x-scroll[0], player_rect.y-scroll[1]))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_w:
                moving_up = True
            if event.key == K_s:
                moving_down = True
            if event.key == K_x and game_state.may_reset_or_exit:
                pygame.quit()
                sys.exit()
            if event.key == K_SPACE and game_state.may_reset_or_exit:
                game_state.reset()
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
            if event.key == K_w:
                moving_up = False
            if event.key == K_s:
                moving_down = False


    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
    pygame.display.flip()
    clock.tick(60)
