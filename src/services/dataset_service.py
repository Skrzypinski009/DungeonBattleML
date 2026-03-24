from typing import Iterable

from db.models import BattleHistory, BattleState, Dataset, GameState
from db.models.action_type import ActionType
from db.models.actor import Actor
from db.models.actor_type import ActorType
from pandas import DataFrame
from peewee import Case, ModelSelect, fn
from services import action_service, battle_service


def dataset_query(battle: BattleState):
    # aliasy dla ActorType
    EnemyType = ActorType.alias()
    PlayerType = ActorType.alias()
    Player = Actor.alias()

    # kolejny dataset_nr
    next_dataset_nr = Dataset.select(
        (fn.COALESCE(fn.MAX(Dataset.dataset_nr), 0) + 1)
    )

    attack_avaliable = Case(None, ((Player.energy >= 4, 1),), 0).alias(
        "attack_avaliable"
    )
    heavy_attack_avaliable = Case(None, ((Player.energy >= 6, 1),), 0).alias(
        "heavy_attack_avaliable"
    )
    block_avaliable = Case(None, ((Player.energy >= 2, 1),), 0).alias(
        "block_avaliable"
    )
    regeneration_avaliable = Case(None, ((Player.energy >= 3, 1),), 0).alias(
        "regeneration_avaliable"
    )

    query = (
        BattleHistory.select(
            next_dataset_nr.alias("dataset_nr"),
            BattleHistory.turn_nr,
            BattleHistory.action_nr,
            # player type stats
            PlayerType.max_health.alias("player_max_health"),
            PlayerType.max_energy.alias("player_max_energy"),
            PlayerType.attack_damage.alias("player_attack_damage"),
            # player state
            BattleHistory.player_health,
            BattleHistory.player_energy,
            # enemy type stats
            EnemyType.max_health.alias("enemy_max_health"),
            EnemyType.max_energy.alias("enemy_max_energy"),
            EnemyType.attack_damage.alias("enemy_attack_damage"),
            # enemy state
            BattleHistory.enemy_health,
            BattleHistory.enemy_energy,
            # action type
            ActionType.id.alias("action_type"),
            # last action
            fn.LAG(ActionType.id)
            .over(order_by=[BattleHistory.id])
            .alias("last_action_type"),
            attack_avaliable,
            heavy_attack_avaliable,
            block_avaliable,
            regeneration_avaliable,
        )
        # join dla EnemyType
        .join(EnemyType, on=(BattleHistory.enemy_type == EnemyType.id))
        # join do BattleState → GameState → Actor → PlayerType
        .switch(BattleHistory)
        .join(BattleState, on=(BattleHistory.battle_state == BattleState.id))
        .join(GameState, on=(BattleState.game == GameState.id))
        .join(Player, on=(GameState.player == Player.id))
        .join(PlayerType, on=(Player.type == PlayerType.id))
        # join ActionType dla akcji
        .switch(BattleHistory)
        .join(ActionType, on=(BattleHistory.action_type == ActionType.id))
        # filtracja tylko jednej walki
        .where(BattleHistory.battle_state == battle)
    )

    return query


def get_state(battle: BattleState):

    EnemyType = ActorType.alias()
    Enemy = Actor.alias()

    PlayerType = ActorType.alias()
    Player = Actor.alias()

    LastAction = (
        BattleHistory.select()
        .where(
            BattleHistory.battle_state == BattleState.id,
            BattleHistory.turn_nr <= BattleState.turn_nr,
        )
        .order_by(BattleHistory.action_nr.desc())
        .limit(1)
    )

    attack_avaliable = Case(None, ((Player.energy >= 4, 1),), 0).alias(
        "attack_avaliable"
    )
    heavy_attack_avaliable = Case(None, ((Player.energy >= 6, 1),), 0).alias(
        "heavy_attack_avaliable"
    )
    block_avaliable = Case(None, ((Player.energy >= 2, 1),), 0).alias(
        "block_avaliable"
    )
    regeneration_avaliable = Case(
        None, (((Player.energy >= 3) & (Player.potions > 0), 1),), 0
    ).alias("regeneration_avaliable")

    query = (
        BattleState.select(
            BattleState.turn_nr,
            BattleState.action_nr,
            # player type stats
            PlayerType.max_health.alias("player_max_health"),
            PlayerType.max_energy.alias("player_max_energy"),
            PlayerType.attack_damage.alias("player_attack_damage"),
            # player state
            Player.health.alias("player_health"),
            Player.energy.alias("player_energy"),
            # enemy type stats
            EnemyType.max_health.alias("enemy_max_health"),
            EnemyType.max_energy.alias("enemy_max_energy"),
            EnemyType.attack_damage.alias("enemy_attack_damage"),
            # enemy state
            Enemy.health.alias("enemy_health"),
            Enemy.energy.alias("enemy_energy"),
            # last action
            LastAction.alias("last_action_type"),
            # actions
            attack_avaliable,
            heavy_attack_avaliable,
            block_avaliable,
            regeneration_avaliable,
        )
        .join(Enemy, on=(BattleState.enemy == Enemy.id))
        .join(EnemyType, on=(Enemy.type == EnemyType.id))
        .switch(BattleState)
        .join(GameState, on=(BattleState.game == GameState.id))
        .join(Player, on=(GameState.player == Player.id))
        .join(PlayerType, on=(Player.type == PlayerType.id))
        .switch(BattleState)
        .where(BattleState.id == battle.id)
        .order_by(BattleState.id.desc())
        .limit(1)
    )

    return query


def get_state_tuple(battle: BattleState):
    return get_state(battle).tuples().first()  # drop id field


def state_to_dict(state):
    print(state)
    return {
        "turn_nr": state[0],
        "action_nr": state[1],
        "player_max_health": state[2],
        "player_max_energy": state[3],
        "player_attack_damage": state[4],
        "player_health": state[5],
        "player_energy": state[6],
        "enemy_max_health": state[7],
        "enemy_max_energy": state[8],
        "enemy_attack_damage": state[9],
        # enemy state
        "enemy_health": state[10],
        "enemy_energy": state[11],
        # last action
        "last_action_type": state[12],
        # actions
        "attack_avaliable": state[13],
        "heavy_attack_avaliable": state[14],
        "block_avaliable": state[15],
        "regeneration_avaliable": state[16],
    }


def create_dataset_from_battle_ids(battle_ids: Iterable) -> tuple[Dataset]:
    battles: list[BattleState] = [
        battle_service.get_battle(id) for id in battle_ids
    ]
    print(len(battles))
    union = dataset_query(battles[0])
    print(union.count())
    for battle in battles[1:]:
        union = union.union_all(dataset_query(battle))
    print(union.count())

    return Dataset.insert_from(
        union,
        fields=[
            Dataset.dataset_nr,
            Dataset.turn_nr,
            Dataset.action_nr,
            Dataset.player_max_health,
            Dataset.player_max_energy,
            Dataset.player_attack_damage,
            Dataset.player_health,
            Dataset.player_energy,
            Dataset.enemy_max_health,
            Dataset.enemy_max_energy,
            Dataset.enemy_attack_damage,
            Dataset.enemy_health,
            Dataset.enemy_energy,
            Dataset.action_type,
            Dataset.last_action_type,
            Dataset.attack_avaliable,
            Dataset.heavy_attack_avaliable,
            Dataset.block_avaliable,
            Dataset.regeneration_avaliable,
        ],
    ).execute()


def create_dataset_from_game(game: GameState) -> tuple[Dataset]:
    battle_ids = battle_service.get_battle_ids(game)
    return create_dataset_from_battle_ids(battle_ids)


def get_dataset_ids() -> tuple[int]:
    query = Dataset.select(Dataset.dataset_nr).group_by(Dataset.dataset_nr)
    return tuple(row[0] for row in query.tuples())


def get_dataset_by_id(id: int) -> ModelSelect:
    return Dataset.select().where(Dataset.dataset_nr == id)


def get_datasets() -> list[tuple[Dataset]]:
    ids = get_dataset_ids()
    return [tuple(get_dataset_by_id(id).execute()) for id in ids]


def remove_dataset(id: int) -> None:
    Dataset.delete().where(Dataset.dataset_nr == id).execute()


def get_dict_from_dataset(dataset: Dataset) -> dict:
    return {
        "dataset_nr": dataset.dataset_nr,
        "turn_nr": dataset.turn_nr,
        "action_nr": dataset.action_nr,
        "player_max_health": dataset.player_max_health,
        "player_max_energy": dataset.player_max_energy,
        "player_attack_damage": dataset.player_attack_damage,
        "player_health": dataset.player_health,
        "player_energy": dataset.player_energy,
        "enemy_max_health": dataset.enemy_max_health,
        "enemy_max_energy": dataset.enemy_max_energy,
        "enemy_attack_damage": dataset.enemy_attack_damage,
        "enemy_health ": dataset.enemy_health,
        "enemy_energy": dataset.enemy_energy,
        "action_type": dataset.action_type,
        "last_action_type": dataset.last_action_type,
        "attack_avaliable": dataset.attack_avaliable,
        "heavy_attack_avaliable": dataset.heavy_attack_avaliable,
        "block_avaliable": dataset.block_avaliable,
        "regeneration_avaliable": dataset.regeneration_avaliable,
    }


def get_dataframe_from_dataset(dataset: Dataset) -> DataFrame:
    return DataFrame(get_dict_from_dataset(dataset))


def get_dataset_tuple(dataset: Dataset) -> tuple:
    return tuple(get_dict_from_dataset(dataset).values())


def get_avaliable_actions_by_state(state) -> list:
    d = state_to_dict(state)
    return action_service.get_avaliable(
        d["player_energy"], d["regeneration_avaliable"]
    )


def get_avaliable_sequences(state):
    d = state_to_dict(state)
    player_energy = d["player_energy"]
    can_regen = d["regeneration_avaliable"] == 1

    R = action_service.ActionTypeEnum.REGENERATION

    sequences = action_service.action_sequences()

    sequences = [
        s_dict for s_dict in sequences if s_dict["cost"] <= player_energy
    ]

    if not can_regen:
        sequences = [
            s_dict for s_dict in sequences if R not in s_dict["sequence"]
        ]

    return sequences


def get_avaliable_sequences_ids(state):
    avaliable_sequences = get_avaliable_sequences(state)
    return [seq["id"] for seq in avaliable_sequences]
