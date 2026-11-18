"""Read-only, schablon-COP heating economics sensors."""
from __future__ import annotations

from datetime import timedelta
import math

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity

from .calculations import (
    gas_heat_cost_per_kwh, heat_cost_per_kwh, heat_output_kw, savings_percent,
)
from .const import (
    DOMAIN, CONF_COP, CONF_ELECTRICITY_PRICE_ENTITY, CONF_GAS_ENERGY,
    CONF_GAS_PRICE, CONF_POWER_ENTITY, UPDATE_INTERVAL_SECONDS,
)


def _read_nonnegative_number(hass: HomeAssistant, entity_id: str | None) -> float | None:
    """Return a valid numeric source state, or None on invalid source."""
    if not entity_id:
        return None
    state = hass.states.get(entity_id)
    if state is None or state.state in ("unknown", "unavailable"):
        return None
    try:
        number = float(state.state)
    except (ValueError, TypeError):
        return None
    return number if math.isfinite(number) and number >= 0 else None


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Create calculated sensors and refresh source states periodically."""
    coordinator = DataUpdateCoordinator(
        hass,
        logger=__import__("logging").getLogger(__name__),
        name="Heating Economics",
        update_method=lambda: _async_collect(hass, entry),
        update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
    )
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([
        HeatingEconomicsSensor(coordinator, entry, metric)
        for metric in ("cop", "wood_cost", "gas_cost", "difference", "savings", "heat_power")
    ])


async def _async_collect(hass: HomeAssistant, entry: ConfigEntry) -> dict:
    """Calculate snapshot from sources and configurable assumptions."""
    opts = {**entry.data, **entry.options}
    cop = float(opts[CONF_COP])
    gas_price = float(opts[CONF_GAS_PRICE])
    gas_energy = float(opts[CONF_GAS_ENERGY])
    electricity = _read_nonnegative_number(hass, opts[CONF_ELECTRICITY_PRICE_ENTITY])
    power = _read_nonnegative_number(hass, opts.get(CONF_POWER_ENTITY))
    gas_cost = gas_heat_cost_per_kwh(gas_price, gas_energy)
    wood_cost = heat_cost_per_kwh(electricity, cop) if electricity is not None else None
    return {
        "cop": cop,
        "wood_cost": wood_cost,
        "gas_cost": gas_cost,
        "difference": gas_cost - wood_cost if wood_cost is not None else None,
        "savings": savings_percent(wood_cost, gas_cost) if wood_cost is not None else None,
        "heat_power": heat_output_kw(power, cop) if power is not None else None,
    }


METRICS = {
    "cop": ("Estimated COP", None, None, 2),
    "wood_cost": ("Wood's estimated heat cost", "kr/kWh", SensorStateClass.MEASUREMENT, 3),
    "gas_cost": ("Wecamp estimated heat cost", "kr/kWh", SensorStateClass.MEASUREMENT, 3),
    "difference": ("Estimated savings per kWh of heat", "kr/kWh", SensorStateClass.MEASUREMENT, 3),
    "savings": ("Estimated cost savings", "%", SensorStateClass.MEASUREMENT, 1),
    "heat_power": ("Wood's estimated heat output", UnitOfPower.KILO_WATT, SensorStateClass.MEASUREMENT, 2),
}


class HeatingEconomicsSensor(CoordinatorEntity, SensorEntity):
    """Display one calculated snapshot metric."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry, metric: str):
        super().__init__(coordinator)
        self.metric = metric
        name, unit, state_class, precision = METRICS[metric]
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{metric}"
        self._attr_native_unit_of_measurement = unit
        self._attr_state_class = state_class
        self._attr_suggested_display_precision = precision
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Heating Economics",
            "manufacturer": "Community",
            "model": "Estimated heat economics",
        }
        if metric == "heat_power":
            self._attr_device_class = SensorDeviceClass.POWER

    @property
    def native_value(self):
        """Latest computed value; None means source unavailable."""
        return self.coordinator.data.get(self.metric)

    @property
    def extra_state_attributes(self):
        """Identify assumptions clearly."""
        if self.metric == "cop":
            return {"method": "fixed_assumption", "estimated": True}
        return {"estimated": True}
