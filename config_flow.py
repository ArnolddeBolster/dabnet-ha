from __future__ import annotations

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
import voluptuous as vol

from .const import DOMAIN, CONF_HOST, CONF_NAME, CONF_POLL_INTERVAL, DEFAULT_NAME, DEFAULT_POLL_INTERVAL

async def validate_input(hass: HomeAssistant, data: dict):
    # Hier zou je eventueel een testcall naar de API kunnen doen
    return {"title": data.get(CONF_NAME) or DEFAULT_NAME}

class DabNetConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_import(self, user_input=None):
        return await self.async_step_user(user_input)

class DabNetOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema({
            vol.Optional(
                CONF_POLL_INTERVAL,
                default=self.config_entry.options.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL),
            ): int
        })

        return self.async_show_form(step_id="init", data_schema=schema)

async def async_get_options_flow(config_entry):
    return DabNetOptionsFlowHandler(config_entry)
