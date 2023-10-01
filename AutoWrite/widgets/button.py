from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton, MDTextButton, MDFlatButton, MDRaisedButton, MDRectangleFlatButton

from kivy.lang import Builder

Builder.load_string("""

<RoundButton>
    md_bg_color: app.primary
    size_hint_x: .80
    font_name: app.fonts.medium
    font_size: app.fonts.size.h4
    theme_text_color: "Custom"
    markup: True
<RectangleButton>
    # md_bg_color: app.primary
    size_hint_x: .80
    font_name: app.fonts.medium
    font_size: app.fonts.size.h4
    theme_text_color: "Custom"
    markup: True
<FlatButton>
    # md_bg_color: app.primary
    size_hint_x: .80
    font_name: app.fonts.medium
    font_size: app.fonts.size.h4
    theme_text_color: "Custom"
    markup: True
<TextButton>
    # md_bg_color: app.primary
    # size_hint_x: .80
    markup: True
    font_name: app.fonts.medium
    font_size: app.fonts.size.h4
    markup: True
<IconButton>
    icon_color: app.colors.black
    theme_icon_color: "Custom"
    # icon_size: app.fonts.size.h2
""")


class RoundButton(MDFillRoundFlatButton):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

class RectangleButton(MDRectangleFlatButton):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)


class IconButton(MDIconButton):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)


class TextButton(MDTextButton):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)


class FlatButton(MDFlatButton):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

class RaisedButton(MDRaisedButton):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
