import sys
import time
import math

import pygame
from pygame.locals import *

class Game_error(Exception):
    """Errors related to the game in general"""
    pass

class Illegal_move(Game_error):
    """Errors from illegal moves"""
    pass

class Game_rule_error(Game_error):
    """Errors that arise from rule issues"""
    pass

class EngineV3 (object):
    fps = 30
    window_width = 0
    window_height = 0
    
    def __init__(self):
        super(EngineV3, self).__init__()
        
        self.screens = {}
        self.current_screen = None
        self.images = {}
    
    def quit(self, event=None):
        pygame.quit()
        sys.exit()
    
    def startup(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
    
    def set_screen(self, s, *args, **kwargs):
        # s can be a screen instance or the name of a screen in self.screens
        if s in self.screens:
            s = self.screens[s]
        elif type(s) == str:
            raise KeyError("Screen '%s' not found in screen dictionary" % s)
        
        # Is it an instance or a class? If the latter we make a new instance of it
        # if "__call__" in dir(s):
        if type(s) == type:
            try:
                s = s(self, *args, **kwargs)
            except Exception as e:
                print("Args: %s" % str(args))
                print("Kwargs: %s" % str(kwargs))
                raise
        
        s.engine = self
        s.display = self.display
        
        pygame.display.set_caption(s.name)
        self.current_screen = s
        self.current_screen.activate()
        self.current_screen.update_window()
    
    # Contains main execution loop
    def start(self):
        self.startup()
        
        while True:
            for event in pygame.event.get():
                if event.type == ACTIVEEVENT:       self.current_screen._handle_active(event)
                if event.type == KEYDOWN:           self.current_screen._handle_keydown(event)
                if event.type == KEYUP:             self.current_screen._handle_keyup(event)
                if event.type == MOUSEBUTTONUP:     self.current_screen._handle_mouseup(event)
                if event.type == MOUSEBUTTONDOWN:   self.current_screen._handle_mousedown(event)
                if event.type == MOUSEMOTION:       self.current_screen._handle_mousemotion(event)
                if event.type == QUIT:              self.current_screen.quit(event)
            
            # Check to see if a key has been held down
            self.current_screen._handle_keyhold()
            
            self.current_screen.update()
            self.current_screen.redraw()
            
            if not self.current_screen.self_regulate:
                self.clock.tick(self.fps)
        
        self.quit()

class Animation (object):
    """An object that takes a picture and cuts it up into separate frames
    so that we can animate certain objects"""
    
    def __init__(self, filepath, columns=1, rows=1, animation_rate = 0.5):
        super(Animation, self).__init__()
        
        if columns < 1:
            raise Exception("Cannot have fewer than 1 column in an animation")
        
        if rows < 1:
            raise Exception("Cannot have fewer than 1 row in an animation")
        
        self.images = []
        self.animation_rate = animation_rate
        
        img = pygame.image.load(filepath)
        r = img.get_rect()
        
        tile_width = r.width / columns
        tile_height = r.height / rows
        
        for x in range(columns):
            for y in range(rows):
                tile = pygame.Surface((tile_width, tile_height), SRCALPHA)
                tile.blit(img, (0,0), (x * tile_width, y * tile_height, tile_width, tile_height))
                
                self.images.append(tile)
        
        self.rect = pygame.Rect((0,0, tile_width, tile_height))
    
    def get_rect(self):
        return self.rect
    
    def get(self, img_number=0):
        img_number = int(math.floor(self.animation_rate * img_number))
        
        # Too high a number? Loop around
        if img_number >= len(self.images):
            img_number = img_number % len(self.images)
        
        return self.images[img_number]
    
    def __getitem__(self, key):
        return get(self, key)



