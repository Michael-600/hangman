"""


Hangman using a two classes
1 for logic and 1 for GUI
Widgets:root window,labels,Buttons, canvas
"""

import tkinter as tk
import random


# utility functions: they can be used below

def string_minus(s1, s2):
    """
    s1,s2:strings
    return:string consisting of letters in s1 not in s2
    """
    diff = ""
    for char in s1:
        if not (char in s2):
            diff = diff + char
    return diff


def make_display_word(word, letters_used):
    """
    word:str
    letters_used:str
    return:str - word, with underscores for letters
    that have not been used yet
    e.g. "_ o _ o m o _ t _ _ _" (from locomotive)
    """
    display_word = ""
    for char in word:
        if char in letters_used:
            display_word += char + "  "
        else:
            display_word += "__  "
    return display_word


# logic part of program
class Hangman_game:
    """
    This class exports the following information
    body_parts_remaining
    body_parts_used
    message_string
   

    Meaning: this is the only information about the Game which will 
    be called in the GUI. The GUI will also call Game methods too.

    make_display()
    start()
    update_game()
    
    """

    def __init__(self):

        vocab = open("words.txt")
        self.words = list(vocab)

        self.start()

    def __str__(self):
        return self.make_display()

    def start(self):
        self.body_parts_remaining = ["head", "neck", "left arm", "right arm", "trunk",
                                     "left leg", "right leg"]
        self.body_parts_used = []

        self.word = random.choice(self.words).strip()

        self.letters_used = ""
        self.message_string = "Guess a letter with the keyboard"  # to report a win or loss to player

    def make_display(self):
        """
        creates word (a string) with underscores for missing letters
        """
        return make_display_word(self.word, self.letters_used)

    def update_game(self, char):
        """
        char:str - a single letter
        result:update letters_used, redisplay word.
        If char not in word update body_parts_used,
        redisplay body.    
        Inform player if character has been used already
        This will be called by the GUI
        """
        if char in self.letters_used:  # char already typed
            pass  # LEAVE THIS: it means do nothing.
        elif len(self.body_parts_remaining) == 0 or not string_minus(self.word, self.letters_used):
            # no letters missing in word (see string_minus, above) OR
            # no body parts remaining
            # then we're done. Do nothing
            pass
        else:  # char is new
            self.letters_used += char
            if not (char in self.word):
                self.update_body_parts()
            # check_for_end_game
            if len(self.body_parts_remaining) == 0:
                self.lose_game()
            elif not string_minus(self.word, self.letters_used):
                self.win_game()
            else:
                pass

    def update_body_parts(self):
        if not (self.body_parts_remaining == []):
            self.body_parts_used.append(self.body_parts_remaining.pop(0))

    def win_game(self):
        """
        result:notify player of win
        """
        self.message_string = "you won!!"

    def lose_game(self):
        """
        result:notify player of loss
        """
        self.message_string = "you lost!!\n original word was\n " + \
                              str(make_display_word(self.word, self.word))


# graphical layer
class Hangman_gui:
    """
    The graphical display part of
    Hangman
    """

    def __init__(self):
        """
        hangman_gui attributes:
        a root window, two labels, a button
        and a canvas
        """
        # create a Hangman_game object
        self.game = Hangman_game()

        tkroot = tk.Tk()
        tkroot.bind('<KeyPress>', self.onkeypress)  # Make window
        # react to keystroke

        # title and geometry
        tkroot.title("Hangman Game")
        tkroot.geometry("640x420+5+5")
        tkroot.config(bg="lightblue")

        tkroot.focus()

        self.label1 = tk.Label(tkroot, bg="lightblue")
        self.label2 = tk.Label(tkroot, bg="lightblue")

        self.label1.pack(expand=True, fill='both')
        self.label1.focus()

        self.label2.pack(expand=True, fill='both')
        self.label2.focus()

        button = tk.Button(tkroot, text="Restart")
        button.config(command=self.restart)
        button.config(bg="green")
        button.pack()

        self.canvas = tk.Canvas(tkroot, borderwidth=4, relief="raised", bg="white")
        self.canvas.config(height=300, width=200, bg="grey")
        self.canvas.pack()

        self.start()
        tkroot.mainloop()

    def start(self):
        self.game.start()
        self.canvas.delete("all")
        height = 400
        width = 400
        self.canvas.create_line(width / 40, height / 8, width / 4, height / 8)
        self.canvas.create_line(width / 40, height / 8, width / 40, height / 1.6)
        self.canvas.create_line(0, height / 1.6, width / 20, height / 1.6)
        self.canvas.create_line(width / 40, height / 5, width / 4, height / 8)
        self.canvas.create_line(width / 4, height / 8, width / 4, height / 5.7)

        self.label1.config(text=self.game.make_display())
        self.label2.config(text=self.game.message_string)

    def draw_body(self):

        t = []
        for body_parts in self.game.body_parts_used:
            t.append(body_parts)
            if len(t) == 1:
                self.canvas.create_oval(70, 70, 130, 130, fill="red")
            elif len(t) == 2:
                self.canvas.create_oval(70, 70, 130, 130, fill="red")
                self.canvas.create_line(100, 130, 100, 150)
            elif len(t) == 3:
                self.canvas.create_oval(70, 70, 130, 130, fill="red")
                self.canvas.create_line(100, 130, 100, 150)
                self.canvas.create_line(130, 170, 150, 120)
            elif len(t) == 4:
                self.canvas.create_oval(70, 70, 130, 130, fill="red")
                self.canvas.create_line(100, 130, 100, 150)
                self.canvas.create_line(130, 170, 150, 120)
                self.canvas.create_line(70, 170, 50, 120)
            elif len(t) == 5:
                self.canvas.create_oval(70, 70, 130, 130, fill="red")
                self.canvas.create_line(100, 130, 100, 150)
                self.canvas.create_line(130, 170, 150, 120)
                self.canvas.create_line(70, 170, 50, 120)
                self.canvas.create_rectangle(70, 150, 130, 220, fill="orange")
            elif len(t) == 6:
                self.canvas.create_oval(70, 70, 130, 130, fill="red")
                self.canvas.create_line(100, 130, 100, 150)
                self.canvas.create_line(130, 170, 150, 120)
                self.canvas.create_line(70, 170, 50, 120)
                self.canvas.create_rectangle(70, 150, 130, 220, fill="orange")
                self.canvas.create_line(110, 220, 145, 275)
            elif len(t) == 7:
                self.canvas.create_oval(70, 70, 130, 130, fill="red")
                self.canvas.create_line(100, 130, 100, 150)
                self.canvas.create_line(130, 170, 150, 120)
                self.canvas.create_line(70, 170, 50, 120)
                self.canvas.create_rectangle(70, 150, 130, 220, fill="orange")
                self.canvas.create_line(110, 220, 145, 275)
                self.canvas.create_line(90, 220, 55, 275)

    # event handler (triggered by hitting a key on the keyboard)
    def onkeypress(self, event):
        ch = event.char
        self.game.update_game(ch)
        self.draw_body()
        self.label1.config(text=self.game.make_display())
        self.label2.config(text=self.game.message_string)

    def restart(self):
        self.start()  # reset the GUI (which resets the game)
        self.label1.config(text=self.game.make_display())
        self.label2.config(text="New Game\n Guess a letter with the keyboard")


Hangman_gui()
