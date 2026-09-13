"""Point-family Monocharts cards: the scatter matrix and the bubble cluster."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import reflex as rx

from .. import data as demo
from ..card import mono_card, mono_footer, mono_header, mono_stage
from ..theme import ThemeLike, ink, ink_alpha, is_dark
from ..tooltip import mono_tooltip
from ._common import (
    CHART_MARGIN,
    auto,
    chart_height,
    mono_grid,
    mono_x_axis,
    mono_y_axis,
    resolve,
)

__all__ = ["mono_rounded_bubble_chart", "mono_rounded_scatter_chart"]


def _point_card(
    rows: Any,
    *,
    x_key: str,
    y_key: str,
    z_key: str | None,
    z_range: Sequence[int],
    name: str,
    fill: Any,
    stroke: Any,
    stroke_width: float,
    grid: bool,
    theme: ThemeLike,
    compact: Any,
    title: Any,
    badge: Any,
    value: Any,
    unit: Any,
    footer_left: Any,
    footer_right: Any,
    control: rx.Component | None,
    props: dict[str, Any],
) -> rx.Component:
    """Shared body for the two point charts."""
    children: list[rx.Component] = []
    if grid:
        children.append(mono_grid(theme, "2 2", vertical=True))
    children += [
        mono_x_axis(theme, x_key, type_="number"),
        mono_y_axis(theme, data_key=y_key, type_="number"),
    ]
    if z_key is not None:
        children.append(rx.recharts.z_axis(data_key=z_key, range=list(z_range)))
    children += [
        mono_tooltip(theme, cursor={"strokeDasharray": "3 3"}),
        rx.recharts.scatter(
            data=rows,
            name=name,
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            animation_duration=800,
        ),
    ]

    return mono_card(
        mono_header(
            title, badge, value, unit, theme=theme, control=control, margin_bottom="0.5rem"
        ),
        mono_stage(
            rx.recharts.scatter_chart(*children, margin=CHART_MARGIN, height=chart_height(compact)),
            theme=theme,
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


def mono_rounded_scatter_chart(
    data: Any = None,
    *,
    x_key: str = "x",
    y_key: str = "y",
    z_key: str | None = "z",
    z_range: Sequence[int] = (60, 240),
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Mono Scatter Matrix",
    badge: Any = "Rounded Nodes",
    value: Any = None,
    unit: Any = "mapped",
    footer_left: Any = "Scale-Weighted Nodes",
    footer_right: Any = "99.8% Sync",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """Solid weighted nodes on a dashed grid.

    Args:
        data: Points to plot. Defaults to the built-in demo series.
        x_key: Key of the x coordinate.
        y_key: Key of the y coordinate.
        z_key: Key driving the symbol area, or ``None`` for uniform dots.
        z_range: ``(min, max)`` symbol area in square pixels.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The node count when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.SCATTER_DATA)
    dark = is_dark(theme)
    return _point_card(
        rows,
        x_key=x_key,
        y_key=y_key,
        z_key=z_key,
        z_range=z_range,
        name="Cluster Nodes",
        fill=ink(dark),
        stroke=ink_alpha(dark, 0.5),
        stroke_width=1.5,
        grid=True,
        theme=theme,
        compact=compact,
        title=title,
        badge=badge,
        value=auto(value, rows, lambda d: f"{len(d)} Nodes", "6 Nodes"),
        unit=unit,
        footer_left=footer_left,
        footer_right=footer_right,
        control=control,
        props=props,
    )


def mono_rounded_bubble_chart(
    data: Any = None,
    *,
    x_key: str = "x",
    y_key: str = "y",
    z_key: str | None = "z",
    z_range: Sequence[int] = (100, 500),
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Bubble Clusters",
    badge: Any = "Scaled",
    value: Any = None,
    unit: Any = "mapped",
    footer_left: Any = "Rounded Sphere Circles",
    footer_right: Any = "Z-Scaled Radii",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """Hollow outlined bubbles whose area encodes a third dimension.

    Args:
        data: Points to plot. Defaults to the built-in demo series.
        x_key: Key of the x coordinate.
        y_key: Key of the y coordinate.
        z_key: Key driving the bubble area, or ``None`` for uniform circles.
        z_range: ``(min, max)`` bubble area in square pixels.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The cluster count when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.BUBBLE_DATA)
    dark = is_dark(theme)
    return _point_card(
        rows,
        x_key=x_key,
        y_key=y_key,
        z_key=z_key,
        z_range=z_range,
        name="Clusters",
        fill=ink_alpha(dark, 0.2),
        stroke=ink(dark),
        stroke_width=2,
        grid=False,
        theme=theme,
        compact=compact,
        title=title,
        badge=badge,
        value=auto(value, rows, lambda d: f"{len(d)} Clusters", "4 Clusters"),
        unit=unit,
        footer_left=footer_left,
        footer_right=footer_right,
        control=control,
        props=props,
    )
