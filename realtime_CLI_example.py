from manipur_asr.realtime_speech import N7RealTimeSpeech
import time

THRESHOLD = 10
current_line_word_count = 0
history_words = []

def on_text_segment(text):
    global current_line_word_count, history_words
    words = text.strip().split()

    # Avoid duplicate overlap
    max_overlap = 0
    for k in range(min(len(history_words), len(words)), 0, -1):
        if history_words[-k:] == words[:k]:
            max_overlap = k
            break
    new_words = words[max_overlap:]
    if not new_words:
        return

    # Animate the output of the new words as a smooth "bunch"
    output = ' '.join(new_words) + ' '
    for char in output:
        print(char, end='', flush=True)
        time.sleep(0.01)  # Adjust for smoother/faster animation

    current_line_word_count += len(new_words)
    if current_line_word_count >= THRESHOLD:
        print()
        current_line_word_count = 0

    history_words.extend(new_words)

if __name__ == "__main__":
    N7RealTimeSpeech(lang="mni").start(on_text_segment)
