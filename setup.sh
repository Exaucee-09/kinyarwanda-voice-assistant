#!/bin/bash

echo "Setting up Kinyarwanda Voice Assistant..."

# Install dependencies
echo "Installing required packages..."
pip install transformers==4.34.0
pip install torch torchaudio
pip install wavio==0.0.7
pip install pygame==2.5.2
pip install gtts==2.3.2

# PyAudio requires portaudio development libraries
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Installing portaudio for Linux..."
    sudo apt-get update
    sudo apt-get install -y portaudio19-dev python3-pyaudio
    pip install pyaudio==0.2.13
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Installing portaudio for macOS..."
    brew install portaudio
    pip install pyaudio==0.2.13
else
    echo "Installing PyAudio..."
    pip install pyaudio==0.2.13
fi

# Test imports
echo "Testing imports..."
python -c "import torch; import transformers; import pygame; import gtts; print('Basic imports successful!')"

echo "Setup complete!"
echo "Run 'python voice_assistant.py' to start the voice assistant."