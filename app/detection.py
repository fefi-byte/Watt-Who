from __future__ import annotations

import logging
import time
from typing import List, Optional, Protocol

from .models import Event
from .utils import MedianFilter, clamp_deadband


class DetectionConfigLike(Protocol):
    """Minimal Config Interface"""

    sample_interval_s: int
    min_delta_w_day: float
    min_delta_w_night: float
    min_event_duration_s: int
    deadband_w: float
    hysteresis_w: float


class DeltaPDetector:
    """Einfache ΔP-Event-Detektion."""

    def __init__(self, config: DetectionConfigLike) -> None:
        self.min_delta_day = config.min_delta_w_day
        self.min_delta_night = config.min_delta_w_night
        self.sample_interval = config.sample_interval_s
        self.deadband = config.deadband_w
        self.hysteresis = config.hysteresis_w
        self.prev_clamped = 0.0
        self.prev_power: Optional[float] = None
        self.median = MedianFilter(5)
        self.last_event_ts: Optional[float] = None
        self.last_event_sign: int = 0
        self.logger = logging.getLogger(__name__)

    def _current_min_delta(self) -> float:
        """Bestimme tageszeitabhängige ΔP-Schwelle."""
        hour = time.localtime().tm_hour
        if 0 <= hour < 6 or 22 <= hour:
            return self.min_delta_night
        return self.min_delta_day

    def process(
        self,
        pv_power: float = 0.0,
        net_power: Optional[float] = None,
        grid_import: Optional[float] = None,
        grid_export: Optional[float] = None,
    ) -> List[Event]:
        """Verarbeite einen neuen Messpunkt und liefere ggf. Events."""

        if net_power is not None:
            net = net_power
            gi = ge = 0.0
        else:
            gi = grid_import or 0.0
            ge = grid_export or 0.0
            net = gi - ge
        # Deadband-Zone für geringe Netzleistungen
        if abs(net) < self.deadband:
            gi = ge = 0.0
            net = 0.0
        raw = pv_power + net
        clamped = clamp_deadband(raw, self.deadband, self.hysteresis, self.prev_clamped)
        self.prev_clamped = clamped
        smoothed = self.median.add(clamped)

        events: List[Event] = []
        if self.prev_power is not None:
            delta = smoothed - self.prev_power
            min_delta = self._current_min_delta()
            if abs(delta) >= min_delta:
                ts = time.time()
                sign = 1 if delta > 0 else -1
                # Entprellung: gleichgerichtete kleine Änderungen ignorieren
                if (
                    self.last_event_ts is not None
                    and ts - self.last_event_ts < 8
                    and sign == self.last_event_sign
                    and abs(delta) < 0.6 * min_delta
                ):
                    self.logger.debug("ΔP %sW ignoriert (Entprellung)", delta)
                else:
                    events.append(
                        Event(
                            timestamp=ts,
                            delta_w=delta,
                            duration_s=self.sample_interval,
                            confidence=1.0,
                        )
                    )
                    self.last_event_ts = ts
                    self.last_event_sign = sign
        self.prev_power = smoothed
        return events
