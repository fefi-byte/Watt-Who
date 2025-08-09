import pytest

from app.config import DetectionConfig
from app.detection import DeltaPDetector


def test_delta_p_detector_with_pv_zero_feed() -> None:
    config = DetectionConfig()
    det = DeltaPDetector(config)
    samples = [
        {"pv": 0.0, "net": 0.0},
        {"pv": 0.0, "net": 1200.0},  # Gerät an
        {"pv": 1200.0, "net": 0.0},  # PV deckt Last
        {"pv": 1200.0, "net": -1200.0},  # Gerät aus bei PV-Erzeugung
        {"pv": 0.0, "net": 0.0}
    ]
    events = []
    for s in samples:
        events.extend(det.process(pv_power=s["pv"], net_power=s["net"]))
    assert len(events) == 2
    assert events[0].delta_w == pytest.approx(1200.0)
    assert events[1].delta_w == pytest.approx(-1200.0)
