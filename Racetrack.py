from Environment import *
from QLearner import *
from utils import *
import numpy as np
import json

class RT_Action(Action):
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def __str__(self):
        return '(%d,%d)'%(self.dx, self.dy)

class RT_State(State):
    def __init__(self, is_terminal, x, v):
        self.is_terminal = is_terminal
        self.x = x
        self.v = v
    def __str__(self):
        return '(%s,%s)'%(str(self.x), str(self.v))

class RT_Environment(Environment):
    def __init__(self, gamma, map, map_size, dest):
        self.gamma = gamma
        self.map = map
        self.map_size = map_size

        self.actions = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                self.actions.append(RT_Action(dx, dy))

        self.states = []
        self.dest = dest
        self.state_dict = dict()
        for x in map:
            for vx in range(-3, 4):
                for vy in range(-3, 4):
                    v = (vx, vy)
                    state = RT_State(False, x, v)
                    if x[0] == dest[0] and x[1] == dest[1]:
                        state.is_terminal = True
                    self.states.append(state)
                    self.state_dict[(x, v)] = state
        self.initialize_environment()

    def initialize_environment(self):
        state = np.random.choice(self.states)
        self.state = self.state_dict[(state.x, (0, 0))]

    def possible_actions(self, state):
        return self.actions

    def respond(self, action):
        x = self.state.x[0]
        y = self.state.x[1]
        vx = self.state.v[0]
        vy = self.state.v[1]
        vx += action.dx
        vy += action.dy
        new_x = x + vx
        new_y = y + vy

        for i in range(0, 10):
            px = int(x + vx * i / 10)
            py = int(y + vy * i / 10)
            if not((px, py) in self.map):
                return RT_State(True, (px, py), (vx, vy)), -10

        if(dist_point_line_passing_two_points((x, y), (new_x, new_y), self.dest) < 0.5):
            return RT_State(True, self.dest, (vx, vy)), 10


        if not(((new_x, new_y), (vx, vy)) in self.state_dict):
            return RT_State(True, (new_x, new_y), (vx, vy)), -10

        self.state = self.state_dict[((new_x, new_y), (vx, vy))]
        return self.state, -1

def construct_environment():
    map_size = 20
    map = dict()

    prev_x_min = 0
    prev_x_max = map_size - 1
    for y in range(0, map_size):
        while(True):
            x = np.random.randint(0, map_size - 2)
            w = np.random.randint(1, map_size - x + 1)
            if(not (x > prev_x_max or x + w - 1 < prev_x_min)):
                break
        prev_x_min = x
        prev_x_max = x + w - 1
        for i in range(x, x+w):
            map[(i, y)] = 1

    positions = np.array(list(map.keys()))
    ind = np.random.choice(range(len(positions)))
    dest = (positions[ind][0], positions[ind][1])

    return RT_Environment(0.9, map, map_size, dest)

if __name__ == '__main__':
    RT_env = construct_environment()
    RT_agent = QLearner()
    RT_agent.learn(RT_env)