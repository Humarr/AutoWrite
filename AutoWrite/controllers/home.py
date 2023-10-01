import keyboard
import pyautogui
from kivymd.uix.screen import MDScreen
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import CommonElevationBehavior, RectangularRippleBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import StringProperty, ColorProperty, BooleanProperty, NumericProperty
from kivymd.uix.list import OneLineListItem
# from widgets.notify import alert
from utils.notification import alert
from widgets.notify import Notify
from widgets.popup import Pop


class CustomButton(RectangularRippleBehavior, ButtonBehavior, CommonElevationBehavior, MDFloatLayout):
    """
    A custom button widget that combines multiple behaviors and layouts from the Kivy and KivyMD libraries.

    Attributes:
        text (str): The text displayed on the button.
        icon (str): The path to the icon displayed on the button.
        bg_color (tuple): The background color of the button in RGBA format.
        text_color (tuple): The text color of the button in RGBA format.
        icon_color (tuple): The icon color of the button in RGBA format.
        ripple_scale (int): The scale of the ripple effect.
    """
    text = StringProperty()
    icon = StringProperty()
    bg_color = ColorProperty()
    text_color = ColorProperty()
    icon_color = ColorProperty()
    ripple_scale = NumericProperty(2)


class Content(ButtonBehavior, MDFloatLayout, CommonElevationBehavior):
    """
    A custom widget that combines several behaviors and layouts to create a button-like element with elevation and ripple effects.

    :ivar divider: A field that is set to None.
    :ivar shortcut: A string property that represents the keyboard shortcut.
    :ivar shortcut_info: A string property that represents information about the shortcut.
    :ivar started: A boolean property that indicates if the content has been started.
    """
    divider = None
    shortcut = StringProperty()
    shortcut_info = StringProperty()
    # started = BooleanProperty()


class AddNewShortcut(MDFloatLayout):
    def write_new_hotkey_to_memory(self, hotkey_info, hotkey_combination):
        with open('hotkeys.txt', 'a') as hotkey_file:
            hotkey_file.write(f"{hotkey_info} {hotkey_combination}\n")


class Home(MDScreen):

    pass
    def on_hotkey(self, message) -> bool:
        """
        The on_hotkey function is called when a hotkey is pressed.

        :param self: Represent the instance of the class
        :param message: Pass the string to be typed
        :return: True if the message was typed successfully
        :doc-author: Trelent
        """

        if not isinstance(message, str):
            alert("Message must be a string.")
            # raise ValueError("Message must be a string.")
        if any(command in message for command in ["rm -rf", "shutdown", "format c:"]):
            alert("Message contains malicious commands.")
            # raise ValueError("Message contains malicious commands.")
        try:
            # Type with 0.1-second pause in between each key.
            pyautogui.write(message, interval=0.1)
            return True
        except Exception:
            return False

    def add_hot_key_and_wait(self, hotkey_combination, wait_keyword, message, button_state):
        """
        The add_hot_key_and_wait function is used to add a hotkey and wait keyword.
            The function takes in the following parameters:
                - hotkey_combination: A string representing the combination of keys that will be pressed to trigger an event.
                    For example, &quot;ctrl+alt+a&quot; would trigger an event when ctrl + alt + a are all pressed at once.
                    This parameter must be passed as a string or else it will raise an error.

        :param self: Make the function a method of the class
        :param hotkey_combination: Set the hotkey combination that will be used to trigger the message
        :param wait_keyword: Remove the hotkey from the system
        :param message: Pass the message to the on_hotkey function
        :param button_state: Determine whether the hotkey should be added or removed
        :return: The hotkey_id and wait_keyword
        :doc-author: Trelent
        """

        if button_state == "start":
            # if not keyboard.is_valid_hotkey(hotkey_combination):
            #     raise ValueError("Invalid hotkey combination")

            # if not keyboard.is_valid_hotkey(wait_keyword):
            #     raise ValueError("Invalid wait keyword")

            # self.on_hotkey(message=message)

            hotkey_id = keyboard.add_hotkey(
                hotkey_combination, lambda x: self.on_hotkey(message))

            self.write_new_hotkey_to_memory(hotkey_id, hotkey_combination)

            keyboard.wait(wait_keyword)


        elif button_state == "stop":
            self.remove_key_hot_key_from_memory(hotkey_id=hotkey_id, hotkey=hotkey_combination)

    def remove_key_hot_key_from_memory(self, wait_keyword, hotkey_id):
        """
        The remove_key function removes a hotkey from the keyboard.
            It takes two arguments: wait_keyword and hotkey_id.
            The wait_keyword argument is used to determine when the function should be called,
                while the hotkey_id argument is used to identify which key should be removed.

        :param self: Represent the instance of the class
        :param wait_keyword: Define the keyword that will be used to wait for a hotkey
        :param hotkey_id: Identify which hotkey to remove
        :return: The hotkey_id
        :doc-author: Trelent
        """

        with open('keys.txt', 'r') as hotkey_file:
            hotkeys = hotkey_file.readlines()

            for hotkey in hotkeys:
                if hotkey.split()[0] == wait_keyword:
                    keyboard.remove_hotkey(hotkey_id)
                    hotkeys.remove(hotkey)


    def write_new_hotkey_to_memory(self, hotkey_id, hotkey_combination):
        with open('keys.txt', 'a') as hotkey_file:
            hotkey_file.write(f"{hotkey_id} {hotkey_combination}\n")

    def write_new_hotkey_to_db(self, hotkey_info, hotkey_combination):
        with open('hotkeys.txt', 'a') as hotkey_file:
            hotkey_file.write(f"{hotkey_info} {hotkey_combination}\n")
