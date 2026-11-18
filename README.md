# HA-HeatingEconomics

Read-only Home Assistant custom integration to **estimate** and compare heating costs for a Wood's Cortina 12K Duo heat pump and a Wecamp LPG heater.

> **Development prototype on `dev`.** No beta or stable release yet. The values are model estimates, not measured net heat delivered to the room.

## Initial scope — no thermometers required

- Fixed, **assumed COP** for Wood's (default **2.70**).
- Source electricity-price sensor in **SEK/kWh** (ideally total price including tax and fees).
- Optional source electric-power sensor in **W**, used for estimated instantaneous heat output.
- Wecamp gas reference: **39 SEK/kg**, **13.8 estimated kWh/kg**, configured during setup.
- Sensors for Wood's heat cost, Wecamp heat cost, difference (SEK/kWh), saving (%), COP, and optional heat output.
- **No commands to Wood's, Wecamp, Broadlink or any other heating device.**

## Formulae

- Wood's estimated cost (SEK/kWh heat) = electricity price / assumed COP.
- Wecamp estimated cost (SEK/kWh heat) = LPG price per kg / assumed kWh heat per kg.
- Saving (SEK/kWh heat) = Wecamp cost - Wood's cost.
- Saving (%) = saving / Wecamp cost × 100.
- Estimated Wood's heat output (kW) = electrical power (W) × assumed COP / 1000.

**Limitations:** The single-hose installation and replacement air are deliberately excluded from this simplified estimate. These values should **not** be represented as measured real-world COP or verified net savings. Instantaneous price readings are not daily/monthly costs.

## Install for development testing

1. Copy `custom_components/heating_economics` into your Home Assistant `config/custom_components/` directory.
2. Restart Home Assistant.
3. Settings → Devices & services → Add integration → **Heating Economics**.
4. Select a price entity supplying SEK/kWh, optionally a Wood's power sensor supplying W, and set model assumptions.
5. Inspect the created Heating Economics entities. Inputs are read every 60 seconds.

The first prototype does not auto-convert source units, so **verify SEK/kWh and W**. Unavailable, nonnumeric, or negative price/power source states make dependent sensors unavailable; they are not silently converted to zero.

## Roadmap

1. Validate config and calculations in a live Home Assistant test installation.
2. Add options flow for changing parameters without removing integration.
3. Add fan-speed-adjusted estimated airflows and temperature-based COP when thermometers become available.
4. Add historical daily/monthly energy and cost accounting and a dedicated Lovelace card.
5. Swedish translations, CI, HACS packaging, then beta.

## Development workflow

`dev` → `beta` → `main`. Pure-calculation tests: `pytest tests/test_calculations.py` in an environment with Home Assistant dependencies.

MIT license.
