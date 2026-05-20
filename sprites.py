import pygame
from constants import PLAYER_SIZE, GRAY, PINK, BLACK, ORANGE, YELLOW, WHITE, ENEMY_SIZE, COLLECTIBLE_SIZE

class Sprite:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        print(f"Drawing sprite at ({self.x}, {self.y})")

def create_mouse_sprite():
    """Create a simple mouse sprite"""
    surface = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
    
    # Body (gray)
    pygame.draw.ellipse(surface, GRAY, (5, 10, 22, 18))
    
    # Head (gray)
    pygame.draw.circle(surface, GRAY, (20, 15), 10)
    
    # Ears (pink inside, gray outside)
    pygame.draw.circle(surface, GRAY, (15, 5), 5)
    pygame.draw.circle(surface, PINK, (15, 5), 3)
    pygame.draw.circle(surface, GRAY, (25, 5), 5)
    pygame.draw.circle(surface, PINK, (25, 5), 3)
    
    # Eyes (black)
    pygame.draw.circle(surface, BLACK, (18, 13), 2)
    pygame.draw.circle(surface, BLACK, (22, 13), 2)
    
    # Nose (pink)
    pygame.draw.circle(surface, PINK, (28, 15), 2)
    
    # Tail (gray)
    pygame.draw.line(surface, GRAY, (5, 15), (0, 10), 2)
    pygame.draw.line(surface, GRAY, (0, 10), (2, 5), 2)
    
    return surface

def create_cat_sprite():
    """Create a simple cat sprite"""
    surface = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE), pygame.SRCALPHA)
    
    # Body (orange)
    pygame.draw.ellipse(surface, ORANGE, (5, 12, 22, 16))
    
    # Head (orange)
    pygame.draw.circle(surface, ORANGE, (20, 15), 10)
    
    # Ears (orange with pink inside)
    pygame.draw.polygon(surface, ORANGE, [(12, 5), (15, 0), (18, 5)])
    pygame.draw.polygon(surface, PINK, [(13, 5), (15, 2), (17, 5)])
    pygame.draw.polygon(surface, ORANGE, [(23, 5), (26, 0), (29, 5)])
    pygame.draw.polygon(surface, PINK, [(24, 5), (26, 2), (28, 5)])
    
    # Eyes (yellow)
    pygame.draw.circle(surface, YELLOW, (17, 13), 3)
    pygame.draw.circle(surface, YELLOW, (23, 13), 3)
    pygame.draw.circle(surface, BLACK, (17, 13), 1)
    pygame.draw.circle(surface, BLACK, (23, 13), 1)
    
    # Nose (pink)
    pygame.draw.circle(surface, PINK, (20, 17), 2)
    
    # Whiskers
    pygame.draw.line(surface, WHITE, (15, 16), (10, 15), 1)
    pygame.draw.line(surface, WHITE, (15, 17), (10, 17), 1)
    pygame.draw.line(surface, WHITE, (25, 16), (30, 15), 1)
    pygame.draw.line(surface, WHITE, (25, 17), (30, 17), 1)
    
    return surface

def create_cheese_sprite():
    """Create a simple cheese sprite"""
    surface = pygame.Surface((COLLECTIBLE_SIZE, COLLECTIBLE_SIZE), pygame.SRCALPHA)
    
    # Cheese wedge (yellow)
    pygame.draw.polygon(surface, YELLOW, [(5, 5), (27, 5), (16, 27)])
    
    # Holes (white)
    pygame.draw.circle(surface, WHITE, (12, 12), 3)
    pygame.draw.circle(surface, WHITE, (20, 12), 2)
    pygame.draw.circle(surface, WHITE, (16, 20), 2)
    
    return surface
