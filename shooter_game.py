import pygame
import random

pygame.init()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, win_image, go_x, go_y, go_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(win_image), (50, 50))  
        self.rect = self.image.get_rect()  
        self.rect.x = go_x
        self.rect.y = go_y
        self.speed = go_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) 

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        if self.rect.y > 500: 
            self.reset_position()

    def reset_position(self):
        self.rect.y = random.randint(-100, -40) 
        self.rect.x = random.randint(0, 650)

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed 
        if keys[pygame.K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
        if keys[pygame.K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < 650:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, Bullet_x, Bullet_y):
        super().__init__("bullet.png", Bullet_x + 20, Bullet_y - 10, -10)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y < -10:
            self.kill()

pygame.mixer.init()
pygame.mixer.music.load('space.ogg')  
pygame.mixer.music.play(0)
shoot_sound = pygame.mixer.Sound('fire.ogg')

window = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Догонялки")
background = pygame.transform.scale(pygame.image.load("galaxy.jpg"), (700, 500))

player = Player("rocket.png", 250, 450, 5)

enemies = pygame.sprite.Group()
for i in range(5):
    enemy = Enemy("ufo.png", random.randint(0, 650), random.randint(-100, -40), random.randint(1, 2))
    enemies.add(enemy)

bullets = pygame.sprite.Group()

score_hit = 0
score_missed = 0
font = pygame.font.Font(None, 36)

game = True
clock = pygame.time.Clock()
FPS = 60

while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:   
            game = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.x, player.rect.y)  
                bullets.add(bullet)  
                shoot_sound.play()

    player.update()
    enemies.update()
    bullets.update()

    hits = pygame.sprite.spritecollide(player, enemies, False)
    for hit in hits:
        score_hit += 1
        hit.reset_position()

    for enemy in enemies:
        if enemy.rect.y > 499: 
            score_missed += 1

    bullet_hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
    
    for enemy in bullet_hits.values():
        for hit in enemy:
            score_hit += len(enemy)  
            hit.reset_position()

    window.blit(background, (0, 0))
    
    player.reset()
    enemies.draw(window)
    bullets.draw(window)  

    hit_text = font.render(f'Счёт: {score_hit}', True, (255, 255, 255))
    missed_text = font.render(f'Пропущено: {score_missed}', True, (255, 255, 255))
    
    window.blit(hit_text, (10, 10))
    window.blit(missed_text, (10, 40))

    pygame.display.update()
    clock.tick(FPS)


