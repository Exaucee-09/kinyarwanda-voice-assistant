import sounddevice as sd
import wavio
import time
import os

# Your QA Pairs (combine all into one dictionary for simplicity)
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

# Create a folder to save recordings
output_folder = "recordings"
os.makedirs(output_folder, exist_ok=True)

# Set recording settings
duration = 5  # seconds per recording
fs = 44100    # sample rate

for text in qa_pairs.keys():
    print(f"\nNow recording: {text}")
    print("Recording will start in 2 seconds. Get ready...")
    time.sleep(2)

    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    filename = f"{output_folder}/{text.replace(' ', '_')}.wav"
    wavio.write(filename, recording, fs, sampwidth=2)
    print(f"Saved as {filename}")

    time.sleep(1)

    # Now recording the answer
    answer = qa_pairs[text]
    print(f"\nNow recording ANSWER: {answer}")
    print("Recording will start in 2 seconds. Get ready...")
    time.sleep(2)

    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    filename = f"{output_folder}/{answer.replace(' ', '_')}.wav"
    wavio.write(filename, recording, fs, sampwidth=2)
    print(f"Saved as {filename}")

    time.sleep(1)

print("\nAll recordings done!")
