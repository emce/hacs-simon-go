from __future__ import annotations

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_RGBW_COLOR,
    ColorMode,
    LightEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SimonGoApi
from .const import CONF_HOST, CONF_DEVICE_TYPE

def _to_hex_from_brightness(brightness: int) -> str:
    b = max(0, min(255, int(brightness)))
    return f"{b:02X}"

def _hex_from_rgbw(r, g, b, w) -> str:
    return f"{r:02X}{g:02X}{b:02X}{w:02X}"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    session = async_get_clientsession(hass)
    api = SimonGoApi(entry.data[CONF_HOST], session)
    t = entry.data[CONF_DEVICE_TYPE]

    entities = []
    if t == "dimmer":
        entities.append(SimonGoDimmer(api, entry.title))
    elif t == "dimmer_w":
        entities.append(SimonGoDimmerW(api, entry.title))
    elif t == "dimmer_rgbw":
        entities.append(SimonGoRGBW(api, entry.title))

    if entities:
        async_add_entities(entities)

class BaseSimonLight(LightEntity):
    _attr_should_poll = False
    _attr_assumed_state = True

class SimonGoDimmer(BaseSimonLight):
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}
    _attr_color_mode = ColorMode.BRIGHTNESS

    def __init__(self, api: SimonGoApi, name: str) -> None:
        self._api = api
        self._attr_name = name
        self._is_on = False
        self._attr_brightness = 255

    @property
    def is_on(self) -> bool: return self._is_on

    async def async_turn_on(self, **kwargs):
        brightness = kwargs.get(ATTR_BRIGHTNESS, self._attr_brightness or 255)
        hex_value = _to_hex_from_brightness(brightness)
        if await self._api.dimmer_set_hex(hex_value):
            self._is_on = brightness > 0
            self._attr_brightness = brightness
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        if await self._api.dimmer_set_hex("00"):
            self._is_on = False
            self._attr_brightness = 0
            self.async_write_ha_state()

class SimonGoDimmerW(SimonGoDimmer):
    # Dodatkowo: efekty i łagodne rozjaśnianie dostępne przez usługi domeny
    pass

class SimonGoRGBW(BaseSimonLight):
    _attr_supported_color_modes = {ColorMode.RGBW}
    _attr_color_mode = ColorMode.RGBW

    def __init__(self, api: SimonGoApi, name: str) -> None:
        self._api = api
        self._attr_name = name
        self._is_on = False
        self._attr_rgbw_color = (255, 255, 255, 0)

    @property
    def is_on(self) -> bool: return self._is_on

    @property
    def rgbw_color(self):
        return self._attr_rgbw_color

    async def async_turn_on(self, **kwargs):
        rgbw = kwargs.get(ATTR_RGBW_COLOR, self._attr_rgbw_color)
        r, g, b, w = [max(0, min(255, int(x))) for x in rgbw]
        if await self._api.rgbw_set_hex(_hex_from_rgbw(r, g, b, w)):
            self._is_on = (r+g+b+w) > 0
            self._attr_rgbw_color = (r, g, b, w)
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        if await self._api.rgbw_set_hex("00000000"):
            self._is_on = False
            self._attr_rgbw_color = (0, 0, 0, 0)
            self.async_write_ha_state()
