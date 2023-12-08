import os
import io
import random
import tkinter
from tkinter import *
from tkinter import filedialog
from itertools import count, cycle
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from clean import clean_audio_data
import scipy
from pydub import AudioSegment

# Temp Figures
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

plt.figure()
plt.plot([1, 2])

img_buf1 = io.BytesIO()
plt.savefig(img_buf1, format='png')

root = Tk()

# Update Window Size
def UpdateWindow():
    root.update()
    submitWidth = importButton.winfo_width() + fileNameLabel.winfo_width() + 4
    fileInfoWidth = fileInfoLabel.winfo_width() + 4
    photoWidth = imageLabel.winfo_width()
    windowWidth = max(submitWidth, fileInfoWidth, photoWidth)
    root.geometry('%dx%d' % (windowWidth, layerHeight * 4 + imageLabel.winfo_height()))

# Upload Sound File
def UploadAction(event=None):
    global filename
    filedir = filedialog.askopenfilename()
    if (filedir.lower().endswith('.wav') or filedir.lower().endswith('.mp3')):
        global wav
        wav = clean_audio_data(filedir)
        print('Selected:', filedir)
        filename = os.path.basename(filedir).split('/')[-1]
        fileNameLabel.config(text=filename)
        UpdatePicture()
        UpdateWindow()
    else:
        fileNameLabel.config(text = "Invalid File Format")
        UpdatePicture()
        UpdateWindow()

# Update Checkbox Pictures
def UpdatePicture():
    if ((fileNameLabel.cget("text") != "No File Selected") and ((fileNameLabel.cget("text") != "Invalid File Format"))):
        if (int(lowrCheck.get()) == 0 and int(mediCheck.get()) == 0 and int(highCheck.get()) == 0):
            imageLabel.config(image = "", text = "No Frequencies Being Measured")
        else:
            imageLabel.config(image = img1, text = "")
    elif (fileNameLabel.cget("text") == "Invalid File Format"):
        imageLabel.config(image = "", text = "Invalid File Format")
    else:
        imageLabel.config(image = "", text = "No File Given")
    UpdateWindow()

# Create Import Button
importButton = Button(root, text='Open', command=UploadAction)
importButton.place(x=0, y=0)

# Show File Name If Imported
fileNameLabel = Label(root, text="No File Selected")
fileNameLabel.place(x=0, y=0)
root.update()

# Calculate window variables
layerHeight = importButton.winfo_height()
textHeight = (importButton.winfo_height() - fileNameLabel.winfo_height()) / 2

# Place File Name In Correct Position
fileNameLabel.place(x=importButton.winfo_width() + 2, y=textHeight)
fileInfoLabel = Label(root, text="Time: 0; High Amp: 0; RT60 Dif: 0")
fileInfoLabel.place(x=2, y=layerHeight+textHeight)

# Checkbox Labels
checkLabelLowr = Label(root, text="Low")
checkLabelLowr.place(anchor=N, relx=.25, y=layerHeight*2+textHeight)
checkLabelMedi = Label(root, text="Mid")
checkLabelMedi.place(anchor=N, relx=.50, y=layerHeight*2+textHeight)
checkLabelHigh = Label(root, text="High")
checkLabelHigh.place(anchor=N, relx=.75, y=layerHeight*2+textHeight)

# Checkboxes
lowrCheck = IntVar()
mediCheck = IntVar()
highCheck = IntVar()
lowrC = Checkbutton(root, variable = lowrCheck, onvalue = 1, offvalue = 0, command=UpdatePicture)
mediC = Checkbutton(root, variable = mediCheck, onvalue = 1, offvalue = 0, command=UpdatePicture)
highC = Checkbutton(root, variable = highCheck, onvalue = 1, offvalue = 0, command=UpdatePicture)
lowrC.place(anchor=N, relx=.25, y=layerHeight*3)
mediC.place(anchor=N, relx=.50, y=layerHeight*3)
highC.place(anchor=N, relx=.75, y=layerHeight*3)

# Import Images
img1 = ImageTk.PhotoImage(Image.open(img_buf1))

# Graph Display
imageLabel = Label(root, image = "", text = "No File Given")
imageLabel.place(x=0, y=layerHeight*4)

# Start Window
root.title("Audio Frequencies")
UpdateWindow()
root.resizable(False, False)
root.mainloop()

# Close Generated Images
img_buf1.close()