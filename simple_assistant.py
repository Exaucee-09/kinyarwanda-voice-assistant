"""
Simplified Kinyarwanda Voice Assistant
Uses only essential components for easier setup
"""

import os
import time
from pathlib import Path
from transformers import pipeline
import sounddevice as sd
import wavio
import numpy as np
from gtts import gTTS
import pygame

# Initialize pygame for audio playback
pygame.mixer.init()

# QA Pairs
qa_pairs = {
    "uraho": "uraho neza, Amakuru yawe",
    "amakuru yanjye ni meza": "Ni byiza rwose, nagufasha iki",
    "amakuru": "Ni meza, urakoze kubaza. Nagufasha iki uyumunsi",
    "witwa nde": "Nitwa Robo, umufasha ukoresha ikinyarwanda.",
    "wakora iki": "Nshobora kumva no  gusubiza ikibazo mu kinyarwanda.",
    "uba he": "Ndahari hafi yawe.",
    "mwiriwe": "Mwiriwe neza!",
    "bite": "Ni byiza, urakoze. Nagufasha iki uyumunsi",
    "ufite imyaka ingahe": "Ndi robot, sinagira imyaka.",
    "ukunda iki": "Nkunda gufasha abantu no kuvugana nabo.",
    "urikunyumva neza": "Yego, ndakumva neza.",
    "ubuzima bumeze bute": "Ubuzima ni bwiza, urakoze kubaza.",
    "ufasha iki": "Nshobora kumva no  gusubiza ikibazo mu kinyarwanda.",
    "washobora kuvuga": "Yego, nshobora kuvuga neza mu Kinyarwanda.",
    "uraryama ryari": "Ndi robot, sindyama.",
    "ufite inshuti": "Ndi inshuti ya buri wese.",
    "wakora iki niba ufite ikibazo": "Nashaka ubufasha vuba.",
}

# Create necessary directories
Path("recordings").mkdir(exist_ok=True)
Path("tts_cache").mkdir(exist_ok=True)

print("Loading KinyaWhisper ASR model...")
try:
    asr = pipeline(model="benax-rw/KinyaWhisper", device=-1)  # Use CPU
    print("ASR model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Please ensure you have internet connection and try again.")
    exit(1)

def speak(text):
    """Convert text to speech and play it"""
    try:
        # Create a filename based on the text
        filename = text.replace(" ", "_") + ".mp3"
        filepath = os.path.join("tts_cache", filename)
        
        # Generate TTS if not already cached
        if not os.path.exists(filepath):
            print(f"Generating TTS for: {text}")
            tts = gTTS(text=text, lang='sw')  # 'rw' is the language code for Kinyarwanda
            tts.save(filepath)
        
        # Play the audio
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error in TTS: {e}")

def record_audio(duration=5, fs=44100):
    """Record audio from microphone"""
    print("\nRecording... Speak now!")
    
    # Record audio
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    
    # Save to a temporary file
    temp_file = os.path.join("recordings", "temp_recording.wav")
    wavio.write(temp_file, recording, fs, sampwidth=2)
    
    return temp_file

def find_answer(question):
    """Find the best matching answer for a question"""
    question = question.lower()
    
    # Try direct match
    for key in qa_pairs:
        if key in question:
            return qa_pairs[key]
    
    # Try fuzzy match
    best_match = None
    best_score = 0
    
    for key in qa_pairs:
        # Simple similarity score based on common words
        common_words = sum(1 for word in key.split() if word in question.split())
        if common_words > best_score:
            best_score = common_words
            best_match = key
    
    if best_match and best_score > 0:
        return qa_pairs[best_match]
    
    # Default response
    return "Sinumva neza icyo ushaka. Ushobora kongera kubaza mu buryo butandukanye?"

def main():
    """Main function to run the voice assistant"""
    print("Kinyarwanda Voice Assistant (Simplified)")
    print("=" * 50)
    
    # Greeting
    greeting = "Nitwa Robo, umufasha ukoresha ikinyarwanda. Mbwira icyo ushaka."
    print(f"Assistant: {greeting}")
    speak(greeting)
    
    try:
        while True:
            # Record audio
            print("\nPress Enter to start recording (5 seconds)...")
            input()
            
            audio_file = record_audio()
            
            # Transcribe
            print("Transcribing...")
            try:
                result = asr(audio_file)
                transcription = result["text"].lower()
                print(f"You said: {transcription}")
                
                # Get response
                response = find_answer(transcription)
                print(f"Assistant: {response}")
                
                # Speak response
                speak(response)
                
                # Check for exit command
                if "gusoza" in transcription or "murabeho" in transcription:
                    print("Exiting...")
                    speak("Murabeho! Ndishimiye kukubona.")
                    break
                    
            except Exception as e:
                print(f"Error processing audio: {e}")
                speak("Habaye ikibazo. Dusubize.")
                
    except KeyboardInterrupt:
        print("\nExiting voice assistant...")

if __name__ == "__main__":
    main()