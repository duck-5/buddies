import os
import sys
import queue
import json
import pyaudio
from vosk import Model, KaldiRecognizer

# --- Configuration ---
WAKE_PHRASE = "hey buddy"
MODEL_PATH = "model"  # The folder name where you extracted the Vosk model
DEVICE_INDEX = None   # Set to an integer (e.g., 0, 1) if you need a specific mic

def main():
    # 1. Check if model exists
    if not os.path.exists(MODEL_PATH):
        print(f"Please download a model from https://alphacephei.com/vosk/models")
        print(f"Unpack it as '{MODEL_PATH}' in the current folder.")
        sys.exit(1)

    # 2. Load the Model
    print(f"Loading model from '{MODEL_PATH}'...")
    print("This might take a few seconds on a Raspberry Pi...")
    try:
        model = Model(MODEL_PATH)
    except Exception as e:
        print(f"Failed to load model: {e}")
        sys.exit(1)

    # 3. Create the recognizer
    # IMPORTANT: The list in the 3rd argument restricts the vocabulary.
    # This forces the engine to ONLY recognize "hey buddy" or unknown noise "[unk]".
    # This significantly increases accuracy for this specific phrase.
    rec = KaldiRecognizer(model, 16000, f'["{WAKE_PHRASE}", "[unk]"]')

    # 4. Setup Microphone
    p = pyaudio.PyAudio()
    
    try:
        # Try to open the default device
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=8000,
                        input_device_index=DEVICE_INDEX)
    except Exception as e:
        print(f"Error opening microphone: {e}")
        print("Try running 'audio_bar_visualizer.py' to find your device ID.")
        sys.exit(1)

    print("-" * 50)
    print(f"Listening for: '{WAKE_PHRASE}'")
    print("Speak naturally. Press Ctrl+C to stop.")
    print("-" * 50)

    stream.start_stream()

    try:
        while True:
            # Read data from microphone
            data = stream.read(4000, exception_on_overflow=False)
            
            if len(data) == 0:
                break
            
            # Feed data to the recognizer
            if rec.AcceptWaveform(data):
                # We get a full result
                result_json = json.loads(rec.Result())
                text = result_json.get('text', '')
                
                if text == WAKE_PHRASE:
                    print(f"✅ WAKE WORD DETECTED: {text.upper()}")
                    # Add your trigger code here (e.g., turn on LED, play sound)
            else:
                # Partial result (usually not needed for wake words, but good for debugging)
                # partial = json.loads(rec.PartialResult())
                pass

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        print("Cleaning up...")
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()
