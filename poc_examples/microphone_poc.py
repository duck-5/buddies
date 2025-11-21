import pyaudio
import numpy as np
import time
import sys

# --- Configuration ---
CHUNK = 1024        # Number of audio frames per buffer
FORMAT = pyaudio.paInt16 # Audio format (16-bit integers)
CHANNELS = 1        # Mono audio
RATE = 44100        # Sample rate (samples per second)
BAR_LENGTH = 50     # Maximum length of the visualization bar
SILENCE_THRESHOLD = 500 # Threshold to filter out very low noise (adjust this if needed)

def get_audio_device_info():
    """Prints a list of available audio input devices."""
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    print("--- Available Audio Input Devices ---")
    
    input_devices = []
    
    for i in range(0, numdevices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        
        # Check if the device supports input channels
        if device_info.get('maxInputChannels') > 0:
            input_devices.append({
                'index': i,
                'name': device_info.get('name'),
                'input_channels': device_info.get('maxInputChannels')
            })
            print(f"Device ID {i}: {device_info.get('name')} (Max Input Channels: {device_info.get('maxInputChannels')})")
            
    p.terminate()
    return input_devices

def visualize_audio_input(device_index=None):
    """
    Captures audio from the specified device and displays the volume as a bar.
    
    :param device_index: The index of the input device to use.
    """
    p = pyaudio.PyAudio()

    # If no device index is provided, try to automatically select the default input device
    if device_index is None:
        try:
            device_index = p.get_default_input_device_info()['index']
            print(f"\nUsing default input device: ID {device_index}")
        except OSError:
            print("\nError: No default input device found. Please specify a device index.")
            p.terminate()
            return

    # Check if the device index is valid
    try:
        device_info = p.get_device_info_by_index(device_index)
        print(f"Starting stream on device: {device_info['name']}")
    except IndexError:
        print(f"Error: Invalid device index {device_index}.")
        p.terminate()
        return

    # Open the audio stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=device_index)

    print("\n--- Listening... (Press Ctrl+C to Stop) ---")
    print(f"Max Volume: {2**15 - 1}") # Max theoretical 16-bit PCM value

    try:
        while True:
            # Read audio data from the microphone
            data = stream.read(CHUNK, exception_on_overflow=False)
            
            # Convert audio data from bytes to a 16-bit integer numpy array
            audio_data = np.frombuffer(data, dtype=np.int16)
            
            # --- FIX IS HERE: Cast to int64 to prevent overflow when squaring ---
            # 16-bit int squared can easily exceed 32,767, causing negative numbers
            audio_data_long = audio_data.astype(np.int64)
            
            # Calculate the Root Mean Square (RMS) volume level
            rms = np.sqrt(np.mean(audio_data_long**2))
            
            # Normalize the RMS value to a max of 32767 (max for 16-bit signed integer)
            normalized_rms = rms / (2**15 - 1)
            
            # Apply a threshold to zero out very faint noise
            if rms < SILENCE_THRESHOLD:
                 normalized_rms = 0
            
            # Scale the normalized RMS value to the length of the visualization bar
            bar_scale = int(normalized_rms * BAR_LENGTH)
            
            # Create the visualization bar string
            bar = '█' * bar_scale
            space = ' ' * (BAR_LENGTH - bar_scale)
            
            # Prepare the output line: [Volume Value] | [Bar Visualization]
            output_line = f"[{int(rms):<5}] | {bar}{space} |"
            
            # Print the line and use carriage return (\r) to overwrite the previous line
            sys.stdout.write(f"\r{output_line}")
            sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n\nStopping stream...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        # Stop and close the stream and PyAudio object gracefully
        if 'stream' in locals() and stream.is_active():
            stream.stop_stream()
            stream.close()
        p.terminate()
        print("Cleanup complete. Exiting.")


if __name__ == "__main__":
    print("Lol hi")
    # 1. Show available devices to the user
    devices = get_audio_device_info()
    
    if not devices:
        print("No input devices found. Cannot proceed.")
    else:
        # 2. Prompt the user to select a device or use the default
        selected_index = None
        
        while selected_index is None:
            user_input = input("\nEnter the Device ID you want to use (or press Enter for default): ").strip()
            
            if not user_input:
                # Use default device (will be handled inside the visualization function)
                visualize_audio_input(None)
                break
            
            try:
                index = int(user_input)
                # Check if the entered index is in the list of valid input devices
                if any(d['index'] == index for d in devices):
                    visualize_audio_input(index)
                    break
                else:
                    print("Invalid ID. Please enter one of the listed Device IDs.")
            except ValueError:
                print("Invalid input. Please enter a number or press Enter.")

