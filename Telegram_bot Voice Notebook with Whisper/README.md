# Telegram Speech-to-Text Bot

A simple Telegram bot that converts voice messages to text using Local or OpenAI-API [Whisper](https://github.com/openai/whisper)

## Features

- Your audio files are stored locally where the bot is hosted (when using Local Whisper)
- Transcribe voice messages to text, and it is editable!
- Jump to a specific time in the audio file by clicking on the timestamp on the transcription message
- Also you can use OpenAI-API to transcribe the voice message, it is fast and do not need a GPU locally

## Usage

1. Send a voice message to the bot
2. The bot will reply with the transcribed text
3. You can edit the text and send it back to the bot (reply to the bot's message)
4. The transcribed text will be updated with your edited text, as well as the text file.

## Requirements

- Python 3.x
- CUDA 12.1
- `pip install -r requirements.txt` or manually install the following packages:
    - `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`
    - then `pip install -U openai-whisper`
    - `pip install python-telegram-bot --upgrade`
    - *Skip the first two and use* `pip install openai` *if you want to use OpenAI-API*
- Your Telegram Bot Token

## Deployment

1. Clone this repository
2. Install the requirements
3. Set your Telegram Bot Token in `bot.py`, and your OpenAI-API key in `audio_whisper_openai_api.py`
4. Run `python bot.py`

Modify the `audio_whisper.py` file to change the model path and other configurations.

The default parameters are medium model(required 8GB GPU memory), device is CUDA(able to switch to CPU), and language is Chinese.

## Notes for OpenAI-API users

- OpenAI said "We do not train on your business data (data from ChatGPT Team, ChatGPT Enterprise, or our API Platform)" at <https://openai.com/enterprise-privacy/>
- But they do store it temporarily: "OpenAI may securely retain API inputs and outputs for up to 30 days to provide the services and to identify abuse"
- Use it at your own risk.

## Future Work

- [ ] Add GPT refinement to the transcribed text.

GLHF!
