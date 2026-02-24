"""DataUpdateCoordinator for Mobvoi Treadmill."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

if TYPE_CHECKING:
    from datetime import timedelta
    from logging import Logger

    from homeassistant.core import HomeAssistant
    from pymvtreadmill import TreadmillClient

    from .data import TreadmillConfigEntry


class TreadmillDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: TreadmillConfigEntry
    client: TreadmillClient

    def __init__(
        self,
        hass: HomeAssistant,
        logger: Logger,
        name: str,
        update_interval: timedelta,
        client: TreadmillClient,
    ) -> None:
        """Initialize."""
        super().__init__(hass, logger, name=name, update_interval=update_interval)
        self.client = client

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        # The client properties are updated by BLE notifications in the background.
        # We return a snapshot of the current state.
        return {
            "speed": self.client.speed,
            "inclination": self.client.inclination,
            "distance": self.client.distance,
            "total_distance": self.client.total_distance,
            "last_run_distance": self.client.last_run_distance,
            "is_running": self.client.is_running,
        }
