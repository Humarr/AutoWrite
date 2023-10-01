from kivymd.toast import toast
from kivy.utils import platform



# from kivymd.uix.snackbar.snackbar import MDSnackbar
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from kivy.metrics import dp
from .label import Text
# from kivymd import material_resources
from kivy.clock import Clock, mainthread
from .button import FlatButton

# def snackbar_close(*args):


class Notify:
    """
    The `Notify` class provides a way to display notifications to the user using different methods such as toast, snackbars, and dialogs.

    Example Usage:
    ```python
    notify = Notify()
    notify.notify("Hello World", method="toast")
    ```

    Main functionalities:
    - Displaying a message to the user using different notification methods.
    - Customizing the appearance of the notifications based on the method and error status.
    """

    @mainthread
    def notify(self, message, color=None, method="snack", error=False):
        """
        Displays a message to the user using the specified method.

        Args:
            message (str): The text to be displayed.
            color (str, optional): The color of the text. Defaults to None.
            method (str, optional): The type of notification to be displayed. Defaults to "snack".
            error (bool, optional): Determines whether the message is an error or not. Defaults to False.

        Returns:
            object: The snackbar object.
        """
        if method == "toast":
            toast(message)
        elif method == "snack":
            if platform == "android":
                from kivymd.uix.snackbar import MDSnackbar, MDSnackbarCloseButton
                self.snackbar = MDSnackbar(
                    Text(text=message, text_color="white"),
                    MDSnackbarCloseButton(
                        icon="close",
                        theme_icon_color="Custom",
                        icon_color="#8E353C",
                        _no_ripple_effect=True,
                        on_release=self.snackbar_close
                    ),
                    pos_hint={"center_x": 0.5},
                    size_hint_x=0.9,
                    md_bg_color="red" if error else "green"
                )
                self.snackbar.open()
            else:
                from kivymd.uix.snackbar import Snackbar
                self.snackbar = Snackbar(
                    text=message,
                    pos_hint={"center_x": 0.5},
                    size_hint_x=0.9,
                    bg_color="red" if error else "green"
                )
                self.snackbar.open()
        elif method == "dialog":
            self.dialog = MDDialog(
                text=f"[color={color}]{message}[/color]",
                buttons=[FlatButton(text="Okay", on_press=self.dialog_close)]
            )
            self.dialog.open()

    def snackbar_close(self, *args):
        """
        Closes the snackbar.
        """
        self.snackbar.dismiss()

    def dialog_close(self, obj):
        """
        Closes the dialog.
        """
        self.dialog.dismiss(force=True)
