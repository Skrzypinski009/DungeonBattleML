from peewee import IntegerField

from .base_model import BaseModel


class Dataset(BaseModel):
    dataset_nr = IntegerField(null=False)
    turn_nr = IntegerField(null=False)
    action_nr = IntegerField(null=False)

    player_max_health = IntegerField(null=False)
    player_max_energy = IntegerField(null=False)
    player_attack_damage = IntegerField(null=False)

    player_health = IntegerField(null=False)
    player_energy = IntegerField(null=False)

    enemy_max_health = IntegerField(null=False)
    enemy_max_energy = IntegerField(null=False)
    enemy_attack_damage = IntegerField(null=False)

    enemy_health = IntegerField(null=False)
    enemy_energy = IntegerField(null=False)

    action_type = IntegerField(null=False)
    last_action_type = IntegerField(null=True)

    attack_avaliable = IntegerField(null=True)
    heavy_attack_avaliable = IntegerField(null=True)
    block_avaliable = IntegerField(null=True)
    regeneration_avaliable = IntegerField(null=True)
