"""Provide info to system health."""

import asyncio
import datetime
import logging

from aioautomower.session import AutomowerSession

from homeassistant.components.system_health import SystemHealthRegistration
from homeassistant.core import HomeAssistant, callback

from . import AutomowerConfigEntry
from .const import DOMAIN

background_tasks: set = set()
_LOGGER = logging.getLogger(__name__)


@callback
def async_register(hass: HomeAssistant, register: SystemHealthRegistration) -> None:
    """Register system health callbacks."""
    register.async_register_info(system_health_info)


async def _send_messages(
    automower_client: AutomowerSession,
) -> None:
    """Listen with the client."""
    try:
        await automower_client.send_empty_message()
    except Exception as err:  # noqa: BLE001
        # We need to guard against unknown exceptions to not crash this task.
        _LOGGER.debug("Unexpected exception: %s", err)


async def system_health_info(hass: HomeAssistant) -> dict:
    """Get info for the info page."""
    config_entry: AutomowerConfigEntry = hass.config_entries.async_entries(DOMAIN)[0]
    coordinator = config_entry.runtime_data
    ping_pong_task = asyncio.create_task(_send_messages(coordinator.api))
    background_tasks.add(ping_pong_task)
    coordinator.api.register_pong_callback(pong_callback)
    return {"can_reach_server": coordinator.api.last_ws_message}


def pong_callback(ws_data: datetime.datetime) -> None:
    """Process websocket callbacks and write them to the DataUpdateCoordinator."""
    _LOGGER.debug("Last websocket info: % s", ws_data)
