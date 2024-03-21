from pygame import *
import random

# Шлях до зображення
img_back = "galaxy.jpg"  # Фон
img_hero = "rocket.png"  # Спрайт гравця
img_enemy = "ufo.png"  # Спрайт Ворога
img_enemy2 = "enemy2.png"  # Спрайт другого типу ворога
img_bullet = "bullet.png"  # Спрайт кулі

score = 0  # Кількість збитих кораблів
lost = 0  # Пропущені кораблі
max_lost = 3  # Масимальна пропущено об'єктів до поразки
life = 3
score_to_boss = 10
max_score = 50
boss = 5

# Створення вікна
win_w = 700
win_h = 500

window = display.set_mode((win_w, win_h))
background = transform.scale(image.load(img_back), (win_w, win_h))

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win_text = font1.render("Всі Солов'ї-Розбійники спіймані!", True, (255, 255, 255))
lose_text = font1.render("Ваших друзів спіймали!", True, (180, 0, 0))
font3 = font.Font(None, 24)
game_over_text = font3.render("Game Over! Press ENTER to restart", True, (255, 255, 255))

# Батьківський клас для інших спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Клас головного гравця
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

# Клас ворога
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_h:
            self.rect.x = random.randint(80, win_w - 80)
            self.rect.y = 0
            lost += 1

# Клас другого типу ворога
class MonsterType2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_h:
            self.rect.x = random.randint(80, win_w - 80)
            self.rect.y = 0
            lost += 1

# клас спрайта-кулі
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

# Стовримо спрайти
ship = Player(img_hero, 5, win_h - 100, 80, 100, 10)
monsters = sprite.Group()

# Заповнимо групу спрайтів з обома типами ворогів
for i in range(1, 2):
    monster = Enemy(img_enemy, random.randint(80, win_w - 80), -40, 80, 80, random.randint(1, 5))
    monsters.add(monster)
for i in range(1, 2):
    monster = MonsterType2(img_enemy2, random.randint(80, win_w - 80), -40, 80, 80, random.randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

def restart_game():
    global score, lost, life, finish

    score = 0
    lost = 0
    life = 5
    finish = False
    ship.rect.x = 5
    ship.rect.y = win_h - 100
    monsters.empty()
    bullets.empty()

    # Заповнимо групу спрайтів знову
    for i in range(1, 2):
        monster = Enemy(img_enemy, random.randint(80, win_w - 80), -40, 80, 80, random.randint(1, 5))
        monsters.add(monster)
    for i in range(1, 2):
        monster = MonsterType2(img_enemy2, random.randint(80, win_w - 80), -40, 80, 80, random.randint(1, 5))
        monsters.add(monster)

# Прапорець для визначення закінчення гри
finish = False

run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                ship.fire()
            elif e.key == K_RETURN and finish:
                restart_game()

    if not finish:
        window.blit(background, (0, 0))
        text = font2.render("Рахунок "+ str(score), 1, (255,255,255))
        window.blit(text,(10, 20))
        text_lose = font2.render("Вас вспіймали " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        display.update()

        # Обробка зіткнень між монстрами та гравцем
        for monster in monsters:
            if sprite.collide_rect(ship, monster):
                life -= 1
                monster.rect.x = random.randint(80, win_w - 80)
                monster.rect.y = -40

        # Обробка зіткнень між кулями та монстрами
        collides = sprite.groupcollide(monsters, bullets, False, True)
        for monster in collides:
            if isinstance(monster, MonsterType2):
                score += 2  # Якщо це другий тип монстра, зменшуємо кількість життів
            else:
                score += 1  # Якщо це перший тип монстра, збільшуємо рахунок
            monster.rect.x = random.randint(80, win_w - 80)
            monster.rect.y = -40
            new_monster = Enemy(img_enemy, random.randint(80, win_w - 80), -40, 80, 80, random.randint(1, 5))
            monsters.add(new_monster)

    # Перевірка виграшу чи програшу
    if life == 0 or lost >= max_lost:
        finish = True
        window.blit(lose_text, (200, 200))
        window.blit(game_over_text, (200, 300))
    elif score >= max_score:
        finish = True
        window.blit(win_text, (200, 200))
        window.blit(game_over_text, (200, 300))

    time.delay(50)
    display.update()
