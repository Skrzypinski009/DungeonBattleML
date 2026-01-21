from stable_baselines3 import PPO
import gymnasium as gym
from gymnasium import spaces
import numpy as np


class MyEnv(gym.Env):
    def __init__(self):
        super().__init__()

        self.action_space = spaces.Discrete(4)

        self.observation_space = spaces.Box(
            low=np.array([0, 0, -20, 0, 0], dtype=np.float32),
            high=np.array([10, 500, 20, 1, 1000], dtype=np.float32),
            dtype=np.float32,
        )

        self.state = np.array([])

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = np.array(
            [
                np.random.randint(0, 11),
                np.random.randint(0, 501),
                np.random.randint(-20, 21),
                np.random.randint(0, 2),
                np.random.randint(0, 1001),
            ],
            dtype=np.float32,
        )
        return self.state, {}

    def step(self, action):
        if action == 0:
            self.state[0] += 1
        elif action == 1:
            self.state[1] -= 10
        elif action == 2:
            self.state[2] *= -1
        elif action == 3:
            self.state[4] += 50

        self.state = np.clip(
            self.state, self.observation_space.low, self.observation_space.high
        )

        reward = -abs(self.state[2]) + self.state[3] * 5

        terminated = False
        truncated = False

        return self.state, reward, terminated, truncated, {}


class RL_MLP(PPO):
    def __init__(self):
        super().__init__("MlpPolicy", MyEnv(), verbose=1)

    def learn(self, total_timesteps, *args, **kwargs):
        return super().learn(total_timesteps=total_timesteps, *args, **kwargs)
