from piper import PiperVoice
import sounddevice as sd
import numpy as np
import logging
from config import ONNX_PATH

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

voice = PiperVoice.load(ONNX_PATH)

def talk(message):
    logger.info(f"Talking message: {message}")

    audio_bytes = b""
    for chunk in voice.synthesize(message):
        audio_bytes += chunk.audio_int16_bytes

    # Playing
    logger.debug("Playing")
    audio_arr = np.frombuffer(audio_bytes, dtype="<i2").astype(np.int16)
    sd.play(audio_arr, samplerate=24000, blocking=True)

    logger.info("Finished talking")

if __name__ == '__main__':
    #talk("Say hello to my little friend")
    talk("rega ima ani tehef ba")