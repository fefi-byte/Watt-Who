from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    import json as yaml  # type: ignore


@dataclass
class SourceConfig:
    grid_power_sensor: str | None = None
    grid_import_sensor: str | None = None
    grid_export_sensor: str | None = None
    pv_power_sensor: str = ""


@dataclass
class DetectionConfig:
    sample_interval_s: int = 3
    min_delta_w: float = 60
    min_event_duration_s: int = 10
    deadband_w: float = 40
    hysteresis_w: float = 15


@dataclass
class ClassificationConfig:
    confidence_threshold: float = 0.7


@dataclass
class LocaleConfig:
    language: str = "de"


@dataclass
class AppConfig:
    sources: SourceConfig
    detection: DetectionConfig = field(default_factory=DetectionConfig)
    classification: ClassificationConfig = field(default_factory=ClassificationConfig)
    locale: LocaleConfig = field(default_factory=LocaleConfig)


def load_config(path: str = "config.yaml") -> AppConfig:
    file = Path(path)
    if not file.exists():
        sources: dict[str, Any] = {
            "grid_power_sensor": input("Netzleistung Sensor-ID: "),
            "pv_power_sensor": input("PV-Leistung Sensor-ID: "),
        }
        data = {"sources": sources}
        file.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    else:
        data = yaml.safe_load(file.read_text(encoding="utf-8")) or {}
    return AppConfig(
        sources=SourceConfig(**data.get("sources", {})),
        detection=DetectionConfig(**data.get("detection", {})),
        classification=ClassificationConfig(**data.get("classification", {})),
        locale=LocaleConfig(**data.get("locale", {})),
    )
