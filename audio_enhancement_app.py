import streamlit as st
import io
import numpy as np
from scipy.io.wavfile import write
import librosa
from enhance_audio import (
    multi_stage_filtering, apply_de_reverb, apply_equalization,
    apply_compression, convert_to_audio_segment, plot_waveform, plot_spectrogram
)

# Set the title of the app
st.title("Audio Enhancement App")

# File upload section
st.sidebar.header("Upload Audio File")
uploaded_file = st.sidebar.file_uploader("Choose an MP3 or WAV file", type=["mp3", "wav"])

if uploaded_file is not None:
    # Load the audio file
    data, sample_rate = librosa.load(uploaded_file, sr=None)
    st.audio(uploaded_file, format="audio/wav")
    
    # Enhancement options
    st.sidebar.header("Enhancement Options")
    
    # Noise reduction
    noise_reduction = st.sidebar.checkbox("Apply Noise Reduction")
    
    # De-reverberation with adjustable intensity
    de_reverb = st.sidebar.checkbox("Apply De-reverberation")
    prop_decrease = st.sidebar.slider("De-reverb Intensity", 0.0, 1.0, 0.2, step=0.05)

    # Equalization parameters
    eq_bass = st.sidebar.slider("Equalization Low Cutoff (Hz)", 20, 500, 100)
    eq_treble = st.sidebar.slider("Equalization High Cutoff (Hz)", 5000, 15000, 10000)

    # Compression parameters
    apply_compression_opt = st.sidebar.checkbox("Apply Compression")
    threshold = st.sidebar.slider("Compression Threshold (dB)", -50.0, 0.0, -25.0, step=1.0)
    ratio = st.sidebar.slider("Compression Ratio", 1.0, 10.0, 3.5, step=0.1)
    
    # Apply enhancements
    if st.sidebar.button("Enhance Audio"):
        enhanced_audio = data.copy()

        # Apply Noise Reduction
        if noise_reduction:
            enhanced_audio = multi_stage_filtering(enhanced_audio, sample_rate)
            st.pyplot(plot_waveform(enhanced_audio, "Noise Reduced Audio Waveform"))
        
        # Apply De-reverberation
        if de_reverb:
            enhanced_audio = apply_de_reverb(enhanced_audio, sample_rate, prop_decrease)
            st.pyplot(plot_waveform(enhanced_audio, "De-reverberated Audio Waveform"))
        
        # Apply Equalization
        enhanced_audio = apply_equalization(enhanced_audio, sample_rate, eq_bass, eq_treble)
        st.pyplot(plot_waveform(enhanced_audio, "Equalized Audio Waveform"))

        # Apply Compression
        if apply_compression_opt:
            enhanced_audio_segment = convert_to_audio_segment(enhanced_audio, data)
            enhanced_audio_segment = apply_compression(enhanced_audio_segment, threshold, ratio)
            enhanced_audio = np.array(enhanced_audio_segment.get_array_of_samples())
            st.pyplot(plot_waveform(enhanced_audio, "Compressed Audio Waveform"))

        # Convert and download enhanced audio
        enhanced_audio_buffer = io.BytesIO()
        write(enhanced_audio_buffer, sample_rate, np.int16(enhanced_audio * 32767))
        enhanced_audio_buffer.seek(0)

        # Playback and download
        st.audio(enhanced_audio_buffer, format="audio/wav")
        st.download_button("Download Enhanced Audio", enhanced_audio_buffer, file_name="enhanced_audio.wav")

# Display spectrogram if checkbox is checked
if uploaded_file and st.sidebar.checkbox("Show Spectrogram"):
    plot_spectrogram(data, sample_rate)
