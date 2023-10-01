from widgets.notify import Notify


notify = Notify()


def alert(message: str, method:str, error=True):
    """
    The alert function is a wrapper for the notify.notify function, which
    sends an alert to the user. The alert function takes in
    a string message and sends it as an error notification.

    :param message: str: Pass in a string to the function
    :return: None
    :doc-author: Trelent
    """

    notify.notify(message=message, method=method, error=error)


def inform(message: str, method:str, error=True):
    """
    The inform function is a wrapper for the notify.notify function, which sends a notification to the user's desktop.
        The inform function takes one argument: message, which is the string that will be displayed in the notification.

    :param message: str: Pass a message to the function
    :return: A notification
    :doc-author: Trelent
    """

    notify.notify(message=message, method=method, error=error)
