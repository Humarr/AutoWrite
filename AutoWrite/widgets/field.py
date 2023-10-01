from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import StringProperty, ColorProperty, NumericProperty,BooleanProperty


Builder.load_string("""
<MyTextField>
    text_color_normal: app.colors.black
    text_color_focus: app.colors.black
    hint_text_color_normal: app.colors.black
    hint_text_color_focus: app.colors.black
    # font_name_hint_text: app.fonts.body
    line_color_normal: app.colors.primary
    line_color_focus: app.colors.black
    icon_right_color_normal: app.colors.black
    icon_right_color_focus: app.colors.black
    input_type: "text"
    # font_name: app.fonts.subheading
    mode: "fill"
    radius: [25,0,25,0]
    size_hint_x: .8
    active_line: False
    helper_text_mode: "on_error"
    # on_text: print(self.text)
    fill_color_normal: app.colors.grey
    fill_color_focus: app.colors.grey



<MyInput>:
    hint_text: input.hint_text
    text: input.text
    focus: input.focus
    # text_color: text_color
    size_hint: .4,.08
    # pos_hint: {'center_x': 0.75,'center_y': .94}
    canvas:
        Color:
            rgb: root.background_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [10]
    TextInput:
        id: input
        hint_text: root.hint_text
        text: root.text
        size_hint: 1, None
        pos_hint: {'center_x': .5, 'center_y': .5}
        height: self.minimum_height
        font_size: "18sp"
        cursor_color: root.cursor_color
        foreground_color: root.text_color
        cursor_width: sp(2)
        multiline: False
        focus:root.focus
        disabled: root.disabled
        # cursor_color: 1, 170/255, 23/255, 1
        # foreground_color: 1, 170/255, 23/255, 1
        background_color: 0,0,0,0
        padding: 15
        font_name: root.font_name
        font_size: root.font_size
    MDIcon:
        icon: root.icon
        pos_hint: {'right': .9, 'center_y': .5}
        theme_text_color: "Custom"
        text_color: root.icon_color


""")


class MyTextField(MDTextField):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MyInput(MDFloatLayout):
    hint_text = StringProperty()
    text = StringProperty()
    icon = StringProperty()
    focus = BooleanProperty()
    disabled = BooleanProperty()
    font_name = StringProperty("Roboto")
    font_size = NumericProperty("16sp")
    text_color = ColorProperty()
    icon_color = ColorProperty()
    cursor_color = text_color
    background_color = ColorProperty()