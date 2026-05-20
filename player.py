import pygame
from constants import *
from sprites import create_mouse_sprite

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.sprite = create_mouse_sprite()
    
    def move(self, dx, dy):
        """Move the player with boundary checking"""
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Check boundaries
        if new_x >= GAME_AREA_X and new_x <= GAME_AREA_X + GAME_AREA_WIDTH - self.width:
            self.x = new_x
        if new_y >= GAME_AREA_Y and new_y <= GAME_AREA_Y + GAME_AREA_HEIGHT - self.height:
            self.y = new_y
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
