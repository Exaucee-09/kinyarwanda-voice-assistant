# from transformers import pipeline

# asr = pipeline(model="benax-rw/KinyaWhisper")

# transcription = asr()

from transformers import pipeline
import torch

class KinyarwandaASR:
    def __init__(self):
        # Initialize the ASR model
        print("Loading KinyaWhisper ASR model...")
        self.asr = pipeline(model="benax-rw/KinyaWhisper", device=0 if torch.cuda.is_available() else -1)
        print("ASR model loaded successfully!")
    
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