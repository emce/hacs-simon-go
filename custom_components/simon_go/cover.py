from __future__ import annotations

from homeassistant.components.cover import (
    CoverEntity,
    CoverEntityFeature,
    ATTR_POSITION,
    ATTR_TILT_POSITION,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SimonGoApi
from .const import CONF_HOST, CONF_DEVICE_TYPE

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    session = async_get_clientsession(hass)
    api = SimonGoApi(entry.data[CONF_HOST], session)
    t = entry.data[CONF_DEVICE_TYPE]

    entities = []
    if t == "shutter":
        entities.append(SimonGoShutter(api, entry.title))
    elif t == "rollergate":
        entities.append(SimonGoRollerGate(api, entry.title))
    elif t in ("gatebox", "doorbox"):
        entities.append(SimonGoGateBox(api, entry.title, two_relays=(t=="gatebox")))

    if entities:
        async_add_entities(entities)

class BaseSimonCover(CoverEntity):
    _attr_should_poll = False
    _attr_assumed_state = True

class SimonGoShutter(BaseSimonCover):
    _attr_supported_features = (
        CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP |
        CoverEntityFeature.SET_POSITION | CoverEntityFeature.SET_TILT_POSITION
    )

    def __init__(self, api: SimonGoApi, name: str) -> None:
        self._api = api
        self._attr_name = name
        self._attr_current_cover_position = None
        self._attr_current_cover_tilt_position = None

    async def async_open_cover(self, **kwargs):
        await self._api.shutter_up()

    async def async_close_cover(self, **kwargs):
        await self._api.shutter_down()

    async def async_stop_cover(self, **kwargs):
        await self._api.shutter_stop()

    async def async_set_cover_position(self, **kwargs):
        pos = int(kwargs.get(ATTR_POSITION, 50))
        pos = max(0, min(100, pos))
        await self._api.shutter_set_position(pos)

    async def async_set_cover_tilt_position(self, **kwargs):
        tilt = int(kwargs.get(ATTR_TILT_POSITION, 50))
        tilt = max(0, min(100, tilt))
        await self._api.shutter_set_tilt(tilt)

class SimonGoRollerGate(BaseSimonCover):
    _attr_supported_features = (
        CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP |
        CoverEntityFeature.SET_POSITION
    )

    def __init__(self, api: SimonGoApi, name: str) -> None:
        self._api = api
        self._attr_name = name

    async def async_open_cover(self, **kwargs):
        await self._api.roller_open()

    async def async_close_cover(self, **kwargs):
        await self._api.roller_close()

    async def async_stop_cover(self, **kwargs):
        await self._api.roller_stop()

    async def async_set_cover_position(self, **kwargs):
        pos = int(kwargs.get(ATTR_POSITION, 50))
        pos = max(0, min(100, pos))
        await self._api.roller_set_position(pos)

class SimonGoGateBox(BaseSimonCover):
    # Impulsowe sterowanie – mapujemy open/close/stop na impulsy
    def __init__(self, api: SimonGoApi, name: str, two_relays: bool) -> None:
        self._api = api
        self._attr_name = name
        self._two = two_relays

    async def async_open_cover(self, **kwargs):
        await self._api.gate_pulse1()

    async def async_close_cover(self, **kwargs):
        if self._two:
            await self._api.gate_pulse2()
        else:
            await self._api.gate_pulse1()

    async def async_stop_cover(self, **kwargs):
        # brak natywnego stop – impuls
        await self._api.gate_pulse1()
