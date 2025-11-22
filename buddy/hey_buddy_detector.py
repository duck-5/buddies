import os
import json
import sys
import logging
import pyaudio
from agent.agent.flow import AgentFlow
from vosk import Model, KaldiRecognizer

# Configure logging to look nice and clean
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

class WakeWordEngine:
    """
    A dedicated engine for detecting specific wake phrases using Vosk.
    """

    def __init__(self, model_path: str, wake_phrase: str, device_index: int = None):
        """
        Initialize the engine. Loads the model once to save time later.

        Args:
            model_path (str): Path to the Vosk model folder.
            wake_phrase (str): The specific phrase to trigger on (e.g., "hey buddy").
            device_index (int): Optional microphone device index.
        """
        self.wake_phrase = wake_phrase
        self.device_index = device_index
        self.sample_rate = 16000
        
        # 1. Validation
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found at '{model_path}'. "
                "Please download from https://alphacephei.com/vosk/models"
            )

        # 2. Load Model (The heavy operation)
        logger.info(f"Loading model from '{model_path}'...")
        try:
            self.model = Model(model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load Vosk model: {e}")

        # 3. Configure Recognizer with restricted vocabulary
        # The list ["phrase", "[unk]"] forces the AI to only care about the wake word
        # or noise, significantly improving accuracy.
        vocab_list = f'["{self.wake_phrase}", "[unk]"]'
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate, vocab_list)
        
        logger.info(f"Engine ready. Wake phrase: '{self.wake_phrase}'")

    def wait_for_activation(self, agent_flow: AgentFlow):
        """
        Blocks execution and listens to the microphone until the wake phrase is spoken.
        
        Returns:
            bool: True when wake word is detected.
        """
        p = pyaudio.PyAudio()
        stream = None

        try:
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=self.sample_rate,
                            input=True,
                            frames_per_buffer=8000,
                            input_device_index=self.device_index)
            
            logger.info("Listening... (Press Ctrl+C to stop)")
            stream.start_stream()

            while True:
                data = stream.read(4000, exception_on_overflow=False)
                
                if len(data) == 0:
                    break

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '')

                    if text == self.wake_phrase:
                        logger.info(f"✅ Wake word detected: {text.upper()}")
                        AgentFlow.main_flow()
                        return True

        except KeyboardInterrupt:
            logger.info("Stopping listener...")
            return False
        except Exception as e:
            logger.error(f"Audio stream error: {e}")
            return False
        finally:
            # Clean resource management
            if stream:
                stream.stop_stream()
                stream.close()
            p.terminate()
