# from transformers import pipeline

# asr = pipeline(model="benax-rw/KinyaWhisper")

# transcription = asr()

from transformers import pipeline
import torch
import os

class KinyarwandaASR:
    def __init__(self):
        # Initialize the ASR model
        print("Loading KinyaWhisper ASR model...")
        try:
            # Use CUDA if available, otherwise CPU
            device = 0 if torch.cuda.is_available() else -1
            self.asr = pipeline(model="benax-rw/KinyaWhisper", device=device)
            print("ASR model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Attempting to load with specific cache directory...")
            # Try with specific cache directory
            cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface")
            os.makedirs(cache_dir, exist_ok=True)
            self.asr = pipeline(model="benax-rw/KinyaWhisper", device=-1, cache_dir=cache_dir)
            print("ASR model loaded with alternate configuration.")
    
    def transcribe_audio(self, audio_file_path):
        """
        Transcribe an audio file using the KinyaWhisper model
        
        Parameters:
        - audio_file_path: Path to the audio file to transcribe
        
        Returns:
        - Transcribed text in Kinyarwanda
        """
        try:
            result = self.asr(audio_file_path)
            transcription = result["text"]
            return transcription.lower()
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return ""

# Example usage
if __name__ == "__main__":
    asr = KinyarwandaASR()
    test_file = "test_audio.wav"  # Replace with your test file
    transcription = asr.transcribe_audio(test_file)
    print(f"Transcription: {transcription}")