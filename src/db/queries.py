from .models import BattleHistory, ActorType, ActionType, BattleState
from pandas import DataFrame


def add_last_action(history):
    for i, row in enumerate(history):
        prev_row = history[i - 1] if i != 0 else None
        add_last_action_row(row, prev_row)


def add_last_action_row(row, prev_row):
    if prev_row is not None:
        row["prev_action_type"] = prev_row["action_type"]
        row["prev_action_owner"] = prev_row["action_owner"]
    else:
        row["prev_action_type"] = 0
        row["prev_action_owner"] = 0


def unpacked_battle_history_query(battle_state: BattleState):
    Enemy = ActorType.alias()
    ActionOwner = ActorType.alias()

    return (
        BattleHistory.select(
            BattleHistory.turn_nr,
            BattleHistory.action_nr,
            # player
            BattleHistory.player_health,
            BattleHistory.player_energy,
            # enemy
            Enemy.id.alias("enemy_type"),
            BattleHistory.enemy_health,
            BattleHistory.enemy_energy,
            # action
            ActionOwner.id.alias("action_owner"),
            ActionType.id.alias("action_type"),
            # current_action
        )
        .join(
            Enemy,
            on=(BattleHistory.enemy_type == Enemy.id),
        )
        .switch(BattleHistory)
        .join(
            ActionOwner,
            on=(BattleHistory.action_owner == ActionOwner.id),
        )
        .switch(BattleHistory)
        .join(
            ActionType,
            on=(BattleHistory.action_type == ActionType.id),
        )
        .switch(BattleHistory)
        .join(
            BattleState,
            on=(BattleHistory.battle_state == BattleState.id),
        )
        .where(
            BattleHistory.battle_state == battle_state,
            BattleHistory.action_owner == battle_state.game.player.type,
        )
    )


def make_dataframe(query) -> DataFrame:
    history = list(query.dicts())
    print(history[0])
    add_last_action(history)
    return DataFrame(history)


def unpacked_battle_history_df(battle_state: BattleState) -> DataFrame:
    query = unpacked_battle_history_query(battle_state)
    return make_dataframe(query)
