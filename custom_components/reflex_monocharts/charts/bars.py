"""Bar-family Monocharts cards: pill columns, stacks, hybrids, waterfall, funnel."""

from __future__ import annotations

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

__all__ = [
    "mono_rounded_bar_chart",
    "mono_rounded_composed_chart",
    "mono_rounded_funnel_chart",
    "mono_rounded_stacked_bar_chart",
    "mono_rounded_waterfall_chart",
]


def mono_rounded_bar_chart(
    data: Any = None,
    *,
    x_key: str = "label",
    value_key: str = "primary",
    secondary_key: str | None = "secondary",
    orientation: Any = "columns",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Mono Pill Pillars",
    badge: Any = "Full Radius",
    value: Any = None,
    unit: Any = "units built",
    footer_left: Any = "Corner Radius: 8px All",
    footer_right: Any = "Monochrome Fill",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """Fully-rounded pill bars, as columns or as rows.

    Args:
        data: Rows to plot. Defaults to the built-in demo series.
        x_key: Key holding the category label.
        value_key: Key holding the primary series.
        secondary_key: Key holding the muted series, or ``None`` to omit it.
        orientation: ``"columns"`` for vertical pillars, ``"rows"`` for
            horizontal ones. A Var renders both and switches live.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The primary total when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    if isinstance(orientation, rx.Var):
        kwargs = dict(
            data=data,
            x_key=x_key,
            value_key=value_key,
            secondary_key=secondary_key,
            theme=theme,
            compact=compact,
            title=title,
            badge=badge,
            value=value,
            unit=unit,
            footer_left=footer_left,
            footer_right=footer_right,
            control=control,
            **props,
        )
        return rx.cond(
            orientation == "rows",
            mono_rounded_bar_chart(orientation="rows", **kwargs),
            mono_rounded_bar_chart(orientation="columns", **kwargs),
        )

    rows = resolve(data, demo.BAR_DATA)
    dark = is_dark(theme)
    is_rows = orientation == "rows"
    value = auto(value, rows, lambda d: sum(r[value_key] for r in d), 422)

    radius = [0, 8, 8, 0] if is_rows else [8, 8, 8, 8]
    bar_size = 12 if is_rows else 16

    if is_rows:
        axes = [
            mono_x_axis(theme, type_="number", hide=True),
            mono_y_axis(theme, data_key=x_key, type_="category"),
        ]
        margin = {**CHART_MARGIN, "left": 0}
    else:
        axes = [mono_x_axis(theme, x_key), mono_y_axis(theme)]
        margin = CHART_MARGIN

    bars = [
        rx.recharts.bar(
            data_key=value_key,
            name="Primary Output",
            fill=ink(dark),
            radius=radius,
            bar_size=bar_size,
            animation_duration=800,
        )
    ]
    if secondary_key is not None:
        bars.append(
            rx.recharts.bar(
                data_key=secondary_key,
                name="Secondary Output",
                fill=ink_alpha(dark, 0.2),
                radius=radius,
                bar_size=bar_size,
                animation_duration=1000,
            )
        )

    return mono_card(
        mono_header(
            title, badge, value, unit, theme=theme, control=control, margin_bottom="0.5rem"
        ),
        mono_stage(
            rx.recharts.bar_chart(
                mono_grid(theme),
                *axes,
                mono_tooltip(theme),
                *bars,
                data=rows,
                layout="vertical" if is_rows else "horizontal",
                margin=margin,
                height=chart_height(compact),
            ),
            theme=theme,
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


def mono_rounded_stacked_bar_chart(
    data: Any = None,
    *,
    x_key: str = "label",
    keys: Any = ("layer1", "layer2", "layer3"),
    names: Any = ("Base", "Mid", "Top"),
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Stacked Tones",
    badge: Any = "Layers",
    value: Any = None,
    unit: Any = "cumulative",
    footer_left: Any = None,
    footer_right: Any = "Stacked Geometry",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A stack of monochrome tones with rounded outer ends.

    Args:
        data: Rows to plot. Defaults to the built-in demo series.
        x_key: Key holding the category label.
        keys: Keys stacked bottom to top.
        names: Legend/tooltip names, aligned with ``keys``.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The tallest stack when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption. Derived from the layer count when omitted.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.STACKED_DATA)
    dark = is_dark(theme)
    keys = list(keys)
    names = list(names)
    value = auto(value, rows, lambda d: max(sum(r[k] for k in keys) for r in d), 160)
    footer_left = footer_left or f"{len(keys)} Monochrome Layers"

    # Opacity ramp: solid at the base, fading toward the top of the stack.
    steps = max(len(keys) - 1, 1)
    bars = []
    for idx, key in enumerate(keys):
        alpha = 1.0 - (idx / steps) * 0.8
        fill = ink(dark) if idx == 0 else ink_alpha(dark, round(alpha, 2))
        radius: Any = None
        if idx == 0:
            radius = [0, 0, 8, 8]
        if idx == len(keys) - 1:
            radius = [8, 8, 0, 0] if len(keys) > 1 else [8, 8, 8, 8]
        kw: dict[str, Any] = {}
        if radius is not None:
            kw["radius"] = radius
        if idx == 0:
            kw["bar_size"] = 18
        bars.append(
            rx.recharts.bar(
                data_key=key,
                name=names[idx] if idx < len(names) else key,
                stack_id="a",
                fill=fill,
                animation_duration=800 + idx * 100,
                **kw,
            )
        )

    return mono_card(
        mono_header(
            title, badge, value, unit, theme=theme, control=control, margin_bottom="0.5rem"
        ),
        mono_stage(
            rx.recharts.bar_chart(
                mono_grid(theme),
                mono_x_axis(theme, x_key),
                mono_y_axis(theme),
                mono_tooltip(theme),
                *bars,
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


def mono_rounded_composed_chart(
    data: Any = None,
    *,
    x_key: str = "label",
    bar_key: str = "count",
    line_key: str = "trend",
    show_line: Any = True,
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Mono Hybrid Spline",
    badge: Any = "Pill + Line",
    value: Any = None,
    unit: Any = "quarterly total",
    footer_left: Any = "Minimalist Monochromatic Layers",
    footer_right: Any = "Peak Target",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """Outlined pill columns with a smooth spline overlay.

    Args:
        data: Rows to plot. Defaults to the built-in demo series.
        x_key: Key holding the category label.
        bar_key: Key holding the column series.
        line_key: Key holding the spline series.
        show_line: Whether the spline is visible. Accepts a Var.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The column total when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.COMPOSED_DATA)
    dark = is_dark(theme)
    value = auto(value, rows, lambda d: sum(r[bar_key] for r in d), 980)
    hidden = ~show_line if isinstance(show_line, rx.Var) else (not show_line)

    return mono_card(
        mono_header(
            title, badge, value, unit, theme=theme, control=control, margin_bottom="0.5rem"
        ),
        mono_stage(
            rx.recharts.composed_chart(
                mono_grid(theme),
                mono_x_axis(theme, x_key),
                mono_y_axis(theme),
                mono_tooltip(theme),
                rx.recharts.bar(
                    data_key=bar_key,
                    name="Volume",
                    fill=ink_alpha(dark, 0.18),
                    stroke=ink_alpha(dark, 0.4),
                    stroke_width=1,
                    radius=[8, 8, 8, 8],
                    bar_size=20,
                    animation_duration=800,
                ),
                rx.recharts.line(
                    data_key=line_key,
                    name="Trend",
                    type_="monotone",
                    stroke=ink(dark),
                    stroke_width=3,
                    dot={
                        "r": 4,
                        "fill": ink(dark),
                        "stroke": "#181818",
                        "strokeWidth": 2,
                    },
                    active_dot={"r": 6, "fill": ink(dark)},
                    hide=hidden,
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


def mono_rounded_waterfall_chart(
    data: Any = None,
    *,
    x_key: str = "step",
    base_key: str = "base",
    delta_key: str = "delta",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Waterfall Steps",
    badge: Any = "Delta",
    value: Any = None,
    unit: Any = "net delta",
    footer_left: Any = "Rounded Floating Pillars",
    footer_right: Any = "Sequential Deltas",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """Floating delta pillars, built from an invisible pedestal bar.

    Each row carries a ``base`` (the transparent pedestal that lifts the bar to
    its starting value) and a ``delta`` (the visible change).

    Args:
        data: Rows to plot. Defaults to the built-in demo series.
        x_key: Key holding the step label.
        base_key: Key holding the invisible pedestal.
        delta_key: Key holding the visible change.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The final delta when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.WATERFALL_DATA)
    dark = is_dark(theme)
    value = auto(value, rows, lambda d: f"+{d[-1][delta_key]}", "+80")

    return mono_card(
        mono_header(
            title, badge, value, unit, theme=theme, control=control, margin_bottom="0.5rem"
        ),
        mono_stage(
            rx.recharts.bar_chart(
                mono_x_axis(theme, x_key),
                mono_y_axis(theme),
                mono_tooltip(theme),
                rx.recharts.bar(
                    data_key=base_key, stack_id="a", fill="transparent", legend_type="none"
                ),
                rx.recharts.bar(
                    data_key=delta_key,
                    name="Delta",
                    stack_id="a",
                    fill=ink(dark),
                    radius=[6, 6, 6, 6],
                    bar_size=18,
                    animation_duration=800,
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


def mono_rounded_funnel_chart(
    data: Any = None,
    *,
    stage_key: str = "stage",
    value_key: str = "volume",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Stage Funnel",
    badge: Any = "Pipeline",
    value: Any = None,
    unit: Any = "conversion",
    footer_left: Any = "Rounded Horizontal Pills",
    footer_right: Any = None,
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """Horizontal pill bars, one per pipeline stage.

    Args:
        data: Stages, widest first. Defaults to the built-in demo series.
        stage_key: Key holding the stage name.
        value_key: Key holding the stage volume.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. End-to-end conversion when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption. The stage count when omitted.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.FUNNEL_DATA)
    dark = is_dark(theme)
    value = auto(
        value,
        rows,
        lambda d: f"{round(d[-1][value_key] / d[0][value_key] * 100)}%",
        "24%",
    )
    footer_right = auto(footer_right, rows, lambda d: f"{len(d)} Funnel Stages", "4 Funnel Stages")

    return mono_card(
        mono_header(
            title, badge, value, unit, theme=theme, control=control, margin_bottom="0.5rem"
        ),
        mono_stage(
            rx.recharts.bar_chart(
                mono_x_axis(theme, type_="number", hide=True),
                mono_y_axis(theme, data_key=stage_key, type_="category"),
                mono_tooltip(theme),
                rx.recharts.bar(
                    data_key=value_key,
                    name="Volume",
                    fill=ink(dark),
                    radius=[0, 8, 8, 0],
                    bar_size=14,
                    animation_duration=800,
                ),
                data=rows,
                layout="vertical",
                margin={"top": 8, "right": 12, "left": -10, "bottom": 0},
                height=chart_height(compact),
            ),
            theme=theme,
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )
