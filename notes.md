# Importing the library
import pygame
 
# Initializing Pygame
pygame.init()
 
# Initializing surface
surface = pygame.display.set_mode((400,300))
 
# Initializing Color
color = (255,0,0)
 
# Drawing Rectangle
pygame.draw.rect(surface, color, pygame.Rect(30, 30, 60, 60))
pygame.display.flip()

clock = pygame.time.Clock()

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
    # surface.fill((30, 30, 30))
    pygame.display.update()
    clock.tick(60)
