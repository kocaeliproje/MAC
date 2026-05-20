import pygame
import random
from constants import *
from sprites import create_cat_sprite

# Pygame'in sprite grubuna dahil olabilmesi için (pygame.sprite.Sprite) miras aldık
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=None):
        super().__init__()
        
        # Orijinal kedi görseli
        self.image_original = create_cat_sprite()
        # Aynalanmış (ters çevrilmiş) kedi görseli
        self.image_flipped = pygame.transform.flip(self.image_original, True, False)
        
        # Varsayılan başlangıç görseli
        self.image = self.image_original
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        if speed is None:
            self.speed = random.uniform(2, 4)
        else:
            self.speed = speed
        
        self.direction = random.choice([
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ])
        
        # İlk yöne göre görseli ayarla
        self.adjust_direction_image()
    
    def adjust_direction_image(self):
        """Kedinin gittiği yatay yöne göre bakış açısını günceller"""
        if self.direction[0] > 0:
            # Sağa doğru gidiyorsa (Burayı sprite'ınızın duruşuna göre ayarlayabilirsiniz)
            self.image = self.image_original
        else:
            # Sola doğru gidiyorsa
            self.image = self.image_flipped

    def update(self):
        """Düşman hareketini günceller ve duvarlardan sektirir"""
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        
        # Oyun alanı sınırlarından sekme kontrolü
        if self.rect.left < GAME_AREA_X or self.rect.right > GAME_AREA_X + GAME_AREA_WIDTH:
            self.direction = (-self.direction[0], self.direction[1])
            # Duvara çarpıp yön değiştirdiğinde görseli güncelle:
            self.adjust_direction_image()
            
        if self.rect.top < GAME_AREA_Y or self.rect.bottom > GAME_AREA_Y + GAME_AREA_HEIGHT:
            self.direction = (self.direction[0], -self.direction[1])
            # Dikey sekmede x yönü değişmez ama fonksiyonu çağırmak güvenlidir
            self.adjust_direction_image()