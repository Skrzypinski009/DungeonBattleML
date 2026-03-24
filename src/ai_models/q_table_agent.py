import numpy as np

from ai_models.game_env import GameEnv


class QTableAgent:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.Q = np.zeros((n_states, n_actions))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.n_actions = n_actions

    def act(self, state_idx, legal_actions=None):
        if legal_actions is None:
            legal_actions = list(range(self.n_actions))

        if np.random.rand() < self.epsilon:
            action = np.random.choice(legal_actions)
            return action
            # return GameEnv.SEQUENCES[action]["sequence"]

        q_values = self.Q[state_idx, legal_actions]
        best_idx = np.argmax(q_values)
        action = legal_actions[best_idx]
        return action
        # return GameEnv.SEQUENCES[action]["sequence"]

    def learn(self, state_idx, action, reward, next_state_idx, terminated):
        if terminated:
            target = reward
        else:
            target = reward + self.gamma * np.max(self.Q[next_state_idx])

        print("\n\n\n\n")
        print(state_idx)
        print(action)
        print("\n\n\n\n")
        self.Q[state_idx, action] += self.alpha * (target - self.Q[state_idx, action])

    def predict(self, state, legal_actions=None):
        state_idx = GameEnv.state_to_idx(state)
        action = self.act(state_idx, legal_actions)
        return self.get_sequence(action)

    def get_sequence(self, action):
        return GameEnv.SEQUENCES[action]["sequence"]
