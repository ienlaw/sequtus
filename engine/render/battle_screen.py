"""
BattleScreen is a screen with added functionality for handling things such as
scrolling all of it's information comes from the sim that it connects to
none of the game logic is implemented in the battle_screen at all.

The screen is also used to read in commands such as mouse-clicks.
BattleScreen itself is subclassed by BattleSim so as to keep the logic
code separate from the display/interface code.
"""

import multiprocessing
import time

import pygame
from pygame.locals import *

import screen

UP_ARROW = 273
DOWN_ARROW = 274
RIGHT_ARROW = 275
LEFT_ARROW = 276

NUM0 = 48
NUM1 = 49
NUM2 = 50
NUM3 = 51
NUM4 = 52
NUM5 = 53
NUM6 = 54
NUM7 = 55
NUM8 = 56
NUM9 = 57

NUMBERS = range(NUM0, NUM9+1)

class BattleScreen (screen.Screen):
    self_regulate = True
    
    def __init__(self, engine):
        super(BattleScreen, self).__init__((engine.window_width, engine.window_height))
        
        self.background_image = pygame.Surface((1,1))
        self.background = pygame.Surface((1,1))
        self.have_scrolled = False
        
        self.scroll_speed = 15
        
        self.scroll_up_key = UP_ARROW
        self.scroll_down_key = DOWN_ARROW
        self.scroll_right_key = RIGHT_ARROW
        self.scroll_left_key = LEFT_ARROW
        
        self.allow_mouse_scroll = False
        
        # Defines how far we can scroll in any direction
        self.scroll_boundaries = (-100, -100, 0, 0)
        
        # Ctrl + N to assign, N to select
        self.control_groups = {}
        for i in NUMBERS:
            self.control_groups[i] = []
        
        self.scroll_boundary = 100
        
        self.selected_actors = []
        self.drag_rect = None
        
        self._next_redraw = time.time()
        self._redraw_delay = 0
        self.set_fps(30)
        
    def set_fps(self, fps):
        self._redraw_delay = 1/fps
    
    def redraw(self):
        if time.time() < self._next_redraw:
            return
        
        """Overrides the basic redraw as it's intended to be used with more animation"""
        # Draw background taking into account scroll
        surf = self.engine.display
        surf.blit(self.background_image, pygame.Rect(
            self.scroll_x, self.scroll_y,
            self.engine.window_width, self.engine.window_height)
        )
        
        # Menus
        
        # Actors
        for a in self.actors:
            # Only draw actors within the screen
            if a.rect.left > -a.rect.width and a.rect.right < self.engine.window_width + a.rect.width:
                if a.rect.top > -a.rect.height and a.rect.bottom < self.engine.window_height + a.rect.height:
                    surf.blit(self.engine.images[a.image], a.rect)
            
            if a.selected:
                pygame.draw.rect(surf, (255, 255, 255), a.selection_rect(), 1)
                surf.blit(*a.health_bar())
        
        # Dragrect
        if self.drag_rect != None:
            # draw.rect uses a origin and size arguments, not topleft and bottomright
            line_rect = (
                self.drag_rect[0] + self.scroll_x,
                self.drag_rect[1] + self.scroll_y,
                self.drag_rect[2] - self.drag_rect[0],
                self.drag_rect[3] - self.drag_rect[1],
            )
            
            pygame.draw.rect(surf, (255, 255, 255), line_rect, 1)
        
        pygame.display.flip()
        self._next_redraw = time.time() + self._redraw_delay
    
    def handle_keydown(self, event):
        # 'KMOD_ALT', 'KMOD_CAPS', 'KMOD_CTRL', 'KMOD_LALT', 'KMOD_LCTRL', 'KMOD_LMETA', 'KMOD_LSHIFT', 'KMOD_META', 'KMOD_MODE', 'KMOD_NONE', 'KMOD_NUM', 'KMOD_RALT', 'KMOD_RCTRL', 'KMOD_RMETA', 'KMOD_RSHIFT', 'KMOD_SHIFT'
        mods = pygame.key.get_mods()
        
        # Number key? Select or assign a control group
        if event.key in NUMBERS:
            if KMOD_CTRL & mods:
                self.assign_control_group(event.key)
            else:
                self.select_control_group(event.key)
        
    
    def handle_keyhold(self):
        # Up/Down
        if self.scroll_up_key in self.keys_down:
            self.scroll_up()
        elif self.scroll_down_key in self.keys_down:
            self.scroll_down()
        
        # Right/Left
        if self.scroll_right_key in self.keys_down:
            self.scroll_right()
        elif self.scroll_left_key in self.keys_down:
            self.scroll_left()
        
        super(BattleScreen, self).handle_keyhold()
    
    def handle_mouseup(self, event, drag=False):
        mods = pygame.key.get_mods()
        real_mouse_pos = (event.pos[0] - self.scroll_x, event.pos[1] - self.scroll_y)
        
        if event.button == 1:# Left click
            if not drag:
                if KMOD_SHIFT ^ mods:
                    self.unselect_all_actors()
                
                for a in self.actors:
                    if a.contains_point(real_mouse_pos):
                        self.left_click_actor(a)
                        break
        
        elif event.button == 3:# Right click
            actor_target = None
            for a in self.actors:
                if a.contains_point(real_mouse_pos):
                    actor_target = a
                    break
            
            # Now issue the command
            if not actor_target:
                for a in self.selected_actors:
                    if KMOD_SHIFT ^ mods:
                        a.issue_command("move", real_mouse_pos)
                    else:
                        a.append_command("move", real_mouse_pos)
            else:
                if actor_target.team != self.player_team:
                    for a in self.selected_actors:
                        if KMOD_SHIFT ^ mods:
                            a.issue_command("attack", actor_target)
                        else:
                            a.append_command("attack", actor_target)
                else:
                    for a in self.selected_actors:
                        if KMOD_SHIFT ^ mods:
                            a.issue_command("defend", actor_target)
                        else:
                            a.append_command("defend", actor_target)
            
        else:
            print("battle_screen.handle_mouseup: event.button = %s" % event.button)
    
    def left_click_actor(self, a):
        if a.selected:
            self.unselect_actor(a)
        else:
            self.select_actor(a)
    
    def handle_mousedrag(self, event, drag_rect):
        if event.buttons[0] == 1:
            self.drag_rect = drag_rect
    
    def handle_mousedragup(self, event, drag_rect):
        mods = pygame.key.get_mods()
        self.drag_rect = None
        
        if event.button == 1:
            if KMOD_SHIFT ^ mods:
                self.unselect_all_actors()
            
            for a in self.actors:
                if a.inside(drag_rect):
                    self.select_actor(a)
    
    def unselect_all_actors(self):
        for a in self.selected_actors[:]:
            del(self.selected_actors[self.selected_actors.index(a)])
            a.selected = False
    
    def unselect_actor(self, a):
        del(self.selected_actors[self.selected_actors.index(a)])
        a.selected = False
    
    def select_actor(self, a):
        self.selected_actors.append(a)
        a.selected = True
    
    def update(self):
        # It might be that the mouse is scrolling
        # but we only use this if there are no arrow keys held down
        if self.allow_mouse_scroll:
            if self.scroll_up_key not in self.keys_down:
                if self.scroll_down_key not in self.keys_down:
                    if self.scroll_right_key not in self.keys_down:
                        if self.scroll_left_key not in self.keys_down:
                            # None of our scroll keys are down, we can mouse scroll
                            self.check_mouse_scroll()
    
    def check_mouse_scroll(self):
        left_val = self.scroll_boundary - (self.engine.window_width - self.mouse[0])
        right_val = self.scroll_boundary - self.mouse[0]
        
        up_val = self.scroll_boundary - (self.engine.window_height - self.mouse[1])
        down_val = self.scroll_boundary - self.mouse[1]
        
        # Scroll based on how far it is
        if down_val > 0:
            self.scroll_down(down_val/self.scroll_boundary)
        elif up_val > 0:
            self.scroll_up(up_val/self.scroll_boundary)
        
        if left_val > 0:
            self.scroll_left(left_val/self.scroll_boundary)
        elif right_val > 0:
            self.scroll_right(right_val/self.scroll_boundary)
    
    def assign_control_group(self, key):
        self.control_groups[key] = self.selected_actors[:]
    
    def select_control_group(self, key):
        if len(self.control_groups[key]) > 0:
            self.unselect_all_actors()
            for a in self.control_groups[key][:]:
                self.select_actor(a)
    
    def scroll_right(self, rate = 1):
        last_pos = self.scroll_x
        
        self.scroll_x -= rate * self.scroll_speed
        self.scroll_x = max(self.scroll_boundaries[0], self.scroll_x)                
    
    def scroll_left(self, rate = 1):
        last_pos = self.scroll_x
        
        self.scroll_x += rate * self.scroll_speed
        self.scroll_x = min(self.scroll_boundaries[2], self.scroll_x)
        
    def scroll_down(self, rate = 1):
        last_pos = self.scroll_y
        
        self.scroll_y -= rate * self.scroll_speed
        self.scroll_y = max(self.scroll_boundaries[1], self.scroll_y)
        
    def scroll_up(self, rate = 1):
        last_pos = self.scroll_y
        
        self.scroll_y += rate * self.scroll_speed
        self.scroll_y = min(self.scroll_boundaries[3], self.scroll_y)
    
    def add_actor(self, a):
        a.rect = self.engine.images[a.image].get_rect()
        self.actors.append(a)
