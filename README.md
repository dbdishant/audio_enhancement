# Audio Enhancement App

## Overview
The **Audio Enhancement App** is a Python-based application designed to enhance and restore audio extracted from video files. It uses techniques like noise reduction, de-reverberation, equalization, and compression to improve audio quality. The project is implemented using **Streamlit** for the UI and leverages libraries like `pydub`, `numpy`, `scipy`, and `noisereduce` for processing audio.

---

## Project Structure
The project contains two main files:

### 1. `enhance_audio.py`
- **Description**: Contains the core logic and algorithms for audio enhancement.
- **Features**:
  - Noise Reduction
  - De-reverberation
  - Equalization
  - Compression
  - Visualization: Waveform and spectrogram plotting
- **Usage**: Provides helper functions and processing pipelines to be called from the UI.

### 2. `audio_enhancement_app.py`
- **Description**: Implements the frontend of the application using **Streamlit**.
- **Features**:
  - File upload for audio or video files
  - User-friendly sliders and checkboxes for configuring enhancement parameters
  - Real-time waveform and spectrogram visualizations
  - Playback and download of processed audio

---

## Key Features
1. **Audio Extraction**:
   - Extracts audio from video files like `.mp4`, `.mov`, or `.avi`.
   - Supports direct `.mp3` or `.wav` uploads.

2. **Audio Enhancement Techniques**:
   - **Noise Reduction**: Filters unwanted background noise.
   - **De-reverberation**: Reduces echoes with customizable intensity.
   - **Equalization**: Adjusts bass and treble frequencies.
   - **Compression**: Normalizes dynamic range for consistent volume.

3. **Visualization**:
   - Displays waveform and spectrogram for both original and enhanced audio.

4. **Download & Playback**:
   - Allows playback of the original and enhanced audio directly from the app.
   - Offers downloads for all processed audio stages.

---

## Installation

1. **Clone the repository**:
   ```bash
   $ git clone https://github.com/yourusername/audio-enhancement-app.git
   $ cd audio-enhancement-app
    ```

2. **Install dependencies: Ensure you have Python installed, then run**:
    ```bash
    $ pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    $ streamlit run audio_enhancement_app.py
    ```

---

## How to Use
1. Launch the app by running the command above.
2. Use the sidebar to upload an audio or video file.
3. Select enhancement options and adjust parameters as needed.
4. View visualizations for the audio waveform and spectrogram.
5. Play the enhanced audio or download it.

---

## Dependencies
1. Python 3.8+
2. Libraries:
- streamlit
- moviepy
- pydub
- numpy
- scipy
- noisereduce
- matplotlib
- librosa

---

## Future Improvements
1. Add more advanced noise reduction algorithms.
2. Introduce support for batch processing.
3. Provide additional audio formats for download.
4. Integrate cloud storage for large files.
