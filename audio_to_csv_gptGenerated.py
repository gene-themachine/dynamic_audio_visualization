from pydub import AudioSegment
import numpy as np
import pandas as pd

# Function to calculate decibels
def calculate_decibels(samples):
    samples = samples / np.max(np.abs(samples), axis=0)
    decibels = 20 * np.log10(np.abs(samples) + 1e-10)
    return decibels

# Function to process audio file and save average decibels per second to a CSV file
def process_audio_file(input_file_path, output_file_path):
    audio = AudioSegment.from_file(input_file_path)
    audio = audio.set_channels(1)
    duration_seconds = int(len(audio) / 1000)
    decibel_data = []

    for second in range(duration_seconds):
        start_ms = second * 1000
        end_ms = start_ms + 1000
        chunk = audio[start_ms:end_ms]
        samples = np.array(chunk.get_array_of_samples())
        decibels = calculate_decibels(samples)
        average_decibels = np.mean(decibels)
        decibel_data.append([second, average_decibels])

    df = pd.DataFrame(decibel_data, columns=['Second', 'Average Decibels (dB)'])
    df.to_csv(output_file_path, index=False)


files_to_process = [
    {"input": "path_to_fein_short.mp3", "output": "average_decibels_per_second_fein_short.csv"},
    {"input": "path_to_lose_yourself_short.mp3", "output": "average_decibels_per_second_lose_yourself_short.csv"},
    {"input": "path_to_travis_fein.mp3", "output": "average_decibels_per_second_travis_fein.csv"}
]

for file in files_to_process:
    process_audio_file(file["input"], file["output"])
