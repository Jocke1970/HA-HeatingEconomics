"""Pure calculation checks, deliberately independent of Home Assistant packages."""
import importlib.util
from pathlib import Path

import pytest

MODULE = Path(__file__).resolve().parents[1] / "custom_components" / "heating_economics" / "calculations.py"
spec = importlib.util.spec_from_file_location("heating_economics_calculations", MODULE)
calculations = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calculations)


def test_nominal_example():
    assert calculations.heat_cost_per_kwh(1.5, 2.7) == pytest.approx(0.55555556)
    assert calculations.gas_heat_cost_per_kwh(39, 13.8) == pytest.approx(2.82608696)
    assert calculations.savings_percent(1.5 / 2.7, 39 / 13.8) == pytest.approx(80.34188034)
    assert calculations.heat_output_kw(1100, 2.7) == pytest.approx(2.97)


def test_negative_savings_allowed():
    assert calculations.savings_percent(3.0, 2.0) == pytest.approx(-50)


@pytest.mark.parametrize("price,cop", [(-1, 2), (1, 0), (1, -1)])
def test_invalid_heat_price(price, cop):
    with pytest.raises(ValueError):
        calculations.heat_cost_per_kwh(price, cop)
