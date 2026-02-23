import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Konfigurasi Layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ninja Run")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# Variabel Game
FPS = 60
clock = pygame.time.Clock()
score = 0
font = pygame.font.SysFont("Arial", 24)

# Kelas Ninja (Pemain)
class Ninja:
    def __init__(self):
        self.width = 40
        self.height = 60
        self.x = 50
        self.y = SCREEN_HEIGHT - self.height - 10
        self.vel_y = 0
        self.jump = False

    def draw(self):
        # Kita gunakan kotak hitam sebagai representasi Ninja
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

    def update(self):
        # Logika Gravitasi
        self.y += self.vel_y
        if self.y < SCREEN_HEIGHT - self.height - 10:
            self.vel_y += 1  # Kekuatan gravitasi
        else:
            self.y = SCREEN_HEIGHT - self.height - 10
            self.jump = False
            self.vel_y = 0

    def jump_action(self):
        if not self.jump:
            self.vel_y = -15
            self.jump = True

# Kelas Rintangan (Shuriken/Batu)
class Obstacle:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - self.height - 10
        self.speed = 7

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    def update(self):
        self.x -= self.speed

# Fungsi Utama
def main():
    global score
    player = Ninja()
    obstacles = []
    spawn_timer = 0
    run = True

    while run:
        screen.fill(WHITE)
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump_action()

        # Update Ninja
        player.update()
        player.draw()

        # Update Rintangan
        if spawn_timer <= 0:
            obstacles.append(Obstacle())
            spawn_timer = random.randint(40, 90) # Jeda rintangan
        spawn_timer -= 1

        for obs in obstacles[:]:
            obs.update()
            obs.draw()
            
            # Deteksi Tabrakan
            player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
            obs_rect = pygame.Rect(obs.x, obs.y, obs.width, obs.height)
            
            if player_rect.colliderect(obs_rect):
                print(f"Game Over! Skor Akhir: {score}")
                run = False # Berhenti jika kena rintangan

            # Hapus rintangan yang lewat layar
            if obs.x < -obs.width:
                obstacles.remove(obs)
                score += 1

        # Tampilkan Skor
        score_txt = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_txt, (10, 10))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()