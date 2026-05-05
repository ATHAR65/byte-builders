from __future__ import annotations

from pathlib import Path
import tempfile

import numpy as np
import sounddevice as sd
import soundfile as sf


def record_wav(seconds: int, sample_rate: int) -> Path:
  frames = int(seconds * sample_rate)
  audio = sd.rec(frames, samplerate=sample_rate, channels=1, dtype="float32")
  sd.wait()
  audio = np.squeeze(audio)
  tmp = Path(tempfile.gettempdir()) / "jarvis_input.wav"
  sf.write(tmp, audio, sample_rate)
  return tmp


def play_wav(path: Path) -> None:
  data, sample_rate = sf.read(path, dtype="float32")
  sd.play(data, sample_rate)
  sd.wait()
