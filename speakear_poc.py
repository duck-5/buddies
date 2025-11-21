import pyaudio
import numpy as np
import sys

# --- Configuration ---
CHUNK = 1024            # Frames per buffer
FORMAT = pyaudio.paInt16 
CHANNELS = 1            # Mono
RATE = 44100            # Hz
BAR_LENGTH = 50         # Visualizer size
FREQUENCY = 440.0       # Test tone pitch (Hz) - A4 Note
PULSE_SPEED = 1.0       # How fast the volume fades in/out (Hz)

def get_output_devices():
    """Prints a list of available audio OUTPUT devices."""
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    print("--- Available Audio Output Devices (Speakers) ---")
    
    output_devices = []
    for i in range(0, numdevices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        
        # Check if the device supports OUTPUT channels
        if device_info.get('maxOutputChannels') > 0:
            output_devices.append({
                'index': i,
                'name': device_info.get('name')
            })
            print(f"Device ID {i}: {device_info.get('name')}")
            
    p.terminate()
    return output_devices

def test_speaker_output(device_index=None):
    """Generates a tone and plays it through the selected speaker."""
    p = pyaudio.PyAudio()

    if device_index is None:
        try:
            device_info = p.get_default_output_device_info()
            device_index = device_info['index']
            print(f"\nUsing default output device: ID {device_index}")
        except OSError:
            print("Error: No default output device found.")
            p.terminate()
            return

    try:
        device_info = p.get_device_info_by_index(device_index)
        print(f"Testing Output Device: {device_info['name']}")
    except IndexError:
        print("Invalid device ID.")
        p.terminate()
        return

    # Open stream for Output
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK,
                    output_device_index=device_index)

    print("\n--- Playing Test Tone (440Hz) ---")
    print("(Press Ctrl+C to Stop)")

    frame_count = 0
    
    try:
        while True:
            # 1. Generate Time Array for this chunk
            # We track frame_count globally to ensure the sine wave is continuous 
            # and doesn't "pop" or click between chunks.
            t = np.arange(frame_count, frame_count + CHUNK) / RATE
            
            # 2. Generate Sine Wave (Tone)
            # sin(2 * pi * freq * time)
            tone = np.sin(2 * np.pi * FREQUENCY * t)
            
            # 3. Generate LFO (Low Frequency Oscillator) for pulsing volume
            # Oscillates between 0.1 and 1.0 so it doesn't go completely silent
            volume_pulse = (np.sin(2 * np.pi * PULSE_SPEED * t) + 1) / 2
            volume_pulse = 0.1 + (volume_pulse * 0.9) 
            
            # 4. Combine and Convert to 16-bit Integer
            # Multiply by 32000 (slightly less than max 32767 to avoid clipping)
            audio_data = (tone * volume_pulse * 32000).astype(np.int16)
            
            # 5. Play the sound
            # tobytes() is required for PyAudio
            stream.write(audio_data.tobytes())
            
            # 6. Visualization Logic (Same as before)
            # We calculate RMS of the data we just generated
            audio_data_long = audio_data.astype(np.int64)
            rms = np.sqrt(np.mean(audio_data_long**2))
            
            normalized_rms = rms / 32767
            bar_scale = int(normalized_rms * BAR_LENGTH)
            bar = '█' * bar_scale
            space = ' ' * (BAR_LENGTH - bar_scale)
            
            sys.stdout.write(f"\r[{int(rms):<5}] | {bar}{space} |")
            sys.stdout.flush()
            
            frame_count += CHUNK

    except KeyboardInterrupt:
        print("\n\nStopping test...")
    finally:
        if 'stream' in locals() and stream.is_active():
            stream.stop_stream()
            stream.close()
        p.terminate()

if __name__ == "__main__":
    devices = get_output_devices()
    
    if not devices:
        print("No speakers found.")
    else:
        user_input = input("\nEnter Device ID to test (or Enter for default): ").strip()
        if not user_input:
            test_speaker_output(None)
        else:
            try:
                idx = int(user_input)
                if any(d['index'] == idx for d in devices):
                    test_speaker_output(idx)
                else:
                    print("Invalid ID.")
            except ValueError:
                print("Invalid input.")
