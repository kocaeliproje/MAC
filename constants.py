import pygame

# Ekran boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Oyun alanı
GAME_AREA_X = 50
GAME_AREA_Y = 50
GAME_AREA_WIDTH = 700
GAME_AREA_HEIGHT = 500

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)       
ORANGE = (255, 165, 0)

# Oyuncu ayarları
PLAYER_SIZE = 40
PLAYER_SPEED = 5

# Düşman ve Nesne Boyutları
ENEMY_SIZE = 40              
COLLECTIBLE_SIZE = 32     

# Skor ayarları
SCORE_PER_CHEESE = 1     # Her peynir yendiğinde alınacak puan
PEYNIR_HEDEFI = 10        # Her level için yenmesi gereken peynir sayısı
POINTS_PER_LEVEL = SCORE_PER_CHEESE * PEYNIR_HEDEFI  # 10 puan olunca level atlayacak 
MAX_LEVEL = 10            # Toplam 10 level

# Level bazlı düşman ayarları
# Her level için: (düşman sayısı, minimum hız, maksimum hız)
LEVEL_CONFIG = {
    1: (1, 2, 3),   # 1 düşman, hız 2-3
    2: (2, 2, 3),   # 2 düşman, hız 2-3
    3: (3, 2, 4),   # 3 düşman, hız 2-4
    4: (4, 2, 4),   # 4 düşman, hız 2-4
    5: (5, 3, 5),   # 5 düşman, hız 3-5
    6: (6, 3, 5),   # 6 düşman, hız 3-5
    7: (7, 3, 6),   # 7 düşman, hız 3-6
    8: (8, 4, 6),   # 8 düşman, hız 4-6
    9: (9, 5, 7),   # 9 düşman, hız 5-7 (son 2 level - hızlı)
    10: (10, 6, 8), # 10 düşman, hız 6-8 (son 2 level - çok hızlı)
}

# Düşman hız çarpanı (son 2 level için)
FAST_LEVEL_MULTIPLIER = 1.1
