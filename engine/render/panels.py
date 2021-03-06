from __future__ import division

import math

import pygame
from pygame.locals import *

from engine.libs import actor_lib

# Used to define a section of the screen used for build options
# unit commands, resources etc etc
class Panel (object):
    always_redraw = False
    accepts_keydown = False
    
    def __init__(self, engine):
        super(Panel, self).__init__()
        
        self.engine = engine
        
        # When set to true the menu will scroll with the screen
        # much like an actor will
        self.scrolls = False
        
        self.visible = True
        
        # Used for caching images as panels don't change that often
        self.changed = False
        self.always_changed = False
        self._image = None
        
        self.position = pygame.Rect(0,0,0,0)
    
    def contains(self, point):
        if self.position.left <= point[0] <= self.position.right:
            if self.position.top <= point[1] <= self.position.bottom:
                return True
    
    def image(self):
        # Try to use the cached version
        if self._image != None and not self.changed and not self.always_redraw and not self.always_changed:
            return self._image, self.position
        
        # Draw the iamge
        self.draw()
        
        return self._image, self.position
    
    def draw(self):
        raise Exception("{0}.draw() is not implemented".format(self.__class__))
    
    def handle_mousedrag(self, event):
        pass
    
    def handle_mouseup(self, event, drag=False):
        raise Exception("{0}.handle_mouseup() is not implemented".format(self.__class__))

    def handle_doubleclick(self, first_click, second_click):
        return self.handle_mouseup(second_click)

# Used to draw a grid of information much like the build
# menus from TA or C&C
class TabularMenu (Panel):
    accepts_keyup = True
    
    def __init__(self, engine, screen, size, grid_size, position):
        super(TabularMenu, self).__init__(engine)
        
        self.screen     = screen
        self.size       = size
        self.grid_size  = grid_size
        
        self.position.topleft = position
        self.key_map = {}
        
        self._build_list = None
        
        """
        Buttons is a list of tuples: (image_name, callback, args)
        """
        self.buttons = []
    
    def draw(self):
        self._image = pygame.Surface(self.size)
        self._image.fill((100, 100, 100), pygame.Rect(0, 0, self.size[0], self.size[1]))
        
        font = pygame.font.SysFont(None, 30)
        col_count = math.floor(self.size[0]/self.grid_size[0])
        
        col, row = 0, 0
        for actor_name, image_name, queue_length in self.buttons:
            img = self.engine.images[image_name]
            
            self._image.blit(img.get(), pygame.Rect(
                col * self.grid_size[0], row * self.grid_size[1],
                self.grid_size[0], self.grid_size[1],
            ))
            
            # Print the queue size if needed
            if queue_length > 0:
                textobj = font.render(str(queue_length), 1, (0,0,0))
                textrect = textobj.get_rect()
                textrect.topleft = col * self.grid_size[0] + 5, row * self.grid_size[1] + 3
                self._image.blit(textobj, textrect)
            
            col += 1
            if col >= col_count:
                col = 0
                row += 1
        
        self.position.size = self.size
        self.changed = False
    
    def update_queue_sizes(self, button=None):
        if type(button) in (tuple, list):
            raise Exception("No handler to reference a specific button")
        
        elif button != None:
            raise Exception("No handler to reference a specific actor item")
        
        build_queues = {}
        for a in self.screen.selected_actors:
            for b in a.build_queue:
                if b not in build_queues:
                    build_queues[b] = 0
                
                build_queues[b] += 1
        
        for i in range(len(self.buttons)):
            if self.buttons[i][0] in build_queues:
                self.buttons[i][2] = build_queues[self.buttons[i][0]]
        
        self.changed = True
    
    def build_from_actor_list(self):
        """
        Takes a build dict and a list of actors, it then populates itself based
        on what can be built.
        """
        buttons = []
        
        # First build a list of all the flags
        flags = []
        
        # Build a list of all the things currently in the build queues
        build_queues = {}
        for a in self.screen.selected_actors:
            if a.team != self.screen.player_team: continue
            
            flags.extend(a.flags)
            
            for b in a.build_queue:
                if b not in build_queues:
                    build_queues[b] = 0
                
                build_queues[b] += 1
        
        flags = set(flags)
        
        # Now get a list of what can be built
        for f in flags:
            if f in self.screen.build_lists:
                for a in self.screen.build_lists[f]:
                    if a in self.screen.actor_types:
                        img_name = self.screen.actor_types[a]['menu_image']
                    else:
                        print(a, list(self.screen.actor_types.keys()))
                        raise Exception("No handler for %s" % a)
                    
                    buttons.append([a, img_name, build_queues.get(a, 0)])
        
        self.buttons = buttons
        self.changed = True
    
    def handle_keyup(self, event):
        print(event)
    
    def handle_mouseup(self, event, drag=False):
        # It's simply a timing error
        if self.screen.selected_actors == []:
            return
        
        relative_pos = (event.pos[0] - self.position.left, event.pos[1] - self.position.top)
        
        col = math.floor(relative_pos[0]/self.grid_size[0])
        row = math.floor(relative_pos[1]/self.grid_size[1])
        col_count = int(math.floor(self.size[0]/self.grid_size[0]))
        
        index = int((col_count * row) + col)
        
        # No button there? Ignore the click but they clicked the menu
        # so we don't want to pass this back to the screen
        if index >= len(self.buttons):
            return True
        
        # Get the information for the button
        item_name, item_image, queue_length = self.buttons[index]
        
        # What are we looking at?
        if item_name in self.screen.actor_types:
            actor_type = self.screen.actor_types[item_name]
            
            if "placement_image" in actor_type:
                # It has a placement image, it's placed by the player
                self.screen.place_actor_mode(item_name)
                
            else:
                # No placement image, the actor is added to the build queue
                # and placed later
                # TODO: Make this game-specific rule go in a game-specific file
                # When starting Downstream this errored
                choice = (None, 999999)
                for a in self.screen.selected_actors:
                    if actor_lib.can_build(self.screen.actor_types[a.actor_type], actor_type, self.screen.build_lists):
                        if len(a.build_queue) < choice[1]:
                            choice = (a, len(a.build_queue))
                
                if choice[0] != None:
                    choice[0].build_queue.append(item_name)
                    self.update_queue_sizes()
                else:
                    raise Exception("""Cannot build that unit using current selection:
item_name = %s
Selection: %s""" % (item_name, [a.actor_type for a in self.screen.selected_actors]))
                
                    
        else:
            raise Exception("Not found in actor types")
        
        return True
    

# Used to draw the map
class MiniMap (Panel):
    always_redraw = True
    
    def __init__(self, engine, size, position, map_size):
        super(MiniMap, self).__init__(engine)
        
        self.size       = size
        self.map_size   = map_size
        
        self.position.topleft = position
        self.team_colours = {}
    
    def draw(self):
        self._image = pygame.Surface(self.size)
        self._image.fill((100, 255, 100), pygame.Rect(0, 0, self.size[0], self.size[1]))
        
        xratio = self.map_size[0] / self.size[0]
        yratio = self.map_size[1] / self.size[1]
        
        for a in self.engine.current_screen.actors:
            x,y = a.pos[0] / xratio, a.pos[1] / yratio
            xsize, ysize = a.size[0] / xratio, a.size[1] / yratio
            
            self._image.fill(self.team_colours[a.team], pygame.Rect(x, y, xsize, ysize))
        
        # Draw view screen rect on map, take into account that panels
        # take up some viewable space and draw the white "screen rect"
        # appropriately
        draw_area = self.engine.current_screen.draw_area
        real_width = draw_area[2] - draw_area[0]
        real_height = draw_area[3] - draw_area[1]
        
        # For some reason these overriden values work better, not sure why yet
        real_width = self.engine.window_width - 150
        real_height = self.engine.window_height
        
        r = pygame.Rect(0,0, real_width / xratio, real_height / yratio)
        
        r.left = - self.engine.current_screen.scroll_x / xratio
        r.top = - self.engine.current_screen.scroll_y / yratio
        
        pygame.draw.rect(self._image, (255, 255, 255), r, 1)
        
        self.position.size = self.size
    
    def handle_mouseup(self, event, drag=False):
        if drag:
            if not self.engine.current_screen.mouseup_callback:
                if event.button != 3:
                    return None
        
        # Get the local X and Y
        x, y = event.pos
        x -= self.position[0]
        y -= self.position[1]
        
        draw_area = self.engine.current_screen.draw_area
        
        # Ratios to work out where we are
        xratio = self.map_size[0] / self.size[0]
        yratio = self.map_size[1] / self.size[1]
        
        map_x = x * xratio + draw_area[0]
        map_y = y * yratio + draw_area[1]
        
        if hasattr(event, "button") and event.button == 3:
            return pygame.event.Event(6, button=3, pos=(map_x, map_y))
        
        # If we've left it in callback mode then we need to return
        # the "true" coordinates
        elif self.engine.current_screen.mouseup_callback:
            return pygame.event.Event(6, button=event.button, pos=(map_x, map_y))
        
        self.engine.current_screen.scroll_to_coords(map_x, map_y)
    
    def handle_mousedrag(self, event):
        self.handle_mouseup(event)

# Used to display text upon a blank background
class InfoBox (Panel):
    def __init__(self, engine, size, position, fill_colour = (0, 0, 0), text_colour = (255, 255, 255)):
        super(InfoBox, self).__init__(engine)
        
        self.size               = size
        self.position.topleft   = position
        self.fill_colour        = fill_colour
        self.text_colour        = text_colour
        
        self.texts = []
    
    def add_text(self, obj, attribute, key=None, position=(0,0), colour=None, prefix="", suffix="", typecast="int"):
        if colour == None: colour = self.text_colour
        
        self.texts.append({
            "obj":          obj,
            "attribute":    attribute,
            "key":          key,
            "position":     position,
            "colour":       colour,
            "prefix":       prefix,
            "suffix":       suffix,
            "typecast":     typecast,
        })  
        
    
    def draw(self):
        self._image = pygame.Surface(self.size)
        self._image.fill(self.fill_colour, pygame.Rect(0, 0, self.size[0], self.size[1]))
        
        font = pygame.font.SysFont("Helvetica", 16)
        
        for t in self.texts:
            if t['key'] == None:
                v = getattr(t['obj'], t['attribute'])
            else:
                v = getattr(t['obj'], t['attribute'])[t['key']]
            
            if t['typecast'] == "int":
                v = int(v)
            else:
                raise Exception("No handler for typecast type of '%s'" % t['typecast'])
            
            text = "%s%s%s" % (t['prefix'], v, t['suffix'])
            textobj = font.render(text, 1, t['colour'])
            textrect = textobj.get_rect()
            textrect.topleft = t['position']
            
            self._image.blit(textobj, textrect)
        
        self.position.size = self.size
        
    def draw_text(self, text, surface, x, y, colour=(0,0,0), font_name="Helvetica", font_size=20):
        font = pygame.font.SysFont(font_name, font_size)
        
        textobj = font.render(text, 1, colour)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    
    # Not expected to respond to mouse events
    def handle_mouseup(self, event, drag=False):
        pass

