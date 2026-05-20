import pygame
import random
from constants import *
from sprites import create_cheese_sprite

class Collectible:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = COLLECTIBLE_SIZE
        self.height = COLLECTIBLE_SIZE
        self.sprite = create_cheese_sprite()
    
    def respawn(self):
        """Move collectible to a random position within game area"""
        self.x = random.randint(GAME_AREA_X, GAME_AREA_X + GAME_AREA_WIDTH - self.width)
        self.y = random.randint(GAME_AREA_Y, GAME_AREA_Y + GAME_AREA_HEIGHT - self.height)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
