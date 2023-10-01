import importlib

from kivy.uix.screenmanager import ScreenManager, CardTransition
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.factory import Factory
from kivy.properties import ListProperty
from utils.androidly import Storage
from widgets.button import RoundButton, FlatButton
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder

from widgets.popup import Pop


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the initial state of an object, and it's where you put most of your initialization code.
        The __init__ function can accept arguments, which are passed on to the constructor by Python when an instance is created.

        :param self: Represent the instance of the class
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: The modalview object, which is the loading_dialog
        :doc-author: Trelent
        """

        super().__init__(**kwargs)

        spinner = Factory.MDSpinner(line_width=dp(2.5), color="white")
        self.loading_dialog = ModalView(
            auto_dismiss=False,
            background="",
            background_color=[1, 1, 1, 0],  # same as 0,0,0,0
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            on_pre_open=lambda x: setattr(spinner, "active", True),
            on_dismiss=lambda x: setattr(spinner, "active", False)
        )
        self.loading_dialog.add_widget(spinner)

    path = Storage().get_storage_directory()
    # print(path)
    screens_store = JsonStore("models/screens.json")
    screen_history = ListProperty()

    def load_spinner(self):
        """
        The load_spinner function is used to open the loading dialog.

        :param self: Access the attributes and methods of the class
        :return: A loading dialog
        :doc-author: Trelent
        """
        self.loading_dialog.open()

    def close_spinner(self, obj):
        """
        The close_spinner function closes the loading dialog box.

        :param self: Make the function a method of the class
        :param obj: Pass in the object that is being used to call the function
        :return: Nothing
        :doc-author: Trelent
        """

        self.loading_dialog.dismiss()

    def load_kv_file(self, kv_file_name):
        """
        The load_kv_file function loads a kv file into the current context.

        :param self: Represent the instance of the class
        :param kv_file_name: Load the kv file
        :return: A builder object
        :doc-author: Umar
        """
        Builder.load_file(f"{kv_file_name}")

    added_screens = set()

    def change_screen(self, screen_name: str, hot_reload_active: bool):
        """
        The change_screen function is used to change the current screen of the app.
        It takes in a string argument that represents the name of the screen you want to switch to.
        The function checks if there is already an instance of that screen in memory, and if not, it will load it from file and add it into memory before switching screens.

        :param self: Represent the instance of the object itself
        :param screen_name: str: Pass in the name of the screen that you want to change to

        :param hot_reload_active: bool: Determine if the kv file should be loaded or not.

        Since the hot reload feature loads the kv files passed to its configuration, this is to avoid multiple loading of kv files that can lead to unwanted behavior in the UI.

        :return: The screen name
        """

        # checks if the screen already exists in the screen manager
        # if the screen is not yet in the screen manager,
        # if screen_name not in self.added_screens:
        if not self.has_screen(screen_name):

            # gets the key screen name from the screens.json file
            getter = self.screens_store.get(screen_name)

            if hot_reload_active == False:
                Builder.load_file(f"{getter['kv']}")

            # executes the value of the import key in the screens.json file
            exec(getter['import'])

            # # calls the screen class to get the instance of it
            screen_object = eval(getter["object"])

            # automatically sets the screen name using the arg that passed in set_current
            screen_object.name = screen_name

            # finally adds the screen to the screen-manager
            self.add_widget(screen_object)

            self.added_screens.add(screen_name)

        # if the screens is already in the screen manager,
        # changes the screen to the specified screen
        self.current = screen_name

        # if not __from_goback:
        if self.current != screen_name:
            self.screen_history.append({"name": screen_name, })

        # self.loading_dialog.dismiss()

    def goback(self):
        """
        The goback function is used to go back to the previous screen.
            It checks if there are more than one screens in the history, and then it
            checks if the last screen in history is not equal to current screen. If both
            conditions are true, it pops out that last element from history and changes
            the current screen with that popped element.

        :param self: Make the function work with a class
        :return: The previous screen
        :doc-author: Trelent
        """

        if len(self.screen_history) > 1:
            prev_screen = self.screen_history[-1]
            if prev_screen["name"] != self.current:
                self.screen_history.pop()
                self.change_screen(
                    prev_screen["name"], hot_reload_active=False)

    def logout(self):
        self.change_screen("login")
