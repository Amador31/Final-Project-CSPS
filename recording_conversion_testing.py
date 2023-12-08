from scipy.io import wavfile
import scipy.io
import os
from pydub import AudioSegment

def convert_to_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file)

    # Ensure the output file has a .wav extension
    if not output_file.lower().endswith('.wav'):
        output_file = os.path.splitext(output_file)[0] + '.wav'

    # Export the audio as a WAV file
    audio.export(output_file, format='wav')
    print(f"Conversion successful. Saved as {output_file}")


script_directory = os.path.dirname(os.path.abspath(__file__))
wav_fname = os.path.join(script_directory, 'clap.mp3')

script_directory = os.path.dirname(os.path.abspath(__file__))
wav_fname2 = os.path.join(script_directory, 'clap_test.wav')

convert_to_wav(wav_fname, wav_fname2)

samplerate, data = wavfile.read(wav_fname2)

print(f"number of channels = {data.shape[len(data.shape) - 1]}")
print(f"sample rate = {samplerate}Hz")
length = data.shape[0] / samplerate
print(f"length = {length}s")
