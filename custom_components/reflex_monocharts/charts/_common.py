"""Shared plumbing for the recharts-backed Monocharts cards."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import reflex as rx

from ..theme import ThemeLike, axis_tick, grid_stroke, is_dark

__all__ = [
    "CHART_MARGIN",
    "auto",
    "chart_height",
    "compact_value",
    "mono_grid",
    "mono_x_axis",
    "mono_y_axis",
    "resolve",
]

#: The margin every cartesian Monocharts chart uses. The negative left pulls the
#: y-axis labels flush against the stage edge.
CHART_MARGIN: dict[str, int] = {"top": 12, "right": 12, "left": -22, "bottom": 0}


def compact_value(compact: Any, when_compact: Any, when_tall: Any) -> Any:
    """Pick between a compact-card and a regular-card value.

    ``compact`` may be a plain bool or a state Var, so the card size can be
    toggled at runtime.

    Args:
        compact: The card's ``compact`` argument.
        when_compact: Value for the short card.
        when_tall: Value for the tall card.

    Returns:
        One of the two values, or a reactive ``rx.cond``.
    """
    if isinstance(compact, rx.Var):
        return rx.cond(compact, when_compact, when_tall)
    return when_compact if compact else when_tall


def chart_height(compact: Any, tall: int = 160, short: int = 130) -> Any:
    """Plot height in pixels for the compact and regular card sizes."""
    return compact_value(compact, short, tall)


def resolve(data: Any, default: Sequence[dict[str, Any]]) -> Any:
    """Return ``data`` if given, else the component's built-in demo dataset."""
    return default if data is None else data


def auto(value: Any, data: Any, compute: Callable[[Any], Any], fallback: Any) -> Any:
    """Derive a headline metric from the data when that is possible.

    A plain Python list can be summed or indexed here and now. A state ``Var``
    cannot, so the caller's fallback (usually the original card's literal) is
    used instead - pass ``value=...`` explicitly to drive it from state.

    Args:
        value: An explicit metric supplied by the caller, or ``None``.
        data: The dataset, plain or reactive.
        compute: Called with a plain list to derive the metric.
        fallback: Used when the dataset is reactive or ``compute`` fails.

    Returns:
        The metric to render.
    """
    if value is not None:
        return value
    if isinstance(data, rx.Var):
        return fallback
    try:
        return compute(data)
    except Exception:  # noqa: BLE001  # pragma: no cover - defensive, never breaks a render
        return fallback


def mono_grid(theme: ThemeLike, dasharray: str = "2 2", **props: Any) -> rx.Component:
    """A horizontal-only dashed cartesian grid."""
    dark = is_dark(theme)
    props.setdefault("vertical", False)
    return rx.recharts.cartesian_grid(stroke_dasharray=dasharray, stroke=grid_stroke(dark), **props)


def mono_x_axis(theme: ThemeLike, data_key: Any = None, **props: Any) -> rx.Component:
    """An unstyled-chrome x-axis: no tick line, no axis line, 10px labels."""
    dark = is_dark(theme)
    if data_key is not None:
        props["data_key"] = data_key
    props.setdefault("tick_line", False)
    props.setdefault("axis_line", False)
    props.setdefault("tick", axis_tick(dark))
    return rx.recharts.x_axis(**props)


def mono_y_axis(theme: ThemeLike, **props: Any) -> rx.Component:
    """An unstyled-chrome y-axis matching :func:`mono_x_axis`."""
    dark = is_dark(theme)
    props.setdefault("tick_line", False)
    props.setdefault("axis_line", False)
    props.setdefault("tick", axis_tick(dark))
    return rx.recharts.y_axis(**props)
