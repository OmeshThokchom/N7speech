import os
import warnings
# Suppress ONNXRuntime and CUDA warnings before importing onnxruntime
os.environ["CUDA_VISIBLE_DEVICES"] = ""  # Prevent CUDA provider warning
os.environ["ORT_DISABLE_EXTERNAL_WARNINGS"] = "1"
warnings.filterwarnings("ignore", category=UserWarning)

import onnxruntime as ort
import numpy as np
import librosa

class N7SpeechRecognizer:
    """
    Speech recognizer using ONNX model for Meitei speech-to-text.
    Supports input as wav/mp3 file or numpy array.
    """
    def __init__(self, model_path="manipur_asr/model.onnx", vocab_path="manipur_asr/vocab.txt", providers=None):
        if providers is None:
            # Only use available providers, avoid warning for unavailable CUDA
            available = ort.get_available_providers()
            providers = [p for p in ['CUDAExecutionProvider', 'CPUExecutionProvider'] if p in available]
            if not providers:
                providers = ['CPUExecutionProvider']
        self.sess = ort.InferenceSession(model_path, providers=providers)
        with open(vocab_path, "r") as f:
            self.vocab = [line.strip() for line in f]

    def preprocess_audio(self, audio, target_sr=16000, from_file=True):
        if from_file:
            # Load audio file (wav, mp3, etc.)
            audio, sr = librosa.load(audio, sr=target_sr)
        else:
            sr = target_sr
            # audio is already a numpy array at target_sr
        # Normalize audio
        audio = audio / np.max(np.abs(audio))
        # Convert to mono if needed
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=0)
        # Extract Mel spectrogram features (80 bands matches your model input)
        mel_spec = librosa.feature.melspectrogram(
            y=audio,
            sr=target_sr,
            n_mels=80,
            n_fft=512,
            hop_length=160,
            win_length=320
        )
        # Convert to log scale
        log_mel = librosa.power_to_db(mel_spec)
        # Normalize (optional, depends on how your model was trained)
        log_mel = (log_mel - log_mel.mean()) / log_mel.std()
        # Add batch dimension: [1, 80, time_frames]
        log_mel = np.expand_dims(log_mel, axis=0)
        return log_mel.astype(np.float32)

    def transcribe(self, audio_input, sr=16000):
        """
        Transcribe audio from a file (wav/mp3) or numpy array.

        Args:
            audio_input (str or np.ndarray): Path to audio file or numpy array.
            sr (int): Sample rate for numpy array input.

        Returns:
            str: Transcribed text.
        """
        if isinstance(audio_input, str):
            ext = os.path.splitext(audio_input)[1].lower()
            if ext in [".wav", ".mp3"]:
                input_data = self.preprocess_audio(audio_input, from_file=True)
            else:
                raise ValueError("Unsupported audio file format: {}".format(ext))
        elif isinstance(audio_input, np.ndarray):
            input_data = self.preprocess_audio(audio_input, target_sr=sr, from_file=False)
        else:
            raise TypeError("audio_input must be a file path or numpy array.")

        input_length = np.array([input_data.shape[2]], dtype=np.int64)
        outputs = self.sess.run(
            None,
            {
                "audio_signal": input_data,
                "length": input_length
            }
        )
        logits = outputs[0]
        token_ids = np.argmax(logits, axis=-1)[0]
        transcript = " ".join([self.vocab[idx] for idx in token_ids if idx < len(self.vocab)])
        transcript = "".join(transcript.split())
        transcript = transcript.replace("▁", " ").strip()
        return transcript