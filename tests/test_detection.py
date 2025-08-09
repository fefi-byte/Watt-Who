import time
import pytest

from app.config import DetectionConfig
from app.detection import DeltaPDetector


def fake_localtime(hour: int) -> time.struct_time:
    """Hilfsfunktion für fixe Uhrzeit."""
    return time.struct_time((2024, 1, 1, hour, 0, 0, 0, 1, -1))


def test_short_pv_dip_no_event(monkeypatch) -> None:
    """Kurzer PV-Einbruch löst kein Ereignis aus."""
    monkeypatch.setattr(time, "localtime", lambda: fake_localtime(12))
    det = DeltaPDetector(DetectionConfig())
    samples = (
        [{"pv": 0.0, "net": 0.0}] * 5
        + [{"pv": 0.0, "net": 150.0}] * 2
        + [{"pv": 0.0, "net": 0.0}] * 5
    )
    events = []
    for s in samples:
        events.extend(det.process(pv_power=s["pv"], net_power=s["net"]))
    assert events == []


def test_step_triggers_event(monkeypatch) -> None:
    """Echter Leistungssprung wird erkannt."""
    monkeypatch.setattr(time, "localtime", lambda: fake_localtime(12))
    det = DeltaPDetector(DetectionConfig())
    samples = (
        [{"pv": 0.0, "net": 0.0}] * 5
        + [{"pv": 0.0, "net": 1200.0}] * 5
    )
    events = []
    for s in samples:
        events.extend(det.process(pv_power=s["pv"], net_power=s["net"]))
    assert len(events) == 1
    assert events[0].delta_w == pytest.approx(1200.0)


def test_zero_feed_stable(monkeypatch) -> None:
    """Null-Einspeisung bleibt trotz kleiner Fluktuationen stabil."""
    monkeypatch.setattr(time, "localtime", lambda: fake_localtime(12))
    det = DeltaPDetector(DetectionConfig())
    samples = [
        {"pv": 0.0, "net": 10.0},
        {"pv": 0.0, "net": -20.0},
        {"pv": 0.0, "net": 15.0},
        {"pv": 0.0, "net": -5.0},
        {"pv": 0.0, "net": 0.0},
        {"pv": 0.0, "net": 5.0},
        {"pv": 0.0, "net": -10.0},
    ]
    events = []
    for s in samples:
        events.extend(det.process(pv_power=s["pv"], net_power=s["net"]))
    assert events == []
