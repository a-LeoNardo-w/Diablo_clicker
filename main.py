import pygame
import os
import sys
import random
import time

pygame.init()
size = width, height = 1024, 1000
screen = pygame.display.set_mode(size)
monstr_exist_flag = False

# Начальный экран начало--------------------------
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def monstar_create():
    global monstr, monstr_exist_flag, hpbar
    monstr = monstr()
    hpbar = healthBar()
    monstr_exist_flag = True


def exit_menu():
    global game
    game = game()


class menu_button(pygame.sprite.Sprite):
    def __init__(self, name_butn, pos, mousepos):
        super().__init__(all_sprites)
        self.name = name_butn
        self.mousepos = mousepos
        self.image = load_image(f"{self.name}_1.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if pygame.sprite.collide_mask(self, mouse):
            self.image = load_image(f"{self.name}_2.png")
            if mouse.click and self.name == 'but_start':
                all_sprites.empty()
                exit_menu()
            elif mouse.click and self.name == 'but_exit':
                exit()
        else:
            self.image = load_image(f"{self.name}_1.png")


class menu(pygame.sprite.Sprite):
    menu_imag = load_image("bkgd.jpg")
    menu_imag = pygame.transform.scale(menu_imag, size)

    def __init__(self, pos, dx, dy, mousepos):
        super().__init__(all_sprites)
        self.image = self.menu_imag
        self.rect = self.image.get_rect()
        self.mousepos = mousepos
        self.butn_start = menu_button('but_start', (350, 200), mousepos)
        self.butn_exit = menu_button('but_exit', (350, 400), mousepos)


# Начальный экран конец--------------------------
# Game Начало
class monstr(pygame.sprite.Sprite):
    monstres = [load_image("monstr1.png"), load_image("monstr2.png"), load_image("monstr3.png"),
                       load_image("monstr4.png"), load_image("monstr5.png")]

    def __init__(self, hp=10, exp=10):
        super().__init__(monstr_sprites)
        self.image = random.choice(self.monstres)
        self.image = pygame.transform.scale(self.image, (600, 800))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.monstr_already_move = True
        self.rect.x = 160
        self.helthPoint = hp
        self.experience = exp
        self.oldHelthPoint = self.helthPoint

    def update(self):
        if pygame.sprite.collide_mask(self, mouse):
            mouse.image = load_image('attack.png')
            mouse.image = pygame.transform.scale(mouse.image, (100, 100))
            mouse.rect.x = mouse.mousepos[0] - 24
            mouse.rect.y = mouse.mousepos[1] - 10
        else:
            mouse.image = load_image('mouse_cursor.png')
            mouse.image = pygame.transform.scale(mouse.image, (60, 60))

    def take_damage(self, event):
        if pygame.sprite.collide_mask(self,
                                      mouse) and event.type == pygame.MOUSEBUTTONDOWN and self.monstr_already_move and \
                pygame.mouse.get_pressed(3)[0]:
            self.rect.x += 5
            self.rect.y += 5
            self.helthPoint -= 2
            if self.helthPoint <= 0:
                self.helthPoint = self.oldHelthPoint + 10
                self.oldHelthPoint += 10
                self.experience += 10
                self.image = random.choice(self.monstres)
            self.monstr_already_move = False
            print(self.helthPoint)
        elif event.type == pygame.MOUSEBUTTONUP and self.monstr_already_move == False:
            self.rect.x -= 5
            self.rect.y -= 5
            self.monstr_already_move = True

    def get_max_health(self):
        return self.oldHelthPoint

    def get_current_health(self):
        return self.helthPoint

    def get_xy(self):
        return (self.rect.x, self.rect.y)


class healthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(healthBar_sprite)
        self.image = pygame.Surface((0, 0))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(400, 400))
        pygame.draw.rect(screen, (255, 255, 255), (10, 30, 400, 30))

    def update(self):
        pygame.draw.rect(screen, (255, 255, 255), (260, 90, 400, 30))
        pygame.draw.rect(screen, (255, 0, 0), (260, 90, monstr.get_current_health()/(monstr.get_max_health()/400), 30))
        font = pygame.font.Font(None, 36)
        text = font.render(monstr)


class inventary(pygame.sprite.Sprite):
    pass


class powerPanel(pygame.sprite.Sprite):
    pass


class game(pygame.sprite.Sprite):
    game_background = [load_image("bg_game1.jpg"), load_image("bg_game2.jpg"), load_image("bg_game3.jpg")]

    def __init__(self):
        super().__init__(all_sprites)
        self.image = random.choice(self.game_background)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        monstar_create()
# Game Конец

class mouse(pygame.sprite.Sprite):
    menu_imag = load_image("mouse_cursor.png")
    menu_imag = pygame.transform.scale(menu_imag, (60, 60))

    def __init__(self, pos):
        super().__init__(mouse_sprites)
        self.image = self.menu_imag
        self.rect = self.image.get_rect()
        self.mousepos = pos
        self.click = False

    def mouse_update(self, newpos, click):
        self.click = click
        self.mousepos = newpos
        self.rect.x = newpos[0] - 17
        self.rect.y = newpos[1] - 3



fps = 120
running = True
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
mouse_sprites = pygame.sprite.Group()
monstr_sprites = pygame.sprite.Group()
healthBar_sprite = pygame.sprite.Group()
menu = menu(0, 0, 0, (0, 0))
mouse = mouse((0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse.mouse_update(event.pos, False)
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:
            mouse.mouse_update(event.pos, True)
        if event.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pressed(3)[0] == False:
            mouse.click = False
        if monstr_exist_flag:
            monstr.take_damage(event)

    all_sprites.update()
    all_sprites.draw(screen)
    monstr_sprites.update()
    monstr_sprites.draw(screen)
    mouse_sprites.update()
    mouse_sprites.draw(screen)
    healthBar_sprite.update()
    healthBar_sprite.draw(screen)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)
pygame.quit()
