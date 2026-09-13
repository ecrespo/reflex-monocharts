# reflex-monocharts

Monochromatic, rounded chart cards for [Reflex](https://reflex.dev) — a pure-Python
port of the [Monocharts](https://github.com/Subhan-code/Monocharts) design system.

28 components: splines, pill bars, gradient areas, donuts, radars, radial gauges,
bullet targets, treemaps, heatmaps, candlesticks, Sankey bands and a GitHub-style
contribution grid. All one hue, all rounded, dark and light.

```bash
pip install reflex-monocharts
```

![Monocharts for Reflex, dark](https://raw.githubusercontent.com/ecrespo/reflex-monocharts/main/monocharts_demo/assets/preview-dark.png)
![Monocharts for Reflex, light](https://raw.githubusercontent.com/ecrespo/reflex-monocharts/main/monocharts_demo/assets/preview-light.png)

## Why a port and not a wrapper

Monocharts ships as copy-paste React/TSX built on Recharts and Tailwind, with the
data hard-coded in each component. Reflex already wraps Recharts, so this library
rebuilds the *design system* in Python instead of shipping JavaScript:

- **No npm dependency and no Tailwind requirement.** Every class is translated to
  Reflex style props, so the cards drop into any Reflex app unchanged.
- **Data-driven.** Each chart takes `data` plus `*_key` arguments and binds to
  `rx.State`. Call it with no arguments and you get the original demo card.
- **Reactive theming.** `theme=` accepts `"dark"`, `"light"`, or a state Var, so a
  toggle re-themes every card without a reload. `compact=` works the same way.

## Quick start

```python
import reflex as rx
from reflex_monocharts import monocharts as mc


class State(rx.State):
    theme: str = "dark"
    traffic: list[dict] = [
        {"hour": "02:00", "hits": 18},
        {"hour": "06:00", "hits": 34},
        {"hour": "10:00", "hits": 72},
    ]

    @rx.event
    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"


def index() -> rx.Component:
    return rx.vstack(
        rx.button("Toggle theme", on_click=State.toggle_theme),
        mc.area(
            State.traffic,
            x_key="hour",
            value_key="hits",
            theme=State.theme,
            title="Traffic",
            badge="Live",
            unit="requests",
        ),
        mc.gauge(84, theme=State.theme),
        width="420px",
    )
```

Long names are available too — `mc.area` is `mono_rounded_area_chart`.

## The catalog

| Short name | Function | What it draws |
| --- | --- | --- |
| `mc.line` | `mono_rounded_line_chart` | Spline with a dashed baseline series |
| `mc.step` | `mono_rounded_step_chart` | Discrete staircase |
| `mc.sparkline` | `mono_rounded_sparkline_chart` | Stacked telemetry rows with micro splines |
| `mc.kpi` | `mono_rounded_kpi_card_chart` | Big KPI over a gradient sparkline |
| `mc.bar` | `mono_rounded_bar_chart` | Pill bars, as columns or rows |
| `mc.stacked_bar` | `mono_rounded_stacked_bar_chart` | Tonal stack with rounded ends |
| `mc.composed` | `mono_rounded_composed_chart` | Outlined columns plus a spline |
| `mc.waterfall` | `mono_rounded_waterfall_chart` | Floating delta pillars |
| `mc.funnel` | `mono_rounded_funnel_chart` | Horizontal pipeline stages |
| `mc.bullet` | `mono_rounded_bullet_chart` | Progress bars with benchmark markers |
| `mc.pyramid` | `mono_rounded_pyramid_chart` | Hierarchy tiers |
| `mc.candlestick` | `mono_rounded_candlestick_chart` | OHLC candles with rounded wicks |
| `mc.area` | `mono_rounded_area_chart` | Curved area with a soft gradient |
| `mc.range` | `mono_rounded_range_chart` | Floating min-max band |
| `mc.stream` | `mono_rounded_stream_chart` | Two natural-spline waves |
| `mc.donut` | `mono_rounded_donut_chart` | Donut with rounded caps and a centre readout |
| `mc.radar` | `mono_rounded_radar_chart` | Multi-axis polygon web |
| `mc.polar` | `mono_rounded_polar_chart` | 360-degree radial pillars |
| `mc.radial_group` | `mono_rounded_radial_bar_group` | Half-circle arc group |
| `mc.radial_gauge` | `mono_rounded_radial_gauge_chart` | Concentric progress rings |
| `mc.gauge` | `mono_rounded_gauge_arc` | 240-degree speedometer dial |
| `mc.meter` | `mono_rounded_meter_chart` | Semicircle meter |
| `mc.scatter` | `mono_rounded_scatter_chart` | Weighted node matrix |
| `mc.bubble` | `mono_rounded_bubble_chart` | Outlined bubbles, area-encoded |
| `mc.heatmap` | `mono_rounded_heatmap_chart` | Labelled density matrix |
| `mc.treemap` | `mono_rounded_treemap_chart` | Rounded partition tiles |
| `mc.sankey` | `mono_rounded_sankey_chart` | Curved flow bands |
| `mc.activity` | `mono_activity_heatmap` | Contribution grid (green/blue/purple/mono) |

## Common arguments

Every chart accepts these, on top of its own `*_key` arguments:

| Argument | Meaning |
| --- | --- |
| `data` | Rows to plot. Omit for the built-in demo dataset. |
| `theme` | `"dark"`, `"light"`, or a state Var. |
| `compact` | Short card instead of tall. Accepts a Var. |
| `title` / `badge` | The uppercase eyebrow and the pill beside it. |
| `value` / `unit` | The headline metric and its muted suffix. Derived from the data when omitted. |
| `footer_left` / `footer_right` | The two monospace footer captions. |
| `control` | A component rendered flush right in the header. |
| `**props` | Any extra style props, forwarded to the card. |

## Interactive controls

The originals bake their toggles into the component. Here the option is a prop,
so it can be wired to your own state — `mono_segmented` renders the matching pill
control:

```python
from reflex_monocharts import mono_segmented, monocharts as mc


class State(rx.State):
    curve: str = "monotone"

    @rx.event
    def set_curve(self, value: str):
        self.curve = value


mc.area(
    curve=State.curve,
    control=mono_segmented(
        [("monotone", "Monotone"), ("natural", "Natural")],
        State.curve,
        State.set_curve,
        theme=State.theme,
    ),
)
```

The same pattern drives `series=` on the line card, `orientation=` on the bar card
and `show_trend=` on the hybrid card.

## Building your own cards

The chrome is exported, so a custom chart can sit in the same system:

```python
from reflex_monocharts import mono_card, mono_header, mono_stage, mono_footer, mono_tooltip

mono_card(
    mono_header("My Metric", "Custom", "1,204", "events", theme="dark"),
    mono_stage(my_chart, theme="dark"),
    mono_footer("Left caption", "Right caption", theme="dark"),
    theme="dark",
)
```

`ink()`, `ink_alpha()`, `pick()` and `is_dark()` from `reflex_monocharts.theme`
resolve the monochrome palette for either a plain theme string or a Var.

## Notes and deliberate differences

- **Badge and footer rule are theme-aware here.** Upstream hard-codes
  `bg-white/10 text-white` and `border-white/5`, which is invisible on the light
  card; this port resolves both per theme.
- **The tooltip is `rx.recharts.graphing_tooltip`** styled to match the original's
  blurred dark panel. Recharts' `content` render-prop takes a React component,
  which Reflex cannot pass, so the styling is reproduced through
  `content_style` / `item_style` / `label_style`.
- **Gradients are defined in a hidden sibling `<svg>`** with a process-unique id,
  so several gradient-filled cards can share a page.
- **`mono_activity_heatmap` seeds its RNG** so the grid is stable across
  re-renders. Pass `seed=None` to `data.activity_contributions` for the original
  random behaviour, and use a native `title` tooltip per cell rather than a
  server round-trip for 140 cells.
- **`mono_rounded_candlestick_chart` needs explicit `low_bound`/`high_bound`**
  when `data` is a state Var, since the price scale cannot be derived at build
  time. `mono_rounded_sankey_chart` computes its band geometry in Python and
  takes a plain list.

## Demo app

```bash
cd monocharts_demo
uv run reflex run
```

The gallery shows every chart, a live-state section wired to `rx.State`, a theme
toggle, a compact toggle and a category filter.

## Credits

Design system by [Syed Subhan](https://github.com/Subhan-code) — see
[Monocharts](https://github.com/Subhan-code/Monocharts) and
[amicro](https://amicro.vercel.app/mono-charts). This is an independent Python
port for Reflex, not affiliated with the original project.

MIT licensed.
