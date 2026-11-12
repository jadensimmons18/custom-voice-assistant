from kokoro_onnx import Kokoro
import soundfile as sf

kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

fable = kokoro.get_voice_style("bm_fable")
lewis = kokoro.get_voice_style("bm_lewis")
atlas = fable * 0.4 + lewis * 0.6

spellings = ["Jaden", "Jayden", "Jaiden", "Jay-den", "Jay den"]

for i, spelling in enumerate(spellings):
    text = f"Welcome back, {spelling}."
    samples, sample_rate = kokoro.create(text, voice=atlas, speed=0.9, lang="en-gb")
    sf.write(f"name_{i}.wav", samples, sample_rate)
    print(f"name_{i}.wav  ->  {spelling}")