import pygame
import os
import sys
import random
import time

# head
pygame.init()
size = width, height = 1024, 1000
screen = pygame.display.set_mode(size)
monster_exist_flag = False  # переменная необходимая для создания монстра и всех компонентов после начала игры
endscreen_exist_flag = True
inventory_already_exist = True
inventory_already_open = True
shop_already_open = True
inventory = []
shop_item_already_exist = True


# Начальный экран начало--------------------------
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def monstar_create():  # создания монстров и всех компонентов
    global monster, monster_exist_flag, hpbar, power_panel, player, shop, shop_items, arm
    hpbar = HealthBar()
    player = Player()
    monster_exist_flag = True
    power_panel = PowerPanel()
    monster = Monster()
    shop = ShopIcon()
    shop_items = []

    for i in range(3):
        for k in range(5):
            inventory.append(InventoryIndex((15 + 82 * k - 500, 643 + 77 * i)))

    shop_items.append(ShopItem(price=100, dmg=7, id=0))
    shop_items.append(ShopItem(price=70, dmg=3, id=1))
    shop_items.append(ShopItem(price=50, dmg=1, id=2))
    shop_items.append(ShopItem(price=500, dmg=12, id=3))
    shop_items.append(ShopItem(price=315, dmg=9, id=4))
    shop_items.append(ShopItem(price=150, dmg=4, id=5))

    arm = Arm((-500, 0))
    pygame.mixer.music.load('data/bg_music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.4)



def endscreen_create():
    global endscreen_exist_flag, endscreen, monster, hpbar, power_panel, player
    endscreen = Endscreen()
    monster.kill()
    hpbar.kill()
    power_panel.power1.kill()
    power_panel.power2.kill()
    power_panel.power3.kill()
    power_panel.power4.kill()
    power_panel.power5.kill()
    power_panel.kill()
    player.kill()
    endscreen_exist_flag = False


def exit_menu():  # закрытие меню создание элемента Game()
    global game
    game = Game()


class MenuButton(pygame.sprite.Sprite):  # класс кнопки в меню
    def __init__(self, name_butn, pos):
        super().__init__(button_sprites)
        self.name = name_butn  # картинка кнопки
        self.image = load_image(f"{self.name}_1.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = pos

    def update(self):  # изменения при наведении на кнопку и нажатие
        if pygame.sprite.collide_mask(self, mouse):
            self.image = load_image(f"{self.name}_2.png")
            if mouse.click and self.name == 'but_start':  # проверяем состояние нажатия мыши и то на что мы навились
                all_sprites.empty()  # удаляем меню(чистим спрайты)
                button_sprites.empty()
                exit_menu()  # запускаем функцию по созданию игры
            elif mouse.click and self.name == 'but_exit':
                exit()
            elif mouse.click and self.name == 'but_close':
                exit()
        else:
            self.image = load_image(f"{self.name}_1.png")


class Menu(pygame.sprite.Sprite):  # класс Меню
    menu_imag = load_image("bkgd.jpg")  # картинка меню
    menu_imag = pygame.transform.scale(menu_imag, size)  # изменение размеров картинки

    def __init__(self):
        super().__init__(all_sprites)
        self.image = self.menu_imag
        self.rect = self.image.get_rect()
        self.butn_start = MenuButton('but_start', (350, 200))  # добавление кнопки
        self.butn_exit = MenuButton('but_exit', (350, 400))  # добавление кнопки


# Начальный экран конец--------------------------
# Game Начало
class Monster(pygame.sprite.Sprite):  # класс монстра
    monstres = [load_image("monstr1.png"), load_image("monstr2.png"), load_image("monstr3.png"),
                load_image("monstr4.png"), load_image("monstr5.png")]  # список монстров

    def __init__(self, hp=10, exp=10):
        super().__init__(monstr_sprites)
        self.image = random.choice(self.monstres)
        self.image = pygame.transform.scale(self.image, (600, 800))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.monstr_already_move = True  # переменная необходимая для проверки нажал ли игрок на монстра
        self.rect.x = 160
        self.helthPoint = hp
        self.experience = exp
        self.money = 2
        self.oldHelthPoint = self.helthPoint  # нужна для HealthBar, чтобы помнить максимальное количество hp;
        # также нужно, чтобы создать следующего монстра с увеличенным Hp
        self.player_list_is_off = True
        self.clickDmg = power_panel.power1.damage
        self.dmg_to_monster_baff = power_panel.power1.baff_dmg

    def update(self):
        self.dmg_to_monster_baff = power_panel.power1.baff_dmg
        if pygame.sprite.collide_mask(self, mouse) and self.player_list_is_off:  # если мышка касается монстра, то
            mouse.image = load_image('attack.png')  # курсор мыши меняется на меч
            mouse.image = pygame.transform.scale(mouse.image, (100, 100))  # снова создаётся обводка(колайдер)
            mouse.rect.x, mouse.rect.y = mouse.mousepos[0] - 24, mouse.mousepos[1] - 10  # изменения в
            # расположении картинки, чтобы меч был примерно там, где мышка
        else:  # иначе
            mouse.image = load_image('mouse_cursor.png')  # вернуть старый курсор мыши
            mouse.image = pygame.transform.scale(mouse.image, (60, 60))  # вернуть старую обводку(колайдер)

        if self.helthPoint <= 0:  # если жизни монстра становятся меншье нуля, то(!это типо я создам нового монстра!)
            player.experience += self.experience
            player.money += self.money
            self.money = self.money + 1
            self.helthPoint = self.oldHelthPoint + 10  # восстанавливаем hp и добавляем ещё 10(типо сильнее)
            self.oldHelthPoint = self.helthPoint
            self.experience += 10  # увеличение опыта получаемое при убийстве
            self.image = random.choice(self.monstres)  # смена картинки на нового монстра
            self.mask = pygame.mask.from_surface(self.image)  # создания новой обводки(колайдера)

    def take_damage(self, event):  # функция для получения урона монстром !от мышки!
        if pygame.sprite.collide_mask(self, mouse) and self.monstr_already_move and pygame.mouse.get_pressed(3)[0] \
                and self.player_list_is_off:
            # если мышка касается монстра и игрок уже нажал на монстра и мы нажали лкм
            self.rect.x += 5
            self.rect.y += 5
            if random.randint(1, 10) in [1, 2, 3]:
                self.helthPoint -= ((self.clickDmg + self.dmg_to_monster_baff + arm.item.dmg) * 2)
                Crits(mouse.mousepos, ((self.clickDmg + self.dmg_to_monster_baff + arm.item.dmg) * 2))
            else:
                self.helthPoint -= (self.clickDmg + self.dmg_to_monster_baff + arm.item.dmg)
            self.monstr_already_move = False  # ждём пока игрок отожмёт лкм, это нужно для того, чтобы
            # игрок не мог просто зажать лкм и наносить беспрерывный урон
        elif event.type == pygame.MOUSEBUTTONUP and self.monstr_already_move == False and self.player_list_is_off:  # отжатие кнопки
            self.rect.x -= 5
            self.rect.y -= 5
            self.monstr_already_move = True

    def get_max_health(self):
        return self.oldHelthPoint

    def get_current_health(self):  # вернуть текущее hp
        return self.helthPoint

    def get_xy(self):
        return (self.rect.x, self.rect.y)


class HealthBar(pygame.sprite.Sprite):  # класс полоска жизни
    def __init__(self):
        super().__init__(healthBar_sprite)
        self.image = pygame.Surface((0, 0))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(400, 400))

    def update(self):  # сложные махинации, !ничего не трогать!
        pygame.draw.rect(screen, (100, 100, 100), (260, 90, 400, 30))
        pygame.draw.rect(screen, (255, 0, 0),
                         (260, 90, monster.get_current_health() / (monster.get_max_health() / 400), 30))
        f1 = pygame.font.Font(None, 36)  # текст hp
        text1 = f1.render(str(monster.get_current_health()), True,
                          (0, 180, 0))
        screen.blit(text1, (445, 95))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_sprites)
        self.frames = []
        self.cut_sheet(load_image("avatares_r.png"), 5, 2)
        self.lvl = 1
        self.experience = 0
        self.experience_for_new_lvl = 10
        self.money = 0
        self.image = random.choice(self.frames)
        self.image = pygame.transform.scale(self.image, (160, 160))
        self.rect = self.rect.move(0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.mouse_already_press = True

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        global inventory_already_open, inventory
        if self.mouse_already_press == False and pygame.mouse.get_pressed(3)[0] == False and inventory_already_open:
            self.mouse_already_press = True
            inventory_already_open = False
        elif pygame.sprite.collide_mask(self, mouse) and pygame.mouse.get_pressed(3)[0] and self.mouse_already_press:
            # если мышка касается монстра и игрок уже нажал на монстра и мы нажали лкм
            self.playerlist = PlayerList(10, 10, 10)
            for i in inventory:
                i.rect.x = i.rect.x + 500
            self.mouse_already_press = False
        if self.experience >= self.experience_for_new_lvl:
            self.lvl += 1
            self.experience = 0
            self.experience_for_new_lvl = self.experience_for_new_lvl + 10 * self.lvl


class ShopIcon(pygame.sprite.Sprite):  # класс ячейки инвентаря
    def __init__(self):
        super().__init__(player_list_sprites)
        self.image = load_image('shop.png')
        self.image = pygame.transform.scale(self.image, (160, 160))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (width - 160, 0)
        self.mouse_already_press = False

    def update(self):
        global shop_already_open
        if self.mouse_already_press == False and pygame.mouse.get_pressed(3)[0] == False and shop_already_open:
            self.mouse_already_press = True
            shop_already_open = False
        elif pygame.sprite.collide_mask(self, mouse) and pygame.mouse.get_pressed(3)[0] and self.mouse_already_press:
            # если мышка касается монстра и игрок уже нажал на монстра и мы нажали лкм
            self.shop = Shop()
            self.mouse_already_press = False


class ShopItem(pygame.sprite.Sprite):  # класс ячейки инвентаря
    def __init__(self, pos=(-500, 470), price=0, dmg=0, id=-1):
        super().__init__(button_sprites)
        self.frames = []
        self.frames_chosen = []
        self.chosen_item = id
        self.cut_sheet(load_image("shop_items.png"), 3, 2, self.frames)
        self.cut_sheet(load_image("shop_item_chosen.png"), 3, 2, self.frames_chosen)
        self.image = self.frames[self.chosen_item]
        self.image = pygame.transform.scale(self.image, (164, 154))
        self.rect = self.rect.move(pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.itemPrice = price
        self.mouse_preessed = True
        self.dmg = dmg

    def cut_sheet(self, sheet, columns, rows, frame):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frame.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        global inventory_already_open
        if pygame.sprite.collide_mask(self, mouse):
            self.image = self.frames_chosen[self.chosen_item]
            self.image = pygame.transform.scale(self.image, (164, 154))
            if mouse.click:
                mouse.click = False
                if self.itemPrice <= player.money:
                    for i in inventory:
                        if i.item == None:
                            i.item = self
                            player.money -= self.itemPrice
                            print(i)
                            break
                else:
                    print('not enough money')
                mouse.click = False
        else:
            self.image = self.frames[self.chosen_item]
            self.image = pygame.transform.scale(self.image, (164, 154))



class AddButton(pygame.sprite.Sprite):

    def __init__(self, item=None, pos=(0, 0)):
        super().__init__(button_sprites)
        self.image = load_image('equip_text.png')
        self.image = pygame.transform.scale(self.image, (60, 25))
        self.rect = self.image.get_rect()
        self.secondImg = load_image('equip_text.png')
        self.secondImg = pygame.transform.scale(self.secondImg, (60, 25))
        self.item = item
        self.rect.x, self.y = (pos[0] - 10, pos[1] - 5)
        self.open_butt = True
        self.pos = pos

    def update(self):
        if not pygame.sprite.collide_mask(self, mouse):
            self.rect.x, self.rect.y = self.pos
            self.open_butt = False
        if not pygame.sprite.collide_mask(self, mouse):
            self.kill()
        elif pygame.sprite.collide_mask(self, mouse) and mouse.click:
            arm.item = self.item
            arm.image = arm.frames[self.item.chosen_item]
            arm.image = pygame.transform.scale(arm.image, (50, 65))
            mouse.click = False
        elif pygame.sprite.collide_mask(self, mouse):
            self.image = self.secondImg



class Shop(pygame.sprite.Sprite):
    def __init__(self):
        global shop_items
        super().__init__(player_list_sprites)
        self.image = load_image('but_close_1.png')
        self.image = pygame.transform.scale(self.image, (140, 35))
        self.rect = self.image.get_rect()
        self.rect.x = 750
        self.rect.y = 800
        monster.player_list_is_off = False
        self.shopImg = load_image('shop_inside.png')
        self.shopImg = pygame.transform.scale(self.shopImg, (430, 700))
        self.shopImg_rect = self.shopImg.get_rect()
        self.shopitem = random.choice(shop_items)
        self.shopitem.rect.x = 735
        self.shopitem.rect.y = 400


    def update(self):
        global shop_already_open
        self.shopitem.rect.move(735, 470)
        screen.blit(self.shopImg, [width - self.rect.width - 290, 190])
        font = pygame.font.Font(None, 27)  # шрифт
        money_txt = font.render(f'Ваше золото {player.money}', True, (0, 180, 0))  # текст money
        screen.blit(money_txt, (750, 620))
        price_txt = font.render(f'Стоимость {self.shopitem.itemPrice}', True, (0, 180, 0))  # текст money
        screen.blit(price_txt, (750, 590))
        if pygame.sprite.collide_mask(self, mouse):
            self.image = load_image('but_close_2.png')
            self.image = pygame.transform.scale(self.image, (140, 35))
            if pygame.mouse.get_pressed(3)[0]:
                shop_already_open = True
                monster.player_list_is_off = True
                self.kill()
                self.shopitem.rect.x = -500
        else:
            self.image = load_image('but_close_1.png')
            self.image = pygame.transform.scale(self.image, (140, 35))

class InventoryIndex(pygame.sprite.Sprite):  # класс ячейки инвентаря
    def __init__(self, pos, item=None, id=-1):
        super().__init__(button_sprites)
        self.image = load_image('index_inventory.png')
        self.image = pygame.transform.scale(self.image, (82, 77))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.item = item
        self.id = id

    def update(self):
        if inventory_already_open is False and pygame.sprite.collide_mask(self, mouse):
            for i in inventory:
                if self.item == i.item and pygame.sprite.collide_mask(self, mouse) and mouse.rightClick and self != arm.item:
                    self.but = AddButton(self.item, mouse.mousepos)
                    print(mouse.mousepos)
                    mouse.rightClick = False

class Arm(pygame.sprite.Sprite):

    def __init__(self, pos=(-500, 470), item=None):
        super().__init__(button_sprites)
        self.frames = []
        self.cut_sheet(load_image("in_arm_sprites.png"), 3, 2, self.frames)
        self.image = load_image('arm.png')
        self.image = pygame.transform.scale(self.image, (50, 65))
        self.rect = self.rect.move(pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.mouse_preessed = True
        self.item = item

    def update(self):
        if pygame.sprite.collide_mask(self, mouse):
            print(1)

    def cut_sheet(self, sheet, columns, rows, frame):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frame.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

class PlayerList(pygame.sprite.Sprite):
    def __init__(self, exp, money, count_died_monsters):
        global inventory
        super().__init__(player_list_sprites)
        self.exp = exp
        self.money = money
        self.count_died_monsters = count_died_monsters
        self.image = load_image('but_close_1.png')
        self.rect = self.image.get_rect()
        self.rect.x = 40
        self.rect.y = 525
        self.image = pygame.transform.scale(self.image, (350, 50))
        monster.player_list_is_off = False
        self.playerlist = load_image('inventory.png')
        self.playerlist = pygame.transform.scale(self.playerlist, (430, 700))
        self.player_rect = self.playerlist.get_rect()
        for i in inventory:
            if i.item != None:
                i.image = i.item.image
                i.image = pygame.transform.scale(i.image, (82, 77))
        arm.rect.x, arm.rect.y = (182, 394)

    def update(self):
        global inventory_already_open
        screen.blit(self.playerlist, [0, 190])
        self.avatar = player.image
        self.avatar_rect = self.avatar.get_rect()
        self.avatar = pygame.transform.scale(self.avatar, (120, 120))
        screen.blit(self.avatar, [50, 320])
        font = pygame.font.Font(None, 27)  # шрифт
        lvl_txt = font.render(f'Уровень {player.lvl}', True, (0, 180, 0))  # текст lvl
        screen.blit(lvl_txt, (50, 480))
        money_txt = font.render(f'Золото {player.money}', True, (0, 180, 0))  # текст money
        screen.blit(money_txt, (50, 580))
        if pygame.sprite.collide_mask(self, mouse):
            self.image = load_image('but_close_2.png')
            self.image = pygame.transform.scale(self.image, (140, 35))
            if pygame.mouse.get_pressed(3)[0]:
                monster.player_list_is_off = True
                self.kill()
                for index in inventory:
                    index.rect.x = index.rect.x - 500
                arm.rect.x = arm.rect.x - 500
                inventory_already_open = True

        else:
            self.image = load_image('but_close_1.png')
            self.image = pygame.transform.scale(self.image, (140, 35))


class button(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('but_close_1')


class PowerPanel(pygame.sprite.Sprite):  # класс панели способностей
    power_panel_img = load_image('powers_panel.png')
    power_panel_img = pygame.transform.scale(power_panel_img, (width + 100, 200))

    def __init__(self):
        super().__init__(player_sprites)
        self.image = self.power_panel_img
        self.rect = self.image.get_rect()
        self.rect.x = -50
        self.rect.y = height - self.rect.height + 15
        self.power1 = AnyPower('power_lkm.jpg', 2, 0, 'asd', (583, 924))  # способность лкм
        self.power2 = AnyPower('power_first.jpg', 10, 3, pygame.K_1, (349, 926))  # способность 1
        self.power4 = AnyPower('power_third.jpg', 30, 10, pygame.K_3, (464, 926))  # способность 3
        self.power5 = AnyPower('power_fourth.jpg', 50, 15, pygame.K_4, (522, 926))  # способность 4
        self.power3 = AnyPower('power_second.jpg', 0, 10, pygame.K_2, (405, 926), True, 5, 5)  # способность 2

    def power_panel_powers_update(self, event):
        power_panel.power2.power_update(event)  # проверка на нажатие способности 1
        power_panel.power3.power_update(event)  # проверка на нажатие способности 2
        power_panel.power4.power_update(event)  # проверка на нажатие способности 3
        power_panel.power5.power_update(event)  # проверка на нажатие способности 4


class AnyPower(pygame.sprite.Sprite):  # класс способности
    def __init__(self, power, damage, cooldown, key, pos, baff=False, baff_dmg=0, baff_time=0):
        super().__init__(player_sprites)
        self.power_img = load_image(power)  # картинка способности
        self.power_img_cd = self.power_img  # картинка способности во время кд
        if cooldown != 0:  # условие для такой способности, как лкм(тк нету картинки с кд, тк у лкм нету кд)
            self.power_img_cd = load_image(f'{power[:-4]}_cd.jpg')
        self.image = self.power_img  # присвоение картинки
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (43, 50))
        self.rect.x, self.rect.y = pos
        self.damage = damage  # урон наносимый способностью
        self.cooldown = cooldown * (fps - 50)  # кд способности(cooldown - в сек)
        self.key = key  # на что нажать, чтобы активировать
        self.power_ready = 0  # таймер для кд способности
        self.baff = baff  # проверка является ли способности баффом, а не уроном
        self.baff_dmg = baff_dmg  # урон, конотрый будет дополняться к урону способностей
        self.baff_time = baff_time * (fps - 50)  # время действия баффа
        self.baff_time_work = baff_time * (fps - 50)  # таймер для времени действия баффа

    def update(self):
        if self.power_ready != self.cooldown:  # пока таймер не будет равен времени кд способности, то
            self.power_ready += 1  # прибавляем таймер
            self.image = self.power_img_cd  # меняем на картинку с кд способности
            self.image = pygame.transform.scale(self.image, (43, 50))
        else:  # иначе
            self.image = self.power_img  # обычная(готовая) картинка(способность готова)
            self.image = pygame.transform.scale(self.image, (43, 50))
        if self.baff_time_work != self.baff_time:  # если таймер баффа не равен времени действия бафаа, то
            self.baff_time_work += 1  # прибавляем таймер
            power_panel.power1.baff_dmg = power_panel.power3.baff_dmg  # дополняем доп урон к способности 1
            power_panel.power2.baff_dmg = power_panel.power3.baff_dmg  # дополняем доп урон к способности 2
            power_panel.power4.baff_dmg = power_panel.power3.baff_dmg  # дополняем доп урон к способности 3
            power_panel.power5.baff_dmg = power_panel.power3.baff_dmg  # дополняем доп урон к способности 4
        else:  # после конца действия:
            power_panel.power1.baff_dmg = 0  # убираем доп урон к способности 1
            power_panel.power2.baff_dmg = 0  # убираем доп урон к способности 2
            power_panel.power4.baff_dmg = 0  # убираем доп урон к способности 3
            power_panel.power5.baff_dmg = 0  # убираем доп урон к способности 4

    def power_update(self, event):  # обновление нужное для проверки нажатия на кнопку
        if event.key == self.key and self.power_ready == self.cooldown:  # если нажатая кнопка равна
            # кнопке способности и таймер равен времени кд, то
            if self.baff is False:  # если не бафф
                if random.randint(1, 10) in [1, 2, 3]:
                    monster.helthPoint -= ((self.damage + self.baff_dmg) * 2)
                    Crits((width // 2 - 20, height // 2 - 100), ((self.damage + self.baff_dmg) * 2))
                else:
                    monster.helthPoint -= (self.damage + self.baff_dmg)
                self.power_ready = 0  # и сбрасываем таймер,
                # чтобы он снова начал отсчёт, чтобы мы не могли пользовать способностью
            if self.baff is True:  # если бафф
                self.baff_time_work = 0  # то начинаем работу баффа
                self.power_ready = 0  # и сбрасываем таймер,
                # чтобы он снова начал отсчёт, чтобы мы не могли пользовать способностью


class Game(pygame.sprite.Sprite):  # класс Игры
    game_background = [load_image("bg_game1.jpg"), load_image("bg_game2.jpg"), load_image("bg_game3.jpg")]  # список

    # задних фонов

    def __init__(self):
        super().__init__(all_sprites)
        self.image = random.choice(self.game_background)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        monstar_create()  # функция по созданию монстра и основных компонентов


# Game Конец

class Endscreen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(end_game_sprites)
        self.lvl = player.lvl
        self.money = player.money
        self.image = load_image("bkgd.jpg")
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.buttonEnd = MenuButton('but_close', (350, 500))
        mouse.image = load_image("mouse_cursor.png")
        pygame.transform.scale(mouse.image, (60, 60))
        self.end_menu = load_image('end_menu.png')
        self.end_menu_rect = self.end_menu.get_rect()
        self.endresult = EndResult(self.lvl, self.money)


    def update(self):
        pass


class EndResult(pygame.sprite.Sprite):
    def __init__(self, lvl, money):
        self.lvl = lvl
        self.money = money
        super().__init__(button_sprites)
        self.image = load_image('end_menu.png')
        self.rect = self.image.get_rect()
        self.rect.x = 290
        self.rect.y = 200
        self.endtext = EndTextResult(self.lvl, self.money)

    def update(self):
        pass

class Crits(pygame.sprite.Sprite):

    def __init__(self, pos=(10, 10), crit_dmg=0):
        super().__init__(crits_sprites)
        self.image = pygame.font.Font(None, 70).render(f'{crit_dmg}', True, (180, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.velocity = [random.randint(-3, 3), -8]
        self.gravity = 0.2

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.rect.x < 0:
            self.kill()

class EndTextResult(pygame.sprite.Sprite):
    def __init__(self, lvl, money):
        self.lvl = lvl
        self.money = money
        super().__init__(end_game_text_sprites)
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        f1 = pygame.font.Font(None, 36)  # текст hp
        f2 = pygame.font.Font(None, 30)  # текст hp
        self.text1 = f1.render(f'Поздравляю!', True, (0, 180, 0))
        self.text2 = f2.render(f'Ваш счёт: УРОВЕНЬ {self.lvl}', True, (0, 180, 0))
        self.text3 = f2.render(f'Ваш счёт: ЗОЛОТО {self.money}', True, (0, 180, 0))

    def update(self):
        screen.blit(self.text1, (350, 230))
        screen.blit(self.text2, (350, 300))
        screen.blit(self.text3, (350, 350))
class Mouse(pygame.sprite.Sprite):  # класс Мыши
    menu_imag = load_image("mouse_cursor.png")  # картинка мыши
    menu_imag = pygame.transform.scale(menu_imag, (60, 60))

    def __init__(self, pos):
        super().__init__(mouse_sprites)
        self.image = self.menu_imag
        self.rect = self.image.get_rect()
        self.mousepos = pos  # позиция мыши
        self.click = False  # переменная нажата ли клавиша
        self.rightClickclick = False

    def mouse_update(self, newpos, click):
        self.click = click  # постоянно проверяем, нажата ли клавиша
        self.mousepos = newpos  # постоянно проверяем позицию мыши
        self.rect.x = newpos[0] - 17  # изменение позиции КАРТИНКИ мыши, чтобы картинка была там,
        # где должна быть обычная мышка
        self.rect.y = newpos[1] - 3  # изменение позиции КАРТИНКИ мыши, чтобы картинка была там,
        # где должна быть обычная мышка

    def mouse_right_update(self, click_right):
        self.rightClick = click_right

fps = 120  # фпс
running = True  # программа работает
pygame.mouse.set_visible(False)  # отключение видимости обычной мыши
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()  # группа всех спрайтов(пример: меню, кнопки в меню)
mouse_sprites = pygame.sprite.Group()  # группа спрайтов мышки(пример: мышка)
monstr_sprites = pygame.sprite.Group()  # группа спрайтов монстра(пример: монстр)
button_sprites = pygame.sprite.Group()
healthBar_sprite = pygame.sprite.Group()  # группа спрайтов монстра(пример: полоса жизни монстра)
player_sprites = pygame.sprite.Group()  # группа спрайтов монстра(пример: способности, панель способностей)
player_list_sprites = pygame.sprite.Group()
end_game_sprites = pygame.sprite.Group()
end_game_text_sprites = pygame.sprite.Group()
crits_sprites = pygame.sprite.Group()
menu = Menu()  # создание меню
mouse = Mouse((0, 0))  # создание мыши
while running:  # вечный цикл игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:  # отправка данных при движении мыши(координаты)
            mouse.mouse_update(event.pos, False)
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:  # нажата клавиша
            # и нажата лкм
            mouse.mouse_update(event.pos, True)  # обновляем данные, что мы сейчас НАЖАЛИ на кнопку мыши
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[2]:  # нажата клавиша
            # и нажата пкм
            mouse.mouse_right_update(True)
        if event.type == pygame.MOUSEBUTTONUP and (pygame.mouse.get_pressed(3)[0] == False or pygame.mouse.get_pressed(3)[2] == False):  # проверяем что ОТЖАЛИ
            mouse.click = False  # меняем информацию
            mouse.rightClick = False
        if monster_exist_flag:  # проверяем существует ли монстр
            monster.take_damage(event)  # постоянно проверяем получает ли монстр урон
            if event.type == pygame.KEYDOWN:  # проверяем на нажатие клавиши способностей
                power_panel.power_panel_powers_update(event)
            if player.lvl >= 15 and endscreen_exist_flag:
                endscreen_create()
    all_sprites.update()
    all_sprites.draw(screen)
    monstr_sprites.update()
    monstr_sprites.draw(screen)
    player_sprites.update()
    player_sprites.draw(screen)
    healthBar_sprite.update()
    healthBar_sprite.draw(screen)
    player_list_sprites.update()
    player_list_sprites.draw(screen)
    crits_sprites.update()
    crits_sprites.draw(screen)
    end_game_sprites.update()
    end_game_sprites.draw(screen)
    button_sprites.update()
    button_sprites.draw(screen)
    button_sprites.update()
    end_game_text_sprites.draw(screen)
    end_game_text_sprites.update()
    mouse_sprites.draw(screen)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
