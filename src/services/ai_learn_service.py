from ai_models.game_env import GameEnv

from services import dataset_service


def reinforcement_learning(
    agent, episodes: int, enemy_list: list, player_potions: int = 1
) -> dict:
    env = GameEnv(enemy_list, player_potions)
    for episode in range(episodes):

        state, _ = env.reset()
        state_idx = env.state_to_idx(state)
        while True:
            avaliable_actions = dataset_service.get_avaliable_sequences_ids(
                state
            )
            action = agent.act(state_idx, avaliable_actions)

            next_state, reward, terminated, truncated, _ = env.step(action)
            next_state_idx = env.state_to_idx(next_state)

            agent.learn(state_idx, action, reward, next_state_idx, terminated)

            state = next_state
            state_idx = next_state_idx

            if terminated or truncated:
                break

        agent.epsilon = compute_epsilon(episode, episodes, 1.0, 0.05)
    return {"model": agent}


def compute_epsilon(episode, episodes_count, epsilon_start, epsilon_end):
    frac = min(episode / episodes_count, 1.0)
    return epsilon_start - frac * (epsilon_start - epsilon_end)
