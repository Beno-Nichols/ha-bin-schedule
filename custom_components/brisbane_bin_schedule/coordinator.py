"""Fetch and normalize Brisbane waste collection data."""

from __future__ import annotations

from datetime import timedelta
import logging

import async_timeout
from aiohttp import ClientError
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_URL, CONF_STREET, CONF_STREET_NUMBER, CONF_SUBURB, DEFAULT_SCAN_INTERVAL, DOMAIN
from .schedule import parse_schedule


class BrisbaneBinScheduleCoordinator(DataUpdateCoordinator):
    """Coordinate API updates for one address."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.entry = entry
        super().__init__(
            hass,
            logger=logging.getLogger(__name__),
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        params = {
            "where": " AND ".join(
                [
                    f'house_number = "{self.entry.data[CONF_STREET_NUMBER]}"',
                    f'suburb = "{self.entry.data[CONF_SUBURB].upper()}"',
                    f'street_name like "{self.entry.data[CONF_STREET].upper()}%"',
                ]
            ),
            "limit": 20,
        }
        try:
            async with async_timeout.timeout(20):
                session = async_get_clientsession(self.hass)
                async with session.get(API_URL, params=params) as response:
                    response.raise_for_status()
                    payload = await response.json()
                    if not payload.get("results"):
                        raise UpdateFailed("No Brisbane property matched this address")
                    return parse_schedule(payload)
        except (ClientError, TimeoutError, ValueError) as err:
            raise UpdateFailed(f"Unable to fetch Brisbane bin schedule: {err}") from err