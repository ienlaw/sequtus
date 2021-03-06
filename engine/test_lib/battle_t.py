import unittest
import sim_t
from engine.libs import drawing

class BattleTests (sim_t.SimTester):
    def test_load(self):
        sim = self.new_sim(0)
        sim.run()
        
        # State checks
        self.assertEqual(len(sim.actors), 2, "Sim loaded an incorrect number of actors")
        
        self.assertEqual(sim.actors[0].oid, 0, "Sim does not correctly set the first actor's aid")
        self.assertEqual(sim.actors[1].oid, 1, "Sim does not correctly increment actor aid")
        
        self.assertEqual(sim.actors[0].team, 1, "Sim does not correctly assign a team to actors")
        self.assertEqual(sim.actors[1].team, 2, "Sim does not correctly assign a team to actors")
        
        self.assertEqual(sim.actors[0].hp, 5, "Sim does not correctly assign hp to actors")
        self.assertEqual(sim.actors[1].hp, 10, "Sim does not correctly assign hp to actors")
    
    def test_orders(self):
        sim = self.new_sim(150)
        
        sim.actors[0].issue_command("move", (500, 500))
        sim.actors[0].append_command("stop", -1)
        
        sim.actors[1].issue_command("move", (1000, 1000))
        sim.actors[1].issue_command("stop", -1)
        
        sim.run()
        
        self.assertEqual(sim.actors[0].pos, [500, 500, 0], "Actor does not correctly append orders")
        self.assertEqual(sim.actors[1].pos, [1000, 500, 0], "Actor does not correctly issue orders")
    
    def test_flags(self):
        sim = self.new_sim(1)
        
        sim.actors[0].issue_command("move", (500, 500))
        
        sim.run()
        
        self.assertEqual(sim.actors[0].is_moving(), True, "Moving actor does not register .is_moving flag")
        self.assertEqual(sim.actors[1].is_moving(), False, "Stationary actor does not register .is_moving flag")
    
    def test_collision_resolution(self):
        # Note: This does not correctly test the collision resolution
        # in a perfect way, it simply makes sure that every type of
        # collision happens and that the actors end up in the correct
        # places, this is the best I could do for now.
        sim = self.new_sim(200, game_state="collisions.json")
        
        # a1 gets to the location before a2 and thus is moved out of the way
        sim.actors[0].issue_command("move", (200, 200))
        sim.actors[1].issue_command("move", (200, 200))
        
        sim.actors[2].issue_command("move", [400, 100])
        sim.actors[3].issue_command("move", [400, 100])
        
        sim.actors[4].issue_command("move", [700, 400])
        
        sim.actors[6].issue_command("move", [400, 300])
        sim.actors[7].issue_command("move", [300, 300])
        
        sim.actors[8].issue_command("move", [600, 600])
        sim.actors[9].issue_command("move", [600, 500])
        sim.actors[9].max_velocity = 2
        
        sim.actors[10].issue_command("move", [300, 500])
        sim.actors[11].issue_command("move", [200, 600])
        
        sim.actors[12].issue_command("move", [450, 700])
        sim.actors[13].issue_command("move", [450, 700])
        sim.actors[14].issue_command("move", [450, 700])
        
        sim.run()
        
        # testing what happens when one actor gets there first
        self.assertEqual([int(p) for p in sim.actors[0].pos], [246, 246, 0])
        self.assertEqual([int(p) for p in sim.actors[1].pos], [194, 194, 0])
        
        # one actor is stopped (having just moved) and nudged out the way
        # by another actor
        self.assertEqual([int(p) for p in sim.actors[2].pos], [350, 100, 0])
        self.assertEqual([int(p) for p in sim.actors[3].pos], [408, 100, 0])
        
        # one actor is unable to be moved (building)
        self.assertEqual([int(p) for p in sim.actors[4].pos], [700, 400, 0])
        
        # both actors are moving directly towards each other
        self.assertEqual([int(p) for p in sim.actors[6].pos], [400, 300, 0])
        self.assertEqual([int(p) for p in sim.actors[7].pos], [300, 300, 0])
        
        # One actor trying to overtake the other
        self.assertEqual([int(p) for p in sim.actors[8].pos], [600, 600, 0])
        self.assertEqual([int(p) for p in sim.actors[9].pos], [554, 562, 0])
        
        # One actor trying to overtake the other
        self.assertEqual([int(p) for p in sim.actors[10].pos], [300, 500, 0])
        self.assertEqual([int(p) for p in sim.actors[11].pos], [200, 600, 0])
        
        self.assertEqual([int(p) for p in sim.actors[12].pos], [449, 749, 0])
        self.assertEqual([int(p) for p in sim.actors[13].pos], [450, 691, 0])
        self.assertEqual([int(p) for p in sim.actors[14].pos], [496, 728, 0])
        
    
    # Tests that still need to be written
    def ttest_left_click(self): pass
    def ttest_right_click(self): pass
    def ttest_doubleclick(self): pass
    def ttest_drag_select(self): pass
    def ttest_keyboard_scroll(self): pass
    
    def ttest_group_assignment(self): pass# Ctrl + # to assign, # to select
    
    def ttest_issue_orders(self): pass
    def ttest_get_collisions(self): pass


suite = unittest.TestLoader().loadTestsFromTestCase(BattleTests)