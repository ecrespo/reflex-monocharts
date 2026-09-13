"""Polar-family Monocharts cards: donut, radar, radial bars, gauges and meters."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import reflex as rx

from .. import data as demo
from ..card import FONT_MONO, FONT_SANS, mono_card, mono_footer, mono_header, mono_stage
from ..theme import ThemeLike, ink, ink_alpha, is_dark, pick
from ..tooltip import mono_tooltip
from ._common import auto, chart_height, compact_value, resolve

__all__ = [
    "mono_rounded_donut_chart",
    "mono_rounded_gauge_arc",
    "mono_rounded_meter_chart",
    "mono_rounded_polar_chart",
    "mono_rounded_radar_chart",
    "mono_rounded_radial_bar_group",
    "mono_rounded_radial_gauge_chart",
]

#: Opacity ramp applied by index so segments stay distinguishable in one hue.
ALPHA_RAMP: tuple[float, ...] = (1.0, 0.7, 0.4, 0.2, 0.14, 0.1, 0.08, 0.06)


def ramp_color(dark: Any, index: int) -> Any:
    """The monochrome fill for the nth segment of a series."""
    alpha = ALPHA_RAMP[index] if index < len(ALPHA_RAMP) else ALPHA_RAMP[-1]
    return ink(dark) if alpha >= 1.0 else ink_alpha(dark, alpha)


def _ramp_var(dark: Any, index: Any) -> Any:
    """The same ramp, resolved reactively from a foreach index Var."""
    result: Any = ramp_color(dark, len(ALPHA_RAMP) - 1)
    for i in range(len(ALPHA_RAMP) - 2, -1, -1):
        result = rx.cond(index == i, ramp_color(dark, i), result)
    return result


def _cells(dark: Any, rows: Any, **cell_props: Any) -> list[rx.Component]:
    """One recharts ``Cell`` per row, coloured from the ramp."""
    if isinstance(rows, rx.Var):
        return [
            rx.foreach(
                rows,
                lambda _item, i: rx.recharts.cell(fill=_ramp_var(dark, i), **cell_props),
            )
        ]
    return [rx.recharts.cell(fill=ramp_color(dark, i), **cell_props) for i in range(len(rows))]


def mono_rounded_donut_chart(
    data: Any = None,
    *,
    name_key: str = "name",
    value_key: str = "value",
    center_value: Any = None,
    center_label: Any = "Mono Arc",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Mono Rounded Donut",
    badge: Any = "Soft Arc Caps",
    value: Any = None,
    unit: Any = "allocation",
    footer_left: Any = None,
    footer_right: Any = None,
    legend: bool = True,
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A donut with rounded, spaced segment caps and a centre readout.

    Args:
        data: Segments to draw. Defaults to the built-in demo series.
        name_key: Key holding the segment name.
        value_key: Key holding the segment value.
        center_value: Big number in the middle of the ring. The total when omitted.
        center_label: Caption under the centre number.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The total when omitted.
        unit: Muted suffix after the metric.
        footer_left: Replaces the legend footer when given.
        footer_right: Right-hand footer caption, used with ``footer_left``.
        legend: Render the dotted segment legend as the footer.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.DONUT_DATA)
    dark = is_dark(theme)
    total = auto(value, rows, lambda d: f"{sum(r[value_key] for r in d)}%", "100%")
    center = auto(center_value, rows, lambda d: f"{sum(r[value_key] for r in d)}%", "100%")

    def legend_item(item: Any, index: Any = 0) -> rx.Component:
        return rx.hstack(
            rx.box(
                width="0.375rem",
                height="0.375rem",
                border_radius="9999px",
                background=ink_alpha(dark, 0.7),
                flex_shrink="0",
            ),
            rx.text(item[name_key], color=pick(dark, "#A3A3A3", "#525252")),
            spacing="1",
            align="center",
        )

    if footer_left is not None or not legend:
        footer = mono_footer(
            footer_left or "Rounded Segment Caps",
            footer_right or "Mono Donut",
            theme=theme,
        )
    else:
        items = (
            rx.foreach(rows, legend_item)
            if isinstance(rows, rx.Var)
            else rx.fragment(*[legend_item(r) for r in rows])
        )
        footer = rx.box(
            items,
            width="100%",
            display="flex",
            flex_direction="row",
            justify_content="space-around",
            align_items="center",
            gap="0.5rem",
            flex_wrap="wrap",
            margin_top="0.75rem",
            padding_top="0.25rem",
            border_top=pick(dark, "1px solid rgba(255,255,255,0.05)", "1px solid rgba(0,0,0,0.06)"),
            font_size="0.625rem",
        )

    return mono_card(
        mono_header(title, badge, total, unit, theme=theme, control=control),
        mono_stage(
            rx.recharts.pie_chart(
                mono_tooltip(theme),
                rx.recharts.pie(
                    *_cells(dark, rows, stroke=pick(dark, "#181818", "#FFFFFF")),
                    data=rows,
                    data_key=value_key,
                    name_key=name_key,
                    cx="50%",
                    cy="50%",
                    inner_radius=compact_value(compact, 38, 46),
                    outer_radius=compact_value(compact, 58, 68),
                    padding_angle=6,
                    stroke=pick(dark, "#181818", "#FFFFFF"),
                    stroke_width=2,
                    animation_duration=900,
                    custom_attrs={"cornerRadius": 8},
                ),
                height=chart_height(compact),
            ),
            rx.vstack(
                rx.text(
                    center,
                    font_size="0.875rem",
                    font_weight="700",
                    font_variant_numeric="tabular-nums",
                ),
                rx.text(
                    center_label,
                    font_size="0.625rem",
                    color=pick(dark, "#A3A3A3", "#737373"),
                ),
                position="absolute",
                top="0",
                left="0",
                right="0",
                bottom="0",
                align="center",
                justify="center",
                spacing="0",
                pointer_events="none",
            ),
            theme=theme,
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        footer,
        theme=theme,
        compact=compact,
        **props,
    )


def mono_rounded_radar_chart(
    data: Any = None,
    *,
    subject_key: str = "subject",
    value_key: str = "metric",
    domain: Sequence[int] = (0, 100),
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Polygon Web",
    badge: Any = "Radar",
    value: Any = None,
    unit: Any = "score",
    footer_left: Any = None,
    footer_right: Any = "Polygon Net",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A multi-axis polygon web.

    Args:
        data: One row per axis. Defaults to the built-in demo series.
        subject_key: Key holding the axis name.
        value_key: Key holding the plotted metric.
        domain: Radial domain as ``(min, max)``.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The mean when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption. The axis count when omitted.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.RADAR_DATA)
    dark = is_dark(theme)
    value = auto(value, rows, lambda d: round(sum(r[value_key] for r in d) / len(d)), 85)
    footer_left = auto(
        footer_left, rows, lambda d: f"{len(d)} Multi-Axis Nodes", "5 Multi-Axis Nodes"
    )

    return mono_card(
        mono_header(title, badge, value, unit, theme=theme, control=control),
        mono_stage(
            rx.recharts.radar_chart(
                rx.recharts.polar_grid(stroke=ink_alpha(dark, 0.08)),
                rx.recharts.polar_angle_axis(
                    data_key=subject_key,
                    tick={"fontSize": 9, "fill": pick(dark, "#71717A", "#A1A1AA")},
                ),
                rx.recharts.polar_radius_axis(domain=list(domain), tick=False, axis_line=False),
                mono_tooltip(theme),
                rx.recharts.radar(
                    data_key=value_key,
                    name="Metric",
                    stroke=ink(dark),
                    stroke_width=2,
                    fill=ink(dark),
                    fill_opacity=0.15,
                    dot=False,
                    animation_duration=800,
                    custom_attrs={"strokeLinecap": "round", "strokeLinejoin": "round"},
                ),
                data=rows,
                cx="50%",
                cy="50%",
                outer_radius=compact_value(compact, 42, 52),
                height=chart_height(compact),
            ),
            theme=theme,
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


def mono_rounded_polar_chart(
    data: Any = None,
    *,
    name_key: str = "name",
    value_key: str = "count",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Polar Pillars",
    badge: Any = "Radial",
    value: Any = None,
    unit: Any = "polar angle",
    footer_left: Any = "Rounded 360 Polar Arcs",
    footer_right: Any = "Radial Pillars",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """Full-circle radial pillars with rounded caps.

    Args:
        data: One row per band. Defaults to the built-in demo series.
        name_key: Key holding the band name.
        value_key: Key holding the band value.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The band count when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.POLAR_DATA)
    dark = is_dark(theme)
    value = auto(value, rows, lambda d: f"{len(d)} Bands", "3 Bands")

    return mono_card(
        mono_header(title, badge, value, unit, theme=theme, control=control),
        mono_stage(
            rx.recharts.radial_bar_chart(
                mono_tooltip(theme),
                rx.recharts.radial_bar(
                    data_key=value_key,
                    background={"fill": pick(dark, "rgba(255,255,255,0.05)", "rgba(0,0,0,0.05)")},
                    animation_duration=800,
                    custom_attrs={"cornerRadius": 6, "fill": ink(dark)},
                ),
                data=rows,
                cx="50%",
                cy="50%",
                inner_radius="25%",
                outer_radius="85%",
                bar_size=12,
                start_angle=90,
                end_angle=-270,
                height=chart_height(compact),
            ),
            theme=theme,
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


def mono_rounded_radial_bar_group(
    data: Any = None,
    *,
    name_key: str = "name",
    value_key: str = "value",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Radial Group",
    badge: Any = "Multi-Arc",
    value: Any = None,
    unit: Any = "active",
    footer_left: Any = "Rounded 180 Radial Caps",
    footer_right: Any = None,
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A half-circle group of concentric rounded arcs, one per row.

    Args:
        data: One row per arc. Defaults to the built-in demo series.
        name_key: Key holding the arc name.
        value_key: Key holding the arc value.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The ring count when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption. The ring count when omitted.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.RADIAL_GROUP_DATA)
    dark = is_dark(theme)
    value = auto(value, rows, lambda d: f"{len(d)} Rings", "4 Rings")
    footer_right = auto(footer_right, rows, lambda d: f"{len(d)} Gauge Arcs", "4 Gauge Arcs")

    return mono_card(
        mono_header(title, badge, value, unit, theme=theme, control=control),
        mono_stage(
            rx.recharts.radial_bar_chart(
                mono_tooltip(theme),
                rx.recharts.radial_bar(
                    *_cells(dark, rows),
                    data_key=value_key,
                    background={"fill": pick(dark, "rgba(255,255,255,0.05)", "rgba(0,0,0,0.05)")},
                    animation_duration=800,
                    custom_attrs={"cornerRadius": 8},
                ),
                data=rows,
                cx="50%",
                cy="50%",
                inner_radius="20%",
                outer_radius="95%",
                bar_size=8,
                start_angle=180,
                end_angle=0,
                height=chart_height(compact),
            ),
            theme=theme,
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


def mono_rounded_radial_gauge_chart(
    data: Any = None,
    *,
    name_key: str = "name",
    value_key: str = "value",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Radial Rings",
    badge: Any = "Concentric",
    value: Any = None,
    unit: Any = "core utilization",
    footer_left: Any = "Concentric Caps",
    footer_right: Any = None,
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """Full-circle concentric progress rings.

    Args:
        data: One row per ring, outermost first. Defaults to the demo series.
        name_key: Key holding the ring name.
        value_key: Key holding the ring percentage.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The first ring when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption. The ring count when omitted.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.RADIAL_GAUGE_DATA)
    dark = is_dark(theme)
    value = auto(value, rows, lambda d: f"{d[0][value_key]}%", "90%")
    footer_right = auto(
        footer_right, rows, lambda d: f"{len(d)} Progress Meters", "3 Progress Meters"
    )

    return mono_card(
        mono_header(title, badge, value, unit, theme=theme, control=control),
        mono_stage(
            rx.recharts.radial_bar_chart(
                mono_tooltip(theme),
                rx.recharts.radial_bar(
                    *_cells(dark, rows),
                    data_key=value_key,
                    background={"fill": pick(dark, "rgba(255,255,255,0.05)", "rgba(0,0,0,0.05)")},
                    animation_duration=800,
                    custom_attrs={"cornerRadius": 5},
                ),
                data=rows,
                cx="50%",
                cy="50%",
                inner_radius="30%",
                outer_radius="90%",
                bar_size=10,
                start_angle=180,
                end_angle=-180,
                height=chart_height(compact),
            ),
            theme=theme,
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


def _arc_gauge(
    percent: Any,
    *,
    start_angle: int,
    end_angle: int,
    inner: int,
    outer: int,
    corner: int,
    theme: ThemeLike,
    compact: Any,
    title: Any,
    badge: Any,
    unit: Any,
    caption: Any,
    readout: Any,
    readout_size: str,
    readout_weight: str,
    footer_left: Any,
    footer_right: Any,
    value: Any,
    control: rx.Component | None,
    props: dict[str, Any],
) -> rx.Component:
    """Shared body for the two arc gauges."""
    dark = is_dark(theme)
    remainder = 100 - percent
    rows = [{"name": "Active", "value": percent}, {"name": "Remaining", "value": remainder}]
    metric = value if value is not None else f"{percent}%"
    readout = readout if readout is not None else metric

    return mono_card(
        mono_header(title, badge, metric, unit, theme=theme, control=control),
        mono_stage(
            rx.recharts.pie_chart(
                rx.recharts.pie(
                    rx.recharts.cell(fill=ink(dark)),
                    rx.recharts.cell(fill=ink_alpha(dark, 0.1)),
                    data=rows,
                    data_key="value",
                    name_key="name",
                    cx="50%",
                    cy="70%",
                    start_angle=start_angle,
                    end_angle=end_angle,
                    inner_radius=compact_value(compact, inner - 10, inner),
                    outer_radius=compact_value(compact, outer - 12, outer),
                    padding_angle=4,
                    stroke="none",
                    is_animation_active=True,
                    animation_duration=900,
                    custom_attrs={"cornerRadius": corner},
                ),
                height=compact_value(compact, 120, 140),
            ),
            rx.vstack(
                rx.text(
                    readout,
                    font_size=readout_size,
                    font_weight=readout_weight,
                    font_variant_numeric="tabular-nums",
                    font_family=FONT_SANS,
                ),
                rx.text(
                    caption,
                    font_size="0.625rem",
                    font_family=FONT_MONO,
                    color=pick(dark, "#A3A3A3", "#737373"),
                ),
                position="absolute",
                bottom="1rem",
                left="0",
                right="0",
                align="center",
                spacing="0",
                pointer_events="none",
            ),
            theme=theme,
            display="flex",
            flex_direction="column",
            align_items="center",
            justify_content="center",
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


def mono_rounded_gauge_arc(
    percent: Any = demo.GAUGE_VALUE,
    *,
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Speedometer Arc",
    badge: Any = "Gauge",
    value: Any = None,
    unit: Any = "performance index",
    caption: Any = "Target Met",
    readout: Any = None,
    footer_left: Any = "Rounded 240 Arc Dial",
    footer_right: Any = "Peak Gauge",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A 240-degree speedometer dial with a centre score.

    Args:
        percent: The 0-100 value to fill. Accepts a Var.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. ``"{percent}%"`` when omitted.
        unit: Muted suffix after the metric.
        caption: Small caption under the dial readout.
        readout: Big number inside the dial. The metric when omitted.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    return _arc_gauge(
        percent,
        start_angle=210,
        end_angle=-30,
        inner=54,
        outer=72,
        corner=8,
        theme=theme,
        compact=compact,
        title=title,
        badge=badge,
        unit=unit,
        caption=caption,
        readout=readout,
        readout_size="1.25rem",
        readout_weight="800",
        footer_left=footer_left,
        footer_right=footer_right,
        value=value,
        control=control,
        props=props,
    )


def mono_rounded_meter_chart(
    percent: Any = demo.METER_VALUE,
    *,
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Arc Meter",
    badge: Any = "Speedometer",
    value: Any = None,
    unit: Any = "load index",
    caption: Any = "Optimal Load",
    readout: Any = None,
    footer_left: Any = "Rounded Semi-Circle Arc",
    footer_right: Any = "Gauge Meter",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A true semicircle meter with a centre readout.

    Args:
        percent: The 0-100 value to fill. Accepts a Var.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. ``"{percent}%"`` when omitted.
        unit: Muted suffix after the metric.
        caption: Small caption under the dial readout.
        readout: Big number inside the dial. The metric when omitted.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    return _arc_gauge(
        percent,
        start_angle=180,
        end_angle=0,
        inner=52,
        outer=70,
        corner=6,
        theme=theme,
        compact=compact,
        title=title,
        badge=badge,
        unit=unit,
        caption=caption,
        readout=readout,
        readout_size="1.125rem",
        readout_weight="700",
        footer_left=footer_left,
        footer_right=footer_right,
        value=value,
        control=control,
        props=props,
    )
