from random import randint

class Weapon:
    def __init__(self, damage):
        self.damage = damage

class DefaultWeapon(Weapon):
    def __init__(self):
        super().__init__(damage=10)

class RareWeapon(Weapon):
    def __init__(self):
        super().__init__(damage=14)

class LegendaryWeapon(Weapon):
    def __init__(self):
        super().__init__(damage=20)

class Armor:
    def __init__(self, protection_percentage):
        self.protection_percentage = protection_percentage / 100  # Проценты в десятичную дробь

    def reduce_damage(self, damage):
        reduced_damage = damage * (1 - self.protection_percentage)
        return max(reduced_damage, 0)

    def __str__(self):
        return f"{self.__class__.__name__}, защита: {self.protection_percentage * 100}%"

class DefaultArmor(Armor):
    def __init__(self):
        super().__init__(protection_percentage=5)

class RareArmor(Armor):
    def __init__(self):
        super().__init__(protection_percentage=8)

class LegendaryArmor(Armor):
    def __init__(self):
        super().__init__(protection_percentage=12)

def generate_loot():
    loot_table = [DefaultWeapon, RareWeapon, LegendaryWeapon, DefaultArmor, RareArmor, LegendaryArmor]
    loot_class = loot_table[randint(0, len(loot_table) - 1)]
    return loot_class()

class Player:
    def __init__(self):
        self.hp = 100
        self.damage = 10
        self.wins = 0
        self.weapon = DefaultWeapon()
        self.armor = None

p = Player()

class Enemy:
    def __init__(self):
        self.hp = randint(70, 130)
        self.damage = randint(6, 13)
        self.armor = None

e = Enemy()

def reset_game():
    global p, e
    p = Player()
    e = Enemy()

def menu(p, e):
    while True:
        print("1) Сражаться")
        print("2) Посмотреть статистику")
        print("3) Открыть сундук")
        print("4) Начать новую игру")
        try:
            n = int(input("Введите число: "))

            if n == 1:
                menu_fight(p, e)
            elif n == 2:
                menu_stats(p)
            elif n == 3:
                menu_chests(p)
            elif n == 4:
                reset_game()
                print("Новая игра началась!")
            else:
                print("Чего ждем?")

        except ValueError:
            print("Введите число")

def menu_stats(p):
    print("Статистика игрока")
    print("*****************")
    print(f"Вы hp: {p.hp} damage: {p.weapon.damage}")
    if p.armor:
        print(f"Броня: {p.armor.__class__.__name__}, защита: {p.armor.protection_percentage * 100}%")
    else:
        print("Нет брони.")
    input("Нажмите Enter для продолжения.")

def menu_chests(p):
    print("Вам доступен сундук, хотите его открыть?")
    choice = input("1) Да, 2) Нет: ")
    if choice == "1":
        loot = generate_loot()
        print(f'Вы получили: {loot}')
        apply_loot(p, loot)
    else:
        print("Вы решаете не открывать сундук")

def apply_loot(player, loot):
    if isinstance(loot, Weapon):
        print(f"Вы получили новое оружие! {loot.__class__.__name__}, урон: {loot.damage}")
        player.weapon = loot
        player.damage = loot.damage  # Обновляем урон игрока
    elif isinstance(loot, Armor):
        if player.armor is None or loot.protection_percentage > player.armor.protection_percentage:
            print(f"Вы получили новую броню! {loot.__class__.__name__}, защита: {loot.protection_percentage * 100}%")
            player.armor = loot
        else:
            print(f"Вы получили броню, но она не лучше вашей текущей.")
        print(f"Ваша общая защита: {player.armor.protection_percentage * 100 if player.armor else 0}%")

def menu_fight(p, e):
    while e.hp > 0 and p.hp > 0:
        print(f"Вы hp: {p.hp} damage: {p.weapon.damage} armor: {p.armor}")
        print(f"Враг hp: {e.hp} damage: {e.damage}")
        print("**********************")
        print("1)Ударить")
        print("2)Хил 0-5")
        try:
            n = int(input("Введите число: "))
        except ValueError:
            print("Введите число")
            continue
        if n == 1:
            damage_dealt = p.weapon.damage
            if e.armor:
                damage_dealt = e.armor.reduce_damage(damage_dealt)
            e.hp -= damage_dealt
            print(f"Вы ударили противника, у него осталось {e.hp} hp")
            p.hp -= e.damage
            print(f"Противник ударил вас, у вас осталось {p.hp} hp")
        elif n == 2:
            p.hp += randint(0, 5)
            p.hp = min(p.hp, 100)
            print(f"Ваши хп {p.hp}")
        else:
            print("Чего ждем?")

        if p.hp <= 0:
            print("Вы проиграли")
        elif e.hp <= 0:
            print("Вы победили")

        print("******************")

# Вызов меню.
menu(p, e)
