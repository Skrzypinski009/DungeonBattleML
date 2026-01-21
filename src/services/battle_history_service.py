from numpy._core.numeric import full
from db.queries import unpacked_battle_history_df
from db.models import BattleHistory, BattleState
from services.action_service import ActionTypeEnum


def get_history_battle(battle: BattleState):
    return (
        BattleHistory.select()
        .where(BattleHistory.battle_state == battle)
        .order_by(BattleHistory.action_nr.desc())
    )


def prev_history_select(battle_state: BattleState):
    return (
    )


def get_prev_history_row(history: BattleHistory):
    history_rows = list(
        BattleHistory.select()
        .where(
            BattleHistory.battle_state == history.battle_state,
            BattleHistory.turn_nr <= history.turn_nr,
        )
        .order_by(BattleHistory.action_nr.desc())
    )
    if len(history_rows) >= 2:
        return history_rows[1]
    return None


def history_log(history: BattleHistory, current_battle: BattleState):
    logs: list[str] = []

    prev_history_select = BattleHistory.select().where(
        BattleHistory.battle_state == current_battle,
    )
    prev_history = None
    if len(prev_history_select) > 1:
        prev_history = prev_history_select[-2]

    action_owner_name = history.action_owner.name

    match history.action_type:
        case ActionTypeEnum.ATTACK:
            logs.append(f"[{action_owner_name}] Wykonuje atak")
            logs.append(damage_log(history, prev_history, current_battle))

        case ActionTypeEnum.HEAVY_ATTACK:
            logs.append(f"[{action_owner_name}] Wykonuje silny atak")
            logs.append(damage_log(history, prev_history, current_battle))

        case ActionTypeEnum.BLOCK:
            logs.append(f"[{action_owner_name}] Blokuje następny atak")

        case ActionTypeEnum.REGENERATION:
            logs.append(f"[{action_owner_name}] Regeneruje punkty zdrowia")

        case ActionTypeEnum.NONE:
            logs.append(f"[{action_owner_name}] Kończy swoją turę")
    return logs


def damage_log(
    history: BattleHistory,
    prev_history: BattleHistory | None,
    current_battle: BattleState,
):
    dmg: int = 0
    name: str = ""

    player = current_battle.game.player
    enemy = current_battle.enemy

    # Enemy taking damage
    if player.type == history.action_owner:
        name = enemy.type.name
        if prev_history == None:
            dmg = enemy.type.max_health - history.enemy_health
        else:
            dmg = prev_history.enemy_health - history.enemy_health

    # Player taking damage
    elif enemy.type == history.action_owner:
        name = player.type.name
        if prev_history == None:
            dmg = player.type.max_health - history.player_health
        else:
            dmg = prev_history.player_health - history.player_health

    return f"[{name}] Otrzymuje {dmg} punktów obrażeń"


def is_current_actor_changed(battle: BattleState):
    full_history = get_history_battle(battle)
    history_rows_count = full_history.count()
    if history_rows_count < 2:
        return

    last_history_row: BattleHistory = full_history.first()
    prev_history_row: BattleHistory | None = get_prev_history_row(last_history_row)

    if (
        prev_history_row == None
        or last_history_row.action_owner == prev_history_row.action_owner
    ):
        return False
    return True
