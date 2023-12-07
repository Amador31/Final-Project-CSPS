import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def createWavForm():
  # Displays wave form of the file
  file_path = '/content/sample_data/New_Recording_68.wav'

  # Read the .wav file
  sample_rate, data = wavfile.read(file_path)

  # Duration of the file
  duration = len(data) / sample_rate

  # Create time array for x-axis
  time = np.linspace(0., duration, len(data))

  # Plot the waveform
  plt.figure(figsize=(10, 4))
  plt.plot(time, data, lw=0.5)
  plt.title('Waveform of {}'.format(file_path))
  plt.xlabel('Time (s)')
  plt.ylabel('Amplitude')
  plt.show()
