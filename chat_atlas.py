import os

import anthropic
from dotenv import load_dotenv

from atlas_voice import speak

load_dotenv()  # reads the .env file in this folder into environment variables
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API"))

SYSTEM_PROMPT = """You are Atlas, the AI assistant for this home.
Personality: warm, polite and charismatic, with gentle dry wit. A small clever remark now and then, never goofy, never sarcastic toward the user.
The user's name is Jaden. Usually address him by first name; occasionally "sir".

Your replies are spoken aloud by a text-to-speech voice, so:
- Keep answers short: one or two sentences unless asked for more detail.
- Never use markdown, bullet points, emoji, or symbols.
- Write numbers, times and units the way they're spoken, for example "seventy-two degrees", not "72°F".
You cannot control any devices yet. If asked to, say so politely."""

history = []  # the conversation so far, so Atlas remembers context


def ask_atlas(user_text):
    """Send the user's message to Claude and return Atlas's reply as text."""
    history.append({"role": "user", "content": user_text})

    response = client.messages.create(
        model="claude-haiku-5-5",             # cheapest current Claude model
        max_tokens=1024,                      # spoken replies are short
        output_config={"effort": "low"},      # quicker replies for casual chat
        system=SYSTEM_PROMPT,
        messages=history,
    )

    history.append({"role": "assistant", "content": response.content})

    if response.stop_reason == "refusal":
        return "I'm afraid I can't help with that one."

    return " ".join(block.text for block in response.content if block.type == "text")


if __name__ == "__main__":
    print("Atlas is online. Type 'quit' to exit.")
    speak("Good evening, Jaden. Atlas is online.")

    while True:
        user_text = input("\nYou: ").strip()
        if not user_text:
            continue
        if user_text.lower() in ("quit", "exit"):
            speak("Very good. I'll be here if you need me.")
            break

        try:
            reply = ask_atlas(user_text)
        except anthropic.AuthenticationError:
            print("Your API key is missing or wrong. Check CLAUDE_API in your .env file.")
            break
        except anthropic.APIConnectionError:
            print("Couldn't reach the API. Check your internet connection.")
            continue

        print(f"Atlas: {reply}")
        speak(reply)