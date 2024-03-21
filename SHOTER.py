from pygame import *
import random

# Шлях до зображення
img_back = "galaxy.jpg"  # Фон
img_hero = "rocket.png"  # Спрайт гравця
img_enemy = "ufo.png"  # Спрайт Ворога
img_bullet = "bullet.png"  # Спрайт кулі
img_ast = "enemy2.png"  # Спрайт астеройда

score = 0  # Кількість збитих кораблів
lost = 0  # Пропущені кораблі
max_lost = 5  # Макс. кількість пропущених кораблів
life = 5
max_score = 40

# Створення вікна
win_w = 700
win_h = 500

window = display.set_mode((win_w, win_h))
background = transform.scale(image.load(img_back), (win_w, win_h))

mixer.init()
mixer.music.load("videoplayback.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render("Перемога!", True, (255, 255, 255))
lose = font1.render("Поразка!", True, (180, 0, 0))


# True - згладжування тексту
# None - стандартний шрифт
# 36 - розмір шрифтта


# Батьківский клас для інших спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        # Завантажимо та змінемо розміри зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # Встановимо початкові координати спрайта
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # Метод для виведення спрайта на екран
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Клас головного гравця (дочірній)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        # key.get_pressed повертає список де кожен елемент вказує чи була натиснута відповідна клавіша
        if keys[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # Зникає, якщо дійде до краю екрана
        if self.rect.y > win_h:
            self.rect.x = random.randint(80, win_w - 80)
            self.rect.y = 0
            lost = lost + 1


# клас спрайта-кулі
class Bullet(GameSprite):
    # рух
    def update(self):
        self.rect.y -= self.speed
        # Зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()


class Rock(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        # Зникає якщо дійде до краю екрана
        if self.rect.y > win_h:
            spawn_chance = random.randint(1, 100)
            if spawn_chance <= 17:  # шанс спавну астероїда 17%
                self.rect.y = 0
                self.rect.x = random.randint(80, win_w - 80)
            else:
                self.rect.y = 0
                self.rect.x = random.randint(80, win_w - 80)
                lost += 1


# Стовримо cпрайти
ship = Player(img_hero, 5, win_h - 100, 80, 100, 10)
# Створимо групу спрайтів.
monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(1, 2):
    asteroid = Rock(img_ast, random.randint(80, win_w - 80), -40, 80, 100, random.randint(1, 5))
    asteroids.add(asteroid)

for i in range(1, 6):
    monster = Enemy(img_enemy, random.randint(80, win_w - 80), -40, 80, 100, random.randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()


def restart_game():
    global score, lost, life, finish

    # Скидання змінних
    score = 0
    lost = 0
    life = 5
    finish = False

    # Скидання положення гравця та монстрів
    ship.rect.x = 5
    ship.rect.y = win_h - 100
    monsters.empty()
    bullets.empty()

    # Створення монстрів
    for i in range(1, 6):
        monster = Enemy(img_enemy, random.randint(80, win_w - 80), -40, 80, 100, random.randint(1, 5))
        monsters.add(monster)
    for i in range(1, 2):
        asteroid = Rock(img_ast, random.randint(80, win_w - 80), -40, 80, 100, random.randint(1, 5))
        asteroids.add(asteroid)


# Прапорець для визначення закінчення гри
finish = False
# Основний цикл

run = True
while run:
    # event.get() - повертаємо список подій,які відбувся в грі
    for e in event.get():
        if e.type == QUIT:
            run = False
        # Подію натискання на пробіл - спрайт буде стріляти
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                ship.fire()
            # Перевірка чи натиснута клавіша ENTER для перезапуску гри
            elif e.key == K_RETURN and finish:
                restart_game()
    if not finish:
        # Оновлення фону
        window.blit(background, (0, 0))
        # Пишемо текст на екрані
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Ворогів пропущено " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # Оновлення руху гравця
        ship.update()  # update - використовуємо для оновлення екрану після змін
        monsters.update()
        asteroids.update()
        bullets.update()
        # Виведення гравця на екран
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        # Перевірка зіткнення кулі та монстрів
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # цикл який повториться стільки разів, скільки монстрів збито
            score = score + 1
            monster = Enemy(img_enemy, random.randint(80, win_w - 80), -40, 80, 100, random.randint(1, 5))
            monsters.add(monster)

        collides2 = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides2:
            # цикл який повториться стільки разів, скільки монстрів збито
            score = score + 5
            asteroid = Rock(img_ast, random.randint(80, win_w - 80), -40, 80, 100, random.randint(1, 5))
            asteroids.add(asteroid)
            # sprite.collide_rect - використовуємо для виявлення зіткнень між двома
        # спрайтами

        if sprite.spritecollide(ship, monsters, False):
            for c in sprite.spritecollide(ship, monsters, False):
                c.rect.x = random.randint(80, win_w - 80)
                c.rect.y = -40
                life = life - 1

        elif sprite.spritecollide(ship, asteroids, False):
            for c in sprite.spritecollide(ship, asteroids, False):
                c.rect.x = random.randint(80, win_w - 80)
                c.rect.y = - 40
                life = life - life

        # Програш
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        # Перевірку виграшу
        if score >= max_score:
            finish = True
            window.blit(win, (200, 200))

        display.update()

    # Затримка для визначення частоти оновлення гри
    time.delay(50)