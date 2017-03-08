"""
Once a model is learned, use this to play it.
"""

from flat_game import carmunkBLE2 as carmunk
import numpy as np
from nn import neural_net
import time

NUM_SENSORS = 5


def play(model):

    car_distance = 0
    game_state = carmunk.GameState()

    # Do nothing to get initial.
    _, state, stuff = game_state.frame_step((2))

    # Move.
    while True:
        #time.sleep(0.05)
        car_distance += 1

        # Choose action.
        action = (np.argmax(model.predict(state, batch_size=1)))

        # Take action.
        _, state,stuff = game_state.frame_step(action)

        # Tell us something.
        if car_distance % 1000 == 0:
            print("\n Current distance: %d frames." % car_distance)


if __name__ == "__main__":
    saved_model = 'saved-models/164-150-100-50000-25000.h5'
    model = neural_net(NUM_SENSORS, [164, 150], saved_model)
    play(model)