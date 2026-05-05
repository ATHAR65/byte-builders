from __future__ import annotations

from assistant.prompts import AGENT_MODE_HINTS


def detect_mode(user_text: str) -> str:
  text = user_text.lower()
  if "sab kuch batao" in text or "full briefing" in text or "daily briefing" in text:
    return "DAILY_BRIEFING"
  for mode in AGENT_MODE_HINTS:
    if mode.lower() in text.lower():
      return mode
  if "physics" in text:
    return "PHYSICS_AGENT"
  if "math" in text:
    return "MATH_AGENT"
  if "c language" in text or "programming" in text or "code" in text:
    return "CS_AGENT"
  if "figma" in text or "website" in text or "webdev" in text:
    return "WEBDEV_AGENT"
  if "upload" in text or "caption" in text or "social" in text:
    return "SOCIAL_AGENT"
  return "GENERAL"


def mode_instruction(mode: str) -> str:
  if mode == "DAILY_BRIEFING":
    return (
      "Give today's full CEO briefing in Urdu-English mix with four sections only: "
      "academic topics, social tasks, webdev progress, motivation."
    )
  return AGENT_MODE_HINTS.get(mode, "Respond as CEO agent with actionable guidance.")
