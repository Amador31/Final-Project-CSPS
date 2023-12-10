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
from plots import plotting
from plots import createWavForm

root = Tk()

# Update Window Size
def UpdateWindow():
    root.update()
    submitWidth = importButton.winfo_width() + fileNameLabel.winfo_width() + 4
    fileInfoWidth = fileInfoLabel.winfo_width() + 4
    photoWidth = imageLabel.winfo_width()
    windowWidth = max(submitWidth, fileInfoWidth, photoWidth, 300)
    root.geometry('%dx%d' % (windowWidth, layerHeight * 5 + imageLabel.winfo_height()))

# Upload Sound File
def UploadAction(event=None):
    global filename
    filedir = filedialog.askopenfilename()
    if 'filedir' in locals():
        if (filedir.lower().endswith('.wav') or filedir.lower().endswith('.mp3')):
            global wav, time
            wav = clean_audio_data(filedir)
            print('Selected:', filedir)
            filename = os.path.basename(filedir).split('/')[-1]
            fileNameLabel.config(text=filename)
            UpdatePicture(0)
            UpdateWindow()
            titleLabel.config(text="No Image Selected")
            # Import Images
            global img1, img2, img3, img4, img5, img6
            global amp1, amp2, amp3, amp4
            global rt60_1, rt60_2, rt60_3, rt60_4
            img1, rt60_1, amp1 = plotting(wav, 100, False, False)
            img2, rt60_2, amp2 = plotting(wav, 1000, False, False)
            img3, rt60_3, amp3 = plotting(wav, 7500, False, False)
            img4, rt60_4, amp4 = plotting(wav, 1000, False, True)
            img5, time = createWavForm(wav)
            img6, rt60_5, amp5 = plotting(wav, 1000, True, False)
            del filedir
            fileInfoLabel.config(text="Time: " + str(time) + " seconds; High Amp: N/A; RT60 Dif: N/A")
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
                titleLabel.config(text="Low Frequencies (100Hz) of " + filename)
                fileInfoLabel.config(text="Time: " + str(time) + " seconds; High Amp: " + str(amp1) + " db; RT60 Dif: " + str(rt60_1) + " seconds")
            case 2:
                imageLabel.config(image=img2, text="")
                titleLabel.config(text="Medium Frequencies (1000Hz) of " + filename)
                fileInfoLabel.config(text="Time: " + str(time) + " seconds; High Amp: " + str(amp2) + " db; RT60 Dif: " + str(rt60_2) + " seconds")
            case 3:
                imageLabel.config(image=img3, text="")
                titleLabel.config(text="High Frequencies (7500Hz) of " + filename)
                fileInfoLabel.config(text="Time: " + str(time) + " seconds; High Amp: " + str(amp3) + " db; RT60 Dif: " + str(rt60_3) + " seconds")
            case 4:
                imageLabel.config(image=img4, text="")
                titleLabel.config(text="Combined Frequencies of " + filename)
                fileInfoLabel.config(text="Time: " + str(time) + " seconds; High Amp: " + str(max(amp1,amp2,amp3)) + " db; (Average) RT60 Dif: " + str(round((rt60_1 + rt60_2+ rt60_3) / 3,2)) + " seconds")
            case 5:
                imageLabel.config(image=img5, text="")
                titleLabel.config(text="Waveform of " + filename)
                fileInfoLabel.config(text="Time: " + str(time) + " seconds; High Amp: " + str(max(amp1,amp2,amp3)) + " db; (Average) RT60 Dif: " + str(round((rt60_1 + rt60_2+ rt60_3) / 3,2)) + " seconds")
            case 6:
                imageLabel.config(image=img6, text="")
                titleLabel.config(text="Spectrogram of " + filename)
                fileInfoLabel.config(text="Time: " + str(time) + " seconds; High Amp: " + str(max(amp1,amp2,amp3)) + " db; (Average) RT60 Dif: " + str(round((rt60_1 + rt60_2+ rt60_3) / 3,2)) + " seconds")
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
fileInfoLabel = Label(root, text="Time: N/A; High Amp: N/A; RT60 Dif: N/A")
fileInfoLabel.place(x=2, y=layerHeight+textHeight)

# Graph Display
titleLabel = Label(root, text = "No Image Selected")
titleLabel.place(anchor=N, relx=.5, y=layerHeight*4+textHeight)

# Graph Display
imageLabel = Label(root, image = "", text = "No File Given")
imageLabel.place(x=0, y=layerHeight*5)

# Picture Options
lowrB = Button(root, text='Low Freq' , width = 10, command=lambda: UpdatePicture(1))
mediB = Button(root, text='Mid Freq' , width = 10, command=lambda: UpdatePicture(2))
highB = Button(root, text='High Freq', width = 10, command=lambda: UpdatePicture(3))
lowrB.place(anchor=N, relx=.15, y=layerHeight*2)
mediB.place(anchor=N, relx=.50, y=layerHeight*2)
highB.place(anchor=N, relx=.85, y=layerHeight*2)
totlB = Button(root, text='All Freq' , width = 10, command=lambda: UpdatePicture(4))
waveB = Button(root, text='Waveform' , width = 10, command=lambda: UpdatePicture(5))
ppppB = Button(root, text='Spectrogram', width = 10, command=lambda: UpdatePicture(6))
totlB.place(anchor=N, relx=.15, y=layerHeight*3)
waveB.place(anchor=N, relx=.50, y=layerHeight*3)
ppppB.place(anchor=N, relx=.85, y=layerHeight*3)

# Start Window
root.title("Audio Frequencies")
UpdateWindow()
root.resizable(False, False)
root.mainloop()

# Close Generated Images
if os.path.exists("converted_audio.wav"):
    os.remove("converted_audio.wav")
if os.path.exists("mono_audio.wav"):
    os.remove("mono_audio.wav")
if 'wav' in globals():
    if os.path.exists(wav):
        os.remove(wav)