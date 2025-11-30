from elevenlabs import generate, save
import os

def generate_audio_overview(text: str, filename="overview.mp3"):
    audio = generate(
        text=text,
        voice="Rachel",
        model="eleven_turbo_v2"
    )
    save(audio, filename)
    print(f"🎙️ Audio saved: {filename}")
