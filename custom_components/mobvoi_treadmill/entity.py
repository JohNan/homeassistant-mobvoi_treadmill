"""TreadmillEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .coordinator import TreadmillDataUpdateCoordinator


class TreadmillEntity(CoordinatorEntity[TreadmillDataUpdateCoordinator]):
    """TreadmillEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: TreadmillDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)

        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    coordinator.config_entry.unique_id,
                ),
            },
            name=coordinator.config_entry.title,
            manufacturer="Mobvoi",
            model="Home Treadmill",
        )
