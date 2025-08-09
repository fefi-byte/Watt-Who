from __future__ import annotations

from collections import deque
from statistics import median
from typing import Deque


def clamp_deadband(value: float, deadband: float, hysteresis: float, prev: float) -> float:
    """Klemm kleine Leistungen um Null."""
    if abs(value) <= deadband:
        return 0.0
    if prev == 0.0 and abs(value) < deadband + hysteresis:
        return 0.0
    if prev != 0.0 and abs(value) < deadband - hysteresis:
        return 0.0
    return value


class MedianFilter:
    """Gleitender Median."""

    def __init__(self, size: int = 3) -> None:
        self.size = size
        self.values: Deque[float] = deque(maxlen=size)

    def add(self, value: float) -> float:
        self.values.append(value)
        if len(self.values) < self.size:
            return value
        return float(median(self.values))
