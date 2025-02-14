import pygame
import time
from random import randint

pygame.init()

back = (200, 255, 255)  # цвет фона
window = pygame.display.set_mode((500, 500))  # окно игры
window.fill(back)  # закрашиваем фон
clock = pygame.time.Clock()  # внутриигровые часы


# класс для карточек
class Area():
    # конструктор, задаем начальные параметры
    # место карточки x y, её ширина и высота width и height
    # и цвет color
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)  # прямоугольная область
        self.fill_color = color  # цвет карточки

    # изменение цвета карточки
    def color(self, new_color):
        self.fill_color = new_color

    # закрашивание карточки цветом
    def fill(self):
        pygame.draw.rect(window, self.fill_color, self.rect)

    # отрисовка рамки у карточки
    def outline(self, frame_color, size):
        pygame.draw.rect(window, frame_color, self.rect, size)

    # проверка на нажатие на карточку
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)


# класс-наследник для карточек с текстом
class Label(Area):
    # установить текст для карточки
    def set_text(self, text, fsize=12, color=(0, 0, 0)):
        self.font = pygame.font.SysFont('verdana', fsize)  # создание шрифта с размером fsize
        self.image = self.font.render(text, True, color)  # картинка с текстом цвета text_color

    # отрисовка карточки и текста
    def draw(self, shift_x=0, shift_y=0):
        self.fill()  # заливаем цветом карточку
        window.blit(self.image,
                    (self.rect.x + shift_x, self.rect.y + shift_y))  # отображаем текст со смещением вправо вниз


# цвета для карточек
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 100)
BLUE = (80, 80, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_RED = (250, 128, 114)
LIGHT_GREEN = (200, 255, 200)

cards = []  # список карточек
num_cards = 4  # количество карточек
x = 70  # координата первой карточки

start_time = time.time()  # время запуска игры
cur_time = start_time

# генерация карточек
for i in range(num_cards):
    card = Label(x, 170, 70, 100, YELLOW)  # карточка
    card.outline(BLUE, 10)  # синяя рамка карточки
    card.set_text('CLICK', 26)  # надпись на карточке
    cards.append(card)  # добавляем карточку в список
    x += 100  # смещаемся вправо

time_text = Label(0, 0, 50, 50, back)  # надпись "Время"
time_text.set_text('Время:', 40, DARK_BLUE)
time_text.draw(20, 20)  # отрисовываем
score_text = Label(380, 0, 50, 50, back)  # надпись "Счёт"
score_text.set_text('Счёт:', 45, DARK_BLUE)
score_text.draw(20, 20)  # отрисовываем

timer = Label(50, 55, 50, 40, back)  # надпись с временем
timer.set_text('0', 40, DARK_BLUE)
timer.draw(0, 0)  # отрисовываем

score = Label(430, 55, 50, 40, back)  # надпись с счетом
score.set_text('0', 40, DARK_BLUE)
score.draw(0, 0)  # отрисовываем

wait = 0  # время ожидания для смены карточки с CLICK
points = 0  # счет

""" Игровой цикл """
while True:
    # если вышло время для надписи CLICK
    if wait == 0:
        wait = 20  # восстанавливаем таймер
        num = randint(0, num_cards - 1)  # номер случайной карточки
        for i in range(num_cards):
            cards[i].color(YELLOW)  # каждую карточку закрашиваем желтым

            # если карточка с нужным номером
            if i == num:
                cards[i].draw(10, 40)  # устанавливаем текст CLICK
            # иначе
            else:
                cards[i].fill()  # просто закрашиваем карточку
    # если не вышло
    else:
        wait -= 1  # уменьшаем время

    # перебираем список событий
    for event in pygame.event.get():
        # если тип события "Нажата клавиша мыши" и клавиша мыши это Левая
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos  # координаты нажатия мышкой
            for i in range(num_cards):
                if cards[i].collidepoint(x, y):  # если нажатие попало в карточку
                    if i == num:  # и эта карточка с текстом CLICK
                        cards[i].color(GREEN)  # закрашиваем зеленым
                        points += 1  # прибавляем одно очко
                    else:  # иначе если НЕ с текстом CLICK
                        cards[i].color(RED)  # закрашиваем красным
                        points -= 1  # отнимаем одно очко
                    cards[i].fill()  # закрашиваем карточку
                    score.set_text(str(points), 40, DARK_BLUE)  # обновляем текст с счетом
                    score.draw(0, 0)

    new_time = time.time()  # фиксируем текущее время

    # если с начала игры прошло 11 или более секунд
    if new_time - start_time >= 11:
        # отображаем надпись "Время вышло!!!"
        lose = Label(0, 0, 500, 500, LIGHT_RED)
        lose.set_text('Время вышло!!!', 60, DARK_BLUE)
        lose.draw(110, 180)
        # и ломаем игровой цикл
        break

    # если прошла одна секунда
    if int(new_time) - int(cur_time) == 1:
        timer.set_text(str(int(new_time - start_time)), 40, DARK_BLUE)  # обновляем текст с временем
        timer.draw(0, 0)
        cur_time = new_time  # обновляем время

    # если счет больше или равен 5
    if points >= 5:
        # отображаем надпись "Ты победил!!!"
        win = Label(0, 0, 500, 500, LIGHT_GREEN)
        win.set_text('Ты победил!!!', 60, DARK_BLUE)
        win.draw(140, 180)
        # и отображаем надпись с временем прохождения игры
        result_time = Label(90, 230, 250, 250, LIGHT_GREEN)
        result_time.set_text('Время прохождения: ' + str(int(new_time - start_time)) + ' сек ', 40, DARK_BLUE)
        result_time.draw(0, 0)
        # и ломаем игровой цикл
        break
    # обновляем все окно игры
    pygame.display.update()
    clock.tick(30)
pygame.display.update()