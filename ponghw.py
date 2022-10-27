from gpiozero import MotionSensor
import time

pir = MotionSensor(17, pull_up = None, active_state = False)
counts = 0
while True:
    pir.wait_for_motion()
    counts += 1
    print("counts = {}".format(counts))
    pir.wait_for_no_motion()