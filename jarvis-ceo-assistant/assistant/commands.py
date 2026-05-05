from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class CommandResult:
  handled: bool
  reply: str = ""
  should_exit: bool = False
  speak: bool = True
  passthrough_to_llm: bool = False


def command_help() -> str:
  return (
    "Available commands:\n"
    "/help - show all commands\n"
    "/modes - list agent modes\n"
    "/mode <MODE_NAME> - set fixed mode\n"
    "/mode auto - return to auto routing\n"
    "/status - current config/state\n"
    "/brief - quick daily CEO briefing\n"
    "/study - generate today's study sprint\n"
    "/webdev - generate today's webdev action list\n"
    "/social - generate today's content action list\n"
    "/voice on|off - enable/disable TTS playback\n"
    "/record <seconds> - change recording duration\n"
    "/clearlog - clear session log file\n"
    "/time - current local time\n"
    "/exit - close assistant\n"
    "\nDirect mode examples:\n"
    "PHYSICS_AGENT: kinematics parao\n"
    "WEBDEV_AGENT: portfolio improve karo\n"
    "SOCIAL_AGENT: reels caption do"
  )


def handle_local_command(
  user_text: str,
  *,
  current_mode: str | None,
  speak_enabled: bool,
  record_seconds: int,
  log_file: Path,
) -> tuple[CommandResult, str | None, bool, int]:
  text = user_text.strip()
  if not text.startswith("/"):
    return CommandResult(handled=False), current_mode, speak_enabled, record_seconds

  parts = text.split()
  cmd = parts[0].lower()
  arg = " ".join(parts[1:]).strip()

  if cmd in {"/help", "/commands"}:
    return CommandResult(True, command_help(), speak=False), current_mode, speak_enabled, record_seconds
  if cmd == "/modes":
    return (
      CommandResult(
        True,
        "Modes: MATH_AGENT, PHYSICS_AGENT, CS_AGENT, ICT_AGENT, ENGLISH_AGENT, "
        "ISLAMIAT_AGENT, PAKISTAN_STUDIES_AGENT, SCIENCE_AGENT, WEBDEV_AGENT, SOCIAL_AGENT, GENERAL",
        speak=False,
      ),
      current_mode,
      speak_enabled,
      record_seconds,
    )
  if cmd == "/mode":
    if not arg:
      return CommandResult(True, "Usage: /mode <MODE_NAME> OR /mode auto", speak=False), current_mode, speak_enabled, record_seconds
    if arg.lower() == "auto":
      return CommandResult(True, "Routing set to auto mode.", speak=False), None, speak_enabled, record_seconds
    return CommandResult(True, f"Fixed mode set to {arg.upper()}", speak=False), arg.upper(), speak_enabled, record_seconds
  if cmd == "/status":
    mode_label = current_mode if current_mode else "AUTO"
    return (
      CommandResult(
        True,
        f"Status -> mode: {mode_label}, voice: {'on' if speak_enabled else 'off'}, record_seconds: {record_seconds}",
        speak=False,
      ),
      current_mode,
      speak_enabled,
      record_seconds,
    )
  if cmd == "/voice":
    if arg.lower() == "off":
      return CommandResult(True, "Voice playback turned OFF.", speak=False), current_mode, False, record_seconds
    if arg.lower() == "on":
      return CommandResult(True, "Voice playback turned ON.", speak=False), current_mode, True, record_seconds
    return CommandResult(True, "Usage: /voice on|off", speak=False), current_mode, speak_enabled, record_seconds
  if cmd == "/record":
    try:
      secs = int(arg)
      secs = max(3, min(30, secs))
      return CommandResult(True, f"Recording duration set to {secs} seconds.", speak=False), current_mode, speak_enabled, secs
    except Exception:
      return CommandResult(True, "Usage: /record <seconds 3-30>", speak=False), current_mode, speak_enabled, record_seconds
  if cmd == "/clearlog":
    log_file.write_text("", encoding="utf-8")
    return CommandResult(True, "Session log cleared.", speak=False), current_mode, speak_enabled, record_seconds
  if cmd == "/time":
    now = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    return CommandResult(True, f"Current local time: {now}", speak=False), current_mode, speak_enabled, record_seconds
  if cmd == "/brief":
    return CommandResult(True, "Sab kuch batao", passthrough_to_llm=True), current_mode, speak_enabled, record_seconds
  if cmd == "/study":
    return (
      CommandResult(True, "Aaj ka study sprint banao with 3 focused sessions for university exams.", passthrough_to_llm=True),
      current_mode,
      speak_enabled,
      record_seconds,
    )
  if cmd == "/webdev":
    return (
      CommandResult(True, "Aaj ke web development tasks do for freelance growth and portfolio output.", passthrough_to_llm=True),
      current_mode,
      speak_enabled,
      record_seconds,
    )
  if cmd == "/social":
    return (
      CommandResult(True, "Aaj ka social media content plan do with reel idea, caption, and CTA.", passthrough_to_llm=True),
      current_mode,
      speak_enabled,
      record_seconds,
    )
  if cmd == "/exit":
    return CommandResult(True, "Session ended.", should_exit=True, speak=False), current_mode, speak_enabled, record_seconds

  return CommandResult(True, "Unknown command. Type /help", speak=False), current_mode, speak_enabled, record_seconds
