from kivy.uix.image import Image

from services.action_service import ActionTypeEnum


class Icon(Image):
    def __init__(self, action_type_id: int, size: int, **kwargs):
        super().__init__(
            source=self.get_path(action_type_id),
            size_hint_x=None,
            size_hint_y=None,
            width=size,
            height=size,
            **kwargs,
        )

    def change_to(self, action_type_id: int):
        if action_type_id == 0:
            self.opacity = 0
            return

        self.source = self.get_path(action_type_id)
        self.opacity = 1

    def get_path(self, action_type_id: int) -> str:
        nr = {
            ActionTypeEnum.ATTACK.id: 1,  # pyright: ignore
            ActionTypeEnum.HEAVY_ATTACK.id: 2,  # pyright: ignore
            ActionTypeEnum.BLOCK.id: 3,  # pyright: ignore
            ActionTypeEnum.REGENERATION.id: 4,  # pyright: ignore
        }[action_type_id]
        return f"img/skill_icon{nr}.png"
