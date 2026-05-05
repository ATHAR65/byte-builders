# Jarvis CEO Assistant (API-based, Voice + Smart Routing)

This is a separate assistant project folder, isolated from your website code.

## What it does
- Voice input (press Enter -> record)
- Speech-to-text using OpenAI transcription
- CEO agent routing for your command style:
  - `Sab kuch batao`
  - `PHYSICS_AGENT: ...`
  - `WEBDEV_AGENT: ...`
  - `SOCIAL_AGENT: ...`
- Voice reply using OpenAI TTS
- Session logging to `session-log.jsonl`

## Requirements
- Python 3.11+
- Working microphone + speaker
- OpenAI API key

## Setup
1. Open terminal in this folder:
   - `d:/byte buldiers/jarvis-ceo-assistant`
2. Create and activate virtual environment:
   - PowerShell:
     - `py -3.11 -m venv .venv`
     - `.venv\Scripts\Activate.ps1`
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Create `.env` from example:
   - copy `.env.example` to `.env`
   - set `OPENAI_API_KEY=...`

## Run
- `python run.py`

## Usage
- Type message and press Enter, or press Enter on empty line to record voice.
- Type `exit` to stop.
- Type `/help` to see command pack.

## Command examples
- `Sab kuch batao`
- `PHYSICS_AGENT: kinematics numericals karao`
- `CS_AGENT: C loops ka assignment solve karao`
- `WEBDEV_AGENT: meri portfolio landing improve karo`
- `SOCIAL_AGENT: aaj ke reel ke liye caption do`

## Built-in command pack
- `/help`
- `/modes`
- `/mode <MODE_NAME>` or `/mode auto`
- `/status`
- `/brief`
- `/study`
- `/webdev`
- `/social`
- `/voice on|off`
- `/record <seconds>`
- `/clearlog`
- `/time`
- `/exit`

## Notes
- This version is designed for stability (push-to-talk style) to reduce live audio errors.
- If you want true wake-word always-listening mode next, we can add `openWakeWord` in phase 2.
