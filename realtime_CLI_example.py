from manipur_asr.realtime_speech import RealTimeSpeech
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Real-time speech transcription from microphone.")
    parser.add_argument("--lang", default="mni", help="Language (default: mni)")
    parser.add_argument("--max-words", type=int, default=20, help="Maximum words per line")
    args = parser.parse_args()

    buffer = []
    last_printed_words = []
    printed_lines = set()

    def print_with_animation(text):
        GREEN = '\033[92m'
        RESET = '\033[0m'
        sys.stdout.write('\r' + GREEN + text + RESET)
        sys.stdout.write(' ' * (80 - len(text)))  # Clear remainder of line
        sys.stdout.flush()

    def on_transcript(text):
        nonlocal buffer, last_printed_words, printed_lines
        words = text.strip().split()
        if not words or words == last_printed_words:
            return

        # Find overlap
        overlap = 0
        for i in range(len(buffer), 0, -1):
            if buffer[-i:] == words[:i]:
                overlap = i
                break
        buffer += words[overlap:]

        current_line = " ".join(buffer)
        # Print updated line only if not already printed
        if current_line not in printed_lines:
            print_with_animation(current_line)

        # If line complete, flush and clear buffer
        if (
            len(buffer) >= args.max_words or
            (buffer and (buffer[-1].endswith('.') or buffer[-1].endswith('꯫')))
        ):
            if current_line not in printed_lines:
                print()  # Newline
                printed_lines.add(current_line)
            last_printed_words = buffer.copy()
            buffer.clear()

    print(f"🎙️ Speak now! Listening for '{args.lang}' language...")
    RealTimeSpeech(lang=args.lang).start(on_transcript)

if __name__ == "__main__":
    main()
