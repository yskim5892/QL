import math

def dist_point_line_passing_two_points(x0, x1, xd):
    if (x0[0] == x1[0] and x0[1] == x1[1]):
        return math.sqrt((x0[0] - xd[0])**2 + (x0[1] - xd[1])**2)

    d2_0d = (x0[0] - xd[0])**2 + (x0[1] - xd[1])**2
    d2_1d = (x1[0] - xd[0])**2 + (x1[1] - xd[1])**2
    d2_01 = (x0[0] - x1[0])**2 + (x0[1] - x1[1])**2

    if d2_0d > d2_1d + d2_01:
        return d2_1d
    if d2_1d > d2_0d + d2_01:
        return d2_0d

    return abs((x0[0] - x1[0]) * xd[1] - (x0[1] - x1[1]) * xd[0] - x1[1] * x0[0] + x1[0] * x0[1])\
        / math.sqrt(d2_01)

