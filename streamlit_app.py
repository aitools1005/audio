import streamlit as st
import wave as w
import numpy as np
import os
import plotly.graph_objects as go

# Function to open file dialog and get the selected file paths
def choose_files():
    file_paths = st.file_uploader("Select Audio Files", type=["wav", "mp3"], accept_multiple_files=True)
    return file_paths

# Main Streamlit app
def main():
    st.title("Audio Waveform Plotter")

    # Get the file paths using the choose_files function
    file_paths = choose_files()

    # Check if the user selected any files
    if file_paths:
        num_files = len(file_paths)
        fig = go.Figure()

        # Plot the amplitude waveforms of each selected audio file
        for i, file_path in enumerate(file_paths, 1):
            op = w.open(file_path, 'rb')
            rate = op.getframerate()
            nsample = op.getnframes()
            channels = op.getnchannels()
            stream = op.readframes(-1)
            t = int(nsample / rate)
            arr = np.frombuffer(stream, dtype=np.int16)

            # Create a subplot for each audio file
            fig.add_trace(go.Scatter(x=np.linspace(0, t, nsample), y=arr, mode='lines',
                                     name=f'Audio Waveform - {os.path.basename(file_path)}'))

        fig.update_layout(
            title="Audio Waveforms",
            xaxis_title="Time (s)",
            yaxis_title="Amplitude",
            height=400 * num_files
        )

        st.plotly_chart(fig)

    else:
        st.warning("No files selected. Please upload audio files.")

if __name__ == "__main__":
    main()
