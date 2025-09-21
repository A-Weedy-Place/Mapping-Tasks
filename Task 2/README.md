Ok so we have some parallel roads lanes (lines) and we need to write the order.
Since, the roads can be in any direction we ant really use the coordinates but as given we can order the roads from right to left.

So, first we need direction.
all the lines have start and end point. so we find the line vectors, divide them by their magnitude and we will be left with the direction.
Now ideally all the lines should have the dame direction but just to be sure we can add all directions and take average.
Now a way to check right is rotate by 90 degrees clockwise which can be done by  (x, y) -> (y, -x) (since right is perp, dot product should be 0, verifies)
Now we find the centre of lanes (bcz we can somehwat bypass edge cases... somewhat)
so we now technically have the direction (right dir) and also the vectors (from 1 lane to the other), we can find the magnitude.
Now just compare magnitudes and order them accordingly (highest is right)