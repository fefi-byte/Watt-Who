from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Event:
    timestamp: float
    delta_w: float
    duration_s: float
    device_id: Optional[int] = None
    confidence: float = 1.0
