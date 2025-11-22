import os
import queue
import json
import time  # Added for timing
import pyaudio
from vosk import Model, KaldiRecognizer

class SpeechToText:
    def __init__(self, model_path="model", device_index=None, silence_limit=2.0):
        """
        Args:
            silence_limit (float): Seconds of silence to wait before yielding 
                                   the sentence. Higher = better for slow speakers.
        """
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

    def listen(self):
        """
        Yields text only after the user has stopped speaking for 'silence_limit' seconds.
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk,
                        input_device_index=self.device_index)
        
        print(f"Listening... (Waiting for {self.silence_limit}s silence to finalize)")
        stream.start_stream()

        # --- Buffer Logic State ---
        text_buffer = []
        last_speech_time = time.time()
        
        try:
            while True:
                data = stream.read(self.chunk, exception_on_overflow=False)
                current_time = time.time()

                # 1. Check for "Official" Sentence End (Vosk Logic)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '')
                    
                    if text:
                        text_buffer.append(text)
                        last_speech_time = current_time # Reset timer
                
                # 2. Check for "Ongoing" Speech (Partial Logic)
                else:
                    partial = json.loads(self.recognizer.PartialResult())
                    if partial.get('partial', ''):
                        # User is currently speaking (mid-sentence)
                        last_speech_time = current_time # Reset timer

                # 3. The "Timeout" Decision Logic
                # If we have text in buffer AND we haven't heard speech for X seconds
                time_since_speech = current_time - last_speech_time
                
                if text_buffer and (time_since_speech > self.silence_limit):
                    # Join all buffered segments into one clean sentence
                    full_sentence = " ".join(text_buffer)
                    yield full_sentence
                    
                    # Reset state
                    text_buffer = []
                    
        except KeyboardInterrupt:
            pass
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

if __name__ == "__main__":
    # Set silence_limit to 2.0 or 3.0 for slow speaking
    stt = SpeechToText(model_path="model", silence_limit=2.0)
    
    for sentence in stt.listen():
        print(f"Finalized Sentence: {sentence}")