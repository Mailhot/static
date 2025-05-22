import pygame
from pygame.locals import *
from vector import Vector, cross_prod, Element, Load, Machine, Rotation, Gravity

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self.items = []
        self.origin = (320, 200)
        self.colors = {'RED': (255,179,186),
                        'ORANGE': (255,223,186),
                        'YELLOW': (255,255,186),
                        'GREEN': (186,255,201),
                        'BLUE': (186,225,255),
                        'OTHER_BLUE': (31,162,255),
                        'THIRD_BLUE': (39,253,245),
                        'GREEN_AGAIN': (122,255,180),
                        'PALE_PINK': (249,141,201),
                        'DARK_PINK': (247,101,184),
                        'WHITE': (255, 255, 255), # this is the background do not use in copponents color.
                        'BLACK': (0, 0, 0),
                        }
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        pygame.display.set_caption('Machine drawing')
        self.clock = pygame.time.Clock()
        return True

 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self._display_surf.fill((211, 211, 211))
        # pygame.draw.rect(self._display_surf, self.colors['BLACK'], (200, 150, 100, 10))
        # print('items:', self.items)
        for item in self.items:
            # {'length': 30, 'height': 20, 'angle': 90, 'color': 'RED', 'center': (10, 12)}
            # print('item:', item)
            #the rectangle that rotates
            surface1 = pygame.Surface([item['length'], item['height']])
            surface1.set_colorkey(self.colors['BLACK'])
            surface1.fill(self.colors[item['color']])
            surface1 = pygame.transform.rotate(surface1, item['angle'])
            bounds = surface1.get_rect(center = sum_list([item['center'], self.origin]))
            self._display_surf.blit(surface1, bounds)
            # surface1 = pygame.Surface([element.length, element.height])
        pygame.draw.circle(self._display_surf, self.colors['BLACK'], self.origin, 4)
        pygame.draw.line(self._display_surf, self.colors['BLACK'], self.origin, (self.origin[0]+100, self.origin[1]))
        pygame.draw.line(self._display_surf, self.colors['BLACK'], self.origin, (self.origin[0], self.origin[1]-100))

        pygame.display.flip()
        self.clock.tick(10)


    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()

    def add_element(self, element):
        pass

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


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


def sum_list(items):
    # Will provide a per index sum of list items (must be same size)
    combined = zip(*items)
    result = tuple(map(sum, combined))
    # print('combined')
    return result


def test1():


    m0 = 100
    m1 = 150
    m2 = 70
    m3 = 50
    m4 = 30
    rm0 = (-20, -20)
    rm1 = (50, 0)
    r1 = (100, 0)
    rm2 = (60, 0)
    r2 = (120, 0)
    rm3 = (50, 0)
    r3 = (-20, 50)
    rm4 = (-20, -20)
    theta2 = 45
    theta3 = -45
    theta4 = 15 

    machine1 = Machine(gravity=Gravity())

    ele0 = Element(name='Element 0', length=40, width=40, height=40)
    ele0_mass = Load(Vector(*rm0), m0, _type='mass')
    ele0.loads.append(ele0_mass)
    ele0.rotate(Rotation(gamma=0))

    ele1 = Element(name='Element 1', length=100, width=20, height=20)
    ele1_mass = Load(Vector(*rm1), m1, _type='mass')
    ele1.loads.append(ele1_mass)
    ele1.elements.append(ele0)
    ele1.move(Vector(*r1).rotate(Rotation(gamma=-15)))

    ele2 = Element(name='Element 2', length=120, width=20, height=20)
    ele2_mass = Load(Vector(*rm2).rotate(Rotation(gamma=15)), m2, _type='mass')
    ele2.loads.append(ele2_mass)
    ele2.elements.append(ele1)
    # ele2.move(Vector(*r2))

    machine1.elements.append(ele2)
    # machine1.reactions()
    
    items = machine1.draw()
    
    # randomise colors
    color_key = list(App().colors.keys())
    print(items)
    # randomise color for each components.
    for i, item in enumerate(items):
        item['color'] = color_key[i]
    return items




def system1():
    # this is to define a system so it can generate an output that can be ingested into the app.
    # desired output: [{'length': 30, 'height': 20, 'angle': 45, 'color': 'RED', 'center': (10, -12)}]
    mast_slide_position = 0 # [0-40] inch 0 is the mast slide raised up all the way
    feed_position = 80 # range [0-160] inch 0 is at bottom of mast
    mast_angle = 20 # range [95 - 0] degree, 0 degree is laying flat
    # Track cat 308
    track_width = 26.1 # 308
    track_length = 114.3
    track_height = 26.1
    track_ground_length = 89.7
    track_mass = 4415 # [lbs] TODO: check with cat if mass is really for the 2 or per side

    rod_rack_angle = 85 # [between 30 and 85 degree] 90 is vertical

    machine_width = 72 # overall width of the mahine (preliminary guess)

    ## Components
    max100 = Machine(gravity=Gravity()) # Set a machine with default gravity

    mast = Element(name='Mast Group')
    max100.elements.append(mast)

    # 2-1 Head (Sliding table)
    head = Element(name="Head", length=30, width=20, height=16)
    head_mast_pos = Vector(10, 8)
    head_mast = Load(head_mast_pos, 600, _type='mass')
    head.loads.append(head_mast)
    mast.elements.append(head)
    
    # 2-2 Mast 
    mast_mast = Element(name='Mast', length=160, width=16, height=16)
    mast_mast_cg_pos = Vector(80, 8)
    mast_mast_cg = Load(mast_mast_cg_pos, 6000, _type='mass')
    mast_mast.loads.append(mast_mast_cg)
    mast.elements.append(mast_mast.move(Vector(-10-mast_slide_position, 0))) # Move the mast 10 inch from bottom (where the pivot will likely be)

    head.move(Vector(feed_position, 16))

    # 2-3 Mast-Pivot
    mast_pivot = Element(name='Mast Pivot', length=40, width=22, height=16)
    pivot_mast_pos = Vector(16, -10)
    pivot_mast = Load(pivot_mast_pos, 800, _type='mass')
    mast_pivot.loads.append(pivot_mast)
    mast.elements.append(mast_pivot)

    mast.move(Vector(-8, 12)) # Center at pivot point
    
    mast.rotate(Rotation(gamma=mast_angle))


    base = Element(name='Base Group')
    max100.elements.append(base)
    
    # 1-3
    pivot_base = Element(name='Base Pivot', length=36, width=24, height=36)
    pivot_base_cg_pos = Vector(18, 18)
    pivot_base_cg = Load(pivot_base_cg_pos, 2000, _type='mass')
    pivot_base.loads.append(pivot_base_cg)
    base.elements.append(pivot_base)
    # mast.move(Vector(8, 24)) # Move the mast assy to center at the base-pivot point
    base.elements.append(pivot_base.move(Vector(-15.15, -36, 0))) # the mast base is positioned at -3, 15 in the base element
    
    # 1-2
    platform = Element(name='Platform', length=120, width=72, height=6)
    platform_pos = Vector(60, 3)
    platform_cg = Load(platform_pos, 2000, _type='mass')
    platform.loads.append(platform_cg)
    base.elements.append(platform)
    pivot_base.move(Vector(10, 6))
    # mast.offset.move(Vector(0, -6))


    base.elements.append(platform.move(Vector(-5.15, -30, 0))) # move platform in base referential and move it in place.


    # Track 308 (this is for the 2 tracks)
    # 1-1
    track = Element(name='track pair', length=track_ground_length, width=machine_width, height=track_height)
    track_cg = Load(Vector(track_ground_length/2, track_ground_length/2), track_mass, _type='mass')
    track.loads.append(track_cg)
    
    track.move(Vector(8, -88))
    base.elements.append(track)
    

    engine = Element(name='Engine', length=46.3, width=22.2, height=33.7)
    engine_base_pos = Vector(13.4, 16.85, 0)
    engine_base = Load(engine_base_pos, 1226, _type='mass')
    engine.loads.append(engine_base)
    base.elements.append(engine.move(Vector(60, -26, 0)))

    print('reactions:', max100.reactions())

    # randomise colors
    items = max100.draw()
    color_key = list(App().colors.keys())

    # randomise color for each components.
    for i, item in enumerate(items):
        item['color'] = color_key[i]

    return items



if __name__ == "__main__" :
    theApp = App()

    theApp.items = test1()
    theApp.on_execute()