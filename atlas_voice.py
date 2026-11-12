import re
import sounddevice as sd
from kokoro_onnx import Kokoro

# --- Load the model once, when this file is imported ---
kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

# --- Atlas's voice: 40% Fable + 60% Lewis ---
ATLAS_VOICE = kokoro.get_voice_style("bm_fable") * 0.4 + kokoro.get_voice_style("bm_lewis") * 0.6
ATLAS_SPEED = 0.9

# --- Pronunciation dictionary: written word -> spelling the engine reads correctly ---
PRONUNCIATIONS = {
    "Jaden": "Jayden",
}


def fix_pronunciation(text):
    """Swap tricky words for spellings the voice engine reads correctly."""
    for word, spoken in PRONUNCIATIONS.items():
        # \b = whole word only, so "Jaden" is replaced but not "Jadenville"
        text = re.sub(rf"\b{re.escape(word)}\b", spoken, text, flags=re.IGNORECASE)
    return text


def speak(text):
    """Say the text out loud in Atlas's voice."""
    text = fix_pronunciation(text)
    samples, sample_rate = kokoro.create(text, voice=ATLAS_VOICE, speed=ATLAS_SPEED, lang="en-gb")
    sd.play(samples, sample_rate)
    sd.wait()  # wait until it finishes talking


# --- Only runs when you execute this file directly, for testing ---
if __name__ == "__main__":
    speak("Welcome back, Jaden. The house is just as you left it.")
    speak("Pardon the interruption. There's someone at the front door.")