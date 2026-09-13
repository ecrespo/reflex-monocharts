"""Design tokens for the Monocharts visual system.

Every colour in Monocharts is derived from a single monochrome pair - white on a
near-black card in dark mode, near-black on white in light mode. These helpers
resolve that pair for either a plain Python string (``"dark"`` / ``"light"``) or
a Reflex ``Var``, so a chart can be wired to a state variable and switch themes
without a page reload.
"""

from __future__ import annotations

from typing import Any

import reflex as rx

__all__ = [
    "ACCENT",
    "CARD_DARK",
    "CARD_HOVER_DARK",
    "CARD_LIGHT",
    "INK_DARK",
    "INK_LIGHT",
    "STAGE_DARK",
    "STAGE_LIGHT",
    "TICK_DARK",
    "TICK_LIGHT",
    "ThemeLike",
    "axis_tick",
    "eyebrow_color",
    "footer_left_color",
    "footer_right_color",
    "grid_stroke",
    "ink",
    "ink_alpha",
    "is_dark",
    "muted_ink",
    "pick",
    "stage_bg",
]

#: Accepted shapes for the ``theme`` argument of every Monocharts component.
ThemeLike = str | bool | rx.Var

# --- raw tokens -------------------------------------------------------------

#: Primary series colour on a dark card.
INK_DARK = "#FFFFFF"
#: Primary series colour on a light card.
INK_LIGHT = "#09090B"

#: Card surface.
CARD_DARK = "#181818"
CARD_LIGHT = "#FFFFFF"
CARD_HOVER_DARK = "#202020"

#: Inner "stage" surface the chart itself sits on.
STAGE_DARK = "#131313"
STAGE_LIGHT = "#F4F4F6"

#: Axis tick labels.
TICK_DARK = "#71717A"
TICK_LIGHT = "#A1A1AA"

#: The one accent colour the monochrome system allows itself (emerald-400),
#: used for benchmark markers and positive deltas.
ACCENT = "#34D399"

#: Muted secondary series stroke.
MUTED_DARK = "#A1A1AA"
MUTED_LIGHT = "#52525B"


# --- resolution helpers -----------------------------------------------------


def is_dark(theme: ThemeLike) -> Any:
    """Return a truthy value (or Var) that is true when ``theme`` is dark.

    Args:
        theme: ``"dark"``/``"light"``, a bool, or a Var holding either.

    Returns:
        A ``bool`` for plain input, or a ``Var[bool]`` for Var input.
    """
    if isinstance(theme, rx.Var):
        # A string Var compares against "dark"; a bool Var is already the flag.
        if issubclass(theme._var_type, bool):
            return theme
        return theme == "dark"
    if isinstance(theme, bool):
        return theme
    return theme == "dark"


def pick(dark_flag: Any, dark_value: Any, light_value: Any) -> Any:
    """Choose between a dark-mode and a light-mode value.

    Args:
        dark_flag: The result of :func:`is_dark`.
        dark_value: Value to use on a dark card.
        light_value: Value to use on a light card.

    Returns:
        One of the two values, or an ``rx.cond`` Var when the flag is reactive.
    """
    if isinstance(dark_flag, rx.Var):
        return rx.cond(dark_flag, dark_value, light_value)
    return dark_value if dark_flag else light_value


def _rgba(rgb: str, alpha: float) -> str:
    return f"rgba({rgb},{alpha})"


def ink(dark_flag: Any) -> Any:
    """The primary monochrome series colour."""
    return pick(dark_flag, INK_DARK, INK_LIGHT)


def ink_alpha(dark_flag: Any, alpha: float) -> Any:
    """The primary series colour at a given alpha, correct for both themes."""
    return pick(
        dark_flag,
        _rgba("255,255,255", alpha),
        _rgba("9,9,11", alpha),
    )


def muted_ink(dark_flag: Any) -> Any:
    """The secondary / baseline series colour."""
    return pick(dark_flag, MUTED_DARK, MUTED_LIGHT)


def stage_bg(dark_flag: Any) -> Any:
    """Background of the inner chart stage."""
    return pick(dark_flag, STAGE_DARK, STAGE_LIGHT)


def grid_stroke(dark_flag: Any) -> Any:
    """Cartesian grid line colour."""
    return pick(dark_flag, "rgba(255,255,255,0.05)", "rgba(0,0,0,0.05)")


def axis_tick(dark_flag: Any, size: int = 10) -> dict:
    """The ``tick`` dict shared by every cartesian and polar axis."""
    return {"fontSize": size, "fill": pick(dark_flag, TICK_DARK, TICK_LIGHT)}


def eyebrow_color(dark_flag: Any) -> Any:
    """Colour of the small uppercase label above the metric."""
    return pick(dark_flag, "#A3A3A3", "#737373")


def footer_left_color(dark_flag: Any) -> Any:
    """Colour of the muted left-hand footer text."""
    return pick(dark_flag, "#A3A3A3", "#525252")


def footer_right_color(dark_flag: Any) -> Any:
    """Colour of the emphasised right-hand footer text."""
    return pick(dark_flag, "#FFFFFF", "#000000")
