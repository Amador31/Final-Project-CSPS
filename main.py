import os
import random
import tkinter
from tkinter import *
from tkinter import filedialog
from itertools import count, cycle
import numpy as np

root = Tk()

def getFilename():
    print("hi")

def UploadAction(event=None):
  global filename
  filedir = filedialog.askopenfilename()
  print('Selected:', filedir)
  filename = os.path.basename(filedir).split('/')[-1]
  fileNameLabel.config(text=filename)
  root.update()
  root.geometry('%dx%d+%d+%d' % (
      max(
        importButton.winfo_width() + fileNameLabel.winfo_width() + 4,
        fileInfoLabel.winfo_width() + 4
      ),
      50,
      0,
      0))

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

time = 0
highAmp = 0
rt60Dif = 0

fileInfoLabel = Label(root, text="Time: " + str(time) + "   ; High Amp: " + str(highAmp) + "    ; RT60 Dif: " + str(rt60Dif))
fileInfoLabel.place(x=2,
    y=importButton.winfo_height())

root.update()

root.geometry('%dx%d+%d+%d' % (fileInfoLabel.winfo_width() + 4, 50, 0, 0))
root.mainloop()
