from Game import Game, GameError
from abc import ABC, abstractmethod
from itertools import product
from tkinter import Button, Tk, Frame, X, Toplevel, StringVar

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
        
        self.__root = root
    
    def _help_callback(self):
        pass
    
    def _play_callback(self):
        self.__game = Game()
        game_win = Toplevel(self.__root)
        game_win.title("Game")
        frame = Frame(game_win)
        frame.grid(row=0, column=0)
        
        Button(game_win, text="Dismiss", command=game_win.destroy).grid(row=1, column=0)
        
        self.__buttons = [[None]*3 for _ in range(3)]
        
        for row, col in product(range(3), range(3)):
            b = StringVar()
            b.set(self.__game.at(row+1, col+1))
            
            cmd = lambda r=row, c=col: self.__play_and_refresh(r,c)
            
            Button(frame, textvariable=b, command=cmd).grid(row=row, column=col)
            self.__buttons[row][col] = b
    
    def __play_and_refresh(self, row, col):
        self.__game.play(row+1, col+1)
        
        for row, col in product(range(3), range(3)):
            text = self.__game.at(row+1, col+1)
            self.__buttons[row][col].set(text)
    
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

