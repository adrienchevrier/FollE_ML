"""
class launching car movement on raspberry
"""
import shared
from flat_game import raspmunk as carmunk
import numpy as np
from nn import neural_net
import time
from threading import Thread,RLock

NUM_SENSORS = 7


class player(Thread):
    """docstring for player"""
    def __init__(self, arg):
        super(player, self).__init__()
        self.model = arg
        
    def play(self):
    
        car_distance = 0
        game_state = carmunk.GameState()
    
        # Do nothing to get initial.
        _, state,stuff = game_state.frame_step((2))
    
        # Move.
        while True:
            #time.sleep(0.05)
            car_distance += 1
    
            # Choose action.
            action = (np.argmax(self.model.predict(state, batch_size=1)))
    
            # Take action.
            _, state,stuff = game_state.frame_step(action)
    
            # Tell us something.
            if car_distance % 1000 == 0:
                with shared.verrou:
                    print("\n Current distance: %d frames." % car_distance)


if __name__ == "__main__":
    shared.init()
    saved_model = 'saved-models/BLE/4sens/164-150-100-50000-150000.h5'
    model = neural_net(NUM_SENSORS, [164, 150], saved_model)
    p = player(model)
    p.play()