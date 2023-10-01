from kivymd.uix.floatlayout import MDFloatLayout
from kivy.lang import Builder

Builder.load_string("""
<Circle>
    size_hint: None, None
    radius: self.width/2

""")

class Circle(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)