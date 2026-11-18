"""Pure, testable estimates for heat-cost comparisons.

Values are estimates. Electricity price must be the all-in SEK/kWh price
if a full cost comparison is desired.
"""
from __future__ import annotations


def heat_cost_per_kwh(electricity_price: float, cop: float) -> float:
    """Return SEK per estimated kWh delivered by the heat pump."""
    if electricity_price < 0 or cop <= 0:
        raise ValueError("Price must be nonnegative and COP positive")
    return electricity_price / cop


def gas_heat_cost_per_kwh(gas_price: float, gas_energy_kwh_per_kg: float) -> float:
    """Return SEK per estimated kWh from LPG, before ventilation losses."""
    if gas_price < 0 or gas_energy_kwh_per_kg <= 0:
        raise ValueError("Gas price must be nonnegative and energy positive")
    return gas_price / gas_energy_kwh_per_kg


def savings_percent(heat_pump_cost: float, reference_cost: float) -> float:
    """Percentage saving against the LPG reference."""
    if heat_pump_cost < 0 or reference_cost <= 0:
        raise ValueError("Costs must be nonnegative and reference positive")
    return (reference_cost - heat_pump_cost) / reference_cost * 100


def heat_output_kw(power_w: float, cop: float) -> float:
    """Estimated delivered heat power in kW."""
    if power_w < 0 or cop <= 0:
        raise ValueError("Power must be nonnegative and COP positive")
    return power_w * cop / 1000
