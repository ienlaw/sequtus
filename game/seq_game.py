import sys
import pygame

from engine.render import core
from engine.libs import sim_lib
from engine.utilities import game_data_editor
from game_screens import main_menu, game_setup, battle

class Sequtus (core.EngineV3):
    name = "Sequtus"
    
    fps = 30
    
    window_width = 1000
    window_height = 1000
    
    def __init__(self):
        super(Sequtus, self).__init__()
        
        fp = sys.path[0] + "/"
        
        self.images = {
            "battlefield":              core.Animation(fp + 'media/battlefield.png'),
            
            # RED
            "red_worker":               core.Animation(fp + "media/red_worker.png"),
            "red_worker_menu":          core.Animation(fp + 'media/red_worker_menu.png'),
            
            "red_tank_body":            core.Animation(fp + "media/red_tank_body.png"),
            "red_tank_turret":          core.Animation(fp + 'media/red_tank_turret.png'),
            "red_tank_menu":            core.Animation(fp + 'media/red_tank_menu.png'),
            
            "red_adv_worker":           core.Animation(fp + "media/red_adv_worker.png"),
            "red_adv_worker_menu":      core.Animation(fp + 'media/red_adv_worker_menu.png'),
            
            "red_heavy_tank_body":      core.Animation(fp + "media/red_heavy_tank_body.png"),
            "red_heavy_tank_turret":    core.Animation(fp + 'media/red_heavy_tank_turret.png'),
            "red_heavy_tank_menu":      core.Animation(fp + 'media/red_heavy_tank_menu.png'),
            
            "red_juggernaut_body":      core.Animation(fp + "media/red_juggernaut_body.png"),
            "red_juggernaut_turret":    core.Animation(fp + 'media/red_juggernaut_turret.png'),
            "red_juggernaut_menu":      core.Animation(fp + 'media/red_juggernaut_menu.png'),
            
            "red_factory":              core.Animation(fp + "media/red_factory.png"),
            "red_factory_placement":    core.Animation(fp + "media/red_factory_placement.png"),
            "red_factory_menu":         core.Animation(fp + 'media/red_factory_menu.png'),
            
            "red_mine":                 core.Animation(fp + "media/red_mine.png"),
            "red_mine_placement":       core.Animation(fp + "media/red_mine_placement.png"),
            "red_mine_menu":            core.Animation(fp + 'media/red_mine_menu.png'),
            
            "red_adv_factory":          core.Animation(fp + "media/red_adv_factory.png"),
            "red_adv_factory_placement":core.Animation(fp + "media/red_adv_factory_placement.png"),
            "red_adv_factory_menu":     core.Animation(fp + 'media/red_adv_factory_menu.png'),
            
            "red_turret":               core.Animation(fp + "media/red_turret.png"),
            "red_turret_placement":     core.Animation(fp + "media/red_turret_placement.png"),
            "red_turret_menu":          core.Animation(fp + 'media/red_turret_menu.png'),
            
            "red_adv_turret":           core.Animation(fp + "media/red_adv_turret.png"),
            "red_adv_turret_placement": core.Animation(fp + "media/red_adv_turret_placement.png"),
            "red_adv_turret_menu":      core.Animation(fp + 'media/red_adv_turret_menu.png'),
            
            # BLU
            "blu_worker":               core.Animation(fp + "media/blu_worker.png"),
            "blu_worker_menu":          core.Animation(fp + 'media/blu_worker_menu.png'),
            
            "blu_tank_body":            core.Animation(fp + "media/blu_tank_body.png"),
            "blu_tank_turret":          core.Animation(fp + 'media/blu_tank_turret.png'),
            "blu_tank_menu":            core.Animation(fp + 'media/blu_tank_menu.png'),
            
            "blu_adv_worker":           core.Animation(fp + "media/blu_adv_worker.png"),
            "blu_adv_worker_menu":      core.Animation(fp + 'media/blu_adv_worker_menu.png'),
            
            "blu_heavy_tank_body":      core.Animation(fp + "media/blu_heavy_tank_body.png"),
            "blu_heavy_tank_turret":    core.Animation(fp + 'media/blu_heavy_tank_turret.png'),
            "blu_heavy_tank_menu":      core.Animation(fp + 'media/blu_heavy_tank_menu.png'),
            
            "blu_artillery":            core.Animation(fp + "media/blu_artillery.png"),
            "blu_artillery_menu":       core.Animation(fp + 'media/blu_artillery_menu.png'),
            
            "blu_factory":              core.Animation(fp + "media/blu_factory.png"),
            "blu_factory_placement":    core.Animation(fp + 'media/blu_factory_placement.png'),
            "blu_factory_menu":         core.Animation(fp + 'media/blu_factory_menu.png'),
            
            "blu_mine":                 core.Animation(fp + "media/blu_mine.png"),
            "blu_mine_placement":       core.Animation(fp + "media/blu_mine_placement.png"),
            "blu_mine_menu":            core.Animation(fp + 'media/blu_mine_menu.png'),
            
            "blu_adv_factory":          core.Animation(fp + "media/blu_adv_factory.png"),
            "blu_adv_factory_placement":core.Animation(fp + 'media/blu_adv_factory_placement.png'),
            "blu_adv_factory_menu":     core.Animation(fp + 'media/blu_adv_factory_menu.png'),
            
            "blu_turret":               core.Animation(fp + "media/blu_turret.png"),
            "blu_turret_placement":     core.Animation(fp + "media/blu_turret_placement.png"),
            "blu_turret_menu":          core.Animation(fp + 'media/blu_turret_menu.png'),
            
            "blu_adv_turret":           core.Animation(fp + "media/blu_adv_turret.png"),
            "blu_adv_turret_placement": core.Animation(fp + "media/blu_adv_turret_placement.png"),
            "blu_adv_turret_menu":      core.Animation(fp + 'media/blu_adv_turret_menu.png'),
            
            # Bullets
            "9px_bullet":               core.Animation(fp + 'media/9px_bullet.png'),
            "11px_bullet":              core.Animation(fp + 'media/11px_bullet.png'),
            "15px_bullet":              core.Animation(fp + 'media/15px_bullet.png'),
        }
    
    def startup(self):
        super(Sequtus, self).startup()
        
        self.screens['Main menu'] = main_menu.MainMenu(self)
        self.screens['Game setup'] = game_setup.build(self)
        self.screens['Battle screen'] = battle.Battle
        
        self.screens['Game data editor'] = game_data_editor.GameDataEditor(self)
        # self.screens['Map editor'] = game_setup.build(self)
        
        self.set_screen('Main menu')
        self.new_game()
    
    def new_game(self, file_path=""):
        self.set_screen('Battle screen')
        
        self.current_screen.name = "Sequtus"
        self.current_screen.background_image = self.images['battlefield'].get().copy()
        self.current_screen.player_team = 1
        
        # self.current_screen.load_all("data/config.json", "data/game_data.json", "data/dummy.json")
        self.current_screen.load_all("data/config.json", "data/game_data.json", "data/scenario_1.json")
        
        # Wrap it in a try block so that the screen can quit it's AI processes
        try:
            pass
            
            # self.current_screen.select_actor(self.current_screen.actors[1])
            
            # self.current_screen.actors[0].build_queue = ['Red tank']
            
            self.current_screen.scroll_to_coords(2000, 2000)
            
            # S key to issue stop command
            # e = pygame.event.Event(3, scancode=2, key=100, mod=0)
            # self.current_screen.handle_keyup(e)
            
            # Fake mouseclick
            # ev = pygame.event.Event(3, button=1, pos=(960, 960))# Corner of view
            # ev = pygame.event.Event(3, button=1, pos=(74, 88))# Corner of map view
            # ev = pygame.event.Event(3, button=1, pos=(96, 96))# Corner of map view
            # ev = pygame.event.Event(3, button=1, pos=(1, 1))
            
            # self.current_screen.place_actor_mode("Red factory")
            # self.current_screen.handle_mouseup(ev)
            
            # self.current_screen.add_order(self.current_screen.actors[0], "aid", target=self.current_screen.actors[2])
            
        except Exception:
            self.current_screen.quit()
            raise
        
        sim_lib.set_speed(self.current_screen, 42)
