"""Area-family Monocharts cards: curved wave, range band and dual stream."""

from __future__ import annotations

from typing import Any

import reflex as rx

from .. import data as demo
from ..card import mono_card, mono_footer, mono_header, mono_stage
from ..theme import ThemeLike, ink, is_dark, muted_ink
from ..tooltip import mono_gradient, mono_tooltip, unique_id
from ._common import (
    CHART_MARGIN,
    auto,
    chart_height,
    mono_grid,
    mono_x_axis,
    mono_y_axis,
    resolve,
)

__all__ = [
    "mono_rounded_area_chart",
    "mono_rounded_range_chart",
    "mono_rounded_stream_chart",
]


def mono_rounded_area_chart(
    data: Any = None,
    *,
    x_key: str = "time",
    value_key: str = "volume",
    curve: Any = "monotone",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Mono Curved Wave",
    badge: Any = "Soft Gradient",
    value: Any = None,
    unit: Any = "peak throughput",
    footer_left: Any = "Minimalist Spline Shading",
    footer_right: Any = "99.9% Linear Flow",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A single curved area with a soft top-down gradient.

    Args:
        data: Rows to plot. Defaults to the built-in demo series.
        x_key: Key holding the category label.
        value_key: Key holding the plotted value.
        curve: Interpolation - ``"monotone"``, ``"natural"``, ``"linear"``, ...
            Accepts a Var so a segmented control can drive it.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The last value when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.AREA_DATA)
    dark = is_dark(theme)
    grad = unique_id("mono-area")
    value = auto(value, rows, lambda d: f"{d[-1][value_key]}%", "48%")

    return mono_card(
        mono_header(
            title, badge, value, unit, theme=theme, control=control, margin_bottom="0.5rem"
        ),
        mono_stage(
            mono_gradient(grad, ink(dark), top_opacity=0.35, bottom_opacity=0.0),
            rx.recharts.area_chart(
                mono_grid(theme),
                mono_x_axis(theme, x_key),
                mono_y_axis(theme),
                mono_tooltip(theme),
                rx.recharts.area(
                    data_key=value_key,
                    name="Volume Flow",
                    type_=curve,
                    stroke=ink(dark),
                    stroke_width=2.5,
                    fill=f"url(#{grad})",
                    dot=False,
                    active_dot={"r": 5, "fill": ink(dark)},
                    animation_duration=900,
                    custom_attrs={"strokeLinecap": "round", "strokeLinejoin": "round"},
                ),
                data=rows,
                margin=CHART_MARGIN,
                height=chart_height(compact),
            ),
            theme=theme,
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


def mono_rounded_range_chart(
    data: Any = None,
    *,
    x_key: str = "day",
    range_key: str = "range",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Range Band",
    badge: Any = "Min-Max",
    value: Any = None,
    unit: Any = "variance band",
    footer_left: Any = "Rounded Spline Boundaries",
    footer_right: Any = "Floating Range Band",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A floating min-max band, drawn from ``[lower, upper]`` pairs.

    Args:
        data: Rows whose ``range_key`` holds a two-element ``[low, high]`` list.
            Defaults to the built-in demo series.
        x_key: Key holding the category label.
        range_key: Key holding the ``[low, high]`` pair.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The widest band when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.RANGE_DATA)
    dark = is_dark(theme)
    grad = unique_id("mono-range")
    value = auto(value, rows, lambda d: max(r[range_key][1] - r[range_key][0] for r in d), 50)

    return mono_card(
        mono_header(
            title, badge, value, unit, theme=theme, control=control, margin_bottom="0.5rem"
        ),
        mono_stage(
            mono_gradient(grad, ink(dark), top_opacity=0.3, bottom_opacity=0.05),
            rx.recharts.area_chart(
                mono_x_axis(theme, x_key),
                mono_y_axis(theme),
                mono_tooltip(theme),
                rx.recharts.area(
                    data_key=range_key,
                    name="Band Range",
                    type_="monotone",
                    stroke=ink(dark),
                    stroke_width=2,
                    fill=f"url(#{grad})",
                    dot=False,
                    active_dot=False,
                    animation_duration=800,
                    custom_attrs={"strokeLinecap": "round", "strokeLinejoin": "round"},
                ),
                data=rows,
                margin=CHART_MARGIN,
                height=chart_height(compact),
            ),
            theme=theme,
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


def mono_rounded_stream_chart(
    data: Any = None,
    *,
    x_key: str = "t",
    primary_key: str = "w1",
    secondary_key: str = "w2",
    stacked: bool = False,
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Stream Wave",
    badge: Any = "Fluid",
    value: Any = None,
    unit: Any = "peak flow",
    footer_left: Any = "Rounded Natural Spline",
    footer_right: Any = "Dual Stream Wave",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """Two overlapping natural-spline waves with separate gradient fills.

    Args:
        data: Rows to plot. Defaults to the built-in demo series.
        x_key: Key holding the category label.
        primary_key: Key of the foreground wave.
        secondary_key: Key of the background wave.
        stacked: Stack the waves instead of overlapping them.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The tallest combined column when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.STREAM_DATA)
    dark = is_dark(theme)
    g1 = unique_id("mono-stream-a")
    g2 = unique_id("mono-stream-b")
    value = auto(value, rows, lambda d: max(r[primary_key] + r[secondary_key] for r in d), 125)
    stack: dict[str, Any] = {"stack_id": "s"} if stacked else {}

    return mono_card(
        mono_header(
            title, badge, value, unit, theme=theme, control=control, margin_bottom="0.5rem"
        ),
        mono_stage(
            mono_gradient(g1, ink(dark), top_opacity=0.4, bottom_opacity=0.05),
            mono_gradient(g2, ink(dark), top_opacity=0.2, bottom_opacity=0.0),
            rx.recharts.area_chart(
                mono_x_axis(theme, x_key),
                mono_y_axis(theme),
                mono_tooltip(theme),
                rx.recharts.area(
                    data_key=primary_key,
                    name="Wave 1",
                    type_="natural",
                    stroke=ink(dark),
                    stroke_width=2,
                    fill=f"url(#{g1})",
                    dot=False,
                    active_dot=False,
                    animation_duration=800,
                    custom_attrs={"strokeLinecap": "round", "strokeLinejoin": "round"},
                    **stack,
                ),
                rx.recharts.area(
                    data_key=secondary_key,
                    name="Wave 2",
                    type_="natural",
                    stroke=muted_ink(dark),
                    stroke_width=1.5,
                    fill=f"url(#{g2})",
                    dot=False,
                    active_dot=False,
                    animation_duration=900,
                    custom_attrs={"strokeLinecap": "round", "strokeLinejoin": "round"},
                    **stack,
                ),
                data=rows,
                margin=CHART_MARGIN,
                height=chart_height(compact),
            ),
            theme=theme,
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )
