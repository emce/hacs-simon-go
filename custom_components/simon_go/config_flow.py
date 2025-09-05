from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import CONF_HOST, CONF_NAME
from .const import DOMAIN, DEVICE_TYPES, CONF_DEVICE_TYPE

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_DEVICE_TYPE): vol.In(DEVICE_TYPES),
    vol.Optional(CONF_NAME, default="Simon GO"): str,
})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)

        host = user_input[CONF_HOST]
        unique_id = f"{host}-{user_input[CONF_DEVICE_TYPE]}"
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=user_input.get(CONF_NAME, "Simon GO"), data=user_input)
