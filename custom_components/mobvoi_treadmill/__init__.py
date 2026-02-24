"""Custom integration to integrate Mobvoi Treadmill with Home Assistant."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.components.bluetooth import async_ble_device_from_address
from homeassistant.const import CONF_ADDRESS, Platform
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.loader import async_get_loaded_integration
from pymvtreadmill import TreadmillClient

from .const import DOMAIN, LOGGER
from .coordinator import TreadmillDataUpdateCoordinator
from .data import TreadmillData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import TreadmillConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TreadmillConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    address = entry.data[CONF_ADDRESS]
    ble_device = async_ble_device_from_address(hass, address)

    if not ble_device:
        raise ConfigEntryNotReady(f"Could not find BLE device with address {address}")

    client = TreadmillClient()

    try:
        await client.connect(ble_device)
    except Exception as exception:
        raise ConfigEntryNotReady(f"Failed to connect to {address}: {exception}") from exception

    coordinator = TreadmillDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(seconds=1),
        client=client,
    )

    entry.runtime_data = TreadmillData(
        client=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: TreadmillConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    # Disconnect client
    try:
        await entry.runtime_data.client.disconnect()
    except Exception:
        LOGGER.exception("Error disconnecting from treadmill")

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: TreadmillConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
