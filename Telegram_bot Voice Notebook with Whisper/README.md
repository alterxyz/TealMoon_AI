# Telegram Speech-to-Text Bot

A simple Telegram bot that converts voice messages to text using Local OpenAI's [Whisper](https://github.com/openai/whisper)

## Features

- Your audio files are stored locally where the bot is hosted
- Transcribe voice messages to text, and it is editable!
- Jump to a specific time in the audio file by clicking on the timestamp on the transcription message

## Usage

1. Send a voice message to the bot
2. The bot will reply with the transcribed text
3. You can edit the text and send it back to the bot (reply to the bot's message)
4. The transcribed text will be updated with your edited text, as well as the text file.

## Requirements

- Python 3.x
- CUDA 12.1
- pip install -r requirements.txt
- Your Telegram Bot Token

## Deployment

1. Clone this repository
2. Install the requirements
3. Set your Telegram Bot Token in `bot.py`
4. Run `python bot.py`

Modify the `audio_whisper.py` file to change the model path and other configurations.
The default parameters are medium model(required 8GB GPU memory), device is CUDA(able to switch to CPU), and language is Chinese.

## Future Work

- [ ] Add GPT refinement to the transcribed text.

GLHF!
