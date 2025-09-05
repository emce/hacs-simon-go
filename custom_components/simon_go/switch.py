from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SimonGoApi
from .const import CONF_HOST, CONF_DEVICE_TYPE

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    session = async_get_clientsession(hass)
    api = SimonGoApi(entry.data[CONF_HOST], session)
    device_type = entry.data[CONF_DEVICE_TYPE]

    entities = []
    if device_type == "switch":
        entities.append(SimonGoSwitch(api, name=entry.title))
    elif device_type == "switch_d":
        entities.append(SimonGoSwitchD(api, name=f"{entry.title} A", channel=0))
        entities.append(SimonGoSwitchD(api, name=f"{entry.title} B", channel=1))

    if entities:
        async_add_entities(entities)

class SimonGoBaseSwitch(SwitchEntity):
    _attr_should_poll = False
    _attr_assumed_state = True

class SimonGoSwitch(SimonGoBaseSwitch):
    def __init__(self, api: SimonGoApi, name: str) -> None:
        self._api = api
        self._attr_name = name
        self._is_on = False

    @property
    def is_on(self) -> bool:
        return self._is_on

    async def async_turn_on(self, **kwargs):
        if await self._api.switch_on():
            self._is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        if await self._api.switch_off():
            self._is_on = False
            self.async_write_ha_state()

class SimonGoSwitchD(SimonGoBaseSwitch):
    def __init__(self, api: SimonGoApi, name: str, channel: int) -> None:
        self._api = api
        self._attr_name = name
        self._channel = channel
        self._is_on = False

    @property
    def is_on(self) -> bool:
        return self._is_on

    async def async_turn_on(self, **kwargs):
        if await self._api.switch_d_set(self._channel, True):
            self._is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        if await self._api.switch_d_set(self._channel, False):
            self._is_on = False
            self.async_write_ha_state()
