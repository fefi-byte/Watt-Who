
import asyncio

from app.config import load_config
from app.detection import DeltaPDetector
from app.ha_integration import sensor_data_stream
from app.storage import Storage


async def main() -> None:
    config = load_config()
    detector = DeltaPDetector(config.detection)
    storage = Storage()
    async for sample in sensor_data_stream(config.detection.sample_interval_s):
        events = detector.process(
            pv_power=sample.get("pv", 0.0),
            net_power=sample.get("net"),
            grid_import=sample.get("grid_import"),
            grid_export=sample.get("grid_export"),
        )
        for event in events:
            storage.insert_event(event)
            print(f"Ereignis: {event.delta_w:.1f} W")


if __name__ == "__main__":
    asyncio.run(main())
