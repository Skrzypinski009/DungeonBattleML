from ctypes import cast
from random import randint, random
from typing import Callable
from pandas import DataFrame
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from ai_models.game_env import GameEnv
from db.models import AI_Model
import joblib
import numpy as np
import pandas as pd
import math

from db.models.action_type import ActionType

from db.models.battle_state import BattleState
from db.models.game_state import GameState
from services import actor_service, battle_service, dataset_service, game_service
from services import action_service
from services.action_service import ActionTypeEnum
from services import ai_learn_service
from ai_models.q_table_agent import QTableAgent
import pickle


def create_ai_model(model_type: str, name: str, model):
    AI_Model.create(
        type=model_type,
        name=name,
        data=pickle.dumps(model),
    )


def get_ai_models():
    return list(AI_Model.select().execute())


def get_model_by_name(name: str) -> AI_Model:
    model = AI_Model.select().where(AI_Model.name == name).first()
    return model


def train_model(type: str, dataset_df: DataFrame) -> dict:
    match (type):
        case "decision_tree":
            print(type)
            return train_decision_tree(dataset_df)
        case "random_forest":
            return train_random_forest(dataset_df)
        case "mlp":
            return train_mlp(dataset_df)

    return {}


def get_splitted_data(df: DataFrame) -> tuple:
    random_state = randint(1, 2000)
    df = df.sample(frac=1, random_state=random_state).reset_index(drop=True)
    df.pop("dataset_nr")
    df.pop("id")

    n = len(df)

    train_size = int(n * 0.7)

    X_train = df.iloc[:train_size]
    X_test = df.iloc[train_size:]

    y_train = X_train.pop("action_type")
    y_test = X_test.pop("action_type")

    return (X_train, X_test, y_train, y_test)


def supervised_learning(df: DataFrame, model, model_type: str) -> dict:
    df.fillna(0, inplace=True)

    (X_train, X_test, y_train, y_test) = get_splitted_data(df)
    # trenowanie
    model.fit(X_train, y_train)
    # predykcja
    y_pred = model.predict(X_test)
    # ocena w %
    score = model.score(X_test, y_test)

    target_names = ["attack", "heavy_attack", "block", "regeneration", "none"]
    # ocena względem każdej akcji
    report = classification_report(
        y_test, y_pred, target_names=target_names, output_dict=True
    )

    rows = [report[label_name] for label_name in target_names]
    print(rows)

    df_report = pd.DataFrame(rows)

    return {
        "type": model_type,
        "model": model,
        "score": score,
        "report": df_report,
    }


def train_random_forest(df: DataFrame) -> dict:
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        max_features="sqrt",
    )
    return supervised_learning(df, model, "random_forest")


def train_decision_tree(df: DataFrame) -> dict:
    model = DecisionTreeClassifier(max_depth=6)
    return supervised_learning(df, model, "decision_tree")


def train_mlp(df: DataFrame) -> dict:
    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "mlp",
                MLPClassifier(
                    hidden_layer_sizes=(64, 32),  # dwie warstwy ukryte
                    activation="relu",
                    solver="adam",
                    max_iter=500,
                    early_stopping=True,
                    random_state=42,
                ),
            ),
        ]
    )
    return supervised_learning(df, model, "mlp")


def train_in_env(model_type: str, enemy_list: list, episodes: int) -> dict:
    result = {}
    if model_type == "q_table":
        model = QTableAgent(GameEnv.N_STATES, GameEnv.N_ACTIONS)
        result = ai_learn_service.reinforcement_learning(model, episodes, enemy_list)

    result["type"] = model_type
    return result


def get_next_action(model, battle_state):

    prediction = None
    if model.type == "q_table":
        state = dataset_service.get_state_tuple(battle_state)
        model_data = pickle.loads(model.data)
        model_data.epsilon = 1

        prediction = predict_reinforcement(
            model_data,
            state,
        )
        return prediction

    else:
        state = dataset_service.get_state(
            battle_state,
        ).dicts()
        prediction = predict_supervised(
            pickle.loads(model.data),
            DataFrame(state).fillna(0),
        )
        return actor_service.action_validate(
            battle_state.game.player,
            prediction,
        )


def predict_supervised(model, state) -> ActionType:
    id = model.predict(state)[0]
    prediction = ActionType.select().where(ActionType.id == id).first()
    return prediction


def predict_reinforcement(model, state) -> list:
    print("------\n\n")
    print("state: ", state)
    avaliable = dataset_service.get_avaliable_sequences_ids(state)
    if len(avaliable) == 0:
        raise Exception

    print("avaliable: ", avaliable)
    prediction = model.predict(state, avaliable)
    print("prediction: ", prediction)
    print("\n\n------")
    return prediction


def remove_model(id: int):
    AI_Model.delete().where(AI_Model.id == id).execute()
