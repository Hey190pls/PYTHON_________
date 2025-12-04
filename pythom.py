import time
from time import sleep
import pygame
import requests  # залишив, якщо хочеш доповнити мережеві фічі
import os
import sys
import random
import ast
import operator

# --- Невелика утиліта для безпечного обчислення виразів ---
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

def safe_eval(expr: str):
    """Безпечний калькулятор — підтримує + - * / ** % // і дужки"""
    try:
        node = ast.parse(expr, mode='eval').body
        return _eval_node(node)
    except Exception as e:
        raise ValueError("Неможливо обчислити вираз.") from e

def _eval_node(node):
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            left = _eval_node(node.left)
            right = _eval_node(node.right)
            return ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            operand = _eval_node(node.operand)
            return ALLOWED_OPERATORS[op_type](operand)
    raise ValueError("Непідтримувана операція в виразі.")

# --- Основний інтерфейс ---
def clear_screen():
    # кросплатформене очищення екрану
    os.system('cls' if os.name == 'nt' else 'clear')

def play_music_safe(path):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"[Музика] Не вдалося завантажити {path}: {e}")

def list_music_folder():
    folder = "music"
    try:
        files = os.listdir(folder)
        for i, f in enumerate(files, start=1):
            print(f"{i}. {f}")
    except Exception:
        print("Папки 'music' не знайдено або вона порожня.")

# Ініціалізація
clear_screen()
usr = input("Введіть свій юзернейм (ім'я)> ")
pss = input("Введіть свій пароль> ")
clear_screen()

pygame.mixer.init()
# завбачливо: якщо немає файлу — просто мовчить
default_track = "music/my_castle_town_slowed.mp3"
try:
    pygame.mixer.music.load(default_track)
    pygame.mixer.music.play(-1)
except Exception:
    print("[Музика] Не вдалося завантажити дефолтну музику. Перевір папку music/")

print("------------------------------------------------")
time.sleep(0.065)
print("| Ласкаво просимо в Новорічну ОС!              |")
time.sleep(0.065)
print("| Напишіть 'help' для списку доступних команд! |")
time.sleep(0.065)
print("------------------------------------------------")

# Динамічний список команд
COMMANDS = {
    "help": "Показати список команд",
    "music": "Керування музикою",
    "ls": "Показати файли в папці music",
    "clear": "Очистити екран",
    "exit": "Вийти з програми",
    "joke": "Розповісти випадковий жарт",
    "time": "Показати поточний час",
    "calc": "Калькулятор: calc 2+2*3",
    "dance": "Танцювальний режим (ASCII-анімація)",
    "???": "??? (спеціальна фраза)",
    "whoami": "Показати логін користувача",
    "surprise": "Невеликий сюрприз (рандомна цитата)"
}

JOKES = [
    "Чому комп'ютер не стрибав? Був заблокований у сплячці.",
    "Що сказав нуль до вісімки? Гарний пояс!",
    "Чому програмісти плутають Halloween і Christmas? Бо 31 OCT == 25 DEC."
]

QUOTES = [
    "Новорічний настрій — у дрібницях.",
    "Код працює — життя прекрасне.",
    "Не бійся робити помилки — бійся не вчитися з них."
]

def print_help():
    print("Список команд:")
    for cmd, desc in COMMANDS.items():
        print(f" - {cmd:<10} : {desc}")

def show_pitsyatko_animation():
    # Анімація для "ПІЦЯТКО СЯ ВРОДИЛО"
    phrase = "П І Ц Я Т К О   С Я   В Р О Д И Л О"
    clear_screen()
    print("... щось трапилось ...")
    sleep(0.6)
    for i in range(1, len(phrase)+1):
        print("\r" + phrase[:i], end="", flush=True)
        sleep(0.08)
    print("\n")
    # додатковий "флеш"
    for _ in range(3):
        print("✨ " + "ПІЦЯТКО СЯ ВРОДИЛО" + " ✨")
        sleep(0.18)
    print("\n(ви ввели '???')")

def dance_animation():
    frames = [
        r"ᕕ( ᐛ )ᕗ",
        r"ᕦ( ͡° ͜ʖ ͡°)ᕤ",
        r"ヽ(⌐■_■)ノ♪♬",
        r"(•_•) ( •_•)>⌐■-■ (⌐■_■)"
    ]
    for _ in range(8):
        clear_screen()
        print(random.choice(frames))
        sleep(0.25)
    print("Втомився танцювати? 😅")

# Основний цикл
while True:
    try:
        com = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nВихід...")
        break

    if com == "":
        continue

    # Розбір простих команд з параметрами
    if com == "help":
        print_help()

    elif com == "music":
        clear_screen()
        print("Виберіть музику:")
        print("1. Toby Fox - My Castle Town (slowed) за замовчуванням")
        print("2. Toby Fox - Reunited (slowed)")
        print("3. Microsoft - Windows XP або title.wma (slowed)")
        print("4. Drax - Happy Happy Christmas (slowed)")
        print("5. Зупинити музику")
        choice = input("> ").strip()
        if choice == "1":
            play_music_safe("music/my_castle_town_slowed.mp3")
            print("Вибрано: My Castle Town")
        elif choice == "2":
            play_music_safe("music/reunited.mp3")
            print("Вибрано: Reunited")
        elif choice == "3":
            play_music_safe("music/title.mp3")
            print("Вибрано: title.wma (mp3замінник)")
        elif choice == "4":
            play_music_safe("music/hhchristmas.mp3")
            print("Вибрано: Happy Happy Christmas")
        elif choice == "5":
            pygame.mixer.music.stop()
            print("Музика зупинена.")
        else:
            print("Виберіть опцію 1-5.")

    elif com == "ls":
        list_music_folder()

    elif com == "clear":
        clear_screen()

    elif com == "exit":
        print("Бувай! ❄️")
        break

    elif com == "joke":
        print(random.choice(JOKES))

    elif com == "time":
        print("Поточний час:", time.strftime("%Y-%m-%d %H:%M:%S"))

    elif com.startswith("calc"):
        # приклад: calc 2+3*4
        parts = com.split(" ", 1)
        if len(parts) == 1 or parts[1].strip() == "":
            print("Використання: calc <вираз>, наприклад: calc 2+2*3")
        else:
            expr = parts[1].strip()
            try:
                result = safe_eval(expr)
                print(f"{expr} = {result}")
            except Exception as e:
                print("Помилка в обчисленні:", e)

    elif com == "dance":
        dance_animation()

    elif com == "whoami":
        print(f"Користувач: {usr}")

    elif com == "surprise":
        print(random.choice(QUOTES))

    elif com == "???":
        # Ось тут — спеціальна реакція
        show_pitsyatko_animation()

    else:
        # Розумніші підказки: схожі команди
        close_matches = [c for c in COMMANDS if sum(1 for a,b in zip(c, com) if a==b) >= max(1, len(c))]
