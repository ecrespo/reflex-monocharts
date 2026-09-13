"""Line-family Monocharts cards: spline, step, sparkline rows and the KPI card."""

from __future__ import annotations

from typing import Any

import reflex as rx

from .. import data as demo
from ..card import FONT_MONO, mono_card, mono_footer, mono_header, mono_stage
from ..theme import ThemeLike, ink, is_dark, muted_ink, pick
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
    "mono_rounded_kpi_card_chart",
    "mono_rounded_line_chart",
    "mono_rounded_sparkline_chart",
    "mono_rounded_step_chart",
]


def mono_rounded_line_chart(
    data: Any = None,
    *,
    x_key: str = "label",
    value_key: str = "value",
    secondary_key: str | None = "secondary",
    series: Any = "all",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Spline Dynamics",
    badge: Any = "Line",
    value: Any = None,
    unit: Any = "nodes",
    footer_left: Any = "Rounded Caps",
    footer_right: Any = None,
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A monochrome spline line chart with a dashed baseline series.

    Args:
        data: Rows to plot. Defaults to the built-in demo series.
        x_key: Key holding the category label.
        value_key: Key holding the primary series.
        secondary_key: Key holding the dashed baseline, or ``None`` to omit it.
        series: ``"all"`` to show both series, anything else for the primary
            only. Accepts a Var so a segmented control can drive it.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. Derived from the last row when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption. Derived from the peak when omitted.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.

    Example:
        ```python
        mono_rounded_line_chart(State.traffic, x_key="hour", value_key="hits")
        ```
    """
    rows = resolve(data, demo.LINE_DATA)
    dark = is_dark(theme)
    value = auto(value, rows, lambda d: f"{d[-1][value_key]}k", "84k")
    footer_right = auto(
        footer_right, rows, lambda d: f"{max(r[value_key] for r in d)}k Peak", "84k Peak"
    )

    children: list[rx.Component] = [
        mono_grid(theme, "3 3"),
        mono_x_axis(theme, x_key),
        mono_y_axis(theme),
        mono_tooltip(theme),
    ]
    if secondary_key is not None:
        children.append(
            rx.recharts.line(
                data_key=secondary_key,
                name="Baseline",
                type_="monotone",
                stroke=muted_ink(dark),
                stroke_width=2,
                stroke_dasharray="4 4",
                dot=False,
                active_dot=False,
                hide=(series != "all"),
                animation_duration=900,
                custom_attrs={"strokeLinecap": "round", "strokeLinejoin": "round"},
            )
        )
    children.append(
        rx.recharts.line(
            data_key=value_key,
            name="Active",
            type_="monotone",
            stroke=ink(dark),
            stroke_width=3,
            dot={
                "r": 4,
                "fill": ink(dark),
                "stroke": pick(dark, "#181818", "#FFFFFF"),
                "strokeWidth": 2,
            },
            active_dot={
                "r": 6,
                "fill": ink(dark),
                "stroke": pick(dark, "#A1A1AA", "#52525B"),
                "strokeWidth": 2,
            },
            animation_duration=800,
            custom_attrs={"strokeLinecap": "round", "strokeLinejoin": "round"},
        )
    )

    return mono_card(
        mono_header(
            title, badge, value, unit, theme=theme, control=control, margin_bottom="0.5rem"
        ),
        mono_stage(
            rx.recharts.line_chart(
                *children,
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


def mono_rounded_step_chart(
    data: Any = None,
    *,
    x_key: str = "step",
    value_key: str = "level",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Step Progression",
    badge: Any = "Staircase",
    value: Any = None,
    unit: Any = "peak step",
    footer_left: Any = "Discrete Steps",
    footer_right: Any = None,
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A discrete staircase chart with rounded joins.

    Args:
        data: Rows to plot. Defaults to the built-in demo series.
        x_key: Key holding the step label.
        value_key: Key holding the level.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The peak level when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.STEP_DATA)
    dark = is_dark(theme)
    value = auto(value, rows, lambda d: max(r[value_key] for r in d), 90)
    footer_right = auto(footer_right, rows, lambda d: f"Level {len(d)} Active", "Level 6 Active")

    return mono_card(
        mono_header(
            title, badge, value, unit, theme=theme, control=control, margin_bottom="0.5rem"
        ),
        mono_stage(
            rx.recharts.line_chart(
                mono_grid(theme, "3 3"),
                mono_x_axis(theme, x_key),
                mono_y_axis(theme),
                mono_tooltip(theme),
                rx.recharts.line(
                    data_key=value_key,
                    name="Level",
                    type_="stepAfter",
                    stroke=ink(dark),
                    stroke_width=3,
                    dot={"r": 4, "fill": ink(dark)},
                    active_dot={"r": 6, "fill": ink(dark)},
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


def mono_rounded_sparkline_chart(
    rows: Any = None,
    *,
    name_key: str = "name",
    value_key: str = "value",
    series_key: str = "data",
    point_key: str = "y",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Sparklines",
    badge: Any = "Telemetry",
    value: Any = None,
    unit: Any = "active",
    footer_left: Any = "Rounded Mini Splines",
    footer_right: Any = "Real-Time Telemetry",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A stack of labelled telemetry rows, each with its own micro spline.

    Args:
        rows: One dict per row, each carrying a label, a readout and a nested
            list of points. Defaults to the built-in demo rows.
        name_key: Key holding the row label.
        value_key: Key holding the row readout.
        series_key: Key holding the nested list of points.
        point_key: Key of the plotted value inside each point.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The row count when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    series = resolve(rows, demo.SPARKLINE_ROWS)
    dark = is_dark(theme)
    value = auto(value, series, lambda d: f"{len(d)} Rows", "3 Rows")

    def row(item: Any) -> rx.Component:
        return rx.hstack(
            rx.vstack(
                rx.text(
                    item[name_key],
                    font_size="0.6875rem",
                    font_weight="500",
                    color=pick(dark, "#FFFFFF", "#000000"),
                ),
                rx.text(
                    item[value_key],
                    font_size="0.625rem",
                    font_family=FONT_MONO,
                    color=pick(dark, "#A3A3A3", "#737373"),
                ),
                spacing="0",
                align="start",
                width="5rem",
                flex_shrink="0",
            ),
            rx.box(
                rx.recharts.line_chart(
                    rx.recharts.line(
                        data_key=point_key,
                        type_="monotone",
                        stroke=ink(dark),
                        stroke_width=2,
                        dot=False,
                        active_dot=False,
                        animation_duration=800,
                        custom_attrs={"strokeLinecap": "round"},
                    ),
                    data=item[series_key],
                    height=28,
                ),
                flex="1",
                height="1.75rem",
            ),
            width="100%",
            align="center",
            spacing="3",
        )

    body = (
        rx.foreach(series, row)
        if isinstance(series, rx.Var)
        else rx.fragment(*[row(item) for item in series])
    )

    return mono_card(
        mono_header(title, badge, value, unit, theme=theme, control=control),
        mono_stage(
            body,
            theme=theme,
            padding="0.75rem",
            display="flex",
            flex_direction="column",
            justify_content="space-around",
            gap="0.5rem",
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


def mono_rounded_kpi_card_chart(
    data: Any = None,
    *,
    value_key: str = "v",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "KPI Stat Card",
    badge: Any = "Metric",
    value: Any = "$48,920",
    unit: Any = "+14.2%",
    footer_left: Any = "Rounded Sparkline Wave",
    footer_right: Any = "Monthly Revenue",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A big KPI number over a gradient-filled sparkline.

    Args:
        data: Points for the sparkline. Defaults to the built-in demo series.
        value_key: Key of the plotted value.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: The KPI itself.
        unit: The delta, rendered in the emerald accent.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.KPI_DATA)
    dark = is_dark(theme)
    grad = unique_id("mono-kpi")

    return mono_card(
        mono_header(
            title,
            badge,
            value,
            unit,
            theme=theme,
            control=control,
            large=True,
            unit_accent=True,
        ),
        mono_stage(
            mono_gradient(grad, ink(dark), top_opacity=0.3, bottom_opacity=0.0),
            rx.box(
                rx.recharts.area_chart(
                    rx.recharts.area(
                        data_key=value_key,
                        type_="monotone",
                        stroke=ink(dark),
                        stroke_width=2.5,
                        fill=f"url(#{grad})",
                        dot=False,
                        active_dot=False,
                        animation_duration=800,
                        custom_attrs={"strokeLinecap": "round"},
                    ),
                    data=rows,
                    height=96,
                ),
                width="100%",
                height="6rem",
            ),
            theme=theme,
            display="flex",
            flex_direction="column",
            justify_content="flex-end",
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )
