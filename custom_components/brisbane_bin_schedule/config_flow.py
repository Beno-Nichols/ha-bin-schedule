"""Config flow for Brisbane bin schedule."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import CONF_STREET, CONF_STREET_NUMBER, CONF_SUBURB, DOMAIN


class BrisbaneBinScheduleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle integration setup."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            await self.async_set_unique_id(
                "-".join(
                    [
                        user_input[CONF_STREET_NUMBER],
                        user_input[CONF_STREET].lower(),
                        user_input[CONF_SUBURB].lower(),
                    ]
                )
            )
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"{user_input[CONF_STREET_NUMBER]} {user_input[CONF_STREET]}, {user_input[CONF_SUBURB]}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SUBURB): selector.TextSelector(),
                    vol.Required(CONF_STREET): selector.TextSelector(),
                    vol.Required(CONF_STREET_NUMBER): selector.TextSelector(),
                }
            ),
        )


@callback
def async_get_options_flow(config_entry):
    return BrisbaneBinScheduleOptionsFlow(config_entry)


class BrisbaneBinScheduleOptionsFlow(config_entries.OptionsFlow):
    """Handle integration options."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))