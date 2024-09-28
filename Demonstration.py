import numpy as np
import pygame, pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.toggle import Toggle

def unitVec(startPos:tuple, endPos:tuple, state=""):
    """
    Creates a unit vector from the specified endpoint of the line

    Parameters:
    startPos: tuple - the starting position of the vector
    endPos: tuple - the end position of the vector
    state: string - changes the behaviour of the function
    
    Returns:
    vec: float - the calculated unit vector
    """
    dx = endPos[0] - startPos[0]
    dy = endPos[1] - startPos[1]
    mag = np.sqrt(dx**2+dy**2)
    if state == "boundary":
        # This will return the normal unit vector of the boundary line produced
        vec = np.array([-dy,dx])
        vec = (1/mag)*vec
        return vec
    else:
        vec = np.array([dx,dy])
        vec = (1/mag)*vec
        return vec

def opticCalc(n1:float, n2:float, vecA:float, vecB:float, vecC=np.array([1,0]), quadrant=1):
    """
    Applies Snell's Law to calculate the refracted angle of the light ray, whilst
    also returning the reflected angle

    Parameter:
    n1: float - the refractive index of the first medium
    n2: float - the refractive index of the second medium
    vecA: float - the unit vector of the light ray
    vecB: float - the unit vector of the axis (the normal to the boundary)
    vecC: float - the unit vector on a unit circle
    quadrant: int - specifies the quadrant where the angle is taken

    Returns:
    All angles are measured in radians and measured relative to vecC
    alphaI: float - the incident angle
    alphaRefl: float - the reflected angle
    alphaRefr: float - the refracted angle
    alphaTrans: float - (only returned in quadrant 1) the angle between vecB and vecC
    """

    if quadrant==1:
        alphaTrans = np.arccos(np.dot(vecC,vecB)) # Angle between vecC and vecB
        alphaI = np.arccos(np.dot(vecA,vecB)) - alphaTrans
        alphaRefl = alphaTrans - alphaI
        if n1/n2 > 1:
            alphaRefr = None
        else:
            alphaRefr = (np.arcsin(n1*np.sin(alphaI)/n2))
        return alphaI,alphaRefl,alphaRefr,alphaTrans
    elif quadrant==2:
        alphaTrans = np.arccos(np.dot(vecC,-vecB)) # For now this is redundant
        alphaI = -np.arccos(np.dot(-vecB,-vecA)) + alphaTrans
        alphaRefl = -alphaI
        if n2/n1 > 1:
            alphaRefr = None
        else:
            alphaRefr = -(np.arcsin(n2*np.sin(alphaI)/n1)) + np.pi
        return alphaI,alphaRefl,alphaRefr

def drawVec(startPos:tuple, alpha:float, colour, window, mag=1000):
    """
    Draws the unit vector using pygame.draw.line()

    Parameter:
    startPos: tuple - the point to draw the unit vector from
    alpha: float - the angle to draw the unit vector
    colour: float - the RGB value of the colour
    window - the pygame window to display the line onto
    mag: int - the magnitude to draw the unit vector
    """
    origin = np.array(startPos)
    if alpha==None:
        pass
    else:
        unitCricle = np.array([np.cos(alpha),np.sin(alpha)])
        endPos = origin + mag*unitCricle
        pygame.draw.line(window,colour,startPos,endPos)

def radToDeg(angle):
    """
    Converts radians to degrees, for a more intuitive understanding of
    the angles the lines are draw at

    Parameter:
    angle: float - the angle which to convert

    Returns:
    val: float - the angle in degrees
    """
    if angle==None:
        val = 0
        return val
    else:
        val = angle*180/np.pi
        return val

# Constants
WHITE = (255,255,255); RED = (255,0,0); BLUE = (0,0,255); BLACK = (0,0,0); GREEN = (52,235,143)
DIM = (800,600); WIDTH, HEIGHT = DIM; origin = (WIDTH/2,HEIGHT/2)

# Initialise world
pygame.init()
screen = pygame.display.set_mode(DIM)
pygame.display.set_caption("Refraction Demonstration")
## Some variables need to exit before the game loop starts
run = True
mousePos = (0,0)
alphaI = 0
alphaR = 0
alpha2 = 0

# Game objects:
## Boxes
footerRect = pygame.Rect(0,HEIGHT-50,WIDTH,50)
boundBox = pygame.Rect(630,25,250,85)
## Text boxes
anglesText = []
for i in range(3):
    anglesText.append(TextBox(screen,635,(i+1)*27,200,25,fontSize=10,borderThickness=1))
    anglesText[i].disable()
titleN1 = TextBox(screen,20,20,65,27,fontSize=14,borderThickness=1); titleN1.disable()
titleN2 = TextBox(screen,420,20,65,27,fontSize=14,borderThickness=1); titleN2.disable()
labelN1 = TextBox(screen,20,HEIGHT-35,25,25,fontSize=10,borderThickness=1); labelN1.disable()
labelN2 = TextBox(screen,210,HEIGHT-35,25,25,fontSize=10,borderThickness=1); labelN2.disable()
outputN1 = TextBox(screen,170,HEIGHT-35,25,25,fontSize=10,borderThickness=1); outputN1.disable()
outputN2 = TextBox(screen,355,HEIGHT-35,25,25,fontSize=10,borderThickness=1); outputN2.disable()
## Sliders
sliderN1 = Slider(screen,55,HEIGHT-30,100,10,min=1,max=3,step=0.01)
sliderN2 = Slider(screen,245,HEIGHT-30,100,10,min=1,max=3,step=0.01)
# Boundary
boundStart = (WIDTH/2,0); boundEnd = (WIDTH/2,HEIGHT)

while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
        elif event.type == pygame.MOUSEMOTION:
            mousePos = pygame.mouse.get_pos()
    
    screen.fill(WHITE)
    # Text Boxes
    n1 = sliderN1.getValue()
    n2 = sliderN2.getValue()
    titleN1.setText("N1 Region")
    titleN2.setText("N2 Region")
    labelN1.setText("N1")
    labelN2.setText("N2")
    outputN1.setText("%.2f" %n1)
    outputN2.setText("%.2f" %n2)

    pygame.draw.line(screen,BLACK,boundStart,boundEnd)
    rayStart = mousePos; rayEnd = origin
    ray = unitVec(rayStart,rayEnd)
    if mousePos[0] < origin[0] and mousePos[1] > origin[1]:
        axis = unitVec(boundStart,boundEnd, state="boundary")
        alphaI, alphaR, alpha2, alphaT= opticCalc(n1,n2,ray,axis)
        pygame.draw.line(screen,RED,rayStart,rayEnd)
        drawVec(origin,alphaR,RED,screen)
        drawVec(origin,alpha2,RED,screen)
        for i in range(3):
            if i == 0:
                anglesText[i].setText("Incident angle: %d" %-radToDeg(alphaI))
            elif i == 1:
                if alpha2==None:
                    anglesText[i].setText("Refracted angle: N/A")
                else:
                    anglesText[i].setText("Refracted angle: %d" %-radToDeg(alpha2))
            elif i == 2:
                anglesText[i].setText("Reflected angle: %d" %-(180-radToDeg(alphaR)))
        #drawVec(origin,alphaI,RED,screen)
    elif mousePos[0] > origin[0] and mousePos[1] > origin[1]:
        quadrant = 2
        axis = unitVec(boundStart,boundEnd, state="boundary")
        alphaI ,alphaR, alpha2= opticCalc(n1,n2,ray,axis,quadrant=2)
        pygame.draw.line(screen,RED,rayStart,rayEnd)
        drawVec(origin,alphaR,RED,screen)
        drawVec(origin,alpha2,RED,screen)
        drawVec(origin,alphaI,RED,screen)
        for i in range(3):
            if i == 0:
                anglesText[i].setText("Incident angle: %d" %-radToDeg(alphaI))
            elif i == 1:
                if alpha2==None:
                    anglesText[i].setText("Refracted angle: N/A")
                else:
                    anglesText[i].setText("Refracted angle: %d" %(radToDeg(alpha2)-180))
            elif i == 2:
                anglesText[i].setText("Reflected angle: %d" %radToDeg(alphaR))

    pygame.draw.rect(screen,GREEN,boundBox)
    pygame.draw.rect(screen,GREEN,footerRect)
    pygame_widgets.update(events)
    pygame.display.update()
