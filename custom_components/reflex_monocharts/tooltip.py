"""The shared Monocharts tooltip and SVG gradient helpers."""

from __future__ import annotations

import itertools
from typing import Any

import reflex as rx

from .card import FONT_SANS
from .theme import ThemeLike, is_dark, pick

__all__ = ["mono_gradient", "mono_tooltip", "unique_id"]

_COUNTER = itertools.count()


def unique_id(prefix: str) -> str:
    """Return a process-unique DOM id, so several cards can coexist on a page.

    The original components namespace their SVG gradient ids with React's
    ``useId``; gradient ids are document-global, so without this two cards on
    one page would share (and fight over) a single gradient definition.

    Args:
        prefix: A readable prefix for the id.

    Returns:
        A unique id string.
    """
    return f"{prefix}-{next(_COUNTER)}"


def mono_tooltip(theme: ThemeLike = "dark", **props: Any) -> rx.Component:
    """The dark, blurred, rounded tooltip used across the whole system.

    Args:
        theme: Theme or theme Var.
        props: Extra props forwarded to ``rx.recharts.graphing_tooltip``.

    Returns:
        A configured recharts tooltip.
    """
    dark = is_dark(theme)
    props.setdefault(
        "content_style",
        {
            "background": pick(dark, "rgba(24,24,24,0.9)", "rgba(255,255,255,0.95)"),
            "borderColor": pick(dark, "rgba(255,255,255,0.1)", "#E5E5E5"),
            "borderWidth": "1px",
            "borderRadius": "0.75rem",
            "padding": "0.5rem 0.75rem",
            "backdropFilter": "blur(8px)",
            "boxShadow": pick(dark, "0 10px 30px rgba(0,0,0,0.8)", "0 10px 30px rgba(0,0,0,0.12)"),
            "fontFamily": FONT_SANS,
            "fontSize": "0.75rem",
            "color": pick(dark, "#FFFFFF", "#171717"),
        },
    )
    props.setdefault(
        "item_style",
        {
            "color": pick(dark, "#FFFFFF", "#171717"),
            "fontSize": "0.75rem",
            "padding": "0.0625rem 0",
            "fontVariantNumeric": "tabular-nums",
        },
    )
    props.setdefault(
        "label_style",
        {
            "color": pick(dark, "#D4D4D4", "#525252"),
            "fontWeight": "500",
            "marginBottom": "0.25rem",
            "letterSpacing": "-0.01em",
        },
    )
    props.setdefault(
        "cursor",
        {"strokeWidth": 1, "stroke": pick(dark, "rgba(255,255,255,0.2)", "rgba(0,0,0,0.2)")},
    )
    return rx.recharts.graphing_tooltip(**props)


def mono_gradient(
    gradient_id: str,
    color: Any,
    *,
    top_opacity: float = 0.35,
    bottom_opacity: float = 0.0,
) -> rx.Component:
    """A zero-size SVG holding one vertical linear gradient.

    SVG paint-server ids resolve document-wide, so a hidden sibling ``<svg>`` is
    enough for a recharts ``fill="url(#id)"`` to find it - this is exactly what
    the original components do.

    Args:
        gradient_id: The DOM id the chart references.
        color: Stop colour (may be a Var).
        top_opacity: Opacity at the top of the area.
        bottom_opacity: Opacity at the baseline.

    Returns:
        An invisible SVG element carrying the gradient definition.
    """
    return rx.el.svg(
        rx.el.svg.defs(
            rx.el.svg.linear_gradient(
                rx.el.svg.stop(offset="0%", stop_color=color, stop_opacity=str(top_opacity)),
                rx.el.svg.stop(offset="100%", stop_color=color, stop_opacity=str(bottom_opacity)),
                id=gradient_id,
                x1="0",
                y1="0",
                x2="0",
                y2="1",
            )
        ),
        position="absolute",
        width="0",
        height="0",
        pointer_events="none",
    )
