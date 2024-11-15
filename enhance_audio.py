import streamlit as st
import moviepy.editor as mp
from pydub import AudioSegment
import numpy as np
import scipy.signal as signal
from pydub.effects import normalize, compress_dynamic_range
import noisereduce as nr
import matplotlib.pyplot as plt
import os

# Helper function to convert numpy array to AudioSegment
def convert_to_audio_segment(audio_data, original_segment):
    audio_data = np.clip(audio_data, -32768, 32767).astype(np.int16)
    return AudioSegment(
        audio_data.tobytes(),
        frame_rate=original_segment.frame_rate,
        sample_width=original_segment.sample_width,
        channels=original_segment.channels
    )
 
# Restoration Techniques with parameters
def multi_stage_filtering(audio_data, sample_rate):
    b, a = signal.butter(3, 500 / (0.5 * sample_rate), btype='highpass')
    audio_data = signal.filtfilt(b, a, audio_data)
    b, a = signal.butter(3, 8000 / (0.5 * sample_rate), btype='lowpass')
    return signal.filtfilt(b, a, audio_data)

def apply_de_reverb(audio_data, sample_rate, prop_decrease=0.2):
    audio_float = audio_data.astype(np.float32) / 32768.0
    de_reverberated = nr.reduce_noise(y=audio_float, sr=sample_rate, stationary=False, prop_decrease=prop_decrease)
    return (de_reverberated * 32767).astype(np.int16)

def apply_equalization(audio_data, sample_rate, low_cutoff=100, high_cutoff=10000):
    b, a = signal.butter(2, [low_cutoff / (0.5 * sample_rate), high_cutoff / (0.5 * sample_rate)], btype='band')
    return signal.filtfilt(b, a, audio_data)

def apply_compression(audio_segment, threshold=-25.0, ratio=3.5):
    return compress_dynamic_range(audio_segment, threshold=threshold, ratio=ratio)

# Visualization
def plot_waveform(audio_data, title):
    fig, ax = plt.subplots()
    ax.plot(audio_data)
    ax.set_title(title)
    return fig

def plot_spectrogram(audio_data, sample_rate):
    frequencies, times, spectrogram = signal.spectrogram(audio_data, sample_rate)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(10 * np.log10(spectrogram), aspect='auto', cmap='viridis', origin='lower')
    ax.set_title("Spectrogram")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_xlabel("Time (s)")
    fig.colorbar(ax.images[0], label="dB")
    st.pyplot(fig)
    plt.close(fig)  

# Streamlit UI with parameter controls
def main():
    st.title("Audio Enhancement and Restoration App")
    
    # Reset Parameters Button
    if st.button("Reset Parameters"):
        st.experimental_rerun()  # Reset parameters by re-running the app
    
    # Step 1: Uploading the Video
    video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])
    if video_file:
        video = mp.VideoFileClip(video_file)
        audio = video.audio
        audio.write_audiofile("original_audio.wav")
        
        st.write("Audio extracted and saved as 'original_audio.wav'.")
        
        # Step 2: Displaying the  Original Waveform
        audio_segment = AudioSegment.from_wav("original_audio.wav")
        audio_data = np.array(audio_segment.get_array_of_samples())
        sample_rate = audio_segment.frame_rate
        st.subheader("Original Audio Waveform")
        st.pyplot(plot_waveform(audio_data, "Original Audio Waveform"))

        # Spectrogram
        if st.checkbox("Show Spectrogram", help="Display a spectrogram of the original audio"):
            plot_spectrogram(audio_data, sample_rate)
        
        # Step 3: Audio Enhancement and Restoration Options with Parameter Controls
        st.subheader("Audio Enhancement and Restoration Options")

        # Noise Reduction with Adjustable prop_decrease
        prop_decrease = st.slider("De-reverb Intensity (prop_decrease)", min_value=0.0, max_value=1.0, value=0.2, step=0.05, help="Adjusts the intensity of de-reverberation applied to the audio.")
        if st.checkbox("Apply Noise Reduction"):
            filtered_audio_data = multi_stage_filtering(audio_data, sample_rate)
            filtered_audio_segment = convert_to_audio_segment(filtered_audio_data, audio_segment)
            filtered_audio_segment.export("noisereduction_audio.wav", format="wav")
            st.success("Noise reduction applied successfully!")
            st.pyplot(plot_waveform(filtered_audio_data, "Noise Reduced Audio Waveform"))

        # De-reverberation
        if st.checkbox("Apply De-reverberation"):
            de_reverbed_audio = apply_de_reverb(filtered_audio_data, sample_rate, prop_decrease=prop_decrease)
            de_reverbed_audio_segment = convert_to_audio_segment(de_reverbed_audio, audio_segment)
            de_reverbed_audio_segment.export("de_reverb_audio.wav", format="wav")
            st.success("De-reverberation applied successfully!")
            st.pyplot(plot_waveform(de_reverbed_audio, "De-reverberated Audio Waveform"))

        # Equalization with Adjustable Low and High Cutoff Frequencies
        low_cutoff = st.slider("Equalization Low Cutoff (Hz)", min_value=20, max_value=500, value=100, step=10, help="Adjusts the low frequency range for equalization.")
        high_cutoff = st.slider("Equalization High Cutoff (Hz)", min_value=5000, max_value=15000, value=10000, step=500, help="Adjusts the high frequency range for equalization.")
        if st.checkbox("Apply Equalization"):
            equalized_audio = apply_equalization(de_reverbed_audio, sample_rate, low_cutoff=low_cutoff, high_cutoff=high_cutoff)
            equalized_audio_segment = convert_to_audio_segment(equalized_audio, audio_segment)
            equalized_audio_segment.export("equalized_audio.wav", format="wav")
            st.success("Equalization applied successfully!")
            st.pyplot(plot_waveform(equalized_audio, "Equalized Audio Waveform"))

        # Compression with Adjustable Threshold and Ratio
        threshold = st.slider("Compression Threshold (dB)", min_value=-50.0, max_value=0.0, value=-25.0, step=1.0, help="Sets the threshold below which compression is applied.")
        ratio = st.slider("Compression Ratio", min_value=1.0, max_value=10.0, value=3.5, step=0.1, help="Determines how much compression is applied to the audio.")
        if st.checkbox("Apply Compression"):
            compressed_audio_segment = apply_compression(equalized_audio_segment, threshold=threshold, ratio=ratio)
            compressed_audio_segment.export("compressed_audio.wav", format="wav")
            st.success("Compression applied successfully!")

        # Comparison Playback
        if st.checkbox("Enable Comparison Playback"):
            st.write("Listen to the Original and Enhanced Audio Side-by-Side")
            if st.button("Play Original Audio"):
                st.audio("original_audio.wav")
            if st.button("Play Enhanced Audio"):
                st.audio("compressed_audio.wav")
        
        # Step 4: Save Each Stage Separately, with file existence checks
        st.subheader("Download Enhanced Stages")
        if os.path.exists("original_audio.wav"):
            st.download_button("Download Original Audio", data=open("original_audio.wav", "rb"), file_name="original_audio.wav")
        if os.path.exists("noisereduction_audio.wav"):
            st.download_button("Download Noise Reduction", data=open("noisereduction_audio.wav", "rb"), file_name="noisereduction_audio.wav")
        if os.path.exists("de_reverb_audio.wav"):
            st.download_button("Download De-reverbed Audio", data=open("de_reverb_audio.wav", "rb"), file_name="de_reverb_audio.wav")
        if os.path.exists("equalized_audio.wav"):
            st.download_button("Download Equalized Audio", data=open("equalized_audio.wav", "rb"), file_name="equalized_audio.wav")
        if os.path.exists("compressed_audio.wav"):
            st.download_button("Download Compressed Audio", data=open("compressed_audio.wav", "rb"), file_name="compressed_audio.wav")

if __name__ == "_main_":
    main()