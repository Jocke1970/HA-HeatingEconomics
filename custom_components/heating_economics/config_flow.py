"""UI configuration for Heating Economics."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    DOMAIN, CONF_COP, CONF_ELECTRICITY_PRICE_ENTITY, CONF_GAS_ENERGY,
    CONF_GAS_PRICE, CONF_POWER_ENTITY, DEFAULT_COP, DEFAULT_GAS_ENERGY,
    DEFAULT_GAS_PRICE,
)


class HeatingEconomicsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Create an estimate-only comparison."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Configure source entities and initial assumptions."""
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id("default")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Heating Economics", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_ELECTRICITY_PRICE_ENTITY):
                selector.EntitySelector(selector.EntitySelectorConfig(domain="sensor")),
            vol.Optional(CONF_POWER_ENTITY):
                selector.EntitySelector(selector.EntitySelectorConfig(domain="sensor")),
            vol.Required(CONF_COP, default=DEFAULT_COP):
                vol.All(vol.Coerce(float), vol.Range(min=0.1, max=15)),
            vol.Required(CONF_GAS_PRICE, default=DEFAULT_GAS_PRICE):
                vol.All(vol.Coerce(float), vol.Range(min=0)),
            vol.Required(CONF_GAS_ENERGY, default=DEFAULT_GAS_ENERGY):
                vol.All(vol.Coerce(float), vol.Range(min=0.1)),
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
