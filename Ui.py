from Game import Game, GameError
from abc import ABC, abstractmethod
from itertools import product
from tkinter import Button, Tk, Frame, X, Toplevel, StringVar, Text, Scrollbar, LEFT, RIGHT, Y, END, N, S, W, E, Grid, Message

class Ui(ABC):

    @abstractmethod
    def run(self):
        raise NotImplementedError

class Gui(Ui):
    def __init__(self):
        root = Tk()
        root.title("Tic Tac Toe")
        frame = Frame(root)
        frame.pack()
        
        Button(
        frame,
        text='Show Help',
        command= self._help_callback).pack(fill=X)
        
        Button(
        frame,
        text='Play',
        command= self._play_callback).pack(fill=X)
            
        Button(
        frame,
        text='Quit',
        command= self._quit_callback).pack(fill=X)
        
        console = Text(frame,height=4,width=50)
        scroll = Scrollbar(frame)
        scroll.pack(side=RIGHT,fill= Y)
        console.pack(side=LEFT,fill= Y)
        
        scroll.config(command=console.yview)
        console.config(yscrollcommand=scroll.set)
        
        self.__root = root
        self.__console = console
        self.__GameInProgress = False
    
    def _help_callback(self):
        help_win = Toplevel(self.__root)
        help_text = "Blah blah"
        Message(help_win, text=help_text).pack(fill=X)
        
        Button(help_win, text="Dismiss", command=help_win.destroy).pack(fill=X)
        
    def dismiss_game(self):
        self.__GameInProgress = False
        self.__game_win.destroy()

    def _play_callback(self):
        if self.__GameInProgress:
            return
        
        self.__GameInProgress = True
        self.__finished = False
        self.__game = Game()
        game_win = Toplevel(self.__root)
        game_win.title("Game")
        frame = Frame(game_win)
        self.__game_win = game_win
        
        # Resizing
        Grid.columnconfigure(game_win,0,weight=1)
        Grid.rowconfigure(game_win,0,weight=1)
        frame.grid(row=0, column=0, sticky=N+S+W+E)
        
        Button(game_win, text="Dismiss", command=self.dismiss_game).grid(row=1, column=0, sticky=N+S+W+E)
        
        self.__buttons = [[None]*3 for _ in range(3)]
        
        for row, col in product(range(3), range(3)):
            b = StringVar()
            b.set(self.__game.at(row+1, col+1))
            
            cmd = lambda r=row, c=col: self.__play_and_refresh(r,c)
            
            Button(frame, textvariable=b, command=cmd).grid(row=row, column=col,  sticky=N+S+W+E)
            self.__buttons[row][col] = b
        
        #Resizing
        for i in range(3):
            Grid.columnconfigure(frame,i,weight=1)
            Grid.rowconfigure(frame,i,weight=1)
            
    
    def __play_and_refresh(self, row, col):
        if self.__finished:
            return
        try:
            self.__game.play(row+1, col+1)
        except GameError as e:
            self.__console.insert(END, f"{e}\n")
        
        for row, col in product(range(3), range(3)):
            text = self.__game.at(row+1, col+1)
            self.__buttons[row][col].set(text)
        
        w = self.__game.winner
        if w is not None:
            self.__finished = True
            if w is Game._DRAW:
                self.__console.insert(END, "The game was drawn\n")
            else:
                self.__console.insert(END, f"The winner was {w}\n")
    
    def _quit_callback(self):
        self.__root.quit()

    def run(self):
        self.__root.mainloop()

class Terminal(Ui):
    def __init__(self):
        self._game = Game()

    def run(self):
        while not self._game.winner:
            print(self._game)
            try:
                row = int(input("Which row? "))
                col = int(input("Which column? "))
            except ValueError:
                #Type check
                print("Non numeric input")
                continue
            if 1 <= row <= 3 and 1 <= col <= 3:
                #Range check
                try:
                    self._game.play(row,col)
                except GameError:
                    print("Cannot play at occupied space")
            else:
                print("Row and column must between 1 and 3")
        
        if self._game.winner == Game._DRAW:
            print("Its a draw")
        else:
            print(self._game)
            w = self._game.winner
            print(f"The winner was {w}")

