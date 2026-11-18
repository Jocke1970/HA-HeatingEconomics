"""Unit tests for estimate-only cost calculations."""
import pytest

from custom_components.heating_economics.calculations import (
    gas_heat_cost_per_kwh, heat_cost_per_kwh, heat_output_kw, savings_percent,
)


def test_nominal_example():
    assert heat_cost_per_kwh(1.5, 2.7) == pytest.approx(0.55555556)
    assert gas_heat_cost_per_kwh(39, 13.8) == pytest.approx(2.82608696)
    assert savings_percent(1.5 / 2.7, 39 / 13.8) == pytest.approx(80.34188034)
    assert heat_output_kw(1100, 2.7) == pytest.approx(2.97)


def test_negative_savings_allowed():
    assert savings_percent(3.0, 2.0) == pytest.approx(-50)


@pytest.mark.parametrize("price,cop", [(-1, 2), (1, 0), (1, -1)])
def test_invalid_heat_price(price, cop):
    with pytest.raises(ValueError):
        heat_cost_per_kwh(price, cop)
