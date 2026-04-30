from hybrid_chat import *
from hybrid_file import *
import tkinter as tk
#add a timer system later


win = tk.Tk()
win.title("gui")
#button click event

title = tk.Label(win,text='encrypted transfer system')
title.grid(column=0,row=0)

#text input box &send button
text = tk.StringVar() #textbox
textbox = tk.Entry(win, width=25,textvariable=text)
textbox.grid(column=0,row=1)
textbox.focus()


def send_button():#send button
    send.configure(text=" x ")


send = tk.Button(win,text=" send > ",command=send_button)
send.grid(column=1,row=1)

win.mainloop()