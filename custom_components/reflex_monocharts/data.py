"""Default demo datasets, mirroring the ones baked into the original components.

Every chart takes a ``data`` argument; when it is omitted the matching constant
here is used, so an un-parameterised chart looks exactly like the original card.
Each constant is a plain list of dicts and can be copied as the starting shape
for your own state variable.
"""

from __future__ import annotations

import datetime
import random
from typing import Any

__all__ = [
    "AREA_DATA",
    "BAR_DATA",
    "BUBBLE_DATA",
    "BULLET_DATA",
    "CANDLE_DATA",
    "COMPOSED_DATA",
    "DONUT_DATA",
    "FUNNEL_DATA",
    "GAUGE_VALUE",
    "HEATMAP_DATA",
    "KPI_DATA",
    "LINE_DATA",
    "METER_VALUE",
    "POLAR_DATA",
    "PYRAMID_DATA",
    "RADAR_DATA",
    "RADIAL_GAUGE_DATA",
    "RADIAL_GROUP_DATA",
    "RANGE_DATA",
    "SANKEY_DATA",
    "SCATTER_DATA",
    "SPARKLINE_ROWS",
    "STACKED_DATA",
    "STEP_DATA",
    "STREAM_DATA",
    "TREEMAP_DATA",
    "WATERFALL_DATA",
    "activity_contributions",
]

LINE_DATA: list[dict[str, Any]] = [
    {"label": "Jan", "value": 24, "secondary": 18},
    {"label": "Feb", "value": 45, "secondary": 32},
    {"label": "Mar", "value": 38, "secondary": 29},
    {"label": "Apr", "value": 65, "secondary": 48},
    {"label": "May", "value": 52, "secondary": 41},
    {"label": "Jun", "value": 84, "secondary": 62},
]

BAR_DATA: list[dict[str, Any]] = [
    {"label": "Mon", "primary": 45, "secondary": 25},
    {"label": "Tue", "primary": 78, "secondary": 40},
    {"label": "Wed", "primary": 62, "secondary": 30},
    {"label": "Thu", "primary": 95, "secondary": 55},
    {"label": "Fri", "primary": 88, "secondary": 50},
    {"label": "Sat", "primary": 54, "secondary": 28},
]

AREA_DATA: list[dict[str, Any]] = [
    {"time": "02:00", "volume": 18},
    {"time": "06:00", "volume": 34},
    {"time": "10:00", "volume": 72},
    {"time": "14:00", "volume": 89},
    {"time": "18:00", "volume": 64},
    {"time": "22:00", "volume": 48},
]

DONUT_DATA: list[dict[str, Any]] = [
    {"name": "Core Engine", "value": 45},
    {"name": "UI Layer", "value": 30},
    {"name": "Assets", "value": 15},
    {"name": "Other", "value": 10},
]

COMPOSED_DATA: list[dict[str, Any]] = [
    {"label": "Q1", "count": 140, "trend": 120},
    {"label": "Q2", "count": 210, "trend": 190},
    {"label": "Q3", "count": 280, "trend": 260},
    {"label": "Q4", "count": 350, "trend": 340},
]

STACKED_DATA: list[dict[str, Any]] = [
    {"label": "Q1", "layer1": 30, "layer2": 25, "layer3": 20},
    {"label": "Q2", "layer1": 45, "layer2": 35, "layer3": 25},
    {"label": "Q3", "layer1": 60, "layer2": 40, "layer3": 30},
    {"label": "Q4", "layer1": 75, "layer2": 50, "layer3": 35},
]

STEP_DATA: list[dict[str, Any]] = [
    {"step": "01", "level": 20},
    {"step": "02", "level": 40},
    {"step": "03", "level": 35},
    {"step": "04", "level": 75},
    {"step": "05", "level": 60},
    {"step": "06", "level": 90},
]

SCATTER_DATA: list[dict[str, Any]] = [
    {"x": 10, "y": 30, "z": 200, "name": "Node A"},
    {"x": 25, "y": 65, "z": 400, "name": "Node B"},
    {"x": 40, "y": 45, "z": 300, "name": "Node C"},
    {"x": 55, "y": 80, "z": 500, "name": "Node D"},
    {"x": 70, "y": 60, "z": 350, "name": "Node E"},
    {"x": 85, "y": 92, "z": 600, "name": "Node F"},
]

BUBBLE_DATA: list[dict[str, Any]] = [
    {"x": 20, "y": 30, "z": 300, "tag": "Cluster 1"},
    {"x": 45, "y": 70, "z": 600, "tag": "Cluster 2"},
    {"x": 70, "y": 40, "z": 450, "tag": "Cluster 3"},
    {"x": 85, "y": 80, "z": 750, "tag": "Cluster 4"},
]

SPARKLINE_ROWS: list[dict[str, Any]] = [
    {
        "name": "CPU Temp",
        "value": "42°C",
        "data": [
            {"x": 1, "y": 10},
            {"x": 2, "y": 25},
            {"x": 3, "y": 18},
            {"x": 4, "y": 40},
            {"x": 5, "y": 30},
        ],
    },
    {
        "name": "GPU Temp",
        "value": "58°C",
        "data": [
            {"x": 1, "y": 15},
            {"x": 2, "y": 30},
            {"x": 3, "y": 22},
            {"x": 4, "y": 55},
            {"x": 5, "y": 48},
        ],
    },
    {
        "name": "Fan Speed",
        "value": "1.2k RPM",
        "data": [
            {"x": 1, "y": 40},
            {"x": 2, "y": 35},
            {"x": 3, "y": 60},
            {"x": 4, "y": 50},
            {"x": 5, "y": 80},
        ],
    },
]

RADAR_DATA: list[dict[str, Any]] = [
    {"subject": "Speed", "metric": 90},
    {"subject": "Memory", "metric": 75},
    {"subject": "Scale", "metric": 85},
    {"subject": "Latency", "metric": 95},
    {"subject": "IOPS", "metric": 80},
]

POLAR_DATA: list[dict[str, Any]] = [
    {"name": "Alpha", "count": 90},
    {"name": "Beta", "count": 65},
    {"name": "Gamma", "count": 40},
]

RADIAL_GROUP_DATA: list[dict[str, Any]] = [
    {"name": "System", "value": 85},
    {"name": "Network", "value": 62},
    {"name": "Storage", "value": 45},
    {"name": "Memory", "value": 30},
]

RADIAL_GAUGE_DATA: list[dict[str, Any]] = [
    {"name": "Core", "value": 90},
    {"name": "Memory", "value": 72},
    {"name": "Cache", "value": 54},
]

GAUGE_VALUE = 84
METER_VALUE = 78

BULLET_DATA: list[dict[str, Any]] = [
    {"title": "Throughput", "actual": 82, "target": 75},
    {"title": "Latency", "actual": 65, "target": 80},
    {"title": "Uptime", "actual": 95, "target": 90},
]

PYRAMID_DATA: list[dict[str, Any]] = [
    {"label": "Executive", "width": 30, "opacity": 1.0},
    {"label": "Management", "width": 50, "opacity": 0.7},
    {"label": "Senior Staff", "width": 70, "opacity": 0.45},
    {"label": "Core Team", "width": 90, "opacity": 0.25},
]

FUNNEL_DATA: list[dict[str, Any]] = [
    {"stage": "Visits", "volume": 100},
    {"stage": "Signup", "volume": 68},
    {"stage": "Active", "volume": 42},
    {"stage": "Pro", "volume": 24},
]

TREEMAP_DATA: list[dict[str, Any]] = [
    {"label": "Storage", "share": 45, "cols": 2, "rows": 2, "opacity": 1.0},
    {"label": "Compute", "share": 30, "cols": 1, "rows": 2, "opacity": 0.6},
    {"label": "Network", "share": 15, "cols": 2, "rows": 1, "opacity": 0.35},
    {"label": "Cache", "share": 10, "cols": 1, "rows": 1, "opacity": 0.2},
]

HEATMAP_DATA: list[dict[str, Any]] = [
    {"label": "Mon", "values": [10, 40, 80, 50, 90, 30, 60]},
    {"label": "Tue", "values": [30, 60, 90, 70, 40, 80, 20]},
    {"label": "Wed", "values": [50, 70, 30, 80, 60, 90, 40]},
    {"label": "Thu", "values": [20, 80, 60, 40, 90, 50, 70]},
    {"label": "Fri", "values": [60, 90, 70, 90, 50, 30, 80]},
]

RANGE_DATA: list[dict[str, Any]] = [
    {"day": "Mon", "range": [20, 50]},
    {"day": "Tue", "range": [35, 75]},
    {"day": "Wed", "range": [25, 60]},
    {"day": "Thu", "range": [40, 90]},
    {"day": "Fri", "range": [55, 85]},
]

KPI_DATA: list[dict[str, Any]] = [
    {"v": 30},
    {"v": 45},
    {"v": 35},
    {"v": 60},
    {"v": 50},
    {"v": 85},
    {"v": 75},
    {"v": 95},
]

CANDLE_DATA: list[dict[str, Any]] = [
    {"time": "09:30", "open": 120, "high": 145, "low": 110, "close": 140},
    {"time": "10:30", "open": 140, "high": 160, "low": 135, "close": 155},
    {"time": "11:30", "open": 155, "high": 158, "low": 125, "close": 130},
    {"time": "12:30", "open": 130, "high": 170, "low": 128, "close": 165},
    {"time": "13:30", "open": 165, "high": 180, "low": 150, "close": 175},
]

WATERFALL_DATA: list[dict[str, Any]] = [
    {"step": "Start", "base": 0, "delta": 50},
    {"step": "Inflow", "base": 50, "delta": 30},
    {"step": "Outflow", "base": 60, "delta": 20},
    {"step": "Net", "base": 0, "delta": 80},
]

STREAM_DATA: list[dict[str, Any]] = [
    {"t": "01", "w1": 20, "w2": 15},
    {"t": "02", "w1": 45, "w2": 30},
    {"t": "03", "w1": 30, "w2": 50},
    {"t": "04", "w1": 70, "w2": 35},
    {"t": "05", "w1": 55, "w2": 60},
    {"t": "06", "w1": 85, "w2": 40},
]

#: Sankey flows: each entry routes a source node to a target with a weight.
SANKEY_DATA: list[dict[str, Any]] = [
    {"source": "Source A", "target": "Target", "value": 60},
    {"source": "Source B", "target": "Target", "value": 40},
]


def activity_contributions(
    weeks: int = 20,
    *,
    seed: int | None = 7,
    end: datetime.date | None = None,
) -> list[dict[str, Any]]:
    """Generate a GitHub-style contribution series.

    The original component regenerates this on every mount with an unseeded
    ``Math.random``. A seed is used here by default so the grid is stable across
    re-renders and across the server/client boundary; pass ``seed=None`` for the
    original random behaviour.

    Args:
        weeks: Number of week columns (7 cells each).
        seed: RNG seed, or ``None`` for a fresh random grid.
        end: Last day in the series. Defaults to today.

    Returns:
        ``weeks * 7`` dicts with ``date``, ``count`` and ``level`` (0-4).
    """
    rng = random.Random(seed)
    last = end or datetime.date.today()  # noqa: DTZ011 - local calendar day is intended
    total = weeks * 7
    out: list[dict[str, Any]] = []
    for i in range(total):
        day = last - datetime.timedelta(days=total - 1 - i)
        level = 0
        count = 0
        if rng.random() > 0.35:
            level = rng.randint(1, 4)
            count = level * 3 + rng.randint(0, 3)
        out.append({"date": day.isoformat(), "count": count, "level": level})
    return out
