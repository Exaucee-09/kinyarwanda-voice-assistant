import os
import tempfile
import time
import wave
import pyaudio
import threading
import pygame
from pathlib import Path

# Import our custom components
from asr import KinyarwandaASR
from tts import KinyarwandaTTS
from nlp import KinyarwandaNLP

class KinyarwandaVoiceAssistant:
    def __init__(self):
        """Initialize the Kinyarwanda Voice Assistant"""
        print("Initializing Kinyarwanda Voice Assistant...")
        
        # Create necessary directories
        Path("recordings").mkdir(exist_ok=True)
        Path("tts_cache").mkdir(exist_ok=True)
        
        # Initialize components
        self.asr = KinyarwandaASR()
        self.tts = KinyarwandaTTS()
        self.nlp = KinyarwandaNLP()
        
        # Recording settings
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.SILENCE_THRESHOLD = 800  # Adjust based on your microphone
        self.RECORD_SECONDS = 5
        
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        
        # Initialize pygame for button sounds
        pygame.mixer.init()
        
        print("Voice Assistant initialized and ready!")
        
    def _play_sound(self, sound_type):
        """Play a system sound"""
        if sound_type == "start":
            self.tts.speak("Ndateze amatwi")  # "I'm listening"
        elif sound_type == "processing":
            self.tts.speak("Ndimo gutanga igisubizo")  # "Processing your request"
            
    def record_audio(self):
        """Record audio from microphone"""
        print("Recording... Speak now!")
        self._play_sound("start")
        
        # Open a temporary file to store the recording
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_filename = temp_file.name
        temp_file.close()
        
        # Start recording
        stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        frames = []
        silence_counter = 0
        
        # Record for a maximum of RECORD_SECONDS
        for _ in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)
            
            # Check for silence to automatically stop recording
            amplitude = max(abs(int.from_bytes(data[i:i+2], byteorder='little', signed=True)) 
                            for i in range(0, len(data), 2))
            
            if amplitude < self.SILENCE_THRESHOLD:
                silence_counter += 1
            else:
                silence_counter = 0
                
            # Stop after 1 second of silence
            if silence_counter > self.RATE / self.CHUNK:
                break
        
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        
        # Save the recording to a WAV file
        with wave.open(temp_filename, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
        
        print(f"Recording saved to {temp_filename}")
        return temp_filename
        
    def process_command(self, audio_file):
        """Process the voice command"""
        self._play_sound("processing")
        
        # Transcribe audio
        print("Transcribing audio...")
        transcription = self.asr.transcribe_audio(audio_file)
        print(f"Transcription: {transcription}")
        
        if not transcription:
            response = "Sinumvise neza. Ushobora kongera kubivuga?"  # I didn't hear clearly. Could you repeat?
        else:
            # Get response from NLP
            response = self.nlp.find_answer(transcription)
            
        print(f"Response: {response}")
        
        # Speak the response
        self.tts.speak(response)
        
        return transcription, response
        
    def run_assistant(self):
        """Run the voice assistant in a continuous loop"""
        print("Kinyarwanda Voice Assistant is running!")
        print("Say something in Kinyarwanda...")
        
        self.tts.speak("Nitwa Robo, umufasha ukoresha ikinyarwanda. Mbwira icyo ushaka.")
        
        try:
            while True:
                # Wait for 1 second before starting a new recording
                time.sleep(1)
                
                # Record audio
                audio_file = self.record_audio()
                
                # Process the command
                transcription, response = self.process_command(audio_file)
                
                # Clean up the temporary file
                os.unlink(audio_file)
                
                # If user says "stop" or "bye" in Kinyarwanda, exit
                if "gusoza" in transcription.lower() or "murabeho" in transcription.lower():
                    self.tts.speak("Murabeho! Ndishimiye kukubona.")  # Goodbye! Happy to see you.
                    break
                    
        except KeyboardInterrupt:
            print("\nStopping voice assistant...")
        finally:
            self.audio.terminate()
            print("Voice assistant stopped.")
    
    def test_assistant(self):
        """Test the assistant with a sample recording"""
        test_file = input("Enter the path to a test audio file: ")
        if os.path.exists(test_file):
            transcription, response = self.process_command(test_file)
            print(f"Test Result - Transcription: {transcription}, Response: {response}")
        else:
            print(f"File not found: {test_file}")

if __name__ == "__main__":
    assistant = KinyarwandaVoiceAssistant()
    
    print("\nChoose an option:")
    print("1. Run the voice assistant")
    print("2. Test with a sample recording")
    
    choice = input("Enter your choice (1/2): ")
    
    if choice == "1":
        assistant.run_assistant()
    elif choice == "2":
        assistant.test_assistant()
    else:
        print("Invalid choice. Exiting.")