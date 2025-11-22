import os
import json
import time
import pyaudio
from vosk import Model, KaldiRecognizer

class SpeechToText:
    def __init__(self, model_path="model", device_index=None, silence_limit=2.0):
        self.model_path = model_path
        self.device_index = device_index
        self.silence_limit = silence_limit
        self.rate = 16000
        self.chunk = 4000 

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found at '{self.model_path}'")
        
        print(f"Loading Vosk model (Silence Limit: {self.silence_limit}s)...")
        self.model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(self.model, self.rate)

    def listen_once(self) -> str:
        """
        Listens for a single sentence. 
        Blocks execution until speech is detected and finished.
        Returns the string and cleans up the audio stream immediately.
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk,
                        input_device_index=self.device_index)
        
        print(f"Listening... (Waiting for input + {self.silence_limit}s silence)")
        stream.start_stream()

        text_buffer = []
        last_speech_time = time.time()
        
        try:
            while True:
                data = stream.read(self.chunk, exception_on_overflow=False)
                current_time = time.time()

                # 1. Check for "Official" Sentence End
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '')
                    if text:
                        text_buffer.append(text)
                        last_speech_time = current_time
                
                # 2. Check for "Ongoing" Speech (Reset timer if user is mid-sentence)
                else:
                    partial = json.loads(self.recognizer.PartialResult())
                    if partial.get('partial', ''):
                        last_speech_time = current_time

                # 3. Return Trigger
                # Only return if we have captured text AND the silence limit has passed
                if text_buffer and (current_time - last_speech_time > self.silence_limit):
                    full_sentence = " ".join(text_buffer)
                    return full_sentence  # <--- Returns string and exits loop
                    
        except KeyboardInterrupt:
            return ""
        finally:
            # This block runs immediately after 'return'
            print("Stopping listener...")
            stream.stop_stream()
            stream.close()
            p.terminate()
