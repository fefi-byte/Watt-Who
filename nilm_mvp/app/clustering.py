from __future__ import annotations

import numpy as np
from typing import Tuple


def cluster_events(features: np.ndarray, n_clusters: int = 2) -> Tuple[np.ndarray, np.ndarray | None]:
    """Cluster ähnliche Events. Fällt zurück auf Dummy, wenn sklearn fehlt."""
    try:
        from sklearn.cluster import KMeans
    except Exception:  # pragma: no cover - fallback
        return np.zeros(len(features)), None
    model = KMeans(n_clusters=n_clusters, n_init=10)
    labels = model.fit_predict(features)
    return labels, model.cluster_centers_
