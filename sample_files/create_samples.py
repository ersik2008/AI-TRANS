"""
Create sample files for testing
"""
import wave
import os
from pathlib import Path

def create_sample_audio():
    """Create a simple WAV file for testing"""
    output_path = Path(__file__).parent / "sample_audio.wav"
    
    sample_rate = 44100
    duration = 3  # seconds
    frequency = 440  # A4 note
    
    import math
    
    frames = []
    for i in range(sample_rate * duration):
        sample = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
        frames.append(sample.to_bytes(2, byteorder='little', signed=True))
    
    with wave.open(str(output_path), 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(frames))
    
    print(f"✅ Created: {output_path}")

if __name__ == "__main__":
    create_sample_audio()
    print("Sample files ready!")
