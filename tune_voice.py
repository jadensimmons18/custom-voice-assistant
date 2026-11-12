from kokoro_onnx import Kokoro
import soundfile as sf

kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

text = "Its currently 72 degrees outside"

fable = kokoro.get_voice_style("bm_fable")
george = kokoro.get_voice_style("bm_george")
lewis = kokoro.get_voice_style("bm_lewis")

# Each entry: (file name, voice, speed)
tests = [
    ("atlas", fable * 0.4 + lewis * 0.6, 0.9),
]

for name, voice, speed in tests:
    samples, sample_rate = kokoro.create(text, voice=voice, speed=speed, lang="en-gb")
    sf.write(f"tune_{name}.wav", samples, sample_rate)
    print(f"Saved tune_{name}.wav")