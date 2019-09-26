from tkinter import *
from ex12.game import Game
from ex12.ai import AI
import os


class Gui:
    """
    this class create object from type gui that include:
    root - the current tkinter root
    users - list of the current players (AI / HUMAN)
    the class manage all the operate of the game and responsible to interface
    with the user
    """
    COLUMNS_DIC = {0: "column 1", 1: "column 2", 2: "column 3", 3: "column 4",
                    4: "column 5", 5: "column 6", 6: "column 7"}

    BALL_SIZE  =   70
    WIDTH_SPACE = 30
    START_POINT = 25

    def __init__(self, root, users):
        """This function is a constructor for graphic game object"""
        self.__dir_path = os.path.dirname(os.path.realpath(__file__))
        self.__img1 = PhotoImage(file=self.__dir_path+'/EAsportslogo.png')
        self.__img2 = PhotoImage(file=self.__dir_path+'/_board.png')
        self.__cur_game = Game()
        self.__root = root
        if users:
            self.__ai = users
        else:
            self.WANT_PLAY = False
            return
        self.__can = self.create_canvas()
        self.__turns = []
        self.__cur_player = 0
        self.__label_img = self.post_background(self.__img1)
        self.__label_img = self.__root.after(3000, self.post_background, self.__img2)
        self.__buttons = []
        self.__root.after(3000, self.create_buttons)
        self.__ai_list = self.create_AI()
        self.__root.after(3050, self.whos_begin)
        self.WANT_PLAY = False
        self.__nonvalids = []




    def whos_begin(self):
        """the function checks whos begin. if AI is the first player to play
        so the function give a command to the game to start automatically"""
        if self.__ai:
            if self.__ai[0] is True:
                self.AI_move()

    def create_AI(self):
        """this function responsible for the create of the AI objects"""
        if not self.__ai:
            return
        ai_list = []
        if self.__ai[0] is True:
            ai_list.append(AI(self.__cur_game, 1))
        else:
            ai_list.append(None)
        if self.__ai[1] is True:
            ai_list.append(AI(self.__cur_game, 2))
        else:
            ai_list.append(None)
        return ai_list

    def create_canvas(self):
        """this function create the main canvas of the game screen and post
        him to the window"""
        canvas_width = 650
        canvas_height = 500
        can = Canvas(self.__root, width=canvas_width, height=canvas_height)
        can.grid(row=0, column=0, columnspan=7, rowspan=6, padx=5, pady=5)
        return can

    def create_buttons(self):
        """this function create all the game buttons
         and post them to the game screen"""
        for column in range(7):
            self.__buttons.append(Button(self.__root, text=self.COLUMNS_DIC[column], command=self._column_event(column)))
            self.__buttons[column].grid(row=7, column=column, sticky='N')

    def post_background(self, img):
        """this function post image to the canva"""
        self.__can.create_image(10, 5, anchor='nw', image=img)
        return img

    def _column_event(self, column):
        """this function is the command function of all the buttons.
        the function responsible to update the Game object and create
        oval in accordance to the column that pressed"""
        def column_pressed():
            row = self.look_for_row(column)
            self.__cur_game.make_move(column)
            if self.__cur_game.get_player_at(row, column) == 1:
                self.__turns.append(self.__can.create_oval(self.START_POINT + column * 90, row * 80 + 10,
                                                           self.START_POINT + column * 90 + self.BALL_SIZE,
                                                           row * 80 + self.BALL_SIZE + 10, fill="BLUE"))
            else:
                self.__turns.append(self.__can.create_oval(self.START_POINT + column * 90, row * 80 + 10,
                                                           self.START_POINT + column * 90 + self.BALL_SIZE,
                                                           row * 80 + self.BALL_SIZE + 10, fill="RED"))
            self.look_for_winner()
            self.__cur_player = (self.__cur_player+1) % 2
            if self.__ai[self.__cur_player]:
                for button in self.__buttons:
                    button.config(state='disabled', bg="WHITE")
                self.__root.after(500, self.AI_move)
        return column_pressed

    def look_for_winner(self):
        """this function checks with the Game object if someone won the game
        and bold the winning ovals in the screen"""
        win_cor = self.__cur_game.win_cor()
        if win_cor:
            for cor in win_cor:
                column, row = cor[0], cor[1]
                self.__turns.append(self.__can.create_oval(self.START_POINT + column * 90, row * 80 + 10,
                                                           self.START_POINT + column * 90 + self.BALL_SIZE,
                                                           row * 80 + self.BALL_SIZE + 10, fill="WHITE"))
            self.win_func(self.__cur_game.get_player_at(row, column))
        elif self.__cur_game.get_winner() == 0:
            self.win_func(0)

    def look_for_row(self, column):
        """this function get a column and look for empty row in
        that specific column to update"""
        for row in range(1, self.__cur_game.ROWS + 1):
            if self.__cur_game.get_player_at(self.__cur_game.ROWS - row, column) is None:
                if row == self.__cur_game.ROWS:
                    self.__nonvalids.append(column)
                    self.__buttons[column].config(state='disabled', bg="WHITE")
                return self.__cur_game.ROWS - row

    def AI_move(self):
        """this function manage the AI moves. the function look for col
        from the ai player and update the game"""
        if self.__cur_game.get_winner() is None:
            if self.__ai_list:
                column = self.__ai_list[self.__cur_player].find_legal_move()
            # row = self.look_for_row(column)
            if column is None:
                return
            column = self.__ai_list[self.__cur_player].find_legal_move()
            self._column_event(column)()
            if self.__ai[0] is False or self.__ai[1] is False:
                for column, button in enumerate(self.__buttons):
                    if column not in self.__nonvalids and\
                            self.__cur_game.get_winner() is None:
                        button.config(state='normal', bg="WHITE")

    def play_again(self):
        """the play again command function"""
        self.__root.destroy()
        self.WANT_PLAY = True

    def exit(self):
        """the exit command function"""
        self.__root.destroy()
        self.WANT_PLAY = False
        quit()

    def win_func(self, winner):
        """this function manage the win (finish) window. the function
        present to the user two optional buttons: play again or exit"""
        self.__ai_list = []
        for button in self.__buttons:
            button.config(state='disabled', bg="WHITE")
        window = Toplevel(self.__root)
        can = Canvas(window, width=435, height=600)
        can.grid(row=0, column=0, columnspan=7, rowspan=6, padx=5, pady=5)
        self.img = PhotoImage(file='ex12/winner_img.png')
        self.label = can.create_image(0, 0, anchor=NW, image=self.img)
        winner_img = self.status_num(window, winner)
        can.create_image(0, 470, anchor=NW, image=winner_img)
        can.photo = winner_img
        can.config(scrollregion=can.bbox(ALL))
        play_again = Button(window, text='PLAY AGAIN', command=self.play_again)
        play_again.grid(row=4, column=0, sticky='N', ipadx=10, ipady=20)
        exit = Button(window, text='I WANT TO GET OUT!', command=self.exit)
        exit.grid(row=4, column=6, sticky='N', ipadx=10, ipady=20)

    def status_num(self, window, winner):
        """this function load the correct img to the winning window in
        accordance to the winner identity"""
        if winner == 1:
            window.wm_title("Player 1 won!")
            winner_img = PhotoImage(file='ex12/player_one_won.png')
        if winner    == 2:
            window.wm_title("Player 2 won!")
            winner_img = PhotoImage(file='ex12/player_two_won.png')
        if winner == 0:
            window.wm_title("It was a draw!")
            winner_img = PhotoImage(file='ex12/draw.png')
        return winner_img



