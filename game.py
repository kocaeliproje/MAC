import pygame
import sys
import random
from constants import *
from sprites import create_mouse_sprite, create_cat_sprite, create_cheese_sprite
from enemy import Enemy

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Orijinal görseli yükle (Varsayılan olarak sağa veya sola bakıyor olabilir)
        self.image_original = create_mouse_sprite()
        
        # Görselin yatayda (sağa/sola) tam tersini (ayna görüntüsünü) oluştur
        self.image_flipped = pygame.transform.flip(self.image_original, True, False)
        
        # Aktif olan görsel (Başlangıçta orijinal olanı seçelim)
        self.image = self.image_original
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PLAYER_SPEED
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        # Sola giderken
        if keys[pygame.K_LEFT] and self.rect.x > GAME_AREA_X:
            self.rect.x -= self.speed
            # Sola giderken ters çevrilmiş (flipped) görseli seçiyoruz:
            self.image = self.image_flipped  
            
        # Sağa giderken
        if keys[pygame.K_RIGHT] and self.rect.x < GAME_AREA_X + GAME_AREA_WIDTH - self.image.get_width():
            self.rect.x += self.speed
            # Sağa giderken orijinal görseli seçiyoruz:
            self.image = self.image_original
            
        if keys[pygame.K_UP] and self.rect.y > GAME_AREA_Y:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < GAME_AREA_Y + GAME_AREA_HEIGHT - self.image.get_height():
            self.rect.y += self.speed

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Pygame grubu için 'image' ve 'rect' zorunludur
        self.image = create_cheese_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def respawn(self):
        # Peyniri rastgele bir yere ışınla
        self.rect.x = random.randint(GAME_AREA_X, GAME_AREA_X + GAME_AREA_WIDTH - self.image.get_width())
        self.rect.y = random.randint(GAME_AREA_Y, GAME_AREA_Y + GAME_AREA_HEIGHT - self.image.get_height())

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mouse vs Cat Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Oyun Durumu: "START" (Giriş Ekranı) veya "PLAYING" (Oyun Modu)
        self.state = "START"
        
        # Sprite grupları
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        
        # Oyuncu oluştur (Fare)
        self.player = Player(GAME_AREA_X + 100, GAME_AREA_Y + 100)
        self.all_sprites.add(self.player)
        
        # Skor ve Level
        self.score = 0
        self.level = 1

        # DOSYADAN REKORU OKUMA ----
        self.high_score_file = "rekor.txt"
        self.high_score = self.load_high_score()
        # -------------------------------------
        
        # Kolektibl oluştur (Peynir)
        self.collectible = Collectible(GAME_AREA_X + 500, GAME_AREA_Y + 200)
        self.all_sprites.add(self.collectible)
        self.collectibles.add(self.collectible)
        
        # Giriş ekranında gösterilecek önizleme sprite yüzeyleri
        self.menu_mouse = create_mouse_sprite()
        self.menu_cheese = create_cheese_sprite()
        self.menu_cat = create_cat_sprite()
        
        # İlk level için düşmanları oluştur
        self.spawn_enemies_for_level()
        
        # Ses dosyaları
        self.collision_sound = None
        self.collect_sound = None  
        try:
            self.collision_sound = pygame.mixer.Sound('collision.wav')
        except:
            pass

        try:
            self.collect_sound = pygame.mixer.Sound('collect.wav')  
        except:
            pass

    def load_high_score(self):
        """Dosyadan en yüksek skoru okur, dosya yoksa 0 döner ve dosyayı yaratır"""
        try:
            with open(self.high_score_file, "r") as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            with open(self.high_score_file, "w") as f:
                f.write("0")
            return 0

    def save_high_score(self):
        """Yeni rekoru dosyaya kaydeder"""
        with open(self.high_score_file, "w") as f:
            f.write(str(self.high_score))

    def spawn_enemies_for_level(self):
        """Mevcut level için düşmanları oluştur"""
        # Önceki düşmanları temizle
        for enemy in self.enemies:
            self.all_sprites.remove(enemy)
        self.enemies.empty()
        
        # Level konfigürasyonunu al
        level_config = LEVEL_CONFIG.get(self.level, LEVEL_CONFIG[1])
        enemy_count, min_speed, max_speed = level_config
        
        # Son 2 level için hız çarpanı uygula
        if self.level >= 9:
            min_speed *= FAST_LEVEL_MULTIPLIER
            max_speed *= FAST_LEVEL_MULTIPLIER
        
        # Yeni düşmanları oluştur
        for i in range(enemy_count):
            x = random.randint(GAME_AREA_X, GAME_AREA_X + GAME_AREA_WIDTH - 50)
            y = random.randint(GAME_AREA_Y, GAME_AREA_Y + GAME_AREA_HEIGHT - 50)
            speed = random.uniform(min_speed, max_speed)
            enemy = Enemy(x, y, speed)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # Giriş ekranındayken herhangi bir tuşa basılırsa oyunu başlat
                elif self.state == "START":
                    self.state = "PLAYING"
        return self.running
    
    def update(self):
        # Oyun sadece "PLAYING" durumundaysa hareketler ve çarpışmalar hesaplanır
        if self.state == "PLAYING":
            self.all_sprites.update()
            
            # Kedi fareyi yakaladı mı?
            if pygame.sprite.spritecollide(self.player, self.enemies, False):
                if self.collision_sound:
                    self.collision_sound.play()
                    pygame.time.delay(500)
                print(f"Oyun Bitti! Level: {self.level}, Skor: {self.score}")
                print("Kediyi besledin. :(")
                self.running = False
            
            # Fare peyniri yedi mi?
            if pygame.sprite.spritecollide(self.player, self.collectibles, False):
                self.score += SCORE_PER_CHEESE 
                print(f"Skor: {self.score}")
                
                # Sesi oynat mantığı hizalandı
                if self.collect_sound:
                    self.collect_sound.play()

                # REKOR KONTROLÜ VE KAYDETME 
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
                
                # Level kontrolü
                new_level = (self.score // POINTS_PER_LEVEL) + 1
                if new_level > self.level and new_level <= MAX_LEVEL:
                    self.level = new_level
                    print(f"Level {self.level}!")
                    self.spawn_enemies_for_level()
                
                # Peyniri yok etmek yerine haritada başka yere ışınlayalım
                self.collectible.respawn()
    
    def draw(self):
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        
        if self.state == "START":
            # --- GİRİŞ EKRANI ÇİZİMİ ---
            title_font = pygame.font.Font(None, 64)
            title_text = title_font.render("MOUSE VS CAT", True, YELLOW)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 120))
            
            # Nesnelerin ekrandaki orta konumu ve hizalanması
            center_y = SCREEN_HEIGHT // 2 - 20
            self.screen.blit(self.menu_mouse, (SCREEN_WIDTH // 2 - 160, center_y))
            self.screen.blit(self.menu_cheese, (SCREEN_WIDTH // 2 - 16, center_y))
            self.screen.blit(self.menu_cat, (SCREEN_WIDTH // 2 + 120, center_y))
            
            # Başlama uyarısı
            start_text = font.render("Press any key to start...", True, WHITE)
            self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT - 180))
            
        elif self.state == "PLAYING":
            # --- OYUN ALANI VE HUD ÇİZİMİ ---
            pygame.draw.rect(self.screen, GRAY, (GAME_AREA_X, GAME_AREA_Y, GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
            pygame.draw.rect(self.screen, WHITE, (GAME_AREA_X, GAME_AREA_Y, GAME_AREA_WIDTH, GAME_AREA_HEIGHT), 2)
            
            self.all_sprites.draw(self.screen)
            
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            level_text = font.render(f"Level: {self.level}/{MAX_LEVEL}", True, WHITE)
            
            self.screen.blit(score_text, (10, 10))
            
            level_x = SCREEN_WIDTH - level_text.get_width() - 20
            self.screen.blit(level_text, (level_x, 10))
        
        # REKOR (High Score) her iki ekranda da sağ altta gösterilir
        record_text = font.render(f"High Score: {self.high_score}", True, YELLOW) 
        record_x = SCREEN_WIDTH - record_text.get_width() - 20
        record_y = SCREEN_HEIGHT - record_text.get_height() - 5  # Değiştirme 
        self.screen.blit(record_text, (record_x, record_y))
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()