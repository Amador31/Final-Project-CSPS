import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram

# Load the .wav file
sample_rate, data = wavfile.read("New_Recording_68.wav")

# Compute the spectrogram using FFT
frequencies, times, spectrum = spectrogram(data, fs=sample_rate, nperseg=1024)

# Select a frequency
def find_target_frequency(freqs, target):
    for x in freqs:
        if x > target:
            break
    return x

def frequency_check(freq_range):
    # Identify a frequency to check
    global target_frequency
    target_frequency = find_target_frequency(frequencies, freq_range)
    index_of_frequency = np.where(frequencies == target_frequency)[0][0]

    # Find sound data for a particular frequency
    data_for_frequency = spectrum[index_of_frequency]

    # Change a digital signal to values in decibels
    data_in_db_fun = 10 * np.log10(data_for_frequency)

    return data_in_db_fun

low = 100
mid = 1000
high = 10000

# Call the function to get the data in decibels
data_in_db = frequency_check(mid)

# Duration of the file
duration = len(data) / sample_rate

# Create time array for x-axis
time = np.linspace(0., duration, len(data))
# Create a time array for x-axis
t = np.arange(len(data_in_db))
# t = np.arange(duration)
print(len(data_in_db))
print(data_in_db)
print(len(t))
print(t)
print(time)
print(len(time))

# Plot the decibels over time
plt.figure(2)
plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')

# Mark the index of the maximum value
index_of_max = np.argmax(data_in_db)
value_of_max = data_in_db[index_of_max]
plt.plot(t[index_of_max], value_of_max, 'go', label='Max Value')

# Slice the array from the max value
sliced_array = data_in_db[index_of_max:]

#find a nearest value of less 5db
def find_nearest_value(array, value):
  array = np.asarray(array)
  idx = (np.abs(array - value)).argmin()
  return array[idx]

# Find the index and value of less 5dB
value_of_max_less_5 = value_of_max - 5
value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)[0][0]
plt.plot(t[index_of_max_less_5], value_of_max_less_5, 'yo', label='5dB Less')

# Find the index and value of less 25dB
value_of_max_less_25 = value_of_max - 25
value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)[0][0]
plt.plot(t[index_of_max_less_25], value_of_max_less_25, 'ro', label='25dB Less')

# Calculate RT20 and RT60
rt20 = t[index_of_max_less_5] - t[index_of_max_less_25]
rt60 = 3 * rt20


plt.xlabel('Time (s)')
plt.ylabel('Power (dB)')
plt.title('Decibels over Time')
plt.grid()
plt.legend()
plt.show()

print(f'The RT60 reverb time at freq {int(target_frequency)} Hz is {round(abs(rt60), 2)} seconds')

print(len(t))
print(len(data))