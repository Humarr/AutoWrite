from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.properties import StringProperty


class Pop(MDDialog):
    title = StringProperty()
    text = StringProperty()

    def __init__(self, *args, **kwargs):
        # pass
        super().__init__(*args, **kwargs)

        # self._spacer_top
        self.radius = [30, 0, 30, 0]
