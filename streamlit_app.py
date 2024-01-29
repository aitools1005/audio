import streamlit as st
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

                    # Read the WAV file
                    rate, arr = np.array([]), np.array([])
                    with open(file_path_str, "rb") as op:
                        rate = op.getframerate()
                        nsample = op.getnframes()
                        stream = op.readframes(-1)
                        t = int(nsample / rate)
                        arr = np.frombuffer(stream, dtype=np.int16)

                    # Create a subplot for each audio file
                    fig.add_trace(go.Scatter(x=np.linspace(0, t, nsample), y=arr, mode='lines',
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
