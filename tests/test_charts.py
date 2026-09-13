"""Smoke tests: every chart must build, statically and bound to state."""

from __future__ import annotations

import pytest
import reflex as rx

import reflex_monocharts as mc


class DemoState(rx.State):
    """A state to bind charts to."""

    theme: str = "dark"
    compact: bool = False
    rows: list[dict] = [{"label": "A", "value": 1, "secondary": 2}]


@pytest.mark.parametrize("chart", mc.ALL_CHARTS, ids=lambda c: c.__name__)
def test_renders_with_defaults(chart):
    """Each chart renders its built-in demo card."""
    chart().render()


@pytest.mark.parametrize("chart", mc.ALL_CHARTS, ids=lambda c: c.__name__)
def test_renders_light(chart):
    """Each chart renders on the light card."""
    chart(theme="light").render()


@pytest.mark.parametrize("chart", mc.ALL_CHARTS, ids=lambda c: c.__name__)
def test_renders_with_reactive_theme_and_size(chart):
    """Theme and card size may both be state Vars."""
    chart(theme=DemoState.theme, compact=DemoState.compact).render()


def test_catalog_is_complete():
    """The namespace and the catalog stay in sync."""
    assert len(mc.ALL_CHARTS) == 28
    exported = {fn for fn in vars(mc.monocharts).values() if callable(fn)}
    assert set(mc.ALL_CHARTS) <= exported


def test_data_driven_line():
    """A chart bound to state rows builds."""
    mc.mono_rounded_line_chart(DemoState.rows, theme=DemoState.theme).render()


def test_candlestick_requires_bounds_for_var_data():
    """The candle scale cannot be derived from a Var, so it must be given."""
    with pytest.raises(TypeError):
        mc.mono_rounded_candlestick_chart(DemoState.rows)


def test_sankey_rejects_var_data():
    """Sankey geometry is computed in Python and needs a plain list."""
    with pytest.raises(TypeError):
        mc.mono_rounded_sankey_chart(DemoState.rows)


def test_activity_contributions_is_seeded():
    """The contribution grid is stable when seeded."""
    a = mc.data.activity_contributions(4, seed=1)
    b = mc.data.activity_contributions(4, seed=1)
    assert a == b
    assert len(a) == 28
