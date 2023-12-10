import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import io
import os
from PIL import Image, ImageTk

def fig2img(fig):
  buf = io.BytesIO()
  fig.savefig(buf)
  buf.seek(0)
  img = Image.open(buf)
  return img

def createWavForm(file_path):
  plt.rcParams["figure.figsize"] = [7.50, 3.50]
  plt.rcParams["figure.autolayout"] = True
  plt.figure()

  # Read the .wav file
  sample_rate, data = wavfile.read(file_path)

  # Duration of the file
  duration = len(data) / sample_rate

  # Create time array for x-axis
  time = np.linspace(0., duration, len(data))

  # Plot the waveform
  plt.plot(time, data, lw=0.5)
  plt.xlabel('Time (s)')
  plt.ylabel('Amplitude')

  fig = plt.gcf()
  plt.close('all')
  return ImageTk.PhotoImage(fig2img(fig)), duration

def plotting(filepath, freq_target_range, printSpec, printAll):
  plt.rcParams["figure.figsize"] = [7.50, 3.50]
  plt.rcParams["figure.autolayout"] = True
  plt.figure()

  sample_rate, data = wavfile.read(filepath)
  spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
  plt.clf()

  duration = len(data) / sample_rate

  def debugg(fstring):
    print(fstring)

  def find_target_frequency(freqs):
    for x in freqs:
      if x > freq_target_range:
        break
    return x

  def frequency_check():
    # debugg(f'freqs {freqs[:10]}]')
    target_frequency = find_target_frequency(freqs)
    # debugg(f'target_frequency {target_frequency}')
    index_of_frequency = np.where(freqs == target_frequency)[0][0]
    # debugg(f'index_of_frequency {index_of_frequency}')

    data_for_frequency = spectrum[index_of_frequency]
    # debugg(f'data_for_frequency {data_for_frequency[:10]}')

    data_in_db_fun = 10 * np.log10(data_for_frequency)
    return data_in_db_fun

  plt.figure()
  if (printAll == True):
    for i in range(3):
      freq_target_range = 2800 * (i ** 2) - (1900 * i) + 100
      data_in_db = frequency_check()
      match i:
        case 0:
          plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#de3163', label='Low')
        case 1:
          plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#00aaff', label='Med')
        case 2:
          plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#800080', label='High')
    plt.legend()
  else:
    data_in_db = frequency_check()
    match freq_target_range:
      case 100:
        plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#de3163')
      case 1000:
        plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#00aaff')
      case 7500:
        plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#800080')
      case _:
        plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')

  plt.xlabel('Time (s)')
  plt.ylabel('Power (dB)')

  index_of_max = np.argmax(data_in_db)

  value_of_max = data_in_db[index_of_max]

  sliced_array = data_in_db[index_of_max:]

  value_of_max_less_5 = value_of_max - 5

  def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

  value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)

  index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)

  value_of_max_less_25 = value_of_max - 25

  value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)

  index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)

  rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]

  rt60 = 3 * rt20

  #plt.grid()
  #plt.show()

  if (printSpec == True):
    plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
  elif (printAll == False):
    plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')
    plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')
    plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

  fig = plt.gcf()
  plt.close('all')
  return ImageTk.PhotoImage(fig2img(fig)), round(abs(rt60), 2), round(value_of_max, 2)