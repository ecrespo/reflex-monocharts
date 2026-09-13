"""Monocharts for Reflex.

A Python port of the Monocharts design system: 28 monochromatic, rounded chart
cards built on ``rx.recharts`` and Reflex layout primitives, with no npm
dependency and no Tailwind requirement.

Every chart is a plain function returning an ``rx.Component``. Called with no
arguments it renders the original demo card; pass ``data`` (and the matching
``*_key`` arguments) to bind it to your own state.

Example:
    ```python
    import reflex as rx
    from reflex_monocharts import monocharts

    class State(rx.State):
        theme: str = "dark"
        traffic: list[dict] = [{"label": "Jan", "value": 24}]

    def index() -> rx.Component:
        return monocharts.line(
            State.traffic, value_key="value", secondary_key=None, theme=State.theme
        )
    ```
"""

from __future__ import annotations

from types import SimpleNamespace

from . import data
from .card import (
    FONT_MONO,
    FONT_SANS,
    mono_card,
    mono_footer,
    mono_header,
    mono_segmented,
    mono_stage,
)
from .charts.areas import (
    mono_rounded_area_chart,
    mono_rounded_range_chart,
    mono_rounded_stream_chart,
)
from .charts.bars import (
    mono_rounded_bar_chart,
    mono_rounded_composed_chart,
    mono_rounded_funnel_chart,
    mono_rounded_stacked_bar_chart,
    mono_rounded_waterfall_chart,
)
from .charts.layout import (
    mono_activity_heatmap,
    mono_rounded_bullet_chart,
    mono_rounded_candlestick_chart,
    mono_rounded_heatmap_chart,
    mono_rounded_pyramid_chart,
    mono_rounded_sankey_chart,
    mono_rounded_treemap_chart,
)
from .charts.lines import (
    mono_rounded_kpi_card_chart,
    mono_rounded_line_chart,
    mono_rounded_sparkline_chart,
    mono_rounded_step_chart,
)
from .charts.points import mono_rounded_bubble_chart, mono_rounded_scatter_chart
from .charts.polar import (
    mono_rounded_donut_chart,
    mono_rounded_gauge_arc,
    mono_rounded_meter_chart,
    mono_rounded_polar_chart,
    mono_rounded_radar_chart,
    mono_rounded_radial_bar_group,
    mono_rounded_radial_gauge_chart,
)
from .theme import (
    ACCENT,
    CARD_DARK,
    CARD_LIGHT,
    INK_DARK,
    INK_LIGHT,
    STAGE_DARK,
    STAGE_LIGHT,
    ThemeLike,
    ink,
    ink_alpha,
    is_dark,
    pick,
)
from .tooltip import mono_gradient, mono_tooltip

__version__ = "0.1.2"

#: Short aliases, so a whole dashboard reads as ``monocharts.line(...)``.
monocharts = SimpleNamespace(
    activity=mono_activity_heatmap,
    area=mono_rounded_area_chart,
    bar=mono_rounded_bar_chart,
    bubble=mono_rounded_bubble_chart,
    bullet=mono_rounded_bullet_chart,
    candlestick=mono_rounded_candlestick_chart,
    composed=mono_rounded_composed_chart,
    donut=mono_rounded_donut_chart,
    funnel=mono_rounded_funnel_chart,
    gauge=mono_rounded_gauge_arc,
    heatmap=mono_rounded_heatmap_chart,
    kpi=mono_rounded_kpi_card_chart,
    line=mono_rounded_line_chart,
    meter=mono_rounded_meter_chart,
    polar=mono_rounded_polar_chart,
    pyramid=mono_rounded_pyramid_chart,
    radar=mono_rounded_radar_chart,
    radial_gauge=mono_rounded_radial_gauge_chart,
    radial_group=mono_rounded_radial_bar_group,
    range=mono_rounded_range_chart,
    sankey=mono_rounded_sankey_chart,
    scatter=mono_rounded_scatter_chart,
    sparkline=mono_rounded_sparkline_chart,
    stacked_bar=mono_rounded_stacked_bar_chart,
    step=mono_rounded_step_chart,
    stream=mono_rounded_stream_chart,
    treemap=mono_rounded_treemap_chart,
    waterfall=mono_rounded_waterfall_chart,
    # chrome
    card=mono_card,
    header=mono_header,
    stage=mono_stage,
    footer=mono_footer,
    segmented=mono_segmented,
    tooltip=mono_tooltip,
)

#: Every chart function, in catalog order - handy for building a gallery.
ALL_CHARTS = (
    mono_activity_heatmap,
    mono_rounded_line_chart,
    mono_rounded_bar_chart,
    mono_rounded_area_chart,
    mono_rounded_donut_chart,
    mono_rounded_composed_chart,
    mono_rounded_scatter_chart,
    mono_rounded_candlestick_chart,
    mono_rounded_kpi_card_chart,
    mono_rounded_pyramid_chart,
    mono_rounded_radial_bar_group,
    mono_rounded_gauge_arc,
    mono_rounded_bullet_chart,
    mono_rounded_sankey_chart,
    mono_rounded_step_chart,
    mono_rounded_stacked_bar_chart,
    mono_rounded_radar_chart,
    mono_rounded_radial_gauge_chart,
    mono_rounded_funnel_chart,
    mono_rounded_heatmap_chart,
    mono_rounded_sparkline_chart,
    mono_rounded_bubble_chart,
    mono_rounded_treemap_chart,
    mono_rounded_stream_chart,
    mono_rounded_meter_chart,
    mono_rounded_waterfall_chart,
    mono_rounded_polar_chart,
    mono_rounded_range_chart,
)

__all__ = [
    "ACCENT",
    "ALL_CHARTS",
    "CARD_DARK",
    "CARD_LIGHT",
    "FONT_MONO",
    "FONT_SANS",
    "INK_DARK",
    "INK_LIGHT",
    "STAGE_DARK",
    "STAGE_LIGHT",
    "ThemeLike",
    "__version__",
    "data",
    "ink",
    "ink_alpha",
    "is_dark",
    "mono_activity_heatmap",
    "mono_card",
    "mono_footer",
    "mono_gradient",
    "mono_header",
    "mono_rounded_area_chart",
    "mono_rounded_bar_chart",
    "mono_rounded_bubble_chart",
    "mono_rounded_bullet_chart",
    "mono_rounded_candlestick_chart",
    "mono_rounded_composed_chart",
    "mono_rounded_donut_chart",
    "mono_rounded_funnel_chart",
    "mono_rounded_gauge_arc",
    "mono_rounded_heatmap_chart",
    "mono_rounded_kpi_card_chart",
    "mono_rounded_line_chart",
    "mono_rounded_meter_chart",
    "mono_rounded_polar_chart",
    "mono_rounded_pyramid_chart",
    "mono_rounded_radar_chart",
    "mono_rounded_radial_bar_group",
    "mono_rounded_radial_gauge_chart",
    "mono_rounded_range_chart",
    "mono_rounded_sankey_chart",
    "mono_rounded_scatter_chart",
    "mono_rounded_sparkline_chart",
    "mono_rounded_stacked_bar_chart",
    "mono_rounded_step_chart",
    "mono_rounded_stream_chart",
    "mono_rounded_treemap_chart",
    "mono_rounded_waterfall_chart",
    "mono_segmented",
    "mono_stage",
    "mono_tooltip",
    "monocharts",
    "pick",
]
