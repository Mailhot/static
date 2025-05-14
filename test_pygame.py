import pygame, math
from pygame.locals import *
     
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
degrees = 0
FPS = 30
  
def move_surface(surface, center=(0, 0)):
    '''Move surface to be centered at center(x, y)'''
    bounds = surface.get_rect(center = center)
    DISPLAYSURF.blit(surface, bounds)
  
def rotate_surface(surface, degrees, origin=(0, 0), offset=0):
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
  
    move_surface(surface, (x, y))
  
pygame.init()
DISPLAYSURF = pygame.display.set_mode((600, 600))
DISPLAYSURF.fill(BLUE)

pygame.display.set_caption('Sailing!')
fpsClock = pygame.time.Clock()
Sail = pygame.Surface([100,10])
Sail.set_colorkey(BLACK)
Sail.fill(WHITE)
rotate_surface(Sail, 30, (200, 150), 50)

pygame.draw.circle(DISPLAYSURF, BLACK, (200, 150), 4)
pygame.draw.line(DISPLAYSURF, BLACK, (200, 150), (200, 0))
pygame.draw.line(DISPLAYSURF, BLACK, (200, 150), (350, 150))


running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            break
       
    
    pygame.display.flip()
    fpsClock.tick(FPS)
    degrees += 1
  
pygame.quit()