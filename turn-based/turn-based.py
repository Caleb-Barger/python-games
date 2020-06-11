import pygame, sys, random
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Turn Based Combat! (sorta...)")

clock = pygame.time.Clock()

WINDOW_SIZE = (900, 600)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

display = pygame.Surface((300,200))

class Player:
    
    current_action = 'attack'
    actions = ['attack', 'item', 'run']
    selector_positions = [(138,120),(138,130),(138,140)]
    selector_position = selector_positions[0]
    

    def next_action(self):
        current_index = self.actions.index(self.current_action)
        if current_index + 1 <= len(self.actions) - 1:
            current_index += 1
        self.current_action = self.actions[current_index]
        self.selector_position = self.selector_positions[current_index]
        print(self.current_action)

    def prev_action(self):
        current_index = self.actions.index(self.current_action)
        if current_index - 1 >= 0:
            current_index -= 1
        self.current_action = self.actions[current_index]
        self.selector_position = self.selector_positions[current_index]
        print(self.current_action)

    def get_selector_position(self):
        return self.selector_position
        
            
            

player = Player()

enemy = pygame.image.load('enemy.png')

selector = pygame.Surface((10,10))
selector.fill((100,50,244))
selector_rect = selector.get_rect()

player_actions = pygame.Surface((45, 60))
player_actions.fill((255, 255, 0))
player_actions_rect = player_actions.get_rect()
player_actions_rect.x = 134
player_actions_rect.y = 120

while True:

    display.fill((100, 200, 244))
    display.blit(enemy, (134, 10))
    display.blit(player_actions, (player_actions_rect.x, player_actions_rect.y))
    display.blit(selector, (player.get_selector_position()))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_w:
                player.prev_action()
            if event.key == K_s:
                player.next_action()

    
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
    pygame.display.flip()
    clock.tick(60)
