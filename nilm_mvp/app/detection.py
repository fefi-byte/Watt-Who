from __future__ import annotations

import time
from typing import List, Optional, Protocol

from .models import Event
from .utils import MedianFilter, clamp_deadband


class DetectionConfigLike(Protocol):
    """Minimal Config Interface"""

    sample_interval_s: int
    min_delta_w: float
    min_event_duration_s: int
    deadband_w: float
    hysteresis_w: float


class DeltaPDetector:
    """Einfache ΔP-Event-Detektion."""

    def __init__(self, config: DetectionConfigLike) -> None:
        self.min_delta = config.min_delta_w
        self.sample_interval = config.sample_interval_s
        self.deadband = config.deadband_w
        self.hysteresis = config.hysteresis_w
        self.prev_clamped = 0.0
        self.prev_power: Optional[float] = None
        self.median = MedianFilter(3)

    def process(
        self,
        pv_power: float = 0.0,
        net_power: Optional[float] = None,
        grid_import: Optional[float] = None,
        grid_export: Optional[float] = None,
    ) -> List[Event]:
        """Verarbeite einen neuen Messpunkt und liefere ggf. Events."""

        if net_power is not None:
            raw = pv_power + net_power
        else:
            gi = grid_import or 0.0
            ge = grid_export or 0.0
            raw = pv_power + gi - ge
        clamped = clamp_deadband(raw, self.deadband, self.hysteresis, self.prev_clamped)
        self.prev_clamped = clamped
        smoothed = self.median.add(clamped)

        events: List[Event] = []
        if self.prev_power is not None:
            delta = smoothed - self.prev_power
            if abs(delta) >= self.min_delta:
                events.append(
                    Event(
                        timestamp=time.time(),
                        delta_w=delta,
                        duration_s=self.sample_interval,
                        confidence=1.0,
                    )
                )
        self.prev_power = smoothed
        return events
