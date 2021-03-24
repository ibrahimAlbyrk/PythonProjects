from brain import *
from win10toast import ToastNotifier


def Main():
    LoadName()
    while 1:
        player_input = playerInput(mic=False)
        print(player_input)
        if player_input.strip() == "":
            continue
        Detects(player_input)


if __name__ == '__main__':
    notifier = ToastNotifier()
    notifier.show_toast("Assistant Quinn", "Merhaba!", "Images/assistantIcon.ico", 2, False)
    Main()
