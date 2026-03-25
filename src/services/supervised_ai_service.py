import pandas as pd
from db.models.action_type import ActionType
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import make_column_transformer
from services import dataset_service
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate
from dataclasses import dataclass
import pandas as pd


@dataclass
class SupervisedOptions:
    cross_validation: int = 0
    grid_search_parameters: list[str] = []
    fixed_parameters: dict[str, list] = {}


def get_parameters_grid(params) -> dict[str, list]:
    param_grid = {
        "max_depth": [5, 10, 15, 20],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "n_estimators": [20, 50, 100, 200, 300],
        "hidden_layer_sizes": [(64, 32), (32, 16, 8), (32, 32)],
        "alpha": [0.0001, 0.001, 0.01],
        "max_iter": [200, 500],
    }
    return {k: param_grid[k] for k in params if k in param_grid}


def gridsearch(model, X, y, supervised_options: SupervisedOptions) -> None:
    param_grid = get_parameters_grid(
        supervised_options.grid_search_paramseters,
    )

    if isinstance(model, Pipeline):
        name = model.steps[-1][0]
        param_grid = {
            name + "__" + k: param_grid[k] for k in param_grid.keys()
        }

    search = GridSearchCV(
        model,
        cv=5,
        param_grid=param_grid,
        scoring="accuracy",
        return_train_score=True,
        refit=False,
    )
    search.fit(X, y)

    model.set_params(**search.best_parameters_)


def cross_validation(model, X, y, cv: int) -> None:
    cv_results = cross_validate(
        model,
        X,
        y,
        cv=cv,
        scoring="accuracy",
        return_train_score=True,
    )

    resutls = pd.DataFrame(cv_results)[["test_score", "train_score"]].mean()
    return resutls


def supervised_learning(
    df: pd.DataFrame,
    model,
    model_type: str,
    supervised_options=SupervisedOptions(),
) -> dict:

    results = {}
    df.fillna(0, inplace=True)
    y = df["action_type"]
    X = df.drop(columns=["action_type"])

    model.set_params(**supervised_options.fixed_parameters)

    if len(supervised_options.grid_search_parameters.keys()) > 0:
        gridsearch(model, X, y, supervised_options)

    if supervised_options.cross_validation:
        cv_results = cross_validate(
            model, X, y, supervised_options.cross_validation
        )
        results["cv_mean_test_score"] = cv_results["test_score"]
        results["cv_mean_train_score"] = cv_results["train_score"]

    model.fit(X, y)
    results["all_data_score"] = model.score(X, y)
    results["model"] = model
    results["model_type"] = model_type

    return results


def train_model(
    model_type: str,
    dataset_df: pd.DataFrame,
    supervised_options=SupervisedOptions(),
) -> dict:
    dataset_df = dataset_df.drop(columns=["dataset_nr", "id"])

    match (model_type):
        case "decision_tree":
            model = get_decision_tree()
        case "random_forest":
            model = get_random_forest()
        case "mlp":
            model = get_mlp()

    supervised_learning(dataset_df, model, model_type, supervised_options)


def get_random_forest() -> dict:
    return RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        max_features="sqrt",
    )


def get_decision_tree() -> dict:
    return DecisionTreeClassifier(max_depth=6)


def pipeline_with_scaler(model_name, model_object) -> Pipeline:
    numerical_columns = dataset_service.get_numerical_columns()
    preprocessor = make_column_transformer(
        (StandardScaler(), numerical_columns),
        remainder="passthrough",
    )
    return Pipeline(
        [
            ("preprocessor", preprocessor),
            (
                model_name,
                model_object,
            ),
        ]
    )


def get_mlp() -> dict:
    return pipeline_with_scaler(
        "mlp",
        MLPClassifier(
            hidden_layer_sizes=(64, 32),
            activation="relu",
            solver="adam",
            max_iter=500,
            early_stopping=True,
            random_state=42,
        ),
    )


def predict_supervised(model, state) -> ActionType:
    id = model.predict(state)[0]
    prediction = ActionType.select().where(ActionType.id == id).first()
    return prediction
