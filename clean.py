from scipy.io import wavfile
import numpy as np
from pydub import AudioSegment
import os
import matplotlib as plt

def clean_audio_data(file_path):
    def convert_to_wav(input_file, output_file):
        audio = AudioSegment.from_file(input_file)

        # Export the audio as a WAV file
        audio.export(output_file, format='wav')
        print(f"Conversion successful. Saved as {output_file}")

        return output_file

    def convert_to_mono(input_file, output_file):
        audio = AudioSegment.from_file(file_path)

        # Set channels to 1
        mono_audio = audio.set_channels(1)

        # Export the audio as a WAV file
        mono_audio.export(output_file, format='wav')
        print(f"Conversion successful. Saved as {output_file}")

        return output_file

    # Convert to WAV file if not already WAV
    if not file_path.lower().endswith('.wav'):
        file_path = convert_to_wav(file_path, 'converted_audio.wav')

    # Extract only samplerate and data
    samplerate, data = wavfile.read(file_path)

    # Check if channel format is more than 1, convert to mono
    if data.ndim > 1:
        file_path = convert_to_mono(file_path, 'mono_audio.wav')
        # Update with new sample rate and data values for mono
        samplerate, data = wavfile.read(file_path)

    # Handles missing values
    data = np.nan_to_num(data)

    newDirectory = os.path.dirname(os.path.abspath(__file__))
    # Create file path for new data
    cleaned_file_path = newDirectory + '\\cleaned_audio.wav'

    # Rewriting file ensures no meta data
    wavfile.write(cleaned_file_path, samplerate, data)
    print(f"Cleaning successful. Saved as {cleaned_file_path}")

    return cleaned_file_path