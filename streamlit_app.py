import streamlit as st
import ffmpeg
from pydub import AudioSegment
import numpy as np
import os
import plotly.graph_objects as go

# Function to open file dialog and get the selected file paths
def choose_files():
    file_paths = st.file_uploader("Select Audio Files", type=["wav", "mp3", "opus"], accept_multiple_files=True)
    return file_paths

# Function to convert Opus file to WAV format
def convert_opus_to_wav(opus_path, wav_path):
    audio = AudioSegment.from_file(opus_path, format="opus")
    audio.export(wav_path, format="wav")

# Function to read audio data from file
def read_audio_file(file_path):
    probe = ffmpeg.probe(file_path, v="error_return", select_streams="a:0", show_entries="format=duration")
    duration = float(probe["format"]["duration"])
    audio = AudioSegment.from_file(file_path)
    rate = audio.frame_rate
    arr = np.array(audio.get_array_of_samples())
    return rate, arr, duration

# Main Streamlit app
def main():
    st.title("Audio Waveform Plotter")

    # Get the file paths using the choose_files function
    file_paths = choose_files()

    # Check if the user selected any files
    if file_paths:
        if isinstance(file_paths, list):
            num_files = len(file_paths)
            fig = go.Figure()

            # Plot the amplitude waveforms of each selected audio file
            for i, uploaded_file in enumerate(file_paths, 1):
                try:
                    file_path_str = f"file_{i}.wav"  # Temporary file name
                    print(f"Processing File {i}: {file_path_str}")

                    # Save the content of the UploadedFile to a temporary file
                    with open(file_path_str, "wb") as f:
                        f.write(uploaded_file.read())

                    # Check if the file is Opus and convert it to WAV if necessary
                    if uploaded_file.type == "audio/opus":
                        opus_path = file_path_str
                        file_path_str = f"file_{i}_converted.wav"
                        convert_opus_to_wav(opus_path, file_path_str)

                    # Read the audio file
                    rate, arr, duration = read_audio_file(file_path_str)

                    # Create a subplot for each audio file
                    fig.add_trace(go.Scatter(x=np.linspace(0, duration, len(arr)), y=arr, mode='lines',
                                             name=f'Audio Waveform - {os.path.basename(file_path_str)}'))

                except Exception as e:
                    st.warning(f"Error processing file {i}: {file_path_str}")
                    st.warning(f"Error details: {str(e)}")

                finally:
                    # Delete the temporary file
                    os.remove(file_path_str)

            fig.update_layout(
                title="Audio Waveforms",
                xaxis_title="Time (s)",
                yaxis_title="Amplitude",
                height=400 * num_files
            )

            st.plotly_chart(fig)

        else:
            st.warning("Invalid file paths. Please upload audio files.")

if __name__ == "__main__":
    main()
