# Atlas Voice Assistant

The voice assistant for a home automation system that may eventually be sold as a product. The planned product line is mmWave door sensors, a doorbell camera (logic mostly built, in `../door-greeter`), an outdoor camera, this smart speaker, and later a hub. Smart home control (lights, Matter) comes later.

The assistant is named **Atlas**: a warm, polite, charismatic British male voice in the "AI butler" style. The brain is the Claude or ChatGPT API (not chosen yet).

## How to work with the user

- **Teach one step at a time.** The user is learning and asked explicitly not to get the whole tutorial at once. Give one step, explain *why* it matters, give copy-paste commands and code, and end with a clear "done when…" check. Wait for the user to confirm before moving on.
- Explain errors in plain language: what they mean, then the fix.
- The user runs the commands themselves; this is a tutorial, not a "do it for me" project.

## Ground rules

- **No training or cloning on JARVIS / Paul Bettany audio**, not even for the private prototype. Anything trained on it can never ship. The goal is an original voice in the same *archetype*.
- Stay on voices and models that are commercially licensable. Kokoro is Apache-2.0. Check licenses before adding any model (many cloning models have non-commercial weights; the newer Piper is GPL-3.0).

## Environment

- macOS, Python 3.14 from the python.org installer, virtual environment in `.venv/` (`source .venv/bin/activate`).
- Python 3.14 from python.org didn't ship with SSL certificates, which broke downloads. Fixed with `sudo "/Applications/Python 3.14/Install Certificates.command"`.
- Installed packages: `piper-tts` (no longer used), `kokoro-onnx`, `soundfile`, `sounddevice`.
- Model files in the project root, not committed: `kokoro-v1.0.onnx`, `voices-v1.0.bin` (from the thewh1teagle/kokoro-onnx GitHub releases, `model-files-v1.0`).
- Target speaker hardware will probably be Linux (e.g. Raspberry Pi). Avoid Mac-only tools like `afplay` in real code; use `sounddevice`.

## Decisions so far

| Decision | Choice | Why |
|---|---|---|
| Text-to-speech engine | **Kokoro** (`kokoro-onnx`) | Much more natural than Piper, runs offline, Apache-2.0 license |
| Rejected | Piper `en_GB-alan-medium` | Sounded dark, robotic and eerie |
| Atlas voice | **40% `bm_fable` + 60% `bm_lewis`**, speed **0.9**, `lang="en-gb"` | User's favorite after tuning. Blending also makes it less generic than one stock voice |
| Brain | Claude API, **`claude-haiku-5-5`** with effort `low` (`chat_atlas.py`) | The user chose the cheapest model. The key is in `.env` as `CLAUDE_API`, loaded with `python-dotenv` |
| Name pronunciation | Pronunciation dictionary that swaps text before synthesis: `"Jaden" → "Jayden"` | The engine misreads "Jaden". "Jayden" and "Jaiden" both work |

## Files

- `atlas_voice.py`: **the voice module.** Loads Kokoro once, defines `ATLAS_VOICE` and `ATLAS_SPEED`, has a `PRONUNCIATIONS` dict plus `fix_pronunciation()`, and `speak(text)` plays audio through `sounddevice`. Everything else should call `speak()`.
- `voice-brief.md`: the voice spec (name, personality, accent, pace). **Incomplete on purpose; paused until the product is closer to launch.** Remaining gaps: the example lines are empty, the only reference voice is JARVIS (add 2–3 others), "quirky" needs defining (dry wit vs playful), and which British accent.
- `compare_voices.py`, `tune_voice.py`, `test_name.py`: tutorial experiment scripts from Steps 3–4.
- `.gitignore` should include `.venv/`, `*.onnx`, `*.bin`, `*.wav` (the models are about 400 MB).

## Roadmap

### Done
1. ✅ **Got text-to-speech working on the Mac.** Installed Piper and heard a stock British voice. Learned that a voice = model file + config.
2. ✅ **Wrote the voice brief** (partially; see above). The user wants warm, polite, charismatic and natural, and never robotic, dark or eerie.
3. ✅ **Compared text-to-speech engines.** Kokoro beat Piper by a wide margin; the favorite was `bm_fable`.
4. ✅ **Tuned the voice.** Settled on the Fable/Lewis 40/60 mix at speed 0.9 and fixed the pronunciation of the user's name.
5. 🔄 **Built `speak()` in `atlas_voice.py`.** The code was given; the user hasn't yet confirmed `python3 atlas_voice.py` works.

### Next
6. **Connect the brain.** Typed question → Claude or ChatGPT API → answer in character → `speak()`. Includes a system prompt for Atlas's personality: polite, warm, dry wit, uses the first name or sir/ma'am, short spoken answers, no markdown or emoji, numbers written out for speech. API keys go in environment variables or `.env`, never in code.
7. **Make it feel instant.** Stream the LLM response, split it into sentences, and speak sentence 1 while the rest generates.
8. **Speech-to-text.** Microphone → text, probably `faster-whisper` running locally.
9. **Wake word.** "Atlas", using openWakeWord (free, supports training custom words) or Picovoice Porcupine (paid for commercial use).
10. **Full loop.** Wake word → listen → transcribe → think → speak, plus conversation memory.
11. **Audio polish and hardware.** Light EQ, compression and short reverb (e.g. `pedalboard`), tuned on the real speaker hardware; port to the target device.

### Later / when it becomes a product
- Smart home control through LLM tool calling (lights, Matter, door sensors, cameras), integrated with the hub and doorbell.
- A per-user pronunciation setup screen so each customer can fix how Atlas says their name (extends `PRONUNCIATIONS`).
- **Custom voice from a voice actor.** Finish the voice brief, hire an actor with a written contract granting AI training and commercial use, record 1–2 hours of clean audio (LJSpeech format), and fine-tune on a rented GPU. Until then, the Kokoro blend is a legally shippable voice, though not exclusive to Atlas.
