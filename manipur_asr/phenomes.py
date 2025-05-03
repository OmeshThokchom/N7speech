"""
Meitei Mayek to phoneme conversion library.

Provides:
    - meitei_mayek_to_phoneme: dict mapping Meitei Mayek characters/sequences to phonemes
    - meitei_lon(text): function to convert Meitei Mayek text to phoneme string
"""

__all__ = ["meitei_mayek_to_phoneme", "meitei_lon"]

# Meitei Mayek to phoneme dictionary
meitei_mayek_to_phoneme = {
    # Multi-character mappings first to ensure they are checked before single characters
    "ꯑꯦ": "ae", "ꯑꯤ": "e", "ꯑꯣ": "o", "ꯑꯧ": "ou", "ꯑꯩ":"ei",


    # Basic Consonants
    "ꯀ": "k", "ꯁ": "s", "ꯂ": "l", "ꯃ": "m", "ꯄ": "p", "ꯅ": "n",
    "ꯆ": "ch", "ꯇ": "t", "ꯈ": "kh", "ꯉ": "ng", "ꯊ": "th", "ꯋ": "w",
    "ꯌ": "y", "ꯍ": "h", "ꯎ": "u", "ꯏ": "i", "ꯐ": "ph", "ꯑ": "a",

    # Old Letters (Historical usage)
    "ꯒ": "g", "ꯓ": "jh", "ꯔ": "r", "ꯕ": "b", "ꯖ": "j", "ꯗ": "d",
    "ꯘ": "gh", "ꯙ": "dh", "ꯚ": "bh", "ꯛ": "k", "ꯜ": "l",
    "ꯝ": "m", "ꯞ": "p", "ꯟ": "n", "ꯠ": "t", "ꯡ": "ng",

    # Vowels and other characters
    "ꯤ": "i", "ꯥ": "a", "ꯦ": "e", "ꯧ": "ou", "ꯨ": "u",
    "ꯩ": "ei", "ꯪ": "ng", "꯫": ".", "ꯣ": "o", "꯭":"",

    # Numbers
    "꯰": "0", "꯱": "1", "꯲": "2", "꯳": "3", "꯴": "4",
    "꯵": "5", "꯶": "6", "꯷": "7", "꯸": "8", "꯹": "9"
}

def meitei_lon(text):
    """
    Convert Meitei Mayek text to phonemes by checking longest possible sequences.

    Args:
        text (str): Input text in Meitei Mayek script.

    Returns:
        str: Phoneme representation.
    """
    max_key_length = max(len(k) for k in meitei_mayek_to_phoneme.keys())
    phonemes = []
    i = 0
    while i < len(text):
        matched = False
        # Check for the longest possible match starting at position i
        for length in range(min(max_key_length, len(text) - i), 0, -1):
            substr = text[i:i+length]
            if substr in meitei_mayek_to_phoneme:
                phonemes.append(meitei_mayek_to_phoneme[substr])
                i += length
                matched = True
                break
        if not matched:
            # If no match, add the character as-is
            phonemes.append(text[i])
            i += 1
    return "".join(phonemes)

