import numpy as np

readings = [1,2,3,45,6]
red = [7,8,9]

state = np.array([readings+red])

print(state)