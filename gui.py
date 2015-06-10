import pygame, sys
from pygame.locals import *
from random import randint
from updatefield import *

#TODO:
# DONEreplace number in corner with colored box -- FIRST!
# DONEget modes working
# list how many died, etc...
# darken dice colors when cell dies (instead of dark blue)
# sounds!
# make everything resizable

def tocolor(char):
    if char in '123456':
        return diceColors[int(char)-1]
    return colormap[char]


def drawstage(field, num, msg):
    # clear screen
    windowSurfaceObj.fill(whiteColor)

    # draw the field
    for height, row in enumerate(field):
        for width, char in enumerate(row):
            color = tocolor(char)
            pygame.draw.rect(windowSurfaceObj, color, ((boxw+2)*width, (boxh+2)*height, boxw, boxh))

    # write the message
    msgSurfaceObj = msgFontObj.render(msg, False, blackColor)
    msgRectObj = msgSurfaceObj.get_rect()
    msgRectObj.topleft = (100, fieldw)
    windowSurfaceObj.blit(msgSurfaceObj, msgRectObj)

    # draw selection square
    pygame.draw.rect(windowSurfaceObj, tocolor(num), (boxw, windowh-2*boxh, boxw, boxh))

    # update display
    pygame.display.update()


pygame.init()
fpsClock = pygame.time.Clock()

windoww, windowh = 640, 480
windowSurfaceObj = pygame.display.set_mode((windoww, windowh))
pygame.display.set_caption("Forts and Ruins")


redColor      = (255,0,  0  )
darkredColor  = (50, 0,  0  )
greenColor    = (0,  255,0  )
blueColor     = (0,  0,  255)
darkblueColor = (0,  0,   50)
blackColor    = (0,  0,  0  )
grayColor     = (122,122,122)
darkgrayColor = (50, 50, 50 )
whiteColor    = (255,255,255)
diceColors = tuple(tuple(randint(100, 255) for ___ in xrange(3)) for __ in xrange(6))
deaddiceColors = tuple(tuple(val - 50 for val in color) for color in diceColors)

colormap = {'-':darkgrayColor,
            'F':redColor,
            'f':darkredColor,
            'T':blueColor,
            't':darkblueColor}
    

msgFontObj = pygame.font.Font('freesansbold.ttf', 32)
msg = 'make a move, johny!'
num = '1'

boxw, boxh = 20, 20
fieldw, fieldh = 400, 200
field = [ ['-' for __ in xrange(fieldw//(boxw+2))] for ___ in xrange(fieldh//(boxh+2)) ]
field[4][4] = 'F'

history = [deepcopy(field)]
histplace = 0
dicekeys = [K_1, K_2, K_3, K_4, K_5, K_6]
mode = "normal"


while True: # main game loop

    if mode == "normal":
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # if the user pressed a number
            elif event.type==KEYDOWN and event.key in dicekeys:
                num = str(event.key-48)

            elif event.type==MOUSEBUTTONUP and event.button==1:
                mousex, mousey = event.pos
                if 0 < mousex < fieldw and 0 < mousey < fieldh:
                    row = mousey // (boxh + 2)
                    column = mousex // (boxw + 2)
                    char = field[row][column]
                    if char != '-':
                        msg = "must click unused space!"
                        continue
                    field[row][column] = num
                    history.append(deepcopy(field))
                    field = updatefield(field)
                    history.append(deepcopy(field))
                    if not any(any(char in row for row in field) for char in "F123456"):
                        histplace = len(history)-1
                        mode = "replay"
                else:
                    msg = 'you clicked the void!'

        drawstage(field, num, msg)

        fpsClock.tick(30)

    elif mode == "replay":
        drawstage(history[histplace], '1', "REPLAY")
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key == K_LEFT:
                    histplace = max(histplace-1, 0)
                if event.key == K_RIGHT:
                    histplace = min(histplace+1, len(history)-1)
                if event.key == K_q:
                    field = history[0]
                    msg = "new game"
                    num = '1'
                    mode = "normal"
