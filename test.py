# Imports
import sys
import pygame
import ctypes

# Increas Dots Per inch so it looks sharper
# ONLY SET TRUE IF ON WINDOWS
win10 = False

# Pygame Configuration
ifwin = input("are you on windows? [y/n]").strip().lower()

if (ifwin == 'y'):
    win10 = True

if (win10):
    ctypes.windll.shcore.SetProcessDpiAwareness(win10)

pygame.init()
fps = 500
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
brushSize = 20
brushSizeSteps = 3

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

# Changing the Color
def changeColor(color):
    global drawColor
    drawColor = color

# Changing the Brush Size


def changebrushSize(dir):
    global brushSize
    if dir == 'greater':
        brushSize += brushSizeSteps
    else:
        brushSize -= brushSizeSteps

# Save the surface to the Disk


def save():
    pygame.image.save(canvas, "canvas.png")


# Button Variables.
buttonWidth = 150
buttonHeight = 50

# Buttons and their respective functions.
buttons = [
    ['Black', lambda: changeColor([0, 0, 0])],
    ['White', lambda: changeColor([255, 255, 255])],
    ['Blue', lambda: changeColor([0, 0, 255])],
    ['Green', lambda: changeColor([0, 255, 0])],
    ['Eraser', lambda: changeColor([2, 4, 24])],  # nasty hack
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
canvas.fill((2, 4, 24))

# Game loop.
while True:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (
                    pygame.key.get_mods() & pygame.KMOD_CTRL):
                canvas.fill((2, 4, 24))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d and (
                    pygame.key.get_mods() & pygame.KMOD_CTRL):
                pygame.quit()
                sys.exit()

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

    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        # Calculate Position on the Canvas
        if my > canvas_y:
            dx = mx - canvas_x
            dy = my - canvas_y
            pygame.draw.circle(
                canvas,
                drawColor,
                [dx, dy],
                brushSize,
            )
    # Reference Dot
    pygame.draw.circle(
        screen,
        drawColor,
        [1840, 40],
        brushSize,
    )

    pygame.display.flip()
    fpsClock.tick(fps)
