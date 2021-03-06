from engine.logic import core_tests
from game import seq_game
import sys

if __name__ == '__main__':
    from engine.libs import geometry
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        import unittest
        
        core_tests.run()
        
    elif len(sys.argv) > 1 and sys.argv[1] == 'profile':
        from profile_lib import profiler
        profiler.run("")
    
    elif len(sys.argv) > 1 and sys.argv[1] == 'compare':
        from profile_lib import comparer
        comparer.compare()
    
    elif len(sys.argv) > 1 and sys.argv[1] == 'view':
        from profile_lib import profiler
        profiler.view("")
        
    else:
        s = seq_game.Sequtus()
        s.start()