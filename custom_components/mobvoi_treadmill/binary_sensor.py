"""Binary sensor platform for Mobvoi Treadmill."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .entity import TreadmillEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import TreadmillDataUpdateCoordinator
    from .data import TreadmillConfigEntry

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="is_running",
        name="Running",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: TreadmillConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        TreadmillBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class TreadmillBinarySensor(TreadmillEntity, BinarySensorEntity):
    """Treadmill Binary Sensor class."""

    def __init__(
        self,
        coordinator: TreadmillDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.unique_id}_{entity_description.key}"
        )

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary_sensor is on."""
        return self.coordinator.data.get(self.entity_description.key)
