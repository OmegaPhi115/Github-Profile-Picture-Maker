# You can change those values
size = 5 #number of "pixel" per rows and colums
taille_px = 420 #size of the picture
color_primary = (255, 20, 116) #color of the pixels
color_secondary = (240, 240, 240) #color of the backgroun


# Don't change anything from there ! Unless you're working on the code

import random
import pygame
import pygame.mixer
from pygame.locals import *
pygame.init()

#entrées
taille_px_tuple = (taille_px, taille_px)

def Create_image(size):
    image_text = []
    for ia in range(size):
        image_text_compo = []
        for ib in range(size):
            image_text_compo.append(random.choice(["X", " "]))
        image_text.append(image_text_compo)
    return image_text

class image:
    def __init__(self, surface, screen_size, row_size, color_primary, color_secondary):
        self.surface = surface
        self.screen_size = screen_size
        self.row_size = row_size
        self.pixl_size = self.screen_size / (self.row_size + 1)
        self.border_size = self.pixl_size / 2
        self.color_primary = color_primary
        self.color_secondary = color_secondary
        self.last_list = ""

    def draw_pixl(self, x, y):
        a = Rect(self.Coo_to_pixl(x), self.Coo_to_pixl(y), self.pixl_size, self.pixl_size)
        pygame.draw.rect(self.surface, self.color_primary, a)
        pygame.display.flip()

    def Coo_to_pixl(self, x):
        return (x * self.pixl_size) + self.border_size

    def draw_row(self, row):
        for coo in row:
            self.draw_pixl(coo[0], coo[1])

    def draw_list(self, list_coo):
        for row in list_coo:
            self.draw_row(row)

    def make_image(self, list):
        self.last_list = list
        self.surface.fill(self.color_secondary)
        list_coo = []
        y = 0
        for row in list:
            x = 0
            list_coo_compo = []
            for a in row:
                if a == "X":
                    list_coo_compo.append([x, y])
                x += 1
            list_coo.append(list_coo_compo)
            y += 1
        self.draw_list(list_coo)

    def actu(self):
        self.make_image(self.last_list)


image_txt = Create_image(size)
surface = pygame.display.set_mode(taille_px_tuple)
image_maker = image(surface, taille_px, size, color_primary, color_secondary)
image_maker.make_image(image_txt)
Launched = True
while Launched:
    pygame.time.Clock().tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Launched = False

    if event.type == MOUSEBUTTONDOWN and event.button == 1:
        image_txt = Create_image(size)
        image_maker.make_image(image_txt)

    if event.type == MOUSEBUTTONDOWN and event.button == 2:
        image_txt = Create_image(size)
        image_maker.last_list = image_txt
        color_primary = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        image_maker.color_primary = color_primary
        image_maker.actu()

    if event.type == MOUSEBUTTONDOWN and event.button == 3:
        color_primary = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        image_maker.color_primary = color_primary
        image_maker.actu()

    if event.type == KEYDOWN:
        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        #print(pygame.key.get_pressed())
        if event.key == K_s and ctrl_held:
            pygame.image.save(surface, "output.png")

    pygame.display.flip()
