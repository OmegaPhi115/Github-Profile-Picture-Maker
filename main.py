# You can change those values

size_x = 5 # number of squares per rows , 5 is default, put "auto" for automatic
size_y = "auto" # number of squares per colums, 5 is default, put "auto" for automatic


square_chance = 0.5 # chance of a square apearing, betwin 0 and 1


picture_size_px_x = 420 # size of the picture in x, 420 is default
picture_size_px_y = 420 # size of the picture in y, 420 is default


border_width = 42


color_primary = (0, 200, 0) # color of the pixels
color_secondary = (240, 240, 240) # color of the background

# //////// Epilepsy Warning ! /////////
FPS = 5 # higher fps mean more flickering and more cpu load

# Don't change anything from there ! Unless you're working on the code

square_side_lenght = "This is to make Pycharm show this variable in the autocompletion, if you seeing this message " \
                     "while running the code, you screwed"

# first, sanitize inputs:

# Full auto mode don't exist
if size_x == "auto" and size_y == "auto":
    raise Exception("You can't have auto on both sizes !")

#border to large
if border_width*2 >= picture_size_px_x:
    raise Exception("The picture size is too short in the x dimension, try increasing it or reducing the border's width")
elif border_width*2 >= picture_size_px_x:
    raise Exception("The picture size is too short in the y dimension, try increasing it or reducing the border's width")

# then calculate values
def parameter_checker():
    # first, calculate the side lenght of each squares
    #
    # when calculating the side lenght, it the border must be >= border_width
    global square_side_lenght, border_width, size_y, size_x

    if size_y == "auto":
        pixel_space = picture_size_px_x - (border_width * 2)  # calculate area of possible square

        square_side_lenght = int(pixel_space / size_x)  # calculate max possible side lenght in the area

        if square_side_lenght < 1:  # if the lenght is under a pixel large (cannot be displayed) then abord
            raise Exception("The picture size is too short in the x dimension, try increasing it or reducing the "
                            "number of squares to create")

        # recalculate actual pixel space taken
        pixel_space = (square_side_lenght * size_x)

        # now increase the border width with leftover space
        border_width = (picture_size_px_x - pixel_space) / 2
        border_width = int(border_width)

        # finaly calculate size_y
        pixel_space = picture_size_px_y - (border_width * 2)
        size_y = pixel_space / square_side_lenght

    elif size_x == "auto": # same thing but with x & y inverted
        pixel_space = picture_size_px_y - (border_width * 2)  # calculate area of possible square

        square_side_lenght = int(pixel_space / size_y)  # calculate max possible side lenght in the area

        if square_side_lenght < 1:  # if the lenght is under a pixel large (cannot be displayed) then abord
            raise Exception("The picture size is too short in the y dimension, try increasing it or reducing the "
                            "number of squares to create")

        # recalculate actual pixel space taken
        pixel_space = (square_side_lenght * size_y)

        # now increase the border width with leftover space
        border_width = (picture_size_px_y - pixel_space) / 2
        border_width = int(border_width)

        # finaly calculate size_x
        pixel_space = picture_size_px_x - (border_width * 2)
        size_x = pixel_space / square_side_lenght

    else: # both are given: make squares has big as possible
        #todo limited numbers
        pass


parameter_checker()

# import stuffs
import random
import pygame
import pygame.mixer
from pygame.locals import *
import numpy as np

pygame.init()
Image_size_tuple = (picture_size_px_x, picture_size_px_y)


def Create_Image_Structure(sizex, sizey):
    """
    Image structure:
    X: Draw pixel
    O: Don't draw pixel
    E: End of line

    Other characters will be discarded
    """

    image_text = ""
    for Dontcare in range(int(sizey)):

        # Making a row
        image_text_row = ""
        for atall in range(int(sizex)):
            image_text_row += np.random.choice(["X", "O"], p=[square_chance, 1 - square_chance])

        # Putting "end of line" character
        image_text_row += "E"

        # Adding it in the main thing
        image_text += image_text_row
    return image_text

class image: # this class will be deleted, coding at 3am don't help to write good code
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


# Starting display
image_txt = Create_Image_Structure(size_x, size_y)
surface = pygame.display.set_mode(Image_size_tuple)

#oijriuhiuhihiuhiuhiuhih
#image_maker = image(surface, picture_size_px, size_x, color_primary, color_secondary)
#image_maker.make_image(image_txt)
#oijikihkqhspuhfyhuiuhoihwoehf

#mainloop
Launched = True


def Display_changes():
    # clean old squares
    surface.fill(color_secondary)
    # make squares
    cursor = [0, 0]  # what pixel im looking at
    cursor = [border_width, border_width]  # put cursor at the top left corner of drawing area
    for character in image_txt:  # reading letters one-by-one in the image string
        if character == "X":  # Draw a square:
            rect = Rect(cursor[0], cursor[1], square_side_lenght, square_side_lenght)
            pygame.draw.rect(surface, color_primary, rect)
            cursor[0] += square_side_lenght

        elif character == "O":  # skip to the next square
            cursor[0] += square_side_lenght

        elif character == "E":  # go back to the start + one line
            cursor[0] = border_width
            cursor[1] += square_side_lenght
    pygame.display.flip()

Display_changes()
while Launched:
    pygame.time.Clock().tick(5)# reduce to 5fps

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Launched = False

    if event.type == MOUSEBUTTONDOWN and event.button == 1:
        image_txt = Create_Image_Structure(size_x, size_y)
        Display_changes()

    if event.type == MOUSEBUTTONDOWN and event.button == 2:
        image_txt = Create_Image_Structure(size_x, size_y)
        color_primary = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        Display_changes()

    if event.type == MOUSEBUTTONDOWN and event.button == 3:
        color_primary = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        Display_changes()

    if event.type == KEYDOWN:
        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        #print(pygame.key.get_pressed())
        if event.key == K_s and ctrl_held:
            pygame.image.save(surface, "output.png") # todo multiple saves
