from __future__ import annotations

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVACMode,
    ClimateEntityFeature,
)
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SimonGoApi
from .const import CONF_HOST, CONF_DEVICE_TYPE

def _to_raw_temp(temp_c: float) -> int:
    return int(round(temp_c * 100))

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    if entry.data[CONF_DEVICE_TYPE] != "thermo":
        return
    session = async_get_clientsession(hass)
    api = SimonGoApi(entry.data[CONF_HOST], session)
    async_add_entities([SimonGoThermo(api, entry.title)])

class SimonGoThermo(ClimateEntity):
    _attr_should_poll = False
    _attr_assumed_state = True
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT]
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
    _attr_min_temp = 5.0
    _attr_max_temp = 35.0
    _attr_temperature_unit = UnitOfTemperature.CELSIUS

    def __init__(self, api: SimonGoApi, name: str) -> None:
        self._api = api
        self._attr_name = name
        self._attr_hvac_mode = HVACMode.OFF
        self._attr_target_temperature = 21.0

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        if hvac_mode == HVACMode.OFF:
            await self._api.thermo_off()
        else:
            await self._api.thermo_on()
        self._attr_hvac_mode = hvac_mode
        self.async_write_ha_state()

    async def async_set_temperature(self, **kwargs) -> None:
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is None:
            return
        self._attr_target_temperature = float(temp)
        await self._api.thermo_set_raw(_to_raw_temp(self._attr_target_temperature))
        self.async_write_ha_state()

    async def async_turn_on(self) -> None:
        await self._api.thermo_on()
        self._attr_hvac_mode = HVACMode.HEAT
        self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        await self._api.thermo_off()
        self._attr_hvac_mode = HVACMode.OFF
        self.async_write_ha_state()
