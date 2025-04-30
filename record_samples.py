import sounddevice as sd
import wavio
import time
import os
from pathlib import Path
from nlp import qa_pairs

def record_samples(duration=5, sample_rate=44100, output_folder="recordings"):
    """
    Record audio samples for all QA pairs in the database
    
    Parameters:
    - duration: Duration of each recording in seconds
    - sample_rate: Audio sample rate
    - output_folder: Folder to save recordings
    """
    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Count the total number of recordings needed
    total_recordings = len(qa_pairs) * 2  # Questions and answers
    completed = 0
    
    print(f"Starting recording session for {len(qa_pairs)} QA pairs ({total_recordings} recordings total)")
    print("=" * 50)
    
    try:
        for question, answer in qa_pairs.items():
            # Create a clean filename
            q_filename = f"{output_folder}/q_{question.replace(' ', '_')}.wav"
            a_filename = f"{output_folder}/a_{answer.replace(' ', '_')}.wav"
            
            # Skip if files already exist
            if os.path.exists(q_filename) and os.path.exists(a_filename):
                print(f"Skipping existing recordings for: '{question}'")
                completed += 2
                continue
            
            # Record question
            if not os.path.exists(q_filename):
                print(f"\nRecording QUESTION: '{question}'")
                print("Get ready... Recording starts in 3 seconds")
                for i in range(3, 0, -1):
                    print(f"{i}...")
                    time.sleep(1)
                
                print("Recording NOW - Speak clearly!")
                recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
                sd.wait()
                wavio.write(q_filename, recording, sample_rate, sampwidth=2)
                print(f"Saved as {q_filename}")
                completed += 1
            
            # Record answer
            if not os.path.exists(a_filename):
                print(f"\nRecording ANSWER: '{answer}'")
                print("Get ready... Recording starts in 3 seconds")
                for i in range(3, 0, -1):
                    print(f"{i}...")
                    time.sleep(1)
                
                print("Recording NOW - Speak clearly!")
                recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
                sd.wait()
                wavio.write(a_filename, recording, sample_rate, sampwidth=2)
                print(f"Saved as {a_filename}")
                completed += 1
            
            # Show progress
            print(f"Progress: {completed}/{total_recordings} recordings ({(completed/total_recordings)*100:.1f}%)")
            
            # Ask if user wants to continue
            if completed % 10 == 0 and completed < total_recordings:
                response = input("\nDo you want to continue recording? (y/n): ")
                if response.lower() != 'y':
                    print("Recording session paused. You can continue later.")
                    break
    
    except KeyboardInterrupt:
        print("\nRecording session interrupted.")
    
    print(f"\nRecording session completed: {completed}/{total_recordings} recordings done.")

def record_single(text, is_question=True, duration=5, sample_rate=44100, output_folder="recordings"):
    """Record a single sample"""
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    prefix = "q_" if is_question else "a_"
    filename = f"{output_folder}/{prefix}{text.replace(' ', '_')}.wav"
    
    print(f"\nRecording {'QUESTION' if is_question else 'ANSWER'}: '{text}'")
    print("Get ready... Recording starts in 3 seconds")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("Recording NOW - Speak clearly!")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    wavio.write(filename, recording, sample_rate, sampwidth=2)
    print(f"Saved as {filename}")
    return filename

if __name__ == "__main__":
    print("Kinyarwanda Voice Assistant - Recording Tool")
    print("=" * 50)
    print("This tool will help you record audio samples for training the voice assistant.")
    print("You'll record both questions and answers in Kinyarwanda.")
    print("=" * 50)
    
    print("\nChoose an option:")
    print("1. Record all QA pairs")
    print("2. Record a single QA pair")
    
    choice = input("Enter your choice (1/2): ")
    
    if choice == "1":
        # Ask for recording settings
        duration = int(input("Enter recording duration in seconds (default 5): ") or "5")
        record_samples(duration=duration)
    elif choice == "2":
        # Record a single QA pair
        question = input("Enter the question in Kinyarwanda: ")
        answer = input("Enter the answer in Kinyarwanda: ")
        
        # Record both
        duration = int(input("Enter recording duration in seconds (default 5): ") or "5")
        q_file = record_single(question, is_question=True, duration=duration)
        a_file = record_single(answer, is_question=False, duration=duration)
        
        print(f"\nRecorded QA pair: {q_file} and {a_file}")
    else:
        print("Invalid choice. Exiting.")