from __future__ import annotations

import asyncio
from typing import AsyncIterator, Dict


async def sensor_data_stream(sample_interval: int) -> AsyncIterator[Dict[str, float]]:
    """Mock-Sensorwerte. Später MQTT/WS/REST."""
    pv = 0.0
    net = 0.0
    while True:
        await asyncio.sleep(sample_interval)
        yield {"pv": pv, "net": net}
