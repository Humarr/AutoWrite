import asyncio
import sqlite3
import asynckivy
import keyboard
import pyautogui
from app.app import WindowManager
from kivymd.app import MDApp
# from kivymd.app import MDApp
from PIL import ImageGrab
from kivy.utils import platform, QueryDict, rgba
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
# from kaki.app import App
from controllers.home import AddNewShortcut, Content
from utils.androidly import Storage
from utils.notification import alert, inform
from widgets.popup import Pop

# TODO: You may know an easier way to get the size of a computer display.
resolution = ImageGrab.grab().size

platforms = ['linux', 'macosx', 'win']

if platform in platforms:
    Window.size = (350, 690)
    Window.top = 0
    Window.left = resolution[0] - Window.width + 440
# Window.size = (350, 600)


"""
The `Autowrite` class is a part of a Python application that uses the Kivy framework for creating a GUI. It contains methods and fields related to managing screens, handling keyboard events, and interacting with a SQLite database.

Example Usage:
```python
app = Autowrite()
app.build()
app.on_start()
app.display_shortcut_popup()
app.close()
app.add_hot_key_and_wait("ctrl+alt+a", "Hello World", "start")
app.remove_hot_key_from_memory("esc", hotkey_id)
app.write_new_hotkey_to_memory(hotkey_id, "ctrl+alt+a")
app.write_new_hotkey_to_db("Shortcut Info", "ctrl+alt+a")
app.get_screen("home", "hotkey_container")
```

Main functionalities:
- Manages screens and navigation using the `WindowManager` class.
- Handles keyboard events and binds them to specific actions.
- Interacts with a SQLite database to create tables and retrieve data.
- Displays custom popup windows for adding new shortcuts.
- Writes and reads hotkeys to/from a text file and a database.

Methods:
- `build()`: Initializes the application and returns the screen manager.
- `on_start()`: Initializes variables and sets up data before the application runs.
- `create_tables()`: Creates a table in the SQLite database if it doesn't exist.
- `get_shortcuts()`: Retrieves shortcuts from the database and adds them to the home screen.
- `initialize_after_build()`: Binds keyboard events after the window has been built.
- `handle_keyboard_input()`: Handles keyboard input and performs actions based on the pressed key.
- `display_shortcut_popup()`: Creates and displays a custom popup window for adding new shortcuts.
- `close()`: Closes the popup window.
- `on_hotkey()`: Handles the typing of a message when a hotkey is pressed.
- `add_hot_key_and_wait()`: Adds a hotkey and waits for a specific keyword to trigger an event.
- `remove_hot_key_from_memory()`: Removes a hotkey from the system.
- `write_new_hotkey_to_memory()`: Writes a new hotkey to a text file.
- `write_new_hotkey_to_db()`: Writes a new hotkey to the database.
- `get_screen()`: Retrieves a specific widget from a screen.

Fields:
- `DEBUG`: A constant to enable Hot Reload.
- `CLASSES`: A dictionary mapping screen names to their corresponding controller classes.
- `AUTORELOADER_PATHS`: A list of paths to monitor for changes and trigger hot reload.
- `KV_FILES`: A list of paths to the .kv files to load.
- `path`: The storage directory path.
- `screens_store`: A JSON store for storing screen data.
- `colors`: A dictionary-like object for storing color values.
- `fonts`: A dictionary-like object for storing font values.
- `images`: A dictionary-like object for storing image values.

Author: Trelent
"""


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('autowrite.db')
        self.cursor = self.conn.cursor()

    def create_tables(self):
        sql = 'CREATE TABLE IF NOT EXISTS hotkeys (key INTEGER PRIMARY KEY AUTOINCREMENT, message VARCHAR(2000) NOT NULL, shortcut VARCHAR(255) NOT NULL)'
        self.cursor.execute(sql)

    def get_shortcuts(self):
        sql = 'SELECT * FROM hotkeys'
        self.cursor.execute(sql)
        return self.cursor.fetchall()


class Autowrite(MDApp):
    DEBUG = 1  # To enable Hot Reload
    CLASSES = {
        "Home": "controllers.home.Home"
    }

    AUTORELOADER_PATHS = [
        (".", {"recursive": True}),
    ]

    KV_FILES = [
        "views/home.kv"
    ]

    path = Storage().get_storage_directory()

    screens_store = JsonStore(f"Models/screens.json")

    colors = QueryDict()
    colors.primary = rgba("#143EBE")
    colors.bg = rgba("#1f1f1f")
    colors.secondary = rgba("#492b7c")
    colors.warning = rgba("#c83416")
    colors.danger = rgba("#b90000")
    colors.success = rgba("#0F7A60")
    colors.white = rgba("#FFFFFF")
    colors.yellow = rgba("#f6d912")
    colors.orange = rgba("#ed8a0a")
    colors.black = rgba("#333333")
    colors.grey = rgba("#f1f1f1")

    fonts = QueryDict()
    fonts.bold = 'assets/fonts/Poppins-Bold.ttf'
    fonts.regular = 'assets/fonts/Poppins-Regular.ttf'
    fonts.medium = 'assets/fonts/Poppins-Medium.ttf'

    fonts.size = QueryDict()
    fonts.size.heading = sp(30)
    fonts.size.icon = sp(30)
    fonts.size.h1 = sp(24)
    fonts.size.h2 = sp(22)
    fonts.size.h3 = sp(18)
    fonts.size.h4 = sp(16)
    fonts.size.h5 = sp(14)
    fonts.size.h6 = sp(12)
    fonts.size.h7 = sp(5)
    fonts.size.bar = sp(3)

    images = QueryDict()

    Builder.load_file("imports.kv")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wm = WindowManager()

        self.path = Storage().get_storage_directory()
        self.screens_store = JsonStore(f"Models/screens.json")
        # self.shortcut_popup = None

        self.database_manager = DatabaseManager()
        # self.conn = sqlite3.connect("autowrite.db")
        self.conn = self.database_manager.conn
        self.cursor = self.conn.cursor()

        # Define a dictionary to map modifier keys to their angle bracket representations
        self.modifier_mapping = {
            'ctrl': '<ctrl>',
            'shift': '<shift>',
            'alt': '<alt>',
            'cmd': '<cmd>',
            'caps_lock': '<caps_lock>',
            'num_lock': '<num_lock>',
            'scroll_lock': '<scroll_lock>',
        }

    def build(self):

        # Create a list of all screen, loop through it and add it to the screenmanager
        # and return the screenmanager.
        self.theme_cls.primary_hue = "A100"
        self.theme_cls.material_style = "M3"
        # self.theme_cls.theme_style = "Dark"
        # self.wm = WindowManager()

        self.wm.change_screen(screen_name="home", hot_reload_active=False)

        return self.wm

    def on_start(self):
        """
        The on_start function is called when the application starts.
        It is used to initialize variables and set up any data needed before the
        application runs.

        :param self: Represent the instance of the class
        :return: The screen manager
        :doc-author: Trelent
        """

        Clock.schedule_once(lambda ev: self.initialize_after_build(ev), 1)

        self.create_tables()
        self.get_shortcuts()

    def create_tables(self):
        self.database_manager.create_tables()

    def get_shortcuts(self):
        hotkeys = self.database_manager.get_shortcuts()
        for hotkey in hotkeys:
            hotkey_info = hotkey[1]
            hotkey_combination = hotkey[2]

            self.wm.get_screen('home').ids['hotkey_container'].add_widget(

                Content(shortcut=hotkey_combination, shortcut_info=hotkey_info))

    def initialize_after_build(self, ev):
        """
        The initialize_after_build function is a workaround for the fact that Kivy does not allow you to bind keyboard events until after the window has been built.

        :param self: Refer to the current instance of a class
        :param ev: Get the keycode of the pressed key
        :return: The handle_keyboard_input function
        :doc-author: Trelent
        """

        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.handle_keyboard_input)

    def handle_keyboard_input(self, window, key, *largs):
        """
        The handle_keyboard_input function is a function that handles the keyboard input.
            It takes in three arguments: window, key and *largs. The first argument is the window
            which is an instance of Window class from kivy.core.window module, it represents a
            single display surface (screen/monitor). The second argument 'key' represents the keycode
            of the pressed key on your keyboard and *largs are any other arguments passed to this function.

        :param self: Represent the instance of the class
        :param window: Get the window object
        :param key: Check if the key pressed is 27
        :param *largs: Pass a variable number of arguments to the function
        :return: True when the key is 27
        :doc-author: Umar Saadu
        """

        if key == 27:

            print(self.wm.current)
            # if(self.wm.current == 'login'):
            #     self.pop_exit()
            # if(self.wm.current == 'home'):
            #     self.wm.pop_exit()
            # else:
            #     self.wm.goback()
            # return True

    def display_shortcut_popup(self):
        """
        Create and display a custom popup window with the title "Add new shortcut" and a custom content class called `AddNewShortcut`.

        Example Usage:
        ```python
        app = Autowrite()
        app.add_shortcut_popup()
        ```

        Inputs: None

        Flow:
        1. Create an instance of the `Pop` class, which is a custom dialog window.
        2. Initialize the `Pop` instance with a title of "Add new shortcut" and a content class of `AddNewShortcut`.
        3. Open the `Pop` instance, displaying the custom popup window.

        Outputs: None
        """
        if not hasattr(self, "shortcut_popup"):
            self.shortcut_popup = Pop(
                title="Add new shortcut", type="custom", content_cls=AddNewShortcut(),)
        self.shortcut_popup.open()

    def close(self):
        """
        The close function is used to close the popup window when the user clicks on a button.


        :param self: Represent the instance of the class
        :return: Nothing
        :doc-author: Trelent
        """

        if self.shortcut_popup is not None:
            self.shortcut_popup.dismiss()

    def on_hotkey(self, message) -> bool:
        """
        The on_hotkey function is called when the user presses a hotkey.

        :param self: Represent the instance of the class
        :param message: Pass the string to be typed
        :return: True if the message was typed successfully, and false otherwise
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

    def add_hot_key_and_wait(self, hotkey_combination, message, button_state):
        """
        The add_hot_key_and_wait function is used to add a hotkey combination and wait for the user to press it.
            The function takes in three arguments:
                1) hotkey_combination - A string representing the key combination that will be pressed by the user.
                    This can be any valid keyboard shortcut, such as &quot;ctrl+shift+a&quot; or &quot;alt+f4&quot;.
                    For more information on what constitutes a valid keyboard shortcut, see https://github.com/boppreh/keyboard#api-reference

        :param self: Represent the instance of the class
        :param hotkey_combination: Determine which keys are pressed to activate the hotkey
        :param message: Display the message in the gui
        :param button_state: Determine whether the hotkey should be added or removed
        :return: A hotkey_id and a hotkey combination
        :doc-author: Trelent
        """

        if button_state == "stop":
            # if not keyboard.is_valid_hotkey(hotkey_combination):
            #     raise ValueError("Invalid hotkey combination")

            # if not keyboard.is_valid_hotkey(wait_keyword):
            #     raise ValueError("Invalid wait keyword")

            # self.on_hotkey(message=message)
            # global hotkey_id
            hotkey_id = keyboard.add_hotkey(
                hotkey_combination, lambda: self.on_hotkey(message))

            self.write_new_hotkey_to_memory(hotkey_id, hotkey_combination)

            inform(
                message=f"shortcut keys for {hotkey_combination} activated!", method="toast")

        elif button_state == "play":
            self.remove_hot_key_from_memory(
                hotkey_combination=hotkey_combination)

            alert(
                message=f"shortcut keys for {hotkey_combination} deactivated!", method="toast")

    def start_process(self, hotkey_combination, message, button_state):
        """
        The start_process function is the main function that starts the process of
            adding a hotkey to your system. It takes in three arguments:
                1) hotkey_combination - A string representing a keyboard combination,
                                        such as 'Ctrl+Alt+Shift+A' or 'F5'. The full list of
                                        possible combinations can be found here: https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx#virtual_key_codes

        :param self: Represent the instance of the class
        :param hotkey_combination: Set the hotkey combination that will be used to start the process
        :param message: Display a message in the text box
        :param button_state: Determine whether the button should be enabled or disabled
        :return: A list of the hotkey_combination, message and button_state
        :doc-author: Trelent
        """

        self.add_hot_key_and_wait(hotkey_combination, message, button_state)

    def remove_hot_key_from_memory(self, hotkey_combination):
        """
        The remove_hot_key_from_memory function removes a hotkey from memory.
                Args:
                    hotkey_combination (str): The combination of keys that will be removed.
                    hotkey_id (int): The id of the function that is being removed from memory.

        :param self: Represent the instance of the class
        :param hotkey_combination: Identify the hotkey that is to be removed
        :param hotkey_id: Identify the hotkey in the dictionary
        :return: A boolean value
        :doc-author: Trelent
        """

        keyboard.remove_hotkey(hotkey_combination)

    def remove_hot_key_from_db(self, hotkey_combination, widget_id):
        """
        The remove_hot_key_from_db function removes a hotkey from the database.
            Args:
                hotkey_combination (str): The combination of keys that make up the shortcut.
                widget_id (str): The id of the widget to be removed from screen.

        :param self: Refer to the current instance of a class
        :param hotkey_combination: Identify the hotkey combination that will be removed from the database
        :param widget_id: Remove the widget from the hotkey_container
        :return: Nothing
        :doc-author: Trelent
        """

        self.wm.get_screen(
            "home").ids['hotkey_container'].remove_widget(widget_id)

        sql = "DELETE FROM hotkeys WHERE shortcut = ?"
        args = (hotkey_combination,)
        self.cursor.execute(sql, args)

        self.conn.commit()
        # self.get_screen("home", 'hotkey_container').add_widget(Content(shortcut=hotkey_combination, shortcut_info=hotkey_info))

    def write_new_hotkey_to_memory(self, hotkey_id, hotkey_combination):
        """
        The write_new_hotkey_to_memory function writes a new hotkey to the keys.txt file, which is used as memory for the program.

        :param self: Represent the instance of the class
        :param hotkey_id: Identify the hotkey
        :param hotkey_combination: Write the hotkey combination to a file
        :return: None
        :doc-author: Trelent
        """

        with open('keys.txt', 'a') as hotkey_file:
            hotkey_file.write(f"{hotkey_id} {hotkey_combination}\n")

    def write_new_hotkey_to_db(self, hotkey_info, hotkey_combination):
        """
        The write_new_hotkey_to_db function takes in two arguments:
        hotkey_info and hotkey_combination. The function then writes the
        hotkey information to the database, commits it, and adds a new widget
        to the home screen's hotkeys container.

        :param self: Access the class variables and methods
        :param hotkey_info: Store the hotkey information
        :param hotkey_combination: Store the shortcut key combination in the database
        :return: None
        :doc-author: Trelent
        """

        if hotkey_combination == "" and hotkey_info == "":
            alert("Please, fill all the fields")
        else:
            sql = "INSERT INTO hotkeys (message, shortcut) VALUES(?, ?)"
            args = (hotkey_info, hotkey_combination)
            self.cursor.execute(sql, args)

            self.conn.commit()

            self.wm.get_screen("home").ids['hotkey_container'].add_widget(
                Content(shortcut=hotkey_combination, shortcut_info=hotkey_info))

            print(f"screen ids:: {self.wm.ids}")

    def edit_shortcut_combination(self, hotkey_combination, hotkey_info):
        pass

        # sql = "UPDATE hotkeys SET shortcut=?, message=? WHERE shortcut=? AND message=?"
        # args = (hotkey_info, hotkey_combination)
        # self.cursor.execute(sql, args)

        # self.conn.commit()
        #     # self.get_screen("home", 'hotkey_container').add_widget(Content(shortcut=hotkey_combination, shortcut_info=hotkey_info))
        # self.wm.get_screen("home").ids['hotkey_container'].add_widget(Content(shortcut=hotkey_combination, shortcut_info=hotkey_info))

        # print(f"screen ids:: {self.wm.ids}")

    def get_screen(self, screen_name, widget_id):
        """
        The get_screen function is a helper function that allows you to get the screen object from any widget.
            This is useful for when you want to change screens, but need access to the screen object in order
            to do so. For example, if I wanted my button on ScreenOne() (which is a class) to take me back
            home (to ScreenTwo()), I would need access to the root widget of ScreenTwo(). The way this works:

        :param self: Represent the instance of the class
        :param screen_name: Get the screen from the screenmanager
        :param widget_id: Identify the widget that is to be returned
        :return: The widget with the id 'widget_id' from the screen 'screen_name'
        :doc-author: Trelent
        """

        return self.wm.get_screen(screen_name).ids[f'{widget_id}']


if __name__ == '__main__':
    Autowrite().run()
