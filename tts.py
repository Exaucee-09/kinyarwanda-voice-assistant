import os
from gtts import gTTS
import pygame
from pathlib import Path

class KinyarwandaTTS:
    def __init__(self, cache_dir="tts_cache"):
        """
        Initialize the TTS system
        
        Parameters:
        - cache_dir: Directory to cache generated TTS files
        """
        self.cache_dir = cache_dir
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize pygame for audio playback
        pygame.mixer.init()
        
        # Cache for storing generated audio
        self.audio_cache = {}
        
        # Pre-load cached files if they exist
        self._load_cached_files()
    
    def _load_cached_files(self):
        """Load any existing cached TTS files"""
        for file in os.listdir(self.cache_dir):
            if file.endswith(".mp3"):
                text = file[:-4].replace("_", " ")
                self.audio_cache[text] = os.path.join(self.cache_dir, file)
    
    def _generate_audio(self, text):
        """Generate TTS audio for the given text"""
        try:
            # Create a filename based on the text
            filename = text.replace(" ", "_") + ".mp3"
            filepath = os.path.join(self.cache_dir, filename)
            
            # Generate TTS if not already cached
            if text not in self.audio_cache:
                print(f"Generating TTS for: {text}")
                tts = gTTS(text=text, lang='sw')  # 'rw' is the language code for Kinyarwanda
                tts.save(filepath)
                self.audio_cache[text] = filepath
            
            return self.audio_cache[text]
        except Exception as e:
            print(f"Error generating TTS: {e}")
            return None
    
    def speak(self, text):
        """
        Convert text to speech and play it
        
        Parameters:
        - text: The Kinyarwanda text to speak
        """
        audio_file = self._generate_audio(text)
        if audio_file:
            try:
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except Exception as e:
                print(f"Error playing audio: {e}")
    
    def speak_from_file(self, audio_file):
        """Play audio from an existing file"""
        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Error playing audio file: {e}")

# Example usage
if __name__ == "__main__":
    tts = KinyarwandaTTS()
    test_text = "Uraho neza! Nitwa Robo, umufasha ukoresha ikinyarwanda."
    tts.speak(test_text)