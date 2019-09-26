from tkinter import *
import os


class Hello_window:
    """
    this class responsible for the hello window.
    the class include all the relevant method to that part of the game
    like: create buttons, post background and e.c
    """
    COLUMNS_DIC = {0: "HUMAN VS HUMAN", 1: "HUMAN VS PC", 2: "PC VS HUMAN", 3: "PC VS PC"}

    def __init__(self, root):
        self.__dir_path = os.path.dirname(os.path.realpath(__file__))
        self.__img = PhotoImage(file=self.__dir_path+'/start_img.png')
        self.__root = root
        self.__can = self.create_canvas()
        self.__label_img = self.post_background(self.__img)
        self.__users = []
        self.__button_list = self.create_buttons()

    def create_buttons(self):
        """this function create all the 4 chosen buttons of the beginning
         and post them to the hello window screen"""
        button_list = []
        for i in range(4):
             button_list.append(Button(self.__root, text=self.COLUMNS_DIC[i],
                                       width=25, command=self._button_event(i)))
             button_list[i].grid(row=i + 1, column=3, ipady=20)
        return button_list

    def _button_event(self, num):
        """this function is the command function of all the buttons.
        the function changes the users list in accordance to the button that
        pressed"""
        def button_pressed():
            if num == 0:
                self.__users = [False, False]
            elif num == 1:
                self.__users = [False, True]
            elif num == 2:
                self.__users = [True, False]
            elif num == 3:
                self.__users = [True, True]
            self.__root.destroy()
        return button_pressed

    def create_canvas(self):
        """this function create the main canvas of the hello window and post
        him to the window"""
        canvas_width = 650
        canvas_height = 500
        can = Canvas(self.__root, width=canvas_width, height=canvas_height)
        can.grid(row=0, column=0, columnspan=7, rowspan=6, padx=5, pady=5)
        return can

    def post_background(self, img):
        """this function post image to the canvas"""
        self.__can.create_image(10, 5, anchor='nw', image=img)
        return img

    def get_users(self):
        """this function get the users list to other classes"""
        return self.__users
