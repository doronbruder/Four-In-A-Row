from ex12.gui import *
from tkinter import *
from ex12.hello_window import Hello_window


def main_loop():
    """this function manage the run of the game main loop"""
    hello_root = Tk()
    hello = Hello_window(hello_root)
    hello_root.mainloop()
    main_root = Tk()
    new_game = Gui(main_root, hello.get_users())
    if hello.get_users():
        main_root.mainloop()
    while new_game.WANT_PLAY:
        hello_root = Tk()
        hello = Hello_window(hello_root)
        hello_root.mainloop()
        main_root = Tk()
        new_game = Gui(main_root, hello.get_users())
        if hello.get_users():
            main_root.mainloop()


if __name__ == '__main__':
    main_loop()


