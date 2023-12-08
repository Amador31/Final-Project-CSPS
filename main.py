import os
import random
import tkinter
from tkinter import *
from tkinter import filedialog
from itertools import count, cycle
import numpy as np

import io
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

plt.figure()
plt.plot([1, 2])

img_buf1 = io.BytesIO()
plt.savefig(img_buf1, format='png')

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

plt.figure()
plt.plot([3, 1])

img_buf2 = io.BytesIO()
plt.savefig(img_buf2, format='png')

root = Tk()

def updateWindow():
    root.update()
    submitWidth = importButton.winfo_width() + fileNameLabel.winfo_width() + 4
    fileInfoWidth = fileInfoLabel.winfo_width() + 4
    photoWidth = imageLabel.winfo_width()
    windowWidth = max(submitWidth, fileInfoWidth, photoWidth)
    root.geometry('%dx%d' % (windowWidth, layerHeight * 4 + imageLabel.winfo_height()))

def UploadAction(event=None):
    global filename
    filedir = filedialog.askopenfilename()
    print('Selected:', filedir)
    filename = os.path.basename(filedir).split('/')[-1]
    fileNameLabel.config(text=filename)
    updateWindow()

def UpdatePicture():
    print("lowrCheck = " + str(lowrCheck.get()))
    print("mediCheck = " + str(mediCheck.get()))
    print("highCheck = " + str(highCheck.get()))
    imageLabel.config(image=img2)
    updateWindow()

importButton = Button(root, text='Open', command=UploadAction)
importButton.place(x=0, y=0)

fileNameLabel = Label(root, text="No File Selected")
fileNameLabel.place(x=0, y=0)

root.update()

layerHeight = importButton.winfo_height()
textHeight = (importButton.winfo_height() - fileNameLabel.winfo_height()) / 2

fileNameLabel.place(x=importButton.winfo_width() + 2, y=textHeight)

fileInfoLabel = Label(root, text="Time: 0; High Amp: 0; RT60 Dif: 0")
fileInfoLabel.place(x=2, y=layerHeight+textHeight)

checkLabelLowr = Label(root, text="Low Freq")
checkLabelLowr.place(anchor=N, relx=.25, y=layerHeight*2+textHeight)
checkLabelMedi = Label(root, text="Medium Freq")
checkLabelMedi.place(anchor=N, relx=.50, y=layerHeight*2+textHeight)
checkLabelHigh = Label(root, text="High Freq")
checkLabelHigh.place(anchor=N, relx=.75, y=layerHeight*2+textHeight)

lowrCheck = IntVar()
mediCheck = IntVar()
highCheck = IntVar()
lowrC = Checkbutton(root, variable = lowrCheck, onvalue = 1, offvalue = 0, command=UpdatePicture)
mediC = Checkbutton(root, variable = mediCheck, onvalue = 1, offvalue = 0, command=UpdatePicture)
highC = Checkbutton(root, variable = highCheck, onvalue = 1, offvalue = 0, command=UpdatePicture)
lowrC.place(anchor=N, relx=.25, y=layerHeight*3)
mediC.place(anchor=N, relx=.50, y=layerHeight*3)
highC.place(anchor=N, relx=.75, y=layerHeight*3)

img1 = ImageTk.PhotoImage(Image.open(img_buf1))
img2 = ImageTk.PhotoImage(Image.open(img_buf2))

imageLabel = Label(root, image = img1)
imageLabel.place(x=0, y=layerHeight*4)

updateWindow()
root.resizable(False, False)
root.mainloop()

img_buf1.close()
img_buf2.close()