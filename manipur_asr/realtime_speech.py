import torch
import sounddevice as sd
import numpy as np
from queue import Queue
from threading import Thread
from manipur_asr.n7speech import N7SpeechRecognizer
from manipur_asr.phenomes import meitei_lon

# speech_from_file: Transcribes a wav/mp3 file and returns the transcript string.
def speech_from_file(audio_path, lang="mni"):
    """
    Transcribe a wav/mp3 file. Returns the transcript string.

    - Loads the audio file using librosa.
    - Runs the recognizer's transcribe method.
    - If lang is 'mni-latin', converts the output to phonemes.
    """
    recognizer = N7SpeechRecognizer()
    import librosa
    audio, _ = librosa.load(audio_path, sr=16000)
    transcript = recognizer.transcribe(audio)
    if lang == "mni-latin":
        transcript = meitei_lon(transcript)
    return transcript

class N7RealTimeSpeech:
    """Real-time microphone speech recognizer."""
    def __init__(self, lang="mni"):
        # Set up audio and VAD parameters with optimized values
        self.sample_rate = 16000
        self.chunk_duration = 0.1  # Reduced for faster response
        self.chunk_size = int(self.sample_rate * self.chunk_duration)
        self.window_duration = 0.5  # Reduced window size for faster processing
        self.window_size = int(self.sample_rate * self.window_duration)
        self.audio_buffer = np.zeros(self.window_size, dtype=np.float32)
        self.buffer_filled = 0
        self.audio_q = Queue(maxsize=100)  # Limit queue size
        self.lang = lang
        self.recognizer = N7SpeechRecognizer()
        torch.set_num_threads(2)  # Increased threads for VAD
        # Load Silero VAD model and utilities
        self.model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                           model='silero_vad',
                                           force_reload=False)
        (self.get_speech_timestamps, _, _, _, _) = utils
        self.thread = None
        self.running = False

    def _audio_callback(self, indata, frames, time, status):
        """
        Callback for sounddevice InputStream.
        - Receives audio chunks from the microphone.
        - Converts to float32 and normalizes if needed.
        - Puts the chunk into the audio queue for processing.
        """
        if status:
            print("⚠️", status)
        audio_chunk = indata[:, 0].copy()
        if audio_chunk.dtype != np.float32:
            audio_chunk = audio_chunk.astype(np.float32) / np.iinfo(indata.dtype).max
        self.audio_q.put(audio_chunk)

    def _vad_worker(self, on_transcript):
        """
        Worker thread for processing audio chunks and running VAD.
        - Collects audio chunks while speech is detected.
        - When speech ends, runs transcription and calls on_transcript callback.
        """
        last_printed = None
        speech_buffer = []
        collecting = False
        while self.running:
            chunk = self.audio_q.get()
            if chunk is None:
                break
            try:
                # Update rolling buffer
                self.audio_buffer = np.roll(self.audio_buffer, -len(chunk))
                self.audio_buffer[-len(chunk):] = chunk
                self.buffer_filled = min(self.buffer_filled + len(chunk), self.window_size)
                if self.buffer_filled < self.window_size:
                    continue

                # Run VAD on the rolling buffer
                audio_tensor = torch.from_numpy(self.audio_buffer).float()
                self.model.cpu()
                speech_segments = self.get_speech_timestamps(
                    audio_tensor,
                    self.model,
                    sampling_rate=self.sample_rate,
                    threshold=0.3,  # Lower threshold for more sensitive detection
                    min_speech_duration_ms=100  # Shorter minimum duration
                )
                is_speaking = bool(speech_segments)

                # Collect chunks while speaking
                if is_speaking and not collecting:
                    collecting = True
                    speech_buffer = [chunk.copy()]
                elif is_speaking and collecting:
                    speech_buffer.append(chunk.copy())
                # When speech ends, transcribe and call callback
                elif not is_speaking and collecting:
                    collecting = False
                    if speech_buffer:
                        full_audio = np.concatenate(speech_buffer)
                        transcript = self.recognizer.transcribe(full_audio)
                        if self.lang == "mni-latin":
                            transcript = meitei_lon(transcript)
                        if transcript and transcript != last_printed:
                            on_transcript(transcript)
                            last_printed = transcript
                        speech_buffer = []
            except Exception as e:
                print(f"\nError in VAD worker: {e}")

    def start(self, on_transcript):
        """
        Start real-time recognition from microphone.
        - on_transcript: callback function to handle each transcription result.
        - Starts the VAD worker thread and opens the microphone stream.
        """
        print("say someting...")  # Prompt user
        self.running = True
        self.thread = Thread(target=self._vad_worker, args=(on_transcript,), daemon=True)
        self.thread.start()
        try:
            with sd.InputStream(callback=self._audio_callback,
                                channels=1,
                                samplerate=self.sample_rate,
                                blocksize=self.chunk_size):
                while self.running:
                    sd.sleep(100)
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print(f"Audio stream error: {e}")
            self.stop()

    def stop(self):
        """
        Stop the real-time recognizer and clean up the worker thread.
        """
        self.running = False
        self.audio_q.put(None)
        if self.thread:
            self.thread.join()
