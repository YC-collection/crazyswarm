#!/usr/bin/env python

from __future__ import print_function

from math import *
import numpy as np
import random

from pycrazyswarm import *

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    cfs = allcfs.crazyflies


    print("press button to take off...")
    swarm.input.waitUntilButtonPressed()

    rand_heights = None

    if len(cfs) > 1:
        rand_heights = [random.random() for cf in cfs]
        lowest = min(rand_heights)
        highest = max(rand_heights)

        # ensure we fill up the full range of heights
        MIN_HEIGHT = 0.4
        MAX_HEIGHT = 1.8
        scale = (MAX_HEIGHT - MIN_HEIGHT) / (highest - lowest)

        for i in range(len(rand_heights)):
            rand_heights[i] = scale * (rand_heights[i] - lowest) + MIN_HEIGHT
    else:
        rand_heights = [1.0]

    heights = {}
    for cf, height in zip(cfs, rand_heights):
        heights[cf] = height
        duration = height + 1.0
        cf.takeoff(height, duration)

    timeHelper.sleep(max(rand_heights) + 1.0)

    for cf in cfs:
        hover_pos = cf.initialPosition + np.array([0, 0, heights[cf]])
        cf.hover(hover_pos, 0, 2.0)

    timeHelper.sleep(2.5)


    print("press button to start avoiding...")
    swarm.input.waitUntilButtonPressed()

    MAX_DISPLACEMENT = 1.2 * 0.5 # TODO get spacing from init positions
    MAX_SPEED = 1.5 # m/s

    for cf in cfs:
        home = cf.initialPosition + np.array([0, 0, heights[cf]])
        cf.avoidTarget(home, MAX_DISPLACEMENT, MAX_SPEED)


    print("press button to go home...")
    swarm.input.waitUntilButtonPressed()
    for cf in cfs:
        hover_pos = cf.initialPosition + np.array([0, 0, heights[cf]])
        cf.hover(hover_pos, 0, 2.0)

    timeHelper.sleep(2.5)


    print("press button to land...")
    swarm.input.waitUntilButtonPressed()
    allcfs.land(targetHeight = 0.02, duration = 3.5)


if __name__ == "__main__":
    main()

