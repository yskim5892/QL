import numpy as np
from RT_display import *

def max_kv_in_dict(d):
    max_key = None
    max_value = float('-inf')
    for key in d:
        if d[key] > max_value:
            max_key = key
            max_value = d[key]
    return max_key, max_value

class QLearner:
    def epsilon_greedy_policy(self, state, epsilon=0.05):
        actions = list(self.Q[state].keys())
        probs = []
        optimal_action, _ = max_kv_in_dict(self.Q[state])

        for action in actions:
            if action == optimal_action:
                probs.append(1 - epsilon + epsilon / len(actions))
            else:
                probs.append(epsilon / len(actions))

        return np.random.choice(actions, p=probs)

    def initialize_Q(self, env):
        self.Q = dict()
        for state in env.states:
            self.Q[state] = dict()
            for action in env.possible_actions(state):
                if(state.is_terminal):
                    self.Q[state][action] = 0
                else:
                    self.Q[state][action] = -np.random.rand()

    def learn(self, env, alpha = 0.5):
        self.initialize_Q(env)

        TEST_PERIOD = 1000
        episode = 0
        sum_sum_reward = 0
        num_success = 0
        while(True):
            env.initialize_environment()
            episode += 1
            is_testing = (episode % TEST_PERIOD == 0)
            sum_reward = 0
            state_history = [env.state]
            action_history = []

            while(True):
                state = env.state
                if is_testing:
                    action = self.epsilon_greedy_policy(state, epsilon=0)
                else:
                    action = self.epsilon_greedy_policy(state)
                next_state, reward= env.respond(action)
                sum_reward += reward

                if(next_state.is_terminal):
                    max_q = 0
                else:
                    _, max_q = max_kv_in_dict(self.Q[next_state])
                q = self.Q[state][action]

                self.Q[state][action] = q + alpha * (reward + env.gamma * max_q - q)
                if is_testing:
                    action_history.append(action)
                    state_history.append(next_state)
                if(next_state.is_terminal):
                    if reward > 0:
                        num_success += 1
                    break

            sum_sum_reward += sum_reward
            if is_testing:
                print('Episode : ', episode, 'Success Rate :', num_success / TEST_PERIOD, ', Avg_Reward :', sum_sum_reward / TEST_PERIOD)
                sum_sum_reward = 0
                num_success = 0

                RT_display(episode, env.map, env.dest, state_history, action_history)
