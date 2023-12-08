from scipy.io import wavfile
import numpy as np
from pydub import AudioSegment
import os

def convert_to_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file)

    # Ensure the output file has a .wav extension
    if not output_file.lower().endswith('.wav'):
        output_file = os.path.splitext(output_file)[0] + '.wav'

    # Export the audio as a WAV file
    audio.export(output_file, format='wav')
    print(f"Conversion successful. Saved as {output_file}")

    return output_file

def clean_audio_data(file_path):
    if not file_path.lower().endswith('.wav'):
        file_path = convert_to_wav(file_path, 'converted_audio.wav')

    samplerate, data = wavfile.read(file_path)

    # Handle missing values (replace NaN or Inf with zeros)
    data = np.nan_to_num(data)

    # Check and handle inconsistencies in channel format
    if data.ndim == 1:
        # If the data is mono, convert it to stereo by duplicating the channel
        data = np.column_stack((data, data))
        channels = 2
    elif data.shape[1] > 2:
        # If there are more than 2 channels, take the first two channels
        data = data[:, :2]
        channels = data.shape[1]

    # Remove metadata (if any)
    # You can use the pydub library to create a new AudioSegment without metadata
    audio = AudioSegment(data.tobytes(), frame_rate=samplerate, sample_width=data.dtype.itemsize, channels=channels)

    # Now 'data' contains the cleaned audio data

    # Optionally, you can save the cleaned data to a new WAV file
    cleaned_file_path = 'cleaned_audio.wav'
    wavfile.write(cleaned_file_path, samplerate, data)

    return cleaned_file_path

input_file_path = 'clap.mp3'
cleaned_file_path = clean_audio_data(input_file_path)