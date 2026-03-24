import pandas as pd
from db.models.action_type import ActionType
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


def supervised_learning(df: pd.DataFrame, model, model_type: str) -> dict:
    df.fillna(0, inplace=True)
    target = df["action_type"]
    df = df.drop(columns=["dataset_nr", "id", "action_type"])
    X_train, X_test, y_train, y_test = train_test_split(df, target)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    score = model.score(X_test, y_test)

    target_names = ["attack", "heavy_attack", "block", "regeneration", "none"]

    # TODO: delete this
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


def train_model(type: str, dataset_df: pd.DataFrame) -> dict:
    match (type):
        case "decision_tree":
            return train_decision_tree(dataset_df)
        case "random_forest":
            return train_random_forest(dataset_df)
        case "mlp":
            return train_mlp(dataset_df)
    return {}


def train_random_forest(df: pd.DataFrame) -> dict:
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        max_features="sqrt",
    )
    return supervised_learning(df, model, "random_forest")


def train_decision_tree(df: pd.DataFrame) -> dict:
    model = DecisionTreeClassifier(max_depth=6)
    return supervised_learning(df, model, "decision_tree")


def train_mlp(df: pd.DataFrame) -> dict:
    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "mlp",
                MLPClassifier(
                    hidden_layer_sizes=(64, 32),
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


def predict_supervised(model, state) -> ActionType:
    id = model.predict(state)[0]
    prediction = ActionType.select().where(ActionType.id == id).first()
    return prediction
