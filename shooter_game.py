from pygame import *
from random import randint
font.init()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_w, size_h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_w, size_h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 85:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width-80)
            lost += 1
    
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

fire = mixer.Sound('fire.ogg')

image_player = 'rocket.png'

win_width = 700
win_height = 500

lost = 0
score = 0
font2 = font.Font(None, 80)
win = font2.render('YOU WIN!', True, (0, 255, 0))
lose = font2.render('YOU LOSE!', True, (255, 0, 0))

font1 = font.Font(None, 36)

window = display.set_mode((win_width, win_height))
display.set_caption('Space shooter')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

player = Player(image_player, 5, win_height-100, 80, 100, 10)
enemies = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1, 5))
    enemies.add(enemy)
bullets = sprite.Group()
FPS = 60
run = True
finish = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                player.fire()

    if finish:
        window.blit(background, (0, 0))
        enemies_lost = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        score_text = font1.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(score_text, (10, 20))
        window.blit(enemies_lost, (10, 50))
        player.update()
        enemies.update()
        bullets.update()
        player.reset()
        enemies.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
            score += 1
            enemy = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1, 5))
            enemies.add(enemy)
        if sprite.spritecollide(player, enemies, False) or lost >= 3:
            finish = False
            window.blit(lose, (200, 200))
        if score >= 10:
            finish = False
            window.blit(win, (200, 200))
        display.update()
    time.delay(FPS)