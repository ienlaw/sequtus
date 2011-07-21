from game import seq_game
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        import unittest
        from test_lib import *
        
        unittest.TextTestRunner(verbosity=1).run(vector_t.suite)
    elif len(sys.argv) > 1 and sys.argv[1] == 'profile':
        from profile_lib import profiler
        profiler.run("")
        
    elif len(sys.argv) > 1 and sys.argv[1] == 'view':
        from profile_lib import profiler
        profiler.view("")
        
    else:
        s = seq_game.Sequtus()
        s.start()