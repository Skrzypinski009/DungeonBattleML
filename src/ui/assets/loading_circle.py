from kivy.uix.image import Image
from kivy.graphics import PushMatrix, PopMatrix, Rotate
from kivy.clock import Clock


class LoadingCircle(Image):
    def __init__(self, **kwargs):
        super().__init__(source="img/loading_circle.png", **kwargs)
        self.angle = 0

        with self.canvas.before:  # pyright: ignore
            PushMatrix()
            self.rot = Rotate(angle=0, origin=self.center)

        with self.canvas.after:  # pyright: ignore
            PopMatrix()

        self.bind(  # pyright: ignore
            pos=self.update_origin,
            size=self.update_origin,
        )

    def update_origin(self, *_):
        self.rot.origin = self.center

    def start(self):
        Clock.schedule_interval(self.rotate, 1 / 60)

    def stop(self):
        Clock.unschedule(self.rotate)

    def rotate(self, dt):
        self.angle = (self.angle + 180 * dt) % 360
        self.rot.angle = self.angle
