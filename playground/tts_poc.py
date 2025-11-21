from google import genai
import simpleaudio as sa
from google.genai import types
client = genai.Client()

def talk(message):

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=message,
        config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Kore')
                )
            )
        )
    )

    audio_bytes =  response.candidates[0].content.parts[0].inline_data.data

    # 3. Play directly from memory (no saving required)
    play_obj = sa.play_buffer(
    audio_bytes,        # raw audio bytes
    num_channels=1,     # Gemini TTS returns mono
    bytes_per_sample=2, # WAV PCM16 = 2 bytes per sample
    sample_rate=24000   # Gemini TTS uses 24kHz by default
    )

    play_obj.wait_done()

for message in open("messages.txt").readlines():
    talk(message)
