import pygame
import sys
from random import randint

lost = 0

# клас-батько для інших спрайтів
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.speed = player_speed
        self.image = pygame.transform.scale(pygame.image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))


# клас головного гравця
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self, win_width):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self, bullets, screen):                            
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15, screen)
        bullets.add(bullet)


#клас спрайта-ворога
class Enemy(GameSprite):
    def update(self, win_height, win_width):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            global lost
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(0, win_width - 80)


#клас для куль
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()


# Клас гри
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen_width = 700
        self.screen_height = 600
        self.screen_size = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.background = pygame.transform.scale(pygame.image.load('galaxy.jpg'), self.screen_size)

        # створюємо об'єкт гравця
        self.player = Player('rocket.png', 300, 500, 50, 80, 5, self.screen)

        # створюємо групу спрайтів для ворогів
        self.enemies = pygame.sprite.Group()

        # створюємо групу спрайтів для куль
        self.bullets = pygame.sprite.Group()

        self.generate_enemies()
        
        self.clock = pygame.time.Clock()
        self.fps = 50
        self.running = True
        self.finished = False

        # створюємо властивості для підрахунку статистики 
        self.score = 0
        self.hp = 3

        # створюємо свій шрифт для написів
        self.statistic_font = pygame.font.Font(None, 35)
        self.result_font = pygame.font.Font(None, 70)

        self.game_run()


    # метод, який генерує ворогів та додає їх до групи спрайтів
    def generate_enemies(self):
        for i in range(5):
            enemy = Enemy("ufo.png", randint(0, self.screen_width - 80), -40, 80, 50, randint(1, 5), self.screen)
            self.enemies.add(enemy)


    # метод з ігровим циклом
    def game_run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:   
                    if event.key == pygame.K_SPACE:
                        self.player.fire(self.bullets, self.screen)

            if not self.finished:
                global lost

                self.screen.blit(self.background, (0, 0))

                # малюємо та оновлюємо позицію гравця
                self.player.update(self.screen_width) 
                self.player.draw()  

                # малюємо та оновлюємо позицію ворогів
                self.enemies.update(self.screen_width, self.screen_height)
                self.enemies.draw(self.screen)  

                # малюємо та оновлюємо позицію куль
                self.bullets.update()
                self.bullets.draw(self.screen)
                
                # збиття ворогів 
                collides = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
                for c in collides:
                    self.score += 1
                    enemy = Enemy("ufo.png", randint(0, self.screen_width - 80), -40, 80, 50, randint(1, 5), self.screen)
                    self.enemies.add(enemy)

                # Зіткнення з ворогом
                if pygame.sprite.spritecollide(self.player, self.enemies, True):
                    self.hp -= 1

                # Перевірка програшу
                if lost >= 3 or self.hp <= 0:
                    self.finished = True
                    lose_text = self.result_font.render("Game Over", True, (250, 0, 0))
                    self.screen.blit(lose_text, (220, 230))
                
                # Перевірка виграшу
                if self.score >= 10:
                    self.finished = True
                    lose_text = self.result_font.render("You Win!", True, (0, 200, 0))
                    self.screen.blit(lose_text, (230, 230))

                # пишемо статистику на екрані   
                text_score = self.statistic_font.render("Рахунок: " + str(self.score), True, (255, 255, 255))
                self.screen.blit(text_score, (10, 20))

                text_lost = self.statistic_font.render("Пропущено: " + str(lost), True, (255, 255, 255))
                self.screen.blit(text_lost, (10, 50))

                life_score = self.statistic_font.render("Життя: " + str(self.hp), True, (255, 255, 255))
                self.screen.blit(life_score, (550, 20))

            # перезапуск
            else:
                #обнуляємо змінні
                self.finished = False
                self.hp = 3
                self.score= 0
                lost = 0

                #чистимо групи спрайтів
                for b in self.bullets:
                    b.kill()
                for e in self.enemies:
                    e.kill()
                  
                #ставимо паузу на 3 секунди
                pygame.time.delay(3000)

                #створюємо нових ворогів 
                self.generate_enemies()
                 

            self.clock.tick(self.fps)
            pygame.display.update()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    Game()







