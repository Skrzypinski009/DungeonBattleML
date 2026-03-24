from db.models import BattleState, AI_Model
from services import ai_model_service, dataset_service, actor_service
import pickle
import pandas as pd


class AIModelInterface:

    def __init__(self, model: AI_Model):
        self.load_model(model)
        self.next_actions = []

    def load_model(self, model: AI_Model):
        self.model = model
        self.model_instance = pickle.loads(model.data)

        if self.model.type == "q_table":
            self.model_instance.epsilon = 1

    def get_next_action(self, battle_state: BattleState):
        if not self.next_actions:
            if self.model.type == "q_table":
                self.next_actions.extend(
                    self.get_next_action_q_table(battle_state)
                )
            else:
                self.next_actions.append(
                    self.get_next_action_supervised(battle_state)
                )

        return self.next_actions.pop(0)

    def get_next_action_q_table(self, battle_state: BattleState):
        state = dataset_service.get_state_tuple(battle_state)
        prediction = ai_model_service.predict_reinforcement(
            self.model_instance,
            state,
        )
        return prediction

    def get_next_action_supervised(self, battle_state: BattleState):
        state = dataset_service.get_state(
            battle_state,
        ).dicts()
        prediction = ai_model_service.predict_supervised(
            self.model_instance,
            pd.DataFrame(state).fillna(0),
        )
        return actor_service.action_validate(
            battle_state.game.player,
            prediction,
        )
