"""Sensor platform for Mobvoi Treadmill."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfLength, UnitOfSpeed

from .entity import TreadmillEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import TreadmillDataUpdateCoordinator
    from .data import TreadmillConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="speed",
        name="Speed",
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        device_class=SensorDeviceClass.SPEED,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="inclination",
        name="Inclination",
        native_unit_of_measurement="%",
        icon="mdi:slope-uphill",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="distance",
        name="Distance",
        native_unit_of_measurement=UnitOfLength.METERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="total_distance",
        name="Total Distance",
        native_unit_of_measurement=UnitOfLength.METERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.TOTAL,
    ),
    SensorEntityDescription(
        key="last_run_distance",
        name="Last Run Distance",
        native_unit_of_measurement=UnitOfLength.METERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: TreadmillConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        TreadmillSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class TreadmillSensor(TreadmillEntity, SensorEntity):
    """Treadmill Sensor class."""

    def __init__(
        self,
        coordinator: TreadmillDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.unique_id}_{entity_description.key}"
        )

    @property
    def native_value(self) -> float | int | None:
        """Return the native value of the sensor."""
        return self.coordinator.data.get(self.entity_description.key)
