# N7Speech

**N7Speech** is a Python library for real-time and file-based speech recognition and Meitei Mayek phoneme conversion.  
It supports both microphone and audio file (wav/mp3) input, and can output either Meitei Mayek or Latin phoneme representations.

## Author

Dayananda Thokchom

## Features

- Real-time speech recognition from microphone with VAD (voice activity detection)
- Transcription from audio files (wav/mp3)
- Meitei Mayek to phoneme (Latin) conversion
- Simple, high-level API
- ONNX model backend for fast inference

## Installation

### Linux/macOS

```bash
pip install n7speech
```

Or for local development:

```bash
git clone https://github.com/yourusername/N7speech.git
cd N7speech
pip install .
```

### Windows

1. Install Python 3.7+ from [python.org](https://www.python.org/downloads/windows/).
2. Open **Command Prompt** as Administrator.
3. Install the package:

```bash
pip install n7speech
```

4. If you encounter issues with `sounddevice`, install the appropriate wheel from [PyPI](https://pypi.org/project/sounddevice/#files) or use:

```bash
pip install pipwin
pipwin install sounddevice
```

### GPU Acceleration (All Platforms)

> Users can install either `onnxruntime` (CPU) or `onnxruntime-gpu` (GPU) as needed.  
> Here, we specify `onnxruntime` as the default, but recommend for NVIDIA-GPU users to uninstall with  
> `pip uninstall onnxruntime`  
> and install  
> `pip install onnxruntime-gpu`  
> for much faster inference.

## Usage

### Real-time microphone transcription

```python
from n7speech import RealTimeSpeech

RealTimeSpeech(lang="mni-latin").start(lambda t: print(f"\nResult: {t}"))
```

### Transcribe from audio file

```python
from n7speech import speech_from_file

result = speech_from_file("your_audio.wav", lang="mni-latin")
print(result)
```

- `lang="mni"` for Meitei Mayek output, `lang="mni-latin"` for phoneme output.## Platform Support

## RequirementsN7Speech is cross-platform and works on **Linux**, **macOS**, and **Windows**.  
 for these operating systems.
- Python 3.7+
- onnxruntime **or** onnxruntime-gpu (for GPU acceleration, highly recommended for fast transcription; e.g., 20s wav in ~110ms)- For **macOS** and **Windows** users, make sure your Python environment and audio drivers are set up correctly for `sounddevice` and `torch`.
- numpye).
- librosa
- torch- sounddevice

## Model and Vocab

Place your ONNX model as `model.onnx` and vocabulary as `vocab.txt` in the working directory.

## License

MIT License


## Platform Support

N7Speech is cross-platform and works on **Linux**, **macOS**, and **Windows**.  
All dependencies (onnxruntime, torch, numpy, librosa, sounddevice) are available for these operating systems.

- For **macOS** and **Windows** users, make sure your Python environment and audio drivers are set up correctly for `sounddevice` and `torch`.
- For **GPU acceleration**, ensure you install the correct version of `onnxruntime-gpu` and have compatible CUDA drivers (on supported hardware).

