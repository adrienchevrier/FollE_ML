'''File containing shared variables'''

from threading import RLock

def init():
    global s_readings
    global b_readings
    global verrou
    global motors
    s_readings = [1,1,1,1,1]
    b_readings = [-1,-1,-1,-1,-1]
    motors = [0,0]
    verrou = RLock()