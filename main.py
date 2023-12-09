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
import scipy
from pydub import AudioSegment

from clean import clean_audio_data

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
    windowWidth = max(submitWidth, fileInfoWidth, photoWidth, 300)
    root.geometry('%dx%d' % (windowWidth, layerHeight * 4 + imageLabel.winfo_height()))

# Upload Sound File
def UploadAction(event=None):
    global filename
    filedir = filedialog.askopenfilename()
    if 'filedir' in locals():
        if (filedir.lower().endswith('.wav') or filedir.lower().endswith('.mp3')):
            global wav
            wav = clean_audio_data(filedir)
            print('Selected:', filedir)
            filename = os.path.basename(filedir).split('/')[-1]
            fileNameLabel.config(text=filename)
            UpdatePicture(0)
            UpdateWindow()
            # Import Images

            img1 = ImageTk.PhotoImage(Image.open(img_buf1))
            del filedir
        else:
            fileNameLabel.config(text = "Invalid File Format")
            UpdatePicture(0)
            UpdateWindow()

# Update Checkbox Pictures
def UpdatePicture(x):
    if ((fileNameLabel.cget("text") != "No File Selected") and ((fileNameLabel.cget("text") != "Invalid File Format"))):
        match x:
            case 0:
                imageLabel.config(image="", text="Select A Data Visualization Option")
            case 1:
                imageLabel.config(image=img1, text="")
            case 2:
                imageLabel.config(image="", text="Medium Frequencies")
            case 3:
                imageLabel.config(image="", text="High Frequencies")
            case 4:
                imageLabel.config(image="", text="All Frequencies")
            case 5:
                imageLabel.config(image="", text="Waveform")
            case 6:
                imageLabel.config(image="", text="?????????")
            case _:
                imageLabel.config(image="", text="i literally have no idea how you got here")
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

# Graph Display
imageLabel = Label(root, image = "", text = "No File Given")
imageLabel.place(x=0, y=layerHeight*4)

# Picture Options
lowrB = Button(root, text='Low Freq' , width = 10, command=lambda: UpdatePicture(1))
mediB = Button(root, text='Mid Freq' , width = 10, command=lambda: UpdatePicture(2))
highB = Button(root, text='High Freq', width = 10, command=lambda: UpdatePicture(3))
lowrB.place(anchor=N, relx=.15, y=layerHeight*2)
mediB.place(anchor=N, relx=.50, y=layerHeight*2)
highB.place(anchor=N, relx=.85, y=layerHeight*2)
totlB = Button(root, text='All Freq' , width = 10, command=lambda: UpdatePicture(4))
waveB = Button(root, text='Waveform' , width = 10, command=lambda: UpdatePicture(5))
ppppB = Button(root, text='?????????', width = 10, command=lambda: UpdatePicture(6))
totlB.place(anchor=N, relx=.15, y=layerHeight*3)
waveB.place(anchor=N, relx=.50, y=layerHeight*3)
ppppB.place(anchor=N, relx=.85, y=layerHeight*3)

# Start Window
root.title("Audio Frequencies")
UpdateWindow()
root.resizable(False, False)
root.mainloop()

# Close Generated Images
img_buf1.close()

if os.path.exists("converted_audio.wav"):
    os.remove("converted_audio.wav")
if os.path.exists("mono_audio.wav"):
    os.remove("mono_audio.wav")
if 'wav' in globals():
    if os.path.exists(wav):
        os.remove(wav)