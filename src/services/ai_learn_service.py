from ai_models.game_env import GameEnv
from services import action_service, dataset_service


def reinforcement_learning(
    agent, episodes: int, enemy_list: list, player_potions: int = 1
) -> dict:
    env = GameEnv(enemy_list, player_potions)

    history = {
        "win_rate": 0,
        "epsilons": [],
        "episode_lengths": [],
        "episode_rewards": [],
    }

    wins = 0

    for episode in range(episodes):

        episode_length = 0
        episode_reward = 0

        state, _ = env.reset()
        state_idx = env.state_to_idx(state)

        while True:
            avaliable_actions = dataset_service.get_avaliable_sequences_ids(state)
            action = agent.act(state_idx, avaliable_actions)
            sequence = agent.get_sequence(action)

            next_state, reward, terminated, truncated, info = env.step(sequence)
            next_state_idx = env.state_to_idx(next_state)

            agent.learn(state_idx, action, reward, next_state_idx, terminated)

            state = next_state
            state_idx = next_state_idx

            episode_reward += reward
            episode_length += 1

            if terminated or truncated:
                if "winner" in info and info["winner"] == "player":
                    wins += 1
                break
        agent.epsilon = compute_epsilon(episode, episodes, 1.0, 0.05)

        history["epsilons"].append(agent.epsilon)
        history["episode_lengths"].append(episode_length)
        history["episode_rewards"].append(episode_reward)
    history["win_rate"] = wins / episodes

    return {"model": agent, "history": history}


def compute_epsilon(episode, episodes_count, epsilon_start, epsilon_end):
    frac = min(episode / episodes_count, 1.0)
    return epsilon_start - frac * (epsilon_start - epsilon_end)
