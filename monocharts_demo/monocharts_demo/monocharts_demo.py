"""A gallery demo for reflex-monocharts.

Shows every chart in the library, live-themed, with a section of
state-driven cards proving the components are data-driven rather than
decorative.
"""

from __future__ import annotations

import reflex as rx

from reflex_monocharts import FONT_MONO, mono_segmented
from reflex_monocharts import monocharts as mc

from .state import CATEGORIES, DemoState


def pill_button(label: str, on_click) -> rx.Component:
    """A small outlined control button that follows the gallery theme."""
    return rx.el.button(
        label,
        on_click=on_click,
        padding="0.375rem 0.875rem",
        border_radius="9999px",
        font_size="0.75rem",
        font_family=FONT_MONO,
        cursor="pointer",
        white_space="nowrap",
        transition="all 200ms",
        background=rx.cond(DemoState.is_dark, "rgba(255,255,255,0.06)", "#FFFFFF"),
        color=rx.cond(DemoState.is_dark, "#FAFAFA", "#09090B"),
        border=rx.cond(
            DemoState.is_dark,
            "1px solid rgba(255,255,255,0.14)",
            "1px solid #E5E5E5",
        ),
        _hover={"background": rx.cond(DemoState.is_dark, "rgba(255,255,255,0.12)", "#F4F4F5")},
    )


def category_button(name: str) -> rx.Component:
    """One filter chip."""
    selected = DemoState.category == name
    return rx.el.button(
        name,
        on_click=DemoState.set_category(name),
        padding="0.3125rem 0.75rem",
        border_radius="9999px",
        font_size="0.6875rem",
        font_family=FONT_MONO,
        text_transform="uppercase",
        letter_spacing="0.05em",
        cursor="pointer",
        transition="all 200ms",
        border="1px solid transparent",
        background=rx.cond(
            selected,
            rx.cond(DemoState.is_dark, "#FAFAFA", "#09090B"),
            rx.cond(DemoState.is_dark, "rgba(255,255,255,0.05)", "#FFFFFF"),
        ),
        color=rx.cond(
            selected,
            rx.cond(DemoState.is_dark, "#09090B", "#FAFAFA"),
            rx.cond(DemoState.is_dark, "#A1A1AA", "#52525B"),
        ),
        border_color=rx.cond(
            selected,
            "transparent",
            rx.cond(DemoState.is_dark, "rgba(255,255,255,0.12)", "#E5E5E5"),
        ),
    )


def slot(category: str, card: rx.Component) -> rx.Component:
    """Show a card only when its category is selected."""
    return rx.cond(
        (DemoState.category == "all") | (DemoState.category == category),
        card,
        rx.fragment(),
    )


def grid(*children: rx.Component) -> rx.Component:
    """The responsive gallery grid."""
    return rx.box(
        *children,
        display="grid",
        grid_template_columns=rx.breakpoints(
            initial="repeat(1, minmax(0, 1fr))",
            sm="repeat(2, minmax(0, 1fr))",
            lg="repeat(3, minmax(0, 1fr))",
        ),
        gap="1rem",
        width="100%",
    )


def section(title: str, subtitle: str, body: rx.Component) -> rx.Component:
    """A titled block of the page."""
    return rx.vstack(
        rx.vstack(
            rx.heading(
                title,
                size="5",
                letter_spacing="-0.02em",
                color=DemoState.page_color,
            ),
            rx.text(
                subtitle,
                font_size="0.8125rem",
                color=rx.cond(DemoState.is_dark, "#A1A1AA", "#52525B"),
            ),
            spacing="1",
            align="start",
            width="100%",
        ),
        body,
        spacing="4",
        width="100%",
        align="start",
    )


def header() -> rx.Component:
    """The page masthead and global controls."""
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading(
                    "Monocharts for Reflex",
                    size="8",
                    letter_spacing="-0.03em",
                    color=DemoState.page_color,
                ),
                rx.text(
                    "28 monochromatic chart cards, in pure Python, on rx.recharts.",
                    font_size="0.875rem",
                    color=rx.cond(DemoState.is_dark, "#A1A1AA", "#52525B"),
                ),
                spacing="2",
                align="start",
            ),
            rx.spacer(),
            rx.hstack(
                pill_button(
                    rx.cond(DemoState.is_dark, "Light mode", "Dark mode"),
                    DemoState.toggle_theme,
                ),
                pill_button(
                    rx.cond(DemoState.compact, "Tall cards", "Compact cards"),
                    DemoState.toggle_compact,
                ),
                spacing="2",
                wrap="wrap",
            ),
            width="100%",
            align="start",
            wrap="wrap",
            spacing="4",
        ),
        rx.hstack(
            *[category_button(c) for c in CATEGORIES],
            spacing="2",
            wrap="wrap",
            width="100%",
        ),
        spacing="5",
        width="100%",
        align="start",
    )


def live_section() -> rx.Component:
    """Cards bound to state, with working controls."""

    def seg(opts, value, handler):
        return mono_segmented(opts, value, handler, theme=DemoState.theme)

    return section(
        "Live state",
        "These five cards read their rows from rx.State. Shuffle the data or "
        "flip a control and they re-render without a reload.",
        rx.vstack(
            rx.hstack(
                pill_button("Shuffle data", DemoState.shuffle),
                pill_button("Reset data", DemoState.reset_data),
                spacing="2",
                wrap="wrap",
            ),
            grid(
                mc.line(
                    DemoState.traffic,
                    theme=DemoState.theme,
                    compact=False,
                    series=DemoState.series,
                    value=DemoState.traffic_last,
                    footer_right=DemoState.traffic_peak,
                    control=seg(
                        [("all", "Dual"), ("value", "Single")],
                        DemoState.series,
                        DemoState.set_series,
                    ),
                ),
                mc.bar(
                    DemoState.weekly,
                    theme=DemoState.theme,
                    orientation=DemoState.orientation,
                    value=DemoState.weekly_total,
                    control=seg(
                        [("columns", "Col"), ("rows", "Row")],
                        DemoState.orientation,
                        DemoState.set_orientation,
                    ),
                ),
                mc.area(
                    theme=DemoState.theme,
                    curve=DemoState.curve,
                    control=seg(
                        [("monotone", "Monotone"), ("natural", "Natural")],
                        DemoState.curve,
                        DemoState.set_curve,
                    ),
                ),
                mc.donut(
                    DemoState.allocation,
                    theme=DemoState.theme,
                    value=DemoState.allocation_total,
                    center_value=DemoState.allocation_total,
                ),
                mc.composed(
                    theme=DemoState.theme,
                    show_trend=DemoState.show_trend,
                    control=rx.el.button(
                        DemoState.trend_label,
                        on_click=DemoState.toggle_trend,
                        padding="0.25rem 0.625rem",
                        border_radius="9999px",
                        font_size="0.6875rem",
                        cursor="pointer",
                        background="transparent",
                        color=rx.cond(DemoState.is_dark, "#FAFAFA", "#09090B"),
                        border=rx.cond(
                            DemoState.is_dark,
                            "1px solid rgba(255,255,255,0.2)",
                            "1px solid #D4D4D8",
                        ),
                    ),
                ),
                mc.meter(
                    DemoState.load,
                    theme=DemoState.theme,
                    caption="Live load",
                ),
            ),
            spacing="4",
            width="100%",
            align="start",
        ),
    )


def gallery() -> rx.Component:
    """Every chart in the library, filtered by category."""
    t = DemoState.theme
    c = DemoState.compact
    return section(
        "The full catalog",
        "All 28 components with their built-in demo data - the state each card "
        "ships in when you call it with no arguments.",
        grid(
            slot("line", mc.line(theme=t, compact=c)),
            slot("line", mc.step(theme=t, compact=c)),
            slot("line", mc.sparkline(theme=t, compact=c)),
            slot("line", mc.kpi(theme=t, compact=c)),
            slot("bar", mc.bar(theme=t, compact=c)),
            slot("bar", mc.stacked_bar(theme=t, compact=c)),
            slot("bar", mc.composed(theme=t, compact=c)),
            slot("bar", mc.waterfall(theme=t, compact=c)),
            slot("bar", mc.funnel(theme=t, compact=c)),
            slot("bar", mc.bullet(theme=t, compact=c)),
            slot("bar", mc.pyramid(theme=t, compact=c)),
            slot("bar", mc.candlestick(theme=t, compact=c)),
            slot("area", mc.area(theme=t, compact=c)),
            slot("area", mc.range(theme=t, compact=c)),
            slot("area", mc.stream(theme=t, compact=c)),
            slot("radial", mc.donut(theme=t, compact=c)),
            slot("radial", mc.radar(theme=t, compact=c)),
            slot("radial", mc.polar(theme=t, compact=c)),
            slot("radial", mc.radial_group(theme=t, compact=c)),
            slot("radial", mc.radial_gauge(theme=t, compact=c)),
            slot("radial", mc.gauge(theme=t, compact=c)),
            slot("radial", mc.meter(theme=t, compact=c)),
            slot("point", mc.scatter(theme=t, compact=c)),
            slot("point", mc.bubble(theme=t, compact=c)),
            slot("matrix", mc.heatmap(theme=t, compact=c)),
            slot("matrix", mc.treemap(theme=t, compact=c)),
            slot("matrix", mc.sankey(theme=t, compact=c)),
            slot("matrix", mc.activity(theme=t, compact=c, accent="green")),
            slot("matrix", mc.activity(theme=t, compact=c, accent="blue")),
            slot("matrix", mc.activity(theme=t, compact=c, accent="purple")),
            slot("matrix", mc.activity(theme=t, compact=c, accent="mono")),
        ),
    )


def footer() -> rx.Component:
    """Page footer."""
    return rx.hstack(
        rx.text(
            "reflex-monocharts",
            font_family=FONT_MONO,
            font_size="0.75rem",
            color=rx.cond(DemoState.is_dark, "#A1A1AA", "#52525B"),
        ),
        rx.spacer(),
        rx.text(
            "Design ported from Monocharts by Syed Subhan",
            font_family=FONT_MONO,
            font_size="0.75rem",
            color=rx.cond(DemoState.is_dark, "#71717A", "#71717A"),
        ),
        width="100%",
        padding_top="1.5rem",
        border_top=rx.cond(
            DemoState.is_dark,
            "1px solid rgba(255,255,255,0.06)",
            "1px solid #E5E5E5",
        ),
        wrap="wrap",
        spacing="2",
    )


def index() -> rx.Component:
    """The gallery page."""
    return rx.box(
        rx.vstack(
            header(),
            live_section(),
            gallery(),
            footer(),
            spacing="8",
            width="100%",
            max_width="1240px",
            margin="0 auto",
            padding=rx.breakpoints(initial="1.25rem", sm="2.5rem"),
        ),
        min_height="100vh",
        width="100%",
        background=DemoState.page_background,
        color=DemoState.page_color,
        transition="background 300ms",
    )


# The Radix theme is configured in rxconfig.py via RadixThemesPlugin;
# passing theme= to rx.App is deprecated since Reflex 0.9.
app = rx.App()
app.add_page(index, title="Monocharts for Reflex")
