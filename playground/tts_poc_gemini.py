from google import genai
#import simpleaudio as sa
import sounddevice as sd
import numpy as np
from google.genai import types
import logging
import logging.config

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

client = genai.Client()

def talk(message):
    logger.info(f"Talking message: {message}")

    # LLM request
    logger.debug("Sending request to gemini")
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
    logger.debug("Got response!")
    # Audio extraction
    try:
        audio_bytes =  response.candidates[0].content.parts[0].inline_data.data
    except Exception:
        logger.Error("Invalid response")
        breakpoint()

    logger.debug("Response is valid")

    # Playing
    logger.debug("Playing")
    audio_arr = np.frombuffer(audio_bytes, dtype="<i2").astype(np.int16)
    sd.play(audio_arr, samplerate=24000, blocking=True)

    logger.info("Finished talking")
    """
    play_obj = sa.play_buffer(
    audio_bytes,        # raw audio bytes
    num_channels=1,     # Gemini TTS returns mono
    bytes_per_sample=2, # WAV PCM16 = 2 bytes per sample
    sample_rate=24000   # Gemini TTS uses 24kHz by default
    )
    play_obj.wait_done()
    """


if __name__ == '__main__':
    for message in open("messages.txt").readlines():
        talk(message)
