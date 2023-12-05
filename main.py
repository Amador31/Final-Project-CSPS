import os
import random
import tkinter
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from itertools import count, cycle
import numpy as np

root = Tk()


def UploadAction(event=None):
  global filename
  filename = filedialog.askopenfilename()
  print('Selected:', filename)
  labelText = filename
  fileNameLabel.config(text=filename)


importButton = Button(root, text='Open', command=UploadAction)
importButton.place(x=0, y=0)

fileNameLabel = Label(root, text="No File Selected")
fileNameLabel.place(
    x=importButton.winfo_width() + 2,
    y=(importButton.winfo_height() - fileNameLabel.winfo_height()) / 2)

root.update()

fileNameLabel.place(
    x=importButton.winfo_width() + 2,
    y=(importButton.winfo_height() - fileNameLabel.winfo_height()) / 2)

root.geometry('%dx%d+%d+%d' % (100, 100, 0, 0))
root.mainloop()
