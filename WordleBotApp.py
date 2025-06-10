import wordle
import tkinter as tk
from tkinter import messagebox
#from tkinter import ttk
import ttkbootstrap as ttk
import sys
import os

# This is the actual application
if __name__ == "__main__":
    
    def resource_path(relative_path):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    if sys.platform == 'darwin':
        try:
            from Foundation import NSBundle
            bundle = NSBundle.mainBundle()
            if bundle:
                info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
                if info and "CFBundleIconFile" not in info:
                    icon_path = os.path.abspath(resource_path("weirdIcon.icns"))
                    info["CFBundleIconFile"] = icon_path
        except ImportError:
            pass
    # create the basic window
    try:
        window.destroy()
    except:
        pass
    window = ttk.Window(themename = 'darkly')
    window.title('Wordle Solver')
    window.geometry('500x350')
    # window.columnconfigure(0,minsize=100)
    # window.columnconfigure(1,weight=1,minsize=100)
    
    # define and start a new game
    class Game:
        def __init__(self):
            self.recomNextWord = tk.StringVar()
            self.numLeft = tk.IntVar()
            self.reset()
            self.solutionNo = 0

        def resetSolNo(self):
            self.solutionNo = 0
        
        def incrementSolNo(self):
            self.solutionNo += 1

        def increment(self):
            self.currentRound += 1
        
        def setWords(self,i,val):
            self.inputWords[i]=val
        
        def setColors(self,i,val):
            self.inputColors[i]=val
        
        def reset(self):
            self.currentRound = 0
            self.solutionNo = 0
            self.inputWords = ['','','','','','']
            self.inputColors=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
            self.recomNextWord.set('tarse')
            self.numLeft.set(2315)
    

    game = Game()

    def printNextWord():
        if game.currentRound==0:
            nextGuessWord=(2315,sorted(wordle.entropyDictMain.items(), key=lambda x: -x[1])[:50])
        else:
            nextGuessWord=wordle.nextGuess(wordle.stringToChars(game.inputWords[0]),game.inputColors[0],
                                           wordle.stringToChars(game.inputWords[1]),game.inputColors[1],
                                           wordle.stringToChars(game.inputWords[2]),game.inputColors[2],
                                           wordle.stringToChars(game.inputWords[3]),game.inputColors[3],
                                           wordle.stringToChars(game.inputWords[4]),game.inputColors[4],
                                           wordle.stringToChars(game.inputWords[5]),game.inputColors[5])
                
        if game.currentRound>=5 or nextGuessWord[0]==0:
            game.recomNextWord.set('Game over')
            game.numLeft.set(0)
        elif game.inputColors[game.currentRound-1]==[2,2,2,2,2]:
            game.recomNextWord.set('You win!')
            game.numLeft.set(0)
        elif nextGuessWord[0]==1:
            game.recomNextWord.set(nextGuessWord[1])
            game.numLeft.set(nextGuessWord[0])
        else:
            solNo=game.solutionNo
            game.recomNextWord.set(nextGuessWord[1][solNo][0])
            game.numLeft.set(nextGuessWord[0])
            game.incrementSolNo()
            
    # title
    title_label = ttk.Label(master = window, text = 'Guesses so far:', font='Calibri 18 bold')
    title_label.grid(row = 0, column = 0, pady = 2)

    def addToKnowledge(event=None):
        i=game.currentRound
        newEntry=entry_vals[i].get()
        if wordle.stringToChars(newEntry) in wordle.wordleAcceptedGuesses:
            game.setWords(i,newEntry)
        else:
            messagebox.showerror('Error', 'Word not in Database')
            return None
            
        game.increment()
        game.resetSolNo()
        printNextWord()
        if i<5:
            addEntry()



    def addEntry():
        i=game.currentRound
        entries[i].grid(row = i+1, column = 0, pady = 2)
        for j in range(5):
            buttons[i][j].grid(row=i+1, column=2+j, pady=2,padx=2)
        enterButton.grid(row = i+1, column = 7, pady = 2)
        output_recom.grid(row = 3+i, column = 0, pady = 2)
        output_label.grid(row = 3+i, column = 1, pady = 2)
        num_rem.grid(row = 4+i, column = 0, pady = 2)
        num_label.grid(row = 4+i, column = 1, pady = 2)

    entry_vals = [tk.StringVar() for _ in range(6)]
    entries = [ttk.Entry(master = window,textvariable = i,width=10) for i in entry_vals]
    enterButton = ttk.Button(master = window, text='Enter', command=addToKnowledge)

    window.bind_all('<Return>', addToKnowledge)

    entries[0].grid(row = 1, column = 0, pady = 2)
    enterButton.grid(row = 1, column = 7, pady = 2)

    def changecolor(round, num):
        if game.inputColors[round][num]==0:
            buttons[round][num].config(style='warning.TButton')
            game.inputColors[round][num]=1
        elif game.inputColors[round][num]==1:
            buttons[round][num].config(style='success.TButton')
            game.inputColors[round][num]=2
        elif game.inputColors[round][num]==2:
            buttons[round][num].config(style='secondary.TButton')
            game.inputColors[round][num]=0

    buttons = [[None for _ in range(5)] for _ in range(6)]
    for rou in range(6):
        for j in range(5):
            buttons[rou][j] = ttk.Button(window, width=1, style='secondary.TButton', command=lambda y=rou,x=j: changecolor(y,x))
            buttons[rou][j].configure(takefocus=0)
    for j in range(5):
        buttons[0][j].grid(row=1, column=2+j, pady=2,padx=2)

    output_recom = ttk.Label(master = window, text = 'My recommendation: ', font='Calibri 18 bold')
    output_label = ttk.Label(master = window, font='Calibri 18 bold', textvariable = game.recomNextWord)
    num_rem = ttk.Label(master = window, text = 'Remaining words: ', font='Calibri 18 bold')
    num_label = ttk.Label(master = window, font='Calibri 18 bold', textvariable = game.numLeft)
    
    output_recom.grid(row = 3, column = 0, pady = 2)
    output_label.grid(row = 3, column = 1, pady = 2, columnspan = 6)
    num_rem.grid(row = 4, column = 0, pady = 2)
    num_label.grid(row = 4, column = 1, pady = 2, columnspan = 6)

    def resetAll():
        # Reset entry fields
        for var in entry_vals:
            var.set('')
        for rou in range(6):
            for j in range(5):
                if rou!=0:
                    buttons[rou][j].config(style='secondary.TButton')
                    entries[rou].grid_forget()
                    buttons[rou][j].grid_forget()
                else:
                    entries[0].grid(row = 1, column = 0, pady = 2)
                    enterButton.grid(row = 1, column = 7, pady = 2)
                    buttons[rou][j].config(style='secondary.TButton')
                    buttons[rou][j].grid(row=rou+1, column=2+j, pady=2,padx=2)

        game.reset()

        # output_recom.grid(row = 3, column = 0, pady = 2)
        # output_label.grid(row = 3, column = 1, pady = 2, columnspan = 6)
        # num_rem.grid(row = 4, column = 0, pady = 2)
        # num_label.grid(row = 4, column = 1, pady = 2, columnspan = 6)

    newWordButton = ttk.Button(master = window, text='Next', command=printNextWord)
    newWordButton.grid(row=11, column=1, pady=10,columnspan = 6)

    reset_btn = ttk.Button(window, text='Reset', command=resetAll)
    reset_btn.grid(row=11, column=0, pady=10)

    window.mainloop()