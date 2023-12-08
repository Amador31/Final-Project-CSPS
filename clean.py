from scipy.io import wavfile
import numpy as np
from pydub import AudioSegment
import os

def clean_audio_data(file_path):
    def convert_to_wav(input_file, output_file):
        audio = AudioSegment.from_file(input_file)

        # Ensure the output file has a .wav extension
        if not output_file.lower().endswith('.wav'):
            output_file = os.path.splitext(output_file)[0] + '.wav'

        # Export the audio as a WAV file
        audio.export(output_file, format='wav')
        print(f"Conversion successful. Saved as {output_file}")

        return output_file

    # Convert to WAV file if not already WAV
    if not file_path.lower().endswith('.wav'):
        file_path = convert_to_wav(file_path, 'converted_audio.wav')

    # Extract only samplerate and data
    samplerate, data = wavfile.read(file_path)

    # Handles missing values
    data = np.nan_to_num(data)

    # Check if channel format is mono, convert to stereo
    if data.ndim == 1:
        # Convert to stereo by duplicating the mono channel
        data = np.column_stack((data, data))
    # Check if channel format is more than 2, convert to stereo
    elif data.shape[1] > 2:
        # Take the first two channels from multichannel recording
        data = data[:, :2]

    # Create file path for new data
    cleaned_file_path = 'cleaned_audio.wav'
    # Rewriting file ensures no meta data
    wavfile.write(cleaned_file_path, samplerate, data)
    print(f"Cleaning successful. Saved as {cleaned_file_path}")

    return cleaned_file_path

input_file_path = 'clap.mp3'
cleaned_file_path = clean_audio_data(input_file_path)