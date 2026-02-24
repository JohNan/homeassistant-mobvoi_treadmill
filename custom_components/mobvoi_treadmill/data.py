"""Custom types for Mobvoi Treadmill."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration
    from pymvtreadmill import TreadmillClient

    from .coordinator import TreadmillDataUpdateCoordinator


type TreadmillConfigEntry = ConfigEntry[TreadmillData]


@dataclass
class TreadmillData:
    """Data for the Treadmill integration."""

    client: TreadmillClient
    coordinator: TreadmillDataUpdateCoordinator
    integration: Integration
