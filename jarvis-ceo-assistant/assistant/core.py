from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import tempfile

from dotenv import load_dotenv
from openai import OpenAI
import yaml

from assistant.audio import play_wav, record_wav
from assistant.commands import handle_local_command
from assistant.prompts import BASE_SYSTEM_PROMPT
from assistant.router import detect_mode, mode_instruction


class JarvisCEO:
  def __init__(self) -> None:
    load_dotenv()
    config_path = Path(__file__).resolve().parents[1] / "config.yaml"
    self.config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    self.client = OpenAI()
    self.name = self.config.get("assistant_name", "Jarvis")
    self.chat_model = self.config.get("chat_model", "gpt-4.1-mini")
    self.transcribe_model = self.config.get("transcribe_model", "gpt-4o-mini-transcribe")
    self.tts_model = self.config.get("tts_model", "gpt-4o-mini-tts")
    self.tts_voice = self.config.get("tts_voice", "alloy")
    self.sample_rate = int(self.config.get("sample_rate", 16000))
    self.record_seconds = int(self.config.get("record_seconds", 8))
    self.save_logs = bool(self.config.get("save_logs", True))
    self.speak_enabled = bool(self.config.get("speak_enabled", True))
    self.fixed_mode: str | None = None
    self.log_file = Path(__file__).resolve().parents[1] / "session-log.jsonl"

  def run(self) -> None:
    print(f"\n{self.name} CEO Assistant ready.")
    print("Press ENTER to speak, type text directly, or '/help' for commands.\n")
    while True:
      raw = input("You > ").strip()
      if raw.lower() == "exit":
        print("Session ended.")
        break

      if raw == "":
        print("Recording...")
        audio_file = record_wav(seconds=self.record_seconds, sample_rate=self.sample_rate)
        user_text = self._transcribe(audio_file)
        print(f"You (voice) > {user_text}")
      else:
        user_text = raw

      if not user_text:
        print("No speech detected. Try again.")
        continue

      cmd_result, self.fixed_mode, self.speak_enabled, self.record_seconds = handle_local_command(
        user_text,
        current_mode=self.fixed_mode,
        speak_enabled=self.speak_enabled,
        record_seconds=self.record_seconds,
        log_file=self.log_file,
      )
      if cmd_result.handled:
        if cmd_result.should_exit:
          print(cmd_result.reply)
          break
        if not cmd_result.passthrough_to_llm:
          print(f"{self.name} > {cmd_result.reply}\n")
          continue
        user_text = cmd_result.reply

      reply_text = self._respond(user_text)
      print(f"{self.name} > {reply_text}\n")
      if self.speak_enabled and cmd_result.speak:
        self._speak(reply_text)
      self._log_turn(user_text, reply_text)

  def _transcribe(self, audio_path: Path) -> str:
    with audio_path.open("rb") as f:
      result = self.client.audio.transcriptions.create(
        model=self.transcribe_model,
        file=f,
      )
    return (result.text or "").strip()

  def _respond(self, user_text: str) -> str:
    mode = self.fixed_mode or detect_mode(user_text)
    mode_hint = mode_instruction(mode)
    messages = [
      {"role": "system", "content": BASE_SYSTEM_PROMPT},
      {"role": "system", "content": f"Current mode: {mode}. Instruction: {mode_hint}"},
      {"role": "user", "content": user_text},
    ]
    res = self.client.chat.completions.create(
      model=self.chat_model,
      messages=messages,
      temperature=0.5,
    )
    return (res.choices[0].message.content or "").strip()

  def _speak(self, text: str) -> None:
    out_path = Path(tempfile.gettempdir()) / "jarvis_reply.wav"
    audio = self.client.audio.speech.create(
      model=self.tts_model,
      voice=self.tts_voice,
      input=text,
      response_format="wav",
    )
    audio.stream_to_file(out_path)
    play_wav(out_path)

  def _log_turn(self, user_text: str, reply_text: str) -> None:
    if not self.save_logs:
      return
    entry = {
      "time": datetime.now().isoformat(timespec="seconds"),
      "user": user_text,
      "assistant": reply_text,
    }
    with self.log_file.open("a", encoding="utf-8") as f:
      f.write(json.dumps(entry, ensure_ascii=True) + "\n")
