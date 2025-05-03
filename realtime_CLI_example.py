from manipur_asr.realtime_speech import RealTimeSpeech
import sys
import time

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Real-time speech transcription from microphone.")
    parser.add_argument("--lang", default="mni", help="Language (default: mni-latin)")
    parser.add_argument("--max-words", type=int, default=20, help="Maximum words per line (default: 35)")
    args = parser.parse_args()

    buffer = []
    last_printed_words = []

    def print_with_animation(text):
        GREEN = '\033[92m'
        RESET = '\033[0m'
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write(GREEN + text + RESET)
        # Fill the rest of the line with spaces to clear previous content
        sys.stdout.write(' ' * (80 - len(text)))
        sys.stdout.flush()

    def on_transcript(text):
        nonlocal buffer, last_printed_words
        words = text.strip().split()
        if not words:
            return
        # If the recognizer repeats the last printed segment, ignore it
        if words == last_printed_words:
            return
        # If buffer is empty, just add new words
        if not buffer:
            buffer = words
        else:
            # Find overlap
            overlap = 0
            for i in range(len(buffer), 0, -1):
                if buffer[-i:] == words[:i]:
                    overlap = i
                    break
            buffer += words[overlap:]
        # Print the current buffer in-place only if changed, with animation
        print_with_animation(" ".join(buffer))
        # If buffer reaches/exceeds max_words, or ends with a full stop (ASCII or Meetei Mayek), print and clear
        if (
            len(buffer) >= args.max_words or
            (buffer and (buffer[-1].endswith(".") or buffer[-1].endswith("꯫")))
        ):
            print()  # Newline
            last_printed_words = buffer.copy()
            buffer.clear()

    print(f"Speak now! Transcribing from mic using language: {args.lang} ...")
    RealTimeSpeech(lang=args.lang).start(on_transcript)

if __name__ == "__main__":
    main()