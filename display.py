import pygame, math
from pygame.locals import *
     
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
degrees = 0
FPS = 30
  
def move_surface(screen1, surface, center=(0, 0)):
    '''Move surface to be centered at center(x, y)'''
    bounds = surface.get_rect(center = center)
    screen1.blit(surface, bounds)
  
def rotate_surface(screen1, surface, degrees, origin=(0, 0), offset=0):
    '''Rotate surface about an origin.
    surface - The thing to rotate
    degrees - How much to rotate surface in degrees
    origin - Center of rotation
    offset - Distance from center of rotation to center of surface
    '''
    x, y = origin  # Where are we rotating around
  
    # Calculate center of rotated surface
    if offset != 0:
        radians = degrees * math.pi / 180  # Need angle in radians for sin() and cos()
        x += int(offset * math.cos(radians))
        y -= int(offset * math.sin(radians))   # This was +=
  
    # Rotate the surface
    if degrees != 0:
        surface = pygame.transform.rotate(surface, degrees)  # Pygame uses degrees
  
    move_surface(screen1, surface, (x, y))

def init():

    pygame.init()
    screen1 = pygame.display.set_mode((600, 600))
    screen1.fill(BLUE)
    pygame.display.set_caption('Machine drawing')
    pygame.draw.circle(screen1, BLACK, (200, 150), 4)
    pygame.draw.line(screen1, BLACK, (200, 150), (200, 0))
    pygame.draw.line(screen1, BLACK, (200, 150), (350, 150))

    return screen1

def add_element(element, final_position, rotation_angle, color):

    surface1 = pygame.Surface([element.length, element.height])
    surface1.set_colorkey(BLACK)
    surface1.fill(color)
    rotate_surface(surface1, rotation_angle, (200, 150), 50)
 


def run():
    fpsClock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break
        # for ele in elements:
        #     surface.blit(ele, )
            
        pygame.display.flip()
        fpsClock.tick(FPS)
        # degrees += 1
      
    pygame.quit()