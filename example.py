from manipur_asr.realtime_speech import RealTimeSpeech, speech_from_file


if __name__ == "__main__":
    #Example for microphone input
    RealTimeSpeech(lang="mni-latin").start(lambda t: print(f"\nResult: {t}"))

    # Example for wav/mp3 file input
    #result = speech_from_file("output.wav", lang="mni-latin")
    #print("result:",result)
