from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SimonGoApi
from .const import CONF_HOST, CONF_DEVICE_TYPE

ACTIONS = {
    1: "short",
    2: "long",
    3: "falling",
    4: "rising",
    5: "edge",
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    if entry.data[CONF_DEVICE_TYPE] != "control":
        return
    session = async_get_clientsession(hass)
    api = SimonGoApi(entry.data[CONF_HOST], session)
    entities = []
    for x in range(4):  # buttons 0..3
        for code, name in ACTIONS.items():
            entities.append(ControlButton(api, entry.title, x, code, name))
    async_add_entities(entities)

class ControlButton(ButtonEntity):
    _attr_should_poll = False

    def __init__(self, api: SimonGoApi, title: str, btn: int, code: int, name: str) -> None:
        self._api = api
        self._btn = btn
        self._code = code
        self._attr_name = f"{title} B{btn} {name}"

    async def async_press(self) -> None:
        await self._api.get(f"/t/{self._btn}/{self._code}")
