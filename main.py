from typing import *
import dataclasses
import abc
import functools

import pyglet


class FieldVisualizer(pyglet.window.Window):
    @dataclasses.dataclass
    class FieldGizmo:
        x: float
        y: float
        r: float
        color: Tuple[int, int, int]
        circular: bool


    WIDTH_FT = 26 + 7 / 12
    HEIGHT_FT = 54 + 1 / 12

    def __init__(self, height_px: float = 600.0, name: str = "Field"):
        self.height_px = height_px
        self.px_per_ft = self.height_px / self.HEIGHT_FT
        self.width_px = self.height_px * self.WIDTH_FT / self.HEIGHT_FT
        self.gizmos = []

        super().__init__(int(self.width_px), int(self.height_px), name)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.mousex_ft = 0
        self.mousey_ft = 0

    def on_draw(self):
        self.clear()
        for gizmo in self.gizmos:
            rpx = self._topx(gizmo.r)
            xpx, ypx = self._topxpoint(gizmo.x, gizmo.y)
            if gizmo.circular:
                pyglet.shapes.Circle(xpx, ypx, rpx, color=gizmo.color).draw()
            else:
                pyglet.shapes.Rectangle(xpx-rpx, ypx-rpx, rpx*2.0, rpx*2.0, color=gizmo.color).draw()
        print(self.pressed())
    def on_mouse_motion(self, x, y, dx, dy):
        self.mousex_ft, self.mousey_ft = self._toftpoint(x, y)
    def mouse(self) -> Tuple[float, float]: return self.mousex_ft, self.mousey_ft
    def pressed(self) -> List[str]:
        return [str(k) for k, v in self.keys.items() if v]


    def _topx(self, ft: float) -> float:
        return ft * self.px_per_ft

    def _toft(self, px: float) -> float:
        return px / self.px_per_ft

    def _toftpoint(self, x: float, y: float) -> Tuple[float, float]:
        xf = self._toft(x - self.width_px / 2.0)
        yf = self._toft(y - self.height_px / 2.0)
        return xf, yf

    def _topxpoint(self, x: float, y: float) -> Tuple[float, float]:
        xp = self._topx(x + self.WIDTH_FT / 2.0)
        yp = self._topx(y + self.HEIGHT_FT / 2.0)
        return xp, yp
        
FIELD_ELEMENTS = [
    FieldVisualizer.FieldGizmo(
        0, 0, 3, (0, 255, 0), True
    ),
    FieldVisualizer.FieldGizmo(
        10, 10, 3, (0, 255, 0), False
    ),
]

one = FieldVisualizer()
one.gizmos = FIELD_ELEMENTS
two = FieldVisualizer()
pyglet.app.run()
