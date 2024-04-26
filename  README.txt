Milky Way

This program is a traffic simulation. Space roads have become a style. The road system is generated at each start. The cars are depicted in circles and obey the following rules:
    1. The speed is greater than or equal to 0 and less than or equal to the maximum
    2. If there is a car / intersection within the radius of the braking distance + reserve, the car brakes. Otherwise, it maintains the maximum speed.
        • If there is an obstacle in the braking distance at maximum speed, the car does not rev up.
    3. At the crossroads, the car that drove up to him first goes, the rest are standing
        • Such a system can lead to congestion if there are two intersections in a row: the first car waits until the second one leaves the second one, the second one waits until the first one leaves the first one. Therefore, if all cars are at the intersection, then the very first in the queue is given a "kick", i.e. all restrictions about intersections disappear, and the car goes forward, removing the congestion.

There are two types of cars in total – "normal" and "slower". The "slower" has a lower maximum speed, which is why interesting interactions appear: "normal" cars that drive in front of the "slower" are forced by the rules to drive at the same speed.

Instructions for use:
Just run the program and admire) Sometimes the generation turns out to be strange, for example, a huge grid of intersections, but you can always restart.
There is init.py. You ca