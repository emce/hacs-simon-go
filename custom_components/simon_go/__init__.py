from __future__ import annotations
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORM_MAP, CONF_DEVICE_TYPE, CONF_HOST
from .api import SimonGoApi

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    device_type = entry.data.get(CONF_DEVICE_TYPE)
    platforms = PLATFORM_MAP.get(device_type, [])
    await hass.config_entries.async_forward_entry_setups(entry, platforms)

    # Register helpful services (targeted by host)
    async def _api_from_call(call: ServiceCall) -> SimonGoApi:
        host = call.data.get("host") or entry.data.get(CONF_HOST)
        session = hass.helpers.aiohttp_client.async_get_clientsession()
        return SimonGoApi(host, session)

    async def handle_switch_for_time(call: ServiceCall):
        api = await _api_from_call(call)
        seconds = int(call.data["seconds"])
        channel = call.data.get("channel")
        if channel is None:
            await api.get(f"/s/1/forTime/{seconds}/ns/0")
        else:
            await api.get(f"/s/{channel}/1/forTime/{seconds}/ns/0")

    async def handle_switch_toggle(call: ServiceCall):
        api = await _api_from_call(call)
        channel = call.data.get("channel")
        if channel is None:
            await api.get("/s/2")
        else:
            await api.get(f"/s/{channel}/2")

    async def handle_dimmer_set_hex(call: ServiceCall):
        api = await _api_from_call(call)
        await api.get(f"/s/{call.data['hex']}")

    async def handle_dimmer_inc(call: ServiceCall):
        api = await _api_from_call(call)
        await api.get(f"/s/inc/{int(call.data['step'])}")

    async def handle_dimmer_dec(call: ServiceCall):
        api = await _api_from_call(call)
        await api.get(f"/s/dec/{int(call.data['step'])}")

    async def handle_dimmer_effect(call: ServiceCall):
        api = await _api_from_call(call)
        effect = int(call.data["effect"])
        seconds = call.data.get("seconds")
        if seconds is None:
            await api.get(f"/s/x/{effect}")
        else:
            await api.get(f"/s/x/{effect}/forTime/{int(seconds)}")

    async def handle_rgbw_set_hex(call: ServiceCall):
        api = await _api_from_call(call)
        await api.get(f"/s/{call.data['hex']}")

    async def handle_rgbw_effect(call: ServiceCall):
        api = await _api_from_call(call)
        effect = int(call.data["effect"])
        await api.get(f"/s/x/{effect}")

    async def handle_shutter_favorite(call: ServiceCall):
        api = await _api_from_call(call)
        await api.get("/s/f")

    async def handle_shutter_toggle(call: ServiceCall):
        api = await _api_from_call(call)
        await api.get("/s/n")

    async def handle_shutter_tilt(call: ServiceCall):
        api = await _api_from_call(call)
        await api.get(f"/s/t/{int(call.data['percent'])}")

    async def handle_rollergate_vent(call: ServiceCall):
        api = await _api_from_call(call)
        await api.get("/s/w")

    async def handle_gate_pulse1(call: ServiceCall):
        api = await _api_from_call(call)
        await api.get("/s/p")

    async def handle_gate_pulse2(call: ServiceCall):
        api = await _api_from_call(call)
        await api.get("/s/s")

    async def handle_thermo_boost(call: ServiceCall):
        api = await _api_from_call(call)
        await api.get("/s/3")

    async def handle_thermo_set_raw(call: ServiceCall):
        api = await _api_from_call(call)
        await api.get(f"/s/t/{int(call.data['raw'])}")

    hass.services.async_register(DOMAIN, "switch_for_time", handle_switch_for_time)
    hass.services.async_register(DOMAIN, "switch_toggle", handle_switch_toggle)
    hass.services.async_register(DOMAIN, "dimmer_set_hex", handle_dimmer_set_hex)
    hass.services.async_register(DOMAIN, "dimmer_inc", handle_dimmer_inc)
    hass.services.async_register(DOMAIN, "dimmer_dec", handle_dimmer_dec)
    hass.services.async_register(DOMAIN, "dimmer_effect", handle_dimmer_effect)
    hass.services.async_register(DOMAIN, "rgbw_set_hex", handle_rgbw_set_hex)
    hass.services.async_register(DOMAIN, "rgbw_effect", handle_rgbw_effect)
    hass.services.async_register(DOMAIN, "shutter_favorite", handle_shutter_favorite)
    hass.services.async_register(DOMAIN, "shutter_toggle", handle_shutter_toggle)
    hass.services.async_register(DOMAIN, "shutter_set_tilt", handle_shutter_tilt)
    hass.services.async_register(DOMAIN, "rollergate_vent", handle_rollergate_vent)
    hass.services.async_register(DOMAIN, "gate_pulse1", handle_gate_pulse1)
    hass.services.async_register(DOMAIN, "gate_pulse2", handle_gate_pulse2)
    hass.services.async_register(DOMAIN, "thermo_boost", handle_thermo_boost)
    hass.services.async_register(DOMAIN, "thermo_set_raw", handle_thermo_set_raw)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    device_type = entry.data.get(CONF_DEVICE_TYPE)
    platforms = PLATFORM_MAP.get(device_type, [])
    return await hass.config_entries.async_unload_platforms(entry, platforms)
