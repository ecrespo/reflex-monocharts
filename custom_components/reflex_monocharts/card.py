"""The card chrome every Monocharts component shares.

A Monocharts chart is a card: a rounded surface holding a small uppercase
eyebrow, a badge, a large tabular metric, an optional control on the right, the
chart "stage", and a two-column monospace footer. These helpers build that
chrome so the individual charts only have to describe their series.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import reflex as rx

from .theme import (
    ACCENT,
    CARD_DARK,
    CARD_HOVER_DARK,
    CARD_LIGHT,
    ThemeLike,
    eyebrow_color,
    footer_left_color,
    footer_right_color,
    ink,
    is_dark,
    pick,
    stage_bg,
)

__all__ = [
    "FONT_MONO",
    "FONT_SANS",
    "mono_card",
    "mono_footer",
    "mono_header",
    "mono_segmented",
    "mono_stage",
]

FONT_SANS = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif"
FONT_MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def mono_card(
    *children: Any,
    theme: ThemeLike = "dark",
    compact: Any = False,
    **props: Any,
) -> rx.Component:
    """The outer card surface.

    Args:
        children: Header, stage and footer.
        theme: ``"dark"``, ``"light"``, or a Var holding either.
        compact: Use the short fixed-height card instead of the tall one.
        props: Extra style props forwarded to the underlying box.

    Returns:
        The card box.
    """
    dark = is_dark(theme)
    if isinstance(compact, rx.Var):
        size: dict[str, Any] = {"min_height": rx.cond(compact, "228px", "290px")}
    elif compact:
        size = {"height": rx.breakpoints(initial="220px", sm="268px")}
    else:
        size = {"min_height": "290px"}
    return rx.box(
        *children,
        position="relative",
        width="100%",
        border_radius="24px",
        overflow="hidden",
        display="flex",
        flex_direction="column",
        justify_content="space-between",
        padding=rx.breakpoints(initial="1rem", sm="1.25rem"),
        transition="all 300ms",
        font_family=FONT_SANS,
        background=pick(dark, CARD_DARK, CARD_LIGHT),
        color=ink(dark),
        border=pick(dark, "1px solid rgba(255,255,255,0.04)", "1px solid #F5F5F5"),
        box_shadow=pick(
            dark,
            "inset 0 1px 0 rgba(255,255,255,0.04)",
            "0 4px 20px rgba(0,0,0,0.04)",
        ),
        _hover={
            "background": pick(dark, CARD_HOVER_DARK, CARD_LIGHT),
            "boxShadow": pick(
                dark,
                "inset 0 1px 0 rgba(255,255,255,0.04)",
                "0 6px 24px rgba(0,0,0,0.06)",
            ),
        },
        **size,
        **props,
    )


def mono_header(
    title: Any,
    badge: Any,
    value: Any,
    unit: Any = "",
    *,
    theme: ThemeLike = "dark",
    control: rx.Component | None = None,
    large: bool = False,
    unit_accent: bool = False,
    margin_bottom: str = "0.25rem",
) -> rx.Component:
    """The card header: eyebrow, badge, metric, and an optional right-hand control.

    Args:
        title: The small uppercase label.
        badge: The pill next to the label.
        value: The large metric.
        unit: The muted suffix after the metric.
        theme: Theme or theme Var.
        control: Component rendered flush right (usually :func:`mono_segmented`).
        large: Use the bigger KPI-sized metric type.
        unit_accent: Render the suffix in the emerald accent (for deltas).
        margin_bottom: Gap below the header.

    Returns:
        The header row.
    """
    dark = is_dark(theme)
    return rx.hstack(
        rx.box(
            rx.hstack(
                rx.text(
                    title,
                    flex_shrink="1",
                    font_size="0.75rem",
                    font_weight="600",
                    letter_spacing="0.05em",
                    text_transform="uppercase",
                    color=eyebrow_color(dark),
                ),
                rx.text(
                    badge,
                    display="inline-flex",
                    align_items="center",
                    padding="0.125rem 0.375rem",
                    border_radius="9999px",
                    font_size="0.625rem",
                    font_family=FONT_MONO,
                    background=pick(dark, "rgba(255,255,255,0.1)", "rgba(9,9,11,0.06)"),
                    color=pick(dark, "#FFFFFF", "#3F3F46"),
                    border=pick(
                        dark,
                        "1px solid rgba(255,255,255,0.2)",
                        "1px solid rgba(9,9,11,0.12)",
                    ),
                    white_space="nowrap",
                ),
                spacing="2",
                align="center",
                wrap="wrap",
            ),
            rx.hstack(
                rx.text(
                    value,
                    font_size="1.5rem" if large else "1.25rem",
                    font_weight="800" if large else "700",
                    letter_spacing="-0.025em",
                    font_variant_numeric="tabular-nums",
                    line_height="1.2",
                ),
                rx.cond(
                    unit != "",
                    rx.text(
                        unit,
                        font_size="0.75rem",
                        font_weight="400",
                        opacity="1" if unit_accent else "0.7",
                        color=ACCENT if unit_accent else "inherit",
                        font_family=FONT_MONO if unit_accent else FONT_SANS,
                    ),
                    rx.fragment(),
                ),
                spacing="1",
                align="baseline",
                margin_top="0.25rem" if large else "0.125rem",
            ),
            min_width="0",
        ),
        rx.spacer(),
        control if control is not None else rx.fragment(),
        width="100%",
        align="center",
        justify="between",
        margin_bottom=margin_bottom,
        spacing="2",
    )


def mono_segmented(
    options: Sequence[tuple[Any, Any]],
    value: Any,
    on_change: Any,
    *,
    theme: ThemeLike = "dark",
) -> rx.Component:
    """A pill segmented control, matching the toggles on the original cards.

    Args:
        options: ``(value, label)`` pairs, left to right.
        value: The currently selected value (usually a state Var).
        on_change: Event handler receiving the clicked value.
        theme: Theme or theme Var.

    Returns:
        The segmented control.

    Example:
        ```python
        class S(rx.State):
            curve: str = "monotone"

        mono_segmented(
            [("monotone", "Monotone"), ("natural", "Natural")],
            S.curve,
            S.set_curve,
        )
        ```
    """
    dark = is_dark(theme)
    buttons = []
    for opt_value, label in options:
        selected = value == opt_value
        buttons.append(
            rx.el.button(
                label,
                on_click=on_change(opt_value),
                padding="0.125rem 0.625rem",
                border_radius="9999px",
                font_size="0.6875rem",
                font_weight=rx.cond(selected, "600", "500"),
                cursor="pointer",
                border="none",
                transition="all 200ms",
                white_space="nowrap",
                background=rx.cond(
                    selected,
                    pick(dark, "#FFFFFF", "#000000"),
                    "transparent",
                ),
                color=rx.cond(
                    selected,
                    pick(dark, "#000000", "#FFFFFF"),
                    pick(dark, "#A3A3A3", "#525252"),
                ),
                box_shadow=rx.cond(selected, "0 1px 2px rgba(0,0,0,0.2)", "none"),
            )
        )
    return rx.hstack(
        *buttons,
        padding="0.125rem",
        border_radius="9999px",
        border=pick(dark, "1px solid rgba(255,255,255,0.1)", "1px solid #E5E5E5"),
        background=pick(dark, "rgba(255,255,255,0.05)", "#F5F5F5"),
        spacing="0",
        align="center",
        flex_shrink="0",
    )


def mono_stage(
    *children: Any,
    theme: ThemeLike = "dark",
    padding: str = "0.5rem",
    **props: Any,
) -> rx.Component:
    """The inner surface the chart is drawn on.

    Args:
        children: The chart, or hand-built markup.
        theme: Theme or theme Var.
        padding: Inner padding.
        props: Extra style props (layout for the div-based charts).

    Returns:
        The stage box.
    """
    dark = is_dark(theme)
    return rx.box(
        *children,
        position="relative",
        width="100%",
        flex="1",
        border_radius="14px",
        overflow="hidden",
        padding=padding,
        transition="background-color 300ms",
        background=stage_bg(dark),
        **props,
    )


def mono_footer(left: Any, right: Any, *, theme: ThemeLike = "dark") -> rx.Component:
    """The two-column monospace footer.

    Args:
        left: Muted left-hand caption.
        right: Emphasised right-hand caption.
        theme: Theme or theme Var.

    Returns:
        The footer row.
    """
    dark = is_dark(theme)
    return rx.hstack(
        rx.text(left, color=footer_left_color(dark)),
        rx.spacer(),
        rx.text(right, color=footer_right_color(dark), font_weight="500"),
        width="100%",
        align="center",
        justify="between",
        margin_top="0.75rem",
        padding_top="0.25rem",
        border_top=pick(dark, "1px solid rgba(255,255,255,0.05)", "1px solid rgba(0,0,0,0.06)"),
        font_size="0.6875rem",
        font_family=FONT_MONO,
        spacing="2",
    )
