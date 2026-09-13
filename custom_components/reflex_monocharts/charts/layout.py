"""Monocharts cards drawn with layout primitives and SVG instead of recharts.

Bullet bars, pyramids, treemaps, heatmaps, candlesticks, Sankey bands and the
contribution grid are all geometry a chart library gets in the way of, so they
are built directly out of boxes and SVG - exactly as the originals are.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import reflex as rx

from .. import data as demo
from ..card import FONT_MONO, FONT_SANS, mono_card, mono_footer, mono_header, mono_stage
from ..theme import ACCENT, ThemeLike, ink, ink_alpha, is_dark, pick
from ._common import auto, resolve

__all__ = [
    "mono_activity_heatmap",
    "mono_rounded_bullet_chart",
    "mono_rounded_candlestick_chart",
    "mono_rounded_heatmap_chart",
    "mono_rounded_pyramid_chart",
    "mono_rounded_sankey_chart",
    "mono_rounded_treemap_chart",
]

#: Accent ramps for the contribution grid.
ACTIVITY_ACCENTS: dict[str, tuple[str, str]] = {
    "green": ("#39D353", "#34D399"),
    "blue": ("#3B82F6", "#60A5FA"),
    "purple": ("#A855F7", "#C084FC"),
}

#: Opacity per contribution level, 0 through 4.
ACTIVITY_LEVELS: tuple[float, ...] = (0.06, 0.3, 0.55, 0.8, 1.0)


def _each(rows: Any, render: Any) -> rx.Component:
    """Render a list of rows, whether it is a plain list or a state Var."""
    if isinstance(rows, rx.Var):
        return rx.foreach(rows, render)
    return rx.fragment(*[render(row) for row in rows])


def _num(value: Any) -> Any:
    """Type a value read out of an untyped state row as a number."""
    return value.to(float) if isinstance(value, rx.Var) else value


def _numbers(value: Any) -> Any:
    """Type a value read out of an untyped state row as a list of numbers."""
    return value.to(list[float]) if isinstance(value, rx.Var) else value


def _max2(a: Any, b: Any) -> Any:
    """``max`` that also works on two Vars."""
    if isinstance(a, rx.Var) or isinstance(b, rx.Var):
        return rx.cond(a >= b, a, b)
    return max(a, b)


def _min2(a: Any, b: Any) -> Any:
    """``min`` that also works on two Vars."""
    if isinstance(a, rx.Var) or isinstance(b, rx.Var):
        return rx.cond(a <= b, a, b)
    return min(a, b)


# --------------------------------------------------------------------------- #
# Bullet
# --------------------------------------------------------------------------- #


def mono_rounded_bullet_chart(
    data: Any = None,
    *,
    title_key: str = "title",
    actual_key: str = "actual",
    target_key: str = "target",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Bullet Target",
    badge: Any = "Benchmark",
    value: Any = None,
    unit: Any = "evaluated",
    footer_left: Any = "Rounded Bullet Bars",
    footer_right: Any = "Benchmark Marker",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """Progress bars with a benchmark marker per row.

    Args:
        data: One row per measure. Defaults to the built-in demo series.
        title_key: Key holding the measure name.
        actual_key: Key holding the achieved percentage.
        target_key: Key holding the benchmark percentage.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The target count when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.BULLET_DATA)
    dark = is_dark(theme)
    value = auto(value, rows, lambda d: f"{len(d)} Targets", "3 Targets")

    def row(item: Any) -> rx.Component:
        return rx.vstack(
            rx.hstack(
                rx.text(
                    item[title_key],
                    font_weight="500",
                    color=pick(dark, "#FFFFFF", "#000000"),
                ),
                rx.spacer(),
                rx.text(
                    f"{item[actual_key]}% / {item[target_key]}%",
                    color=pick(dark, "#A3A3A3", "#737373"),
                ),
                width="100%",
                align="center",
                font_size="0.6875rem",
                font_family=FONT_MONO,
            ),
            rx.box(
                rx.box(
                    height="100%",
                    width=f"{item[actual_key]}%",
                    border_radius="9999px",
                    background=ink(dark),
                    transition="width 400ms",
                ),
                rx.box(
                    position="absolute",
                    top="0",
                    bottom="0",
                    left=f"calc({item[target_key]}% - 2px)",
                    width="4px",
                    border_radius="9999px",
                    background=ACCENT,
                    box_shadow="0 1px 2px rgba(0,0,0,0.2)",
                ),
                position="relative",
                width="100%",
                height="0.875rem",
                border_radius="9999px",
                overflow="hidden",
                background=ink_alpha(dark, 0.1),
            ),
            width="100%",
            spacing="1",
        )

    return mono_card(
        mono_header(title, badge, value, unit, theme=theme, control=control),
        mono_stage(
            _each(rows, row),
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


# --------------------------------------------------------------------------- #
# Pyramid
# --------------------------------------------------------------------------- #


def mono_rounded_pyramid_chart(
    data: Any = None,
    *,
    label_key: str = "label",
    width_key: str = "width",
    opacity_key: str = "opacity",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Pyramid Stack",
    badge: Any = "Hierarchy",
    value: Any = None,
    unit: Any = "structured",
    footer_left: Any = "Rounded Tier Layers",
    footer_right: Any = "Pyramid Hierarchy",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """Stacked hierarchy tiers, narrowest at the top.

    Args:
        data: One row per tier, top first. Defaults to the built-in demo series.
        label_key: Key holding the tier name.
        width_key: Key holding the tier width as a percentage.
        opacity_key: Key holding the tier fill opacity, 0-1.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The tier count when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.PYRAMID_DATA)
    dark = is_dark(theme)
    value = auto(value, rows, lambda d: f"{len(d)} Tiers", "4 Tiers")

    def tier(item: Any) -> rx.Component:
        opacity = _num(item[opacity_key])
        bright = opacity > 0.6
        return rx.box(
            rx.text(
                item[label_key],
                font_size="0.625rem",
                font_weight="700",
                font_family=FONT_MONO,
                letter_spacing="-0.025em",
            ),
            width=f"{item[width_key]}%",
            height=rx.breakpoints(initial="1.5rem", sm="1.75rem"),
            border_radius="12px",
            display="flex",
            align_items="center",
            justify_content="center",
            border=pick(dark, "1px solid rgba(255,255,255,0.2)", "1px solid rgba(9,9,11,0.2)"),
            background=pick(
                dark,
                f"rgba(255,255,255,{opacity})",
                f"rgba(9,9,11,{opacity})",
            ),
            color=pick(
                dark,
                rx.cond(bright, "#000000", "#FFFFFF"),
                rx.cond(bright, "#FFFFFF", "#000000"),
            ),
            transition="transform 200ms",
            cursor="pointer",
            _hover={"transform": "scale(1.05)"},
            flex_shrink="0",
        )

    return mono_card(
        mono_header(title, badge, value, unit, theme=theme, control=control),
        mono_stage(
            _each(rows, tier),
            theme=theme,
            padding="0.75rem",
            display="flex",
            flex_direction="column",
            align_items="center",
            justify_content="space-around",
            gap="0.5rem",
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


# --------------------------------------------------------------------------- #
# Treemap
# --------------------------------------------------------------------------- #


def mono_rounded_treemap_chart(
    data: Any = None,
    *,
    label_key: str = "label",
    share_key: str = "share",
    cols_key: str = "cols",
    rows_key: str = "rows",
    opacity_key: str = "opacity",
    columns: int = 3,
    grid_rows: int = 3,
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Tile Treemap",
    badge: Any = "Allocation",
    value: Any = None,
    unit: Any = "partitioned",
    footer_left: Any = "Rounded Corner Tiles",
    footer_right: Any = None,
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A rounded-tile partition map laid out on a CSS grid.

    Args:
        data: One row per tile. Defaults to the built-in demo series.
        label_key: Key holding the tile name.
        share_key: Key holding the tile percentage.
        cols_key: Key holding how many grid columns the tile spans.
        rows_key: Key holding how many grid rows the tile spans.
        opacity_key: Key holding the tile fill opacity, 0-1.
        columns: Grid column count.
        grid_rows: Grid row count.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The share total when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption. The tile count when omitted.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    tiles = resolve(data, demo.TREEMAP_DATA)
    dark = is_dark(theme)
    value = auto(value, tiles, lambda d: f"{sum(t[share_key] for t in d)}%", "100%")
    footer_right = auto(
        footer_right, tiles, lambda d: f"{len(d)} Resource Partitions", "4 Resource Partitions"
    )

    def tile(item: Any) -> rx.Component:
        opacity = _num(item[opacity_key])
        bright = opacity > 0.5
        return rx.box(
            rx.text(
                item[label_key],
                font_size="0.6875rem",
                font_weight="700",
                letter_spacing="-0.025em",
                font_family=FONT_SANS,
            ),
            rx.spacer(),
            rx.text(
                f"{item[share_key]}%",
                font_size="0.625rem",
                font_family=FONT_MONO,
                opacity="0.8",
            ),
            grid_column=f"span {item[cols_key]}",
            grid_row=f"span {item[rows_key]}",
            border_radius="12px",
            padding="0.5rem",
            display="flex",
            flex_direction="column",
            justify_content="space-between",
            overflow="hidden",
            border=pick(dark, "1px solid rgba(255,255,255,0.1)", "1px solid rgba(0,0,0,0.1)"),
            background=pick(dark, f"rgba(255,255,255,{opacity})", f"rgba(9,9,11,{opacity})"),
            color=pick(
                dark,
                rx.cond(bright, "#000000", "#FFFFFF"),
                rx.cond(bright, "#FFFFFF", "#000000"),
            ),
            transition="transform 200ms",
            cursor="pointer",
            _hover={"transform": "scale(1.02)"},
        )

    return mono_card(
        mono_header(title, badge, value, unit, theme=theme, control=control),
        mono_stage(
            _each(tiles, tile),
            theme=theme,
            display="grid",
            grid_template_columns=f"repeat({columns}, minmax(0, 1fr))",
            grid_template_rows=f"repeat({grid_rows}, minmax(0, 1fr))",
            gap="0.375rem",
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


# --------------------------------------------------------------------------- #
# Density heatmap
# --------------------------------------------------------------------------- #


def mono_rounded_heatmap_chart(
    data: Any = None,
    *,
    label_key: str = "label",
    values_key: str = "values",
    scale: float = 100.0,
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Matrix Heatmap",
    badge: Any = "Activity",
    value: Any = None,
    unit: Any = "mapped",
    footer_left: Any = "Rounded Node Cells",
    footer_right: Any = None,
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A labelled density matrix, one row per label.

    Args:
        data: One row per label, each with a list of values. Defaults to the
            built-in demo series.
        label_key: Key holding the row label.
        values_key: Key holding the row's list of values.
        scale: The value that maps to full opacity.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The cell count when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption. The grid shape when omitted.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    rows = resolve(data, demo.HEATMAP_DATA)
    dark = is_dark(theme)
    value = auto(value, rows, lambda d: f"{sum(len(r[values_key]) for r in d)} Nodes", "35 Nodes")
    footer_right = auto(
        footer_right,
        rows,
        lambda d: f"{len(d[0][values_key])}x{len(d)} Density Grid",
        "7x5 Density Grid",
    )

    def cell(val: Any) -> rx.Component:
        opacity = _num(val) / scale
        return rx.box(
            height=rx.breakpoints(initial="1rem", sm="1.25rem"),
            flex="1",
            border_radius="6px",
            background=pick(dark, f"rgba(255,255,255,{opacity})", f"rgba(9,9,11,{opacity})"),
            transition="transform 150ms",
            cursor="pointer",
            title=f"{val}",
            _hover={"transform": "scale(1.1)"},
        )

    def row(item: Any) -> rx.Component:
        return rx.hstack(
            rx.text(
                item[label_key],
                font_size="0.625rem",
                font_family=FONT_MONO,
                width="1.75rem",
                flex_shrink="0",
                color=pick(dark, "#A3A3A3", "#737373"),
            ),
            rx.hstack(
                _each(_numbers(item[values_key]), cell),
                flex="1",
                width="100%",
                align="center",
                spacing="1",
            ),
            width="100%",
            align="center",
            spacing="1",
        )

    return mono_card(
        mono_header(title, badge, value, unit, theme=theme, control=control),
        mono_stage(
            _each(rows, row),
            theme=theme,
            padding="0.75rem",
            display="flex",
            flex_direction="column",
            justify_content="center",
            gap="0.375rem",
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


# --------------------------------------------------------------------------- #
# Candlestick
# --------------------------------------------------------------------------- #


def mono_rounded_candlestick_chart(
    data: Any = None,
    *,
    time_key: str = "time",
    open_key: str = "open",
    high_key: str = "high",
    low_key: str = "low",
    close_key: str = "close",
    low_bound: float | None = None,
    high_bound: float | None = None,
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Financial Wicks",
    badge: Any = "Candlestick",
    value: Any = None,
    unit: Any = "close price",
    footer_left: Any = "Rounded Wick Endcaps",
    footer_right: Any = None,
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """OHLC candles with rounded bodies and rounded wick caps.

    Bodies are hollow when the candle closed below its open.

    Args:
        data: OHLC rows. Defaults to the built-in demo series.
        time_key: Key holding the period label.
        open_key: Key holding the open price.
        high_key: Key holding the high price.
        low_key: Key holding the low price.
        close_key: Key holding the close price.
        low_bound: Bottom of the price scale. The dataset low when omitted.
        high_bound: Top of the price scale. The dataset high when omitted.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. The last close when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption. The candle count when omitted.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.

    Raises:
        TypeError: If a reactive dataset is passed without explicit bounds,
            since the price scale cannot then be computed.
    """
    rows = resolve(data, demo.CANDLE_DATA)
    dark = is_dark(theme)

    if isinstance(rows, rx.Var):
        if low_bound is None or high_bound is None:
            msg = (
                "mono_rounded_candlestick_chart needs explicit low_bound and "
                "high_bound when data is a state Var, because the price scale "
                "cannot be derived from a Var at build time."
            )
            raise TypeError(msg)
    else:
        low_bound = min(r[low_key] for r in rows) - 10 if low_bound is None else low_bound
        high_bound = max(r[high_key] for r in rows) + 10 if high_bound is None else high_bound

    span = max(float(high_bound) - float(low_bound), 1e-9)
    value = auto(value, rows, lambda d: f"{d[-1][close_key]:.2f}", "175.00")
    footer_right = auto(footer_right, rows, lambda d: f"{len(d)} Price Candles", "5 Price Candles")

    def candle(item: Any) -> rx.Component:
        o = _num(item[open_key])
        h = _num(item[high_key])
        low = _num(item[low_key])
        c = _num(item[close_key])
        bull = c >= o
        body_top = _max2(o, c)
        body_bottom = _min2(o, c)
        top_pct = (high_bound - body_top) / span * 100
        body_pct = (body_top - body_bottom) / span * 100
        high_pct = (high_bound - h) / span * 100
        low_pct = (low - low_bound) / span * 100
        return rx.box(
            rx.box(
                position="absolute",
                width="2px",
                border_radius="9999px",
                background=ink(dark),
                opacity="0.4",
                top=f"{high_pct}%",
                bottom=f"{low_pct}%",
            ),
            rx.box(
                position="absolute",
                width=rx.breakpoints(initial="1.25rem", sm="1.5rem"),
                border_radius="6px",
                top=f"{top_pct}%",
                height=f"max({body_pct}%, 8%)",
                border="1px solid",
                border_color=ink(dark),
                background=rx.cond(bull, ink(dark), ink_alpha(dark, 0.15))
                if isinstance(bull, rx.Var)
                else (ink(dark) if bull else ink_alpha(dark, 0.15)),
            ),
            rx.text(
                item[time_key],
                position="absolute",
                bottom="0",
                font_size="0.5625rem",
                font_family=FONT_MONO,
                color=pick(dark, "#A3A3A3", "#737373"),
            ),
            position="relative",
            flex="1",
            height="100%",
            display="flex",
            align_items="center",
            justify_content="center",
        )

    return mono_card(
        mono_header(title, badge, value, unit, theme=theme, control=control),
        mono_stage(
            _each(rows, candle),
            theme=theme,
            padding="0.75rem",
            display="flex",
            align_items="center",
            justify_content="space-around",
            gap="0.5rem",
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


# --------------------------------------------------------------------------- #
# Sankey
# --------------------------------------------------------------------------- #


def mono_rounded_sankey_chart(
    data: Any = None,
    *,
    source_key: str = "source",
    target_key: str = "target",
    value_key: str = "value",
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Sankey Flow",
    badge: Any = "Transfer",
    value: Any = None,
    unit: Any = "flow routed",
    footer_left: Any = "Rounded Flow Bands",
    footer_right: Any = "Channel Routing",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """Curved flow bands routing several sources into one target.

    Band thickness is proportional to each flow's share of the total, and the
    SVG is ``viewBox``-scaled so the geometry tracks the card at any width.

    Args:
        data: Flows, each with a source, a target and a weight. Must be a plain
            list - the band geometry is computed at build time.
        source_key: Key holding the source node name.
        target_key: Key holding the target node name.
        value_key: Key holding the flow weight.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label.
        value: Headline metric. ``"100%"`` when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption.
        footer_right: Emphasised footer caption.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.

    Raises:
        TypeError: If ``data`` is a state Var.
    """
    flows = resolve(data, demo.SANKEY_DATA)
    if isinstance(flows, rx.Var):
        msg = (
            "mono_rounded_sankey_chart computes its band geometry at build time "
            "and needs a plain list of flows, not a state Var."
        )
        raise TypeError(msg)

    dark = is_dark(theme)
    total = sum(f[value_key] for f in flows) or 1
    value = value if value is not None else "100%"
    sink = flows[0][target_key] if flows else "Target"

    # viewBox space: sources on the left edge, the sink centred on the right.
    vb_w, vb_h = 280.0, 120.0
    x0, x1 = 58.0, 222.0
    y_mid = vb_h / 2
    n = max(len(flows), 1)
    bands = []
    node_labels = []
    for i, flow in enumerate(flows):
        y = vb_h * (i + 1) / (n + 1)
        share = flow[value_key] / total
        width = max(6.0, share * 34.0)
        bands.append(
            rx.el.svg.path(
                d=f"M {x0},{y:.1f} C {x0 + 70},{y:.1f} {x1 - 70},{y_mid:.1f} {x1},{y_mid:.1f}",
                fill="none",
                stroke=ink(dark),
                stroke_width=f"{width:.1f}",
                stroke_opacity=f"{max(0.12, 0.35 - i * 0.05):.2f}",
                stroke_linecap="round",
            )
        )
        node_labels.append((flow[source_key], round(share * 100)))

    def node(label: str, share: int, index: int) -> rx.Component:
        return rx.box(
            rx.text(label, font_size="0.625rem", font_weight="700", font_family=FONT_MONO),
            rx.text(f"{share}%", font_size="0.5625rem", opacity="0.8", font_family=FONT_MONO),
            width="3.25rem",
            padding="0.25rem",
            border_radius="8px",
            display="flex",
            flex_direction="column",
            align_items="center",
            justify_content="center",
            background=ink_alpha(dark, max(0.35, 0.95 - index * 0.3)),
            color=pick(dark, "#131313", "#FFFFFF"),
            z_index="1",
            flex_shrink="0",
        )

    return mono_card(
        mono_header(title, badge, value, unit, theme=theme, control=control),
        mono_stage(
            rx.el.svg(
                *bands,
                view_box=f"0 0 {vb_w:.0f} {vb_h:.0f}",
                preserve_aspect_ratio="none",
                position="absolute",
                top="0",
                left="0",
                width="100%",
                height="100%",
                pointer_events="none",
            ),
            rx.vstack(
                *[node(lbl, share, i) for i, (lbl, share) in enumerate(node_labels)],
                height="100%",
                justify="center",
                spacing="3",
                z_index="1",
            ),
            rx.spacer(),
            rx.box(
                rx.text(sink, font_size="0.625rem", font_weight="700", font_family=FONT_MONO),
                rx.text("Output", font_size="0.5625rem", opacity="0.8", font_family=FONT_MONO),
                width="3.5rem",
                height="3.5rem",
                border_radius="12px",
                display="flex",
                flex_direction="column",
                align_items="center",
                justify_content="center",
                background=ink(dark),
                color=pick(dark, "#131313", "#FFFFFF"),
                box_shadow="0 4px 10px rgba(0,0,0,0.25)",
                z_index="1",
                flex_shrink="0",
            ),
            theme=theme,
            padding="0.75rem",
            display="flex",
            flex_direction="row",
            align_items="center",
            justify_content="space-between",
            gap="1rem",
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )


# --------------------------------------------------------------------------- #
# Contribution grid
# --------------------------------------------------------------------------- #


def mono_activity_heatmap(
    data: Any = None,
    *,
    accent: str = "green",
    weeks: int = 20,
    months: Sequence[str] = ("Jan", "Feb", "Mar", "Apr", "May"),
    theme: ThemeLike = "dark",
    compact: Any = False,
    title: Any = "Activity Heatmap",
    badge: Any = None,
    value: Any = None,
    unit: Any = "contributions",
    footer_left: Any = None,
    footer_right: Any = "Contribution Grid",
    caption: Any = "Hover tiles for daily counts",
    control: rx.Component | None = None,
    **props: Any,
) -> rx.Component:
    """A GitHub-style contribution grid in one of four accent ramps.

    Each cell carries a native ``title`` tooltip rather than a server round-trip,
    so the grid stays responsive at 140+ cells.

    Args:
        data: Contribution entries with ``date``, ``count`` and ``level``.
            Defaults to a seeded demo series.
        accent: ``"green"``, ``"blue"``, ``"purple"`` or ``"mono"``.
        weeks: Number of week columns to lay out.
        months: Month captions above the grid.
        theme: ``"dark"``, ``"light"``, or a Var.
        compact: Render the short card.
        title: Uppercase eyebrow label.
        badge: Pill beside the label. Derived from the accent when omitted.
        value: Headline metric. The contribution total when omitted.
        unit: Muted suffix after the metric.
        footer_left: Muted footer caption. The grid shape when omitted.
        footer_right: Emphasised footer caption.
        caption: Hint line under the grid.
        control: Component rendered on the right of the header.
        props: Extra style props for the card.

    Returns:
        The chart card.
    """
    entries = data if data is not None else demo.activity_contributions(weeks)
    dark = is_dark(theme)

    if accent in ACTIVITY_ACCENTS:
        cell_color: Any = ACTIVITY_ACCENTS[accent][0]
        default_badge = {
            "green": "Emerald Matrix",
            "blue": "Sky Blue Grid",
            "purple": "Violet Pulse",
        }[accent]
    else:
        cell_color = ink(dark)
        default_badge = "Monochrome Heat"
    badge = badge or default_badge

    value = auto(value, entries, lambda d: sum(e["count"] for e in d), 0)
    footer_left = footer_left or f"{weeks} Weeks x 7 Days Grid"

    def cell(entry: Any) -> rx.Component:
        level = entry["level"]
        opacity: Any = ACTIVITY_LEVELS[-1]
        for idx in range(len(ACTIVITY_LEVELS) - 2, -1, -1):
            opacity = rx.cond(level == idx, ACTIVITY_LEVELS[idx], opacity)
        return rx.box(
            width="100%",
            height=rx.breakpoints(initial="0.75rem", sm="0.875rem"),
            border_radius="3px",
            background=cell_color,
            opacity=opacity,
            transition="transform 150ms",
            cursor="pointer",
            title=f"{entry['count']} on {entry['date']}",
            _hover={"transform": "scale(1.25)"},
        )

    if isinstance(entries, rx.Var):
        grid: rx.Component = rx.box(
            rx.foreach(entries, cell),
            display="grid",
            grid_template_rows="repeat(7, minmax(0, 1fr))",
            grid_auto_flow="column",
            grid_auto_columns="minmax(0, 1fr)",
            gap="0.375rem",
            width="100%",
        )
    else:
        columns = [entries[i : i + 7] for i in range(0, len(entries), 7)]
        grid = rx.hstack(
            *[
                rx.vstack(
                    *[cell(e) for e in col],
                    spacing="0",
                    gap="0.375rem",
                    flex="1",
                    align="center",
                    width="100%",
                )
                for col in columns
            ],
            width="100%",
            align="center",
            spacing="0",
            gap="0.375rem",
            overflow="hidden",
        )

    return mono_card(
        mono_header(
            title, badge, value, unit, theme=theme, control=control, margin_bottom="0.5rem"
        ),
        mono_stage(
            rx.hstack(
                *[
                    rx.text(
                        m,
                        font_size="0.625rem",
                        font_family=FONT_MONO,
                        flex="1",
                        text_align="center",
                        color=pick(dark, "#A3A3A3", "#737373"),
                    )
                    for m in months
                ],
                width="100%",
                margin_bottom="0.375rem",
                gap="0.375rem",
                spacing="0",
            ),
            grid,
            rx.box(
                rx.text(
                    caption,
                    font_size="0.625rem",
                    font_family=FONT_MONO,
                    color=pick(dark, "#A3A3A3", "#737373"),
                ),
                height="1.25rem",
                margin_top="0.5rem",
                display="flex",
                align_items="center",
                justify_content="center",
                width="100%",
            ),
            theme=theme,
            padding="0.75rem",
            display="flex",
            flex_direction="column",
            justify_content="center",
            align_items="center",
        ),
        mono_footer(footer_left, footer_right, theme=theme),
        theme=theme,
        compact=compact,
        **props,
    )
