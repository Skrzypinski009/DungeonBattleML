import pickle

from db.models import AI_Model


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


def remove_model(id: int):
    AI_Model.delete().where(AI_Model.id == id).execute()
