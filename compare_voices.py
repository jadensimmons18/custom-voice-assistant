from kokoro_onnx import Kokoro
import soundfile as sf

kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

text = "Welcome back, sir. The house is just as you left it. Shall I put the kettle on?"

# Kokoro's British male voices ("bm" = British male)
voices = ["bm_george", "bm_lewis", "bm_daniel", "bm_fable"]

for voice in voices:
    samples, sample_rate = kokoro.create(text, voice=voice, speed=1.0, lang="en-gb")
    sf.write(f"kokoro_{voice}.wav", samples, sample_rate)
    print(f"Saved kokoro_{voice}.wav")