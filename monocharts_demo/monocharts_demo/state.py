"""State for the Monocharts demo app."""

from __future__ import annotations

import random

import reflex as rx

from reflex_monocharts import data as demo

CATEGORIES = ["all", "line", "bar", "area", "radial", "matrix", "point"]


class DemoState(rx.State):
    """Everything the gallery can drive from the UI."""

    # --- global chrome -----------------------------------------------------
    theme: str = "dark"
    category: str = "all"
    compact: bool = False

    # --- per-chart controls, wired to mono_segmented -----------------------
    series: str = "all"
    orientation: str = "columns"
    curve: str = "monotone"
    show_trend: bool = True

    # --- live datasets -----------------------------------------------------
    traffic: list[dict] = demo.LINE_DATA
    weekly: list[dict] = demo.BAR_DATA
    allocation: list[dict] = demo.DONUT_DATA
    load: int = demo.METER_VALUE

    @rx.var
    def is_dark(self) -> bool:
        """Whether the gallery is currently in dark mode."""
        return self.theme == "dark"

    @rx.var
    def page_background(self) -> str:
        """Page backdrop behind the cards."""
        return "#0B0B0C" if self.theme == "dark" else "#FAFAFA"

    @rx.var
    def page_color(self) -> str:
        """Page foreground."""
        return "#FAFAFA" if self.theme == "dark" else "#09090B"

    @rx.var
    def trend_label(self) -> str:
        """Label for the composed-chart toggle."""
        return "Spline On" if self.show_trend else "Spline Off"

    @rx.var
    def traffic_last(self) -> str:
        """Latest traffic reading, for the line card's headline."""
        return f"{self.traffic[-1]['value']}k"

    @rx.var
    def traffic_peak(self) -> str:
        """Peak traffic reading, for the line card's footer."""
        return f"{max(row['value'] for row in self.traffic)}k Peak"

    @rx.var
    def weekly_total(self) -> int:
        """Sum of the primary weekly series, for the bar card's headline."""
        return sum(row["primary"] for row in self.weekly)

    @rx.var
    def allocation_total(self) -> str:
        """Share total, for the donut card's headline and centre readout."""
        return f"{sum(row['value'] for row in self.allocation)}%"

    @rx.event
    def set_category(self, value: str):
        """Filter the gallery down to one chart family."""
        self.category = value

    @rx.event
    def set_series(self, value: str):
        """Switch the line card between its dual and single series."""
        self.series = value

    @rx.event
    def set_orientation(self, value: str):
        """Switch the bar card between columns and rows."""
        self.orientation = value

    @rx.event
    def set_curve(self, value: str):
        """Switch the area card's interpolation."""
        self.curve = value

    @rx.event
    def toggle_theme(self):
        """Flip between the dark and light card systems."""
        self.theme = "light" if self.theme == "dark" else "dark"

    @rx.event
    def toggle_compact(self):
        """Flip between the tall and short card sizes."""
        self.compact = not self.compact

    @rx.event
    def toggle_trend(self):
        """Show or hide the spline overlay on the hybrid chart."""
        self.show_trend = not self.show_trend

    @rx.event
    def shuffle(self):
        """Regenerate every live dataset, to prove the charts are data-driven."""
        self.traffic = [
            {
                "label": row["label"],
                "value": random.randint(10, 95),
                "secondary": random.randint(5, 70),
            }
            for row in demo.LINE_DATA
        ]
        self.weekly = [
            {
                "label": row["label"],
                "primary": random.randint(20, 100),
                "secondary": random.randint(10, 60),
            }
            for row in demo.BAR_DATA
        ]
        raw = [random.randint(5, 50) for _ in demo.DONUT_DATA]
        total = sum(raw)
        shares = [round(v / total * 100) for v in raw]
        shares[-1] += 100 - sum(shares)
        self.allocation = [
            {"name": row["name"], "value": share}
            for row, share in zip(demo.DONUT_DATA, shares, strict=True)
        ]
        self.load = random.randint(15, 99)

    @rx.event
    def reset_data(self):
        """Put the built-in demo datasets back."""
        self.traffic = demo.LINE_DATA
        self.weekly = demo.BAR_DATA
        self.allocation = demo.DONUT_DATA
        self.load = demo.METER_VALUE
