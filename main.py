from abc import abstractmethod
import time
import re
import math
import cmath
import random
import sys
import json
import numpy as np
import print_responses


class Encoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class ChatEntry:
    def __init__(self, role, content):
        self.role = role
        self.content = content


class Chat:
    def __init__(self):
        self.entries = []

    def __add_user(self, content):
        self.entries.append(ChatEntry("user", content))

    def __add_bot(self, content):
        self.entries.append(ChatEntry("bot", content))

    def read(self):
        input_str = input("Користувач: ")
        self.__add_user(input_str)
        return input_str

    def write(self, content):
        print('\033[1;32;48m'+f"Бот: {content}"+'\033[1;37;0m')
        self.__add_bot(content)

    def read_files(self):
        self.write(print_responses.ask_text)
        file_name = self.read()
        try:
            with open(file_name, "r") as f:
                file_text = f.read()
                return file_text
        except FileNotFoundError:
            print("Файл не знайдено")
            return ""

    def write_files(self, content):
        self.write(print_responses.ask_text2)
        file_name = self.read()
        try:
            with open(file_name, "w") as f2:
                f2.write(str(content))
        except FileNotFoundError:
            print("Файл не знайдено")


chat = Chat()


class HandleInput:
    def __init__(self, dictionary):
        self.list_of_inputs = re.split(r"\s+|[,.;:_\-?!]", chat.read().strip().lower())
        self.inp = "Default"
        for n in self.list_of_inputs:
            if n == "назад":
                self.inp = "Back"
            elif n == "вихід":
                self.inp = "Stop"
            elif n[:4] in dictionary:
                self.inp = n[:4]
            elif n[:3] in dictionary:
                self.inp = n[:3]
            else:
                pass


class Context:
    def __init__(self, text, dictionary):
        self.text = text
        self._strategy = responses[dictionary][text]

    def do_method(self):
        result = self._strategy.method(self)
        chat.write(result)


class Strategy:
    @abstractmethod
    def method(self):
        pass


class Default(Strategy):
    def method(self):
        return print_responses.warn


class Help(Strategy):
    def method(self):
        return print_responses.help_bot


class Country(Strategy):
    def method(self):
        return print_responses.country


class Tense(Strategy):
    def method(self):
        return print_responses.tense


class Question(Strategy):
    def method(self):
        return print_responses.question


class Reservoir(Strategy):
    def method(self):
        return print_responses.reservoir


class Grammar(Strategy):
    def method(self):
        return print_responses.grammar


class Some(Strategy):
    def method(self):
        return print_responses.some_any


class Quotes(Strategy):
    def method(self):
        return random.choice(print_responses.quotes)


class Season(Strategy):
    def method(self):
        return {1: "Зима", 2: "Зима", 3: "Весна", 4: "Весна", 5: "Весна", 6: "Літо", 7: "Літо",
                8: "Літо", 9: "Осінь", 10: "Осінь", 11: "Осінь", 12: "Зима"}[time.localtime()[1]]


class Year(Strategy):
    def method(self):
        return time.localtime()[0]


class Distance(Strategy):
    def method(self):
        chat.write(print_responses.ask)
        inp_dist = re.split(r"\s+|;", re.sub("[^ 0-9.]", "", chat.read().strip()))
        list_dist = [float(i) for i in inp_dist if re.findall(r"\d", i)][:6]
        if len(list_dist) == 6:
            x1, y1, z1, x2, y2, z2 = list_dist
            res = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        else:
            res = print_responses.warn
        return res


class Area(Strategy):
    def method(self):
        chat.write(print_responses.ask_area)
        inp_dist = re.split(r"\s+", re.sub("[^ 0-9.]", "", chat.read().strip()))
        list_dist = [float(i) for i in inp_dist if re.findall(r"\d", i)][:3]
        if len(list_dist) == 3:
            a, a2, a3 = list_dist
            area = 1 / 2 * (a + a2) * a3
        else:
            area = print_responses.warn
        return area


class Quadratic(Strategy):
    def method(self):
        chat.write(print_responses.ask_equation)
        inp_dist = re.split(r"\s+", re.sub("[^ 0-9.]", "", chat.read().strip()))
        list_dist = [float(i) for i in inp_dist if re.findall(r"\d", i)][:3]
        if len(list_dist) == 3:
            a, b, c = list_dist
            d = (b ** 2) - (4 * a * c)
            sol1 = (-b - cmath.sqrt(d)) / (2 * a)
            sol2 = (-b + cmath.sqrt(d)) / (2 * a)
            return f"{sol1, sol2}"
        else:
            return print_responses.warn


class Circle(Strategy):
    def method(self):
        chat.write(print_responses.ask_circle)
        inp_dist = re.split(r"\s+", re.sub("[^ 0-9.]", "", chat.read().strip()))
        list_dist = [float(i) for i in inp_dist if re.findall(r"\d", i)][:2]
        if len(list_dist) == 2:
            a, a2 = list_dist
            circle = a * a2
        else:
            circle = print_responses.warn
        return circle


class Random(Strategy):
    def method(self):
        number = random.randint(1, 10)
        chat.write(print_responses.ask_num)
        inp_num = chat.read()
        if int(inp_num) == number:
            return f"Моє число: {number}. Ви виграли!"
        else:
            return f"Моє число: {number}. Ви програли!"


class Numbers(Strategy):
    def method(self):
        inp_text = re.split(r"\s+|[,.;:_\-?!]", chat.read_files())
        digits = len([i for i in inp_text if re.findall(r"\d", i)])
        chat.write_files(digits)
        return "Виконано"


class Latin(Strategy):
    def method(self):
        inp_text = re.split(r"\s+|[,.;:_\-?!]", chat.read_files())
        latin = list(dict.fromkeys([i for i in inp_text if re.findall("[a-zA-Z]", i) and inp_text.count(i) >= 10]))
        chat.write_files(latin)
        return "Виконано"


class Reverse(Strategy):
    def method(self):
        inp_text = chat.read_files()
        chat.write_files(inp_text[::-1])
        return "Виконано"


class Upper(Strategy):
    def method(self):
        inp_text = chat.read_files()
        chat.write_files(inp_text.upper())
        return "Виконано"


class Energy(Strategy):
    def method(self):
        chat.write(print_responses.choose_energy)
        inp_topic = chat.read().strip().lower()
        chat.write(print_responses.ask_energy)
        inp_ener = re.split(r"\s+", re.sub("[^ 0-9.]", "", chat.read().strip()))
        list_ener = [float(i) for i in inp_ener if re.findall(r"\d", i)][:3]
        if len(list_ener) == 3:
            a, a2, a3 = list_ener
            result = a3 - (a + a2)
            if "внутр" in inp_topic:
                b = f"Внутрішня енергія = {result}"
            elif "кін" in inp_topic:
                b = f"Кінетична енергія = {result}"
            elif "пот" in inp_topic:
                b = f"Потенційна енергія = {result}"
            else:
                b = print_responses.warn
        else:
            b = print_responses.warn
        return b


class Boyle(Strategy):
    def method(self):
        chat.write(print_responses.choose_boyle)
        inp_topic = chat.read().strip().lower()
        chat.write(print_responses.ask_pressure)
        inp_pres = re.split(r"\s+", re.sub("[^ 0-9.]", "", chat.read().strip()))
        list_pres = [float(i) for i in inp_pres if re.findall(r"\d", i)][:3]
        if len(list_pres) == 3:
            a, a2, a3 = list_pres
            result = (a * a2) / a3
            if "p1" in inp_topic:
                b = f"P1 = {result}"
            elif "v1" in inp_topic:
                b = f"V1 = {result}"
            else:
                b = print_responses.warn
        else:
            b = print_responses.warn
        return b


class Line(Strategy):
    def method(self):
        chat.write(print_responses.ask_line)
        inp_line = re.split(r"\s+", re.sub("[^ 0-9.]", "", chat.read().strip()))
        list_line = [float(i) for i in inp_line if re.findall(r"\d", i)][:9]
        if len(list_line) == 9:
            x1, x2, x3, x4, x5, x6, x7, x8, x9 = list_line
            p = np.array([x1, x2, x3])
            a = np.array([x4, x5, x6])
            b = np.array([x7, x8, x9])
            d = np.divide(b - a, np.linalg.norm(b - a))
            s = np.dot(a - p, d)
            t = np.dot(p - b, d)
            hh = np.maximum.reduce([s, t, 0])
            c = np.cross(p - a, d)
            return np.hypot(hh, np.linalg.norm(c))
        else:
            return print_responses.warn


class Pi(Strategy):
    def method(self):
        return math.pi


class Response1(Strategy):
    def method(self):
        return print_responses.response1


class Response2(Strategy):
    def method(self):
        return print_responses.response2


class Response3(Strategy):
    def method(self):
        return print_responses.response3


class Response4(Strategy):
    def method(self):
        return print_responses.response4


class Response5(Strategy):
    def method(self):
        return print_responses.response5


class Response6(Strategy):
    def method(self):
        return print_responses.response6


class Response7(Strategy):
    def method(self):
        return print_responses.response7


class Response8(Strategy):
    def method(self):
        return print_responses.response8


responses = {
    "мате": {"точк": Distance, "прям": Line, "площ": Area, "пі": Pi, "квад": Quadratic, "кол": Circle,
             "Default": Default, "допо": Help},
    "філо": {"рід": Grammar, "род": Grammar, "час": Tense, "pres": Tense, "пит": Question, "some": Some,
             "Default": Default, "допо": Help},
    "фізи": {"енер": Energy, "бойл": Boyle, "Default": Default, "допо": Help},
    "геог": {"вод": Reservoir, "корд": Country, "Default": Default, "допо": Help},
    "зага": {"пора": Season, "рік": Year, "цита": Quotes, "числ": Random, "Default": Default, "допо": Help},
    "текс": {"лати": Latin, "цифр": Numbers, "звор": Reverse, "верх": Upper, "Default": Default, "допо": Help},
    "інфо": {"інфо": Response1, "комп": Response2, "інте": Response3, "коду": Response4,
             "алго": Response5, "блок": Response6, "прог": Response7, "числ": Response8,
             "Default": Default, "допо": Help},
    "допо": {"Default": Default}}


class Bot:

    @staticmethod
    def log_chat():
        """У файлі config.json введіть шлях до файлу в такому форматі C:\\...\\...\\...\\,
        в іншому разі діалог збережеться в директорії з цим кодом"""
        with open("config.json", "r") as configuration:
            path = json.load(configuration)["path"]
        with open(path + "output.json", "w", encoding="UTF-8") as file:
            json.dump(chat, file, cls=Encoder)

    def chat(self):
        while True:
            chat.write(print_responses.greeting)
            h1 = HandleInput(responses)
            if h1.inp == "Back":
                continue
            elif h1.inp == "Stop":
                self.log_chat()
                sys.exit()
            elif h1.inp == "Default":
                chat.write(print_responses.topics[h1.inp])
                continue
            else:
                while True:
                    chat.write(print_responses.topics[h1.inp])
                    h = HandleInput(responses[h1.inp])
                    if h.inp == "Back":
                        break
                    elif h.inp == "Stop":
                        self.log_chat()
                        sys.exit()
                    else:
                        number_1 = random.randint(1, 50)
                        if number_1 == 1:
                            chat.write(print_responses.google)
                        else:
                            pass
                        Context(h.inp, h1.inp).do_method()


if __name__ == "__main__":
    bot = Bot()
    bot.chat()
