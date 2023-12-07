from scipy.io import wavfile
import scipy.io
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
wav_fname = os.path.join(script_directory, 'clap.wav')

samplerate, data = wavfile.read(wav_fname)
print(f"number of channels = {data.shape[len(data.shape) - 1]}")
print(f"sample rate = {samplerate}Hz")
length = data.shape[0] / samplerate
print(f"length = {length}s")
