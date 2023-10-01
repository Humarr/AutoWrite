from kivymd.uix.label import MDLabel, MDIcon
from kivy.lang import Builder
Builder.load_string("""
<Text>
    markup: True
    shorten: True
    theme_text_color: "Custom"

<Icon>
    theme_text_color: "Custom"


""")

class Text(MDLabel):

    def __init__(self, *args, **kwargs):
        super().__init__( **kwargs)

class Icon(MDIcon):

    def __init__(self, *args, **kwargs):
        super().__init__( **kwargs)
