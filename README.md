# Kinyarwanda Voice Assistant (Robo)

A voice assistant that understands and responds in Kinyarwanda language using the KinyaWhisper ASR model and gTTS for speech synthesis.

## Project Structure

- `voice_assistant.py`: Main application that integrates all components
- `asr.py`: Speech recognition component using KinyaWhisper
- `tts.py`: Text-to-speech component using gTTS
- `nlp.py`: Natural language processing component with Q&A matching
- `record_samples.py`: Tool for recording sample audio for testing and training
- `manualRecording.py`: Original script for recording samples

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

For PyAudio installation on different platforms:

- **Windows**: `pip install pyaudio`
- **macOS**: `brew install portaudio` then `pip install pyaudio`
- **Linux**: `sudo apt-get install python3-pyaudio` or `sudo apt-get install portaudio19-dev` then `pip install pyaudio`

### 2. Download Model

The system will automatically download the KinyaWhisper model from Hugging Face on first run:
- `benax-rw/KinyaWhisper` - Kinyarwanda ASR model

### 3. Record Voice Samples (Optional)

You can record your own voice samples to test the system:

```bash
python record_samples.py
```

This will guide you through recording questions and answers in Kinyarwanda.

## Running the Voice Assistant

To start the voice assistant:

```bash
python voice_assistant.py
```

Choose option 1 to run the assistant in interactive mode, or option 2 to test with a pre-recorded audio file.

## Usage

1. The assistant will greet you in Kinyarwanda
2. Speak your question or command in Kinyarwanda
3. The assistant will process your speech, match it to the closest question in its database, and respond
4. To exit, say "gusoza" (finish) or "murabeho" (goodbye)

## Extending the Assistant

### Adding New Q&A Pairs

You can add new question-answer pairs to the `qa_pairs` dictionary in `nlp.py`:

```python
qa_pairs.update({
    "new question": "new answer",
    "another question": "another answer"
})
```

After adding new pairs, record voice samples using `record_samples.py` for testing.

### Improving Speech Recognition

The KinyaWhisper model provides basic Kinyarwanda speech recognition. For better results:

1. Record in a quiet environment
2. Speak clearly and at a normal pace
3. Use proper Kinyarwanda pronunciation

## Troubleshooting

- **No sound output**: Check your speaker settings and ensure pygame is working properly
- **Poor recognition**: Try recording in a quieter environment or adjust the `SILENCE_THRESHOLD` in `voice_assistant.py`
- **Model download issues**: Ensure you have a good internet connection for the first run

## Credits

- ASR Model: [benax-rw/KinyaWhisper](https://huggingface.co/benax-rw/KinyaWhisper)
- TTS: Google Text-to-Speech (gTTS)