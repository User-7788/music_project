import random

import PIL
from PIL import ImageTk
import pygame
from tkinter.filedialog import askopenfilename
import os
import shutil
from tkinter import *

COLOR_1 = (0, 100, 200)

path_to_music = os.path.abspath('music')
pygame.init()

d = 0
paused_song = None
round_b_is_cliced = False

width = 600
height = 580
size = width, height

screen = pygame.display.set_mode(size)
pygame.display.set_caption("DON'T CLOSE")
running = True

icon = pygame.image.load('data/qwertyy.jpg')
pygame.display.set_icon(icon)

draw_p_bs = [False, -1]

s = False
P = 1


class button:
    def __init__(self, x, y, cliced=False, w=300, h=50, sec=(255, 0, 70)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.cliced = cliced
        self.color_now = (100, 0, 0)
        self.color_2 = sec
        self.color_1 = (100, 0, 0)

    def draw(self, text, xy, big=50):
        font = pygame.font.Font(None, big)
        pygame.draw.rect(screen, self.color_now, (self.x, self.y,
                                                  self.w, self.h))

        screen.blit(font.render(text, 1, (255, 255, 255)), xy)
        # screen.blit(font.render(text, 1, (255, 255, 255)), (self.x + (self.h // 4), self.y + (self.h // 4)))

    def is_cliced(self):
        x_m, y_m = event.pos
        if (x_m <= (self.x + self.w) and (x_m >= self.x)) and (
                y_m <= (self.y + self.h) and (y_m >= self.y)):
            return True
        return False

    def should_i_color(self, pos, do_it=False):
        x_m, y_m = pos
        if ((x_m <= (self.x + self.w) and (x_m >= self.x)) and (
                y_m <= (self.y + self.h) and (y_m >= self.y))) or do_it:
            self.color_now = self.color_2
        else:
            self.color_now = self.color_1


adb = button(5, 5, w=50)
what_b = button(545, 5, w=50)
delete_b = button(440, 5, w=100)
pause_b = button(170, 5, w=50)
r_b = button(225, 5, w=50)
l_b = button(115, 5, w=50)
round_b = button(280, 5, w=50)
shuffle_b = button(335, 5, w=50)


class music:
    def __init__(self, file_name, position, sec=(30, 0, 200), is_pl=False):
        global COLOR_1
        self.file_name = file_name
        self.position = position
        self.y = adb.y + adb.h + (5 * self.position) + ((self.position - 1) * 35)
        self.w = 590
        self.h = 35
        self.x = 5
        self.color_now = COLOR_1
        self.color_2 = sec
        self.color_1 = COLOR_1
        self.is_pl = is_pl

    def draw(self, big=25):
        font = pygame.font.Font(None, big)
        self.y = adb.y + adb.h + (5 * self.position) + ((self.position - 1) * 35)
        pygame.draw.rect(screen, self.color_now, (self.x, self.y,
                                                  self.w, self.h))
        if len(self.file_name) > 80:
            d = self.file_name[:80]
        else:
            d = self.file_name

        screen.blit(font.render(d, 1, (255, 255, 255)), (self.x + (self.h // 4), self.y + (self.h // 4)))

    def should_i_color(self, pos, special=None):

        x_m, y_m = pos
        if ((x_m <= (self.x + self.w) and (x_m >= self.x)) and (
                y_m <= (self.y + self.h) and (y_m >= self.y))):
            if special == None:
                self.color_now = self.color_2
            else:
                self.color_now = special
        else:
            self.color_now = self.color_1

    def is_cliced(self):
        x_m, y_m = event.pos
        if (x_m <= (self.x + self.w) and (x_m >= self.x)) and (
                y_m <= (self.y + self.h) and (y_m >= self.y)):
            return True
        return False


delete_b_is_cliced = False

try:
    list_music = []
    g = open("br.txt", mode="r")
    txt = list(map(int, g.read().split()))
    for dir, subdir, files in os.walk(path_to_music):
        for f in range(len(files)):
            m = music(os.path.basename(os.path.abspath(files[f])), txt[f])
            list_music.append(m)
    g.close()

    list_music.sort(key=lambda i: i.position)

except Exception:
    list_music = []
    for dir, subdir, files in os.walk(path_to_music):
        for f in files:
            m = music(os.path.basename(os.path.abspath(f)), len(list_music) + 1)
            list_music.append(m)

while running:
    pygame.display.flip()
    screen.fill((5, 5, 5))

    for h in list_music:
        if round_b_is_cliced and not pygame.mixer.music.get_busy() and h.is_pl:
            fullname = os.path.join('music', h.file_name)
            pygame.mixer.music.load(fullname)
            pygame.mixer.music.play(0)

        elif not pygame.mixer.music.get_busy() and h.is_pl:
            x = list_music.index(h) + 1
            if x > (len(list_music) - 1):
                x = 0
            fullname = os.path.join('music', list_music[x].file_name)
            pygame.mixer.music.load(fullname)
            pygame.mixer.music.play(0)
            h.is_pl = False
            list_music[x].is_pl = True

            h.color_1 = COLOR_1
            list_music[x].color_1 = (0, 0, 0)

    poss = pygame.mouse.get_pos()

    adb.draw("+", (adb.x + (adb.w // 4), adb.y + (adb.h // 20)), big=60)
    what_b.draw("?", (what_b.x + (what_b.w // 3.5), what_b.y + (what_b.h // 5)), big=52)
    delete_b.draw("DELETE", (delete_b.x + (delete_b.h // 6), delete_b.y + (delete_b.h // 5)), big=30)
    r_b.draw(">>", (r_b.x + (r_b.h // 4), r_b.y + (r_b.h // 4)), big=35)
    l_b.draw("<<", (l_b.x + (l_b.h // 4), l_b.y + (l_b.h // 4)), big=35)
    # ⟳ = u"\u27F3"
    round_b.draw('round', (round_b.x + (round_b.h // 10), round_b.y + (round_b.h // 3)), big=20)
    shuffle_b.draw('shuffle', (shuffle_b.x + (round_b.h // 20), shuffle_b.y + (shuffle_b.h // 3)), big=20)

    if draw_p_bs[0] and draw_p_bs[1] == 1:
        pause_b.draw(u"\u258C" + u"\u258C", (pause_b.x + (pause_b.h // 4), pause_b.y + (pause_b.h // 4)), big=42)

    elif draw_p_bs[0] and draw_p_bs[1] == 2:
        # ▷ = u"\u25B7"
        pause_b.draw('PLAY', (pause_b.x + (pause_b.h // 4), pause_b.y + (pause_b.h // 4)), big=15)

    if s:
        font = pygame.font.Font(None, 20)
        screen.blit(font.render('(choice)', 1, (255, 255, 255))
                    , (delete_b.x + (delete_b.h // 4) + 15, delete_b.y + (delete_b.h // 3.5) + 15))

    adb.should_i_color(poss)
    what_b.should_i_color(poss)
    delete_b.should_i_color(poss)
    pause_b.should_i_color(poss)
    r_b.should_i_color(poss)
    l_b.should_i_color(poss)
    round_b.should_i_color(poss)
    shuffle_b.should_i_color(poss)

    for m in list_music[P - 1:P + 13]:
        m.draw()
        m.should_i_color(poss)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            a = []
            list_music.sort(key=lambda i: i.file_name)
            for i in list_music:
                a.append(str(i.position + P - 1))
            f = open("br.txt", mode="w")
            f.write(' '.join(a))
            f.close()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if shuffle_b.is_cliced():
                poses = list(i.position for i in list_music)
                random.shuffle(list_music)
                for i in range(0, len(list_music)):
                    list_music[i].position = poses[i]
                COLOR_1 = (random.randint(10, 250), random.randint(10, 250), random.randint(10, 250))
                for m in list_music:
                    if not m.is_pl and paused_song != m.is_pl:
                        m.color_1 = COLOR_1

            if r_b.is_cliced():
                for i in list_music:
                    if i.is_pl:
                        x = list_music.index(i) + 1
                        if x > (len(list_music) - 1):
                            x = 0
                        i.is_pl = False
                        list_music[x].is_pl = True
                        fullname = os.path.join('music', list_music[x].file_name)
                        pygame.mixer.music.load(fullname)
                        pygame.mixer.music.play(0)

                        if delete_b_is_cliced:
                            i.color_1 = (150, 100, 0)
                        else:
                            i.color_1 = COLOR_1
                        list_music[x].color_1 = (0, 0, 0)
                        break

            if l_b.is_cliced():
                for i in list_music:
                    if i.is_pl:
                        x = list_music.index(i) - 1
                        if x < 0:
                            x = len(list_music) - 1
                        i.is_pl = False
                        list_music[x].is_pl = True
                        fullname = os.path.join('music', list_music[x].file_name)
                        pygame.mixer.music.load(fullname)
                        pygame.mixer.music.play(0)

                        if delete_b_is_cliced:
                            i.color_1 = (150, 100, 0)
                        else:
                            i.color_1 = COLOR_1
                        list_music[x].color_1 = (0, 0, 0)
                        break

            if pause_b.is_cliced() and draw_p_bs[1] == 1:
                pygame.mixer.music.pause()
                draw_p_bs[1] = 2
                for h in list_music:
                    if h.is_pl:
                        h.is_pl = False
                        paused_song = h

            elif pause_b.is_cliced() and draw_p_bs[1] == 2:
                pygame.mixer.music.unpause()
                draw_p_bs[1] = 1
                paused_song.is_pl = True
                paused_song = None

            if adb.is_cliced():
                try:
                    # formals
                    root = Tk()
                    try:
                        file = askopenfilename(defaultextension='.mp3', filetypes=[('All files', '*.mp3')])
                        f = file[:-4] + '0' + '.mp3'
                        m = music(os.path.basename(f), len(list_music) + 1)
                        if m not in list_music:
                            shutil.copy(file, f)
                            shutil.move(os.path.abspath(f), path_to_music)
                            root.destroy()

                            # interface
                            list_music.append(m)
                        else:
                            os.remove(os.path.basename(f))


                    except Exception:
                        root.destroy()

                except Exception:
                    pass
            if delete_b.is_cliced():
                delete_b_is_cliced = not delete_b_is_cliced
                s = not s
                if delete_b_is_cliced:
                    for m in list_music:
                        if m.is_pl or paused_song == m:
                            m.color_1 = (0, 0, 0)
                        else:
                            m.color_1 = (150, 100, 0)

                else:
                    for m in list_music:
                        if m.is_pl or paused_song == m:
                            m.color_1 = (0, 0, 0)
                        else:
                            m.color_1 = COLOR_1

            if round_b.is_cliced():
                round_b_is_cliced = not round_b_is_cliced
                if round_b_is_cliced:
                    round_b.color_1 = (200, 0, 200)

                else:
                    round_b.color_1 = (100, 0, 0)

            for m in list_music:
                if m.is_cliced() and delete_b_is_cliced:
                    if not m.is_pl and paused_song != m:
                        for mu in list_music[(list_music.index(m) + 1):]:
                            mu.position -= 1
                        list_music.remove(m)
                        os.remove('music' + '\\' + m.file_name)
                elif m.is_cliced():
                    for h in list_music:
                        h.color_1 = COLOR_1
                        h.is_pl = False
                    m.color_1 = (0, 0, 0)
                    m.is_pl = True
                    d += 1

                    fullname = os.path.join('music', m.file_name)
                    pygame.mixer.music.load(fullname)

                    if round_b_is_cliced:
                        pygame.mixer.music.play(-1)

                    else:
                        pygame.mixer.music.play(0)

                    draw_p_bs = [True, 1]

            if what_b.is_cliced():

                root = Tk()
                root.title('Инструкция')
                img = ImageTk.PhotoImage(PIL.Image.open("data/ИНСТРУКЦИЯ.PNG"))
                panel = Label(root, image=img)
                panel.pack(side="bottom", fill="both", expand="yes")
                root.mainloop()

        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if len(list_music) > 13:
                if key[pygame.K_DOWN] and P < len(list_music):
                    P += 1
                    for m in list_music:
                        m.position = m.position - 1

                elif key[pygame.K_UP] and P > 1:
                    P -= 1
                    for m in list_music:
                        m.position = m.position + 1

pygame.quit()
