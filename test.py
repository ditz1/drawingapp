# Imports
import sys
import pygame
import ctypes

# Increas Dots Per inch so it looks sharper
# ONLY SET TRUE IF ON WINDOWS
win10 = 0

# Pygame Configuration
ifwin = input("are you on windows? [y/n]").strip().lower()

if (ifwin == 'y'):
    win10 = 1

if (win10):
    ctypes.windll.shcore.SetProcessDpiAwareness(win10)

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 1920, 900
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

font = pygame.font.SysFont('Arial', 20)

# Variables

# Our Buttons will append themself to this list
objects = []

# Initial color
drawColor = [255, 255, 255]

# Initial brush size
BRUSH_SIZE_DEFAULT = 10
brushSize = 10
brushSizeSteps = 5

# Drawing Area Size
canvasSize = [2000, 1000]

# Button Class:


class Button:
    def __init__(
            self,
            x,
            y,
            width,
            height,
            buttonText='Button',
            onclickFunction=None,
            onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#aaaaaa',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()

        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


# Handler Functions
last_color = ""
current_color = ""
# Changing the Color


def changeColor(color):
    global drawColor, last_color, current_color, brushSize
    drawColor = color

    if current_color == "":
        current_color = color
    else:
        last_color = current_color
        current_color = color

    print("last_color: ", last_color)
    print("current_color: ", current_color)

    if last_color != [2, 4, 0] and current_color == ([2, 4, 0]):
        print("switched to eraser")
        brushSize = brushSize * 3
    if last_color == [2, 4, 0] and current_color == [2, 4, 0]:
        print("stayed on eraser")
    if last_color == [2, 4, 0] and current_color != [2, 4, 0]:
        print("switched to color")
        brushSize = BRUSH_SIZE_DEFAULT

    print(brushSize)

# Changing the Brush Size


def changebrushSize(dir):
    global brushSize, last_color, current_color

    if dir == 'greater':
        brushSize += brushSizeSteps
    else:
        brushSize -= brushSizeSteps


# Save the surface to the Disk


def save():
    filename = input("what would you like to name your file:\n")
    pygame.image.save(canvas, f'{filename}.png')


# Button Variables.
buttonWidth = 150
buttonHeight = 50

# Buttons and their respective functions.
buttons = [
    ['Black', lambda: changeColor([0, 0, 0])],
    ['White', lambda: changeColor([255, 255, 255])],
    ['Blue', lambda: changeColor([0, 0, 255])],
    ['Green', lambda: changeColor([0, 255, 0])],
    ['Eraser', lambda: changeColor([2, 4, 0])],  # nasty hack
    ['Brush Larger', lambda: changebrushSize('greater')],
    ['Brush Smaller', lambda: changebrushSize('smaller')],
    ['Save', save],

]

top_padding = 60

button_y_start = top_padding
# Making the buttons
for index, buttonName in enumerate(buttons):
    Button(index * (buttonWidth + 10) + 10, button_y_start, buttonWidth,
           buttonHeight, buttonName[0], buttonName[1])

# Canvas
canvas = pygame.Surface(canvasSize)
canvas.fill((2, 4, 0))

last_pos = None

# Game loop.
while True:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # refresh canvas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (
                    pygame.key.get_mods() & pygame.KMOD_CTRL):
                canvas.fill((2, 4, 0))

        # clean exit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d and (
                    pygame.key.get_mods() & pygame.KMOD_CTRL):
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            last_pos = None

    x, y = screen.get_size()
    canvas_offset_y = top_padding + buttonHeight + 10
    # button_y = 50
    # Drawing the Buttons
    for object in objects:
        object.process()
    # Draw the Canvas at the center of the screen
        screen.blit(object.buttonSurface, (object.x, top_padding))
    # Drawing with the mouse
    canvas_x = x / 2 - canvasSize[0] / 2
    canvas_y = canvas_offset_y
    # canvas_y = y/2 - canvasSize[1]/2 + max(buttonHeight, brushSize)
    screen.blit(canvas, (canvas_x, canvas_y))

    def draw_smooth_line(surface, start_pos, end_pos, color, width):
        x1, y1 = start_pos
        x2, y2 = end_pos
        dx = x2 - x1
        dy = y2 - y1
        distance = max(abs(dx), abs(dy))

        for i in range(int(distance)):
            x = x1 + (dx * i) / distance
            y = y1 + (dy * i) / distance
            pygame.draw.circle(surface, color, (int(x), int(y)), width)

    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        current_pos = (mx, my)
        # Calculate Position on the Canvas
        if my > canvas_y:
            canvas_pos = (mx - canvas_x, my - canvas_y)
            if last_pos:
                draw_smooth_line(
                    canvas,
                    last_pos,
                    canvas_pos,
                    drawColor,
                    brushSize * 2,
                )
            last_pos = canvas_pos
        else:
            last_pos = None
    # Reference Dot
    # last_pos = None
    pygame.draw.circle(
        screen,
        drawColor,
        [1840, 40],
        brushSize,
    )

    pygame.display.flip()
    fpsClock.tick(fps)
