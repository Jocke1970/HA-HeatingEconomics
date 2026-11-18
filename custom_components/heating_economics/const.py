"""Constants for Heating Economics."""

DOMAIN = "heating_economics"

CONF_ELECTRICITY_PRICE_ENTITY = "electricity_price_entity"
CONF_POWER_ENTITY = "power_entity"
CONF_COP = "cop"
CONF_GAS_PRICE = "gas_price"
CONF_GAS_ENERGY = "gas_energy_kwh_per_kg"

DEFAULT_COP = 2.70
DEFAULT_GAS_PRICE = 39.0  # SEK/kg
DEFAULT_GAS_ENERGY = 13.8  # estimated kWh heat per kg of LPG
UPDATE_INTERVAL_SECONDS = 60
