"""Adds config flow for Mobvoi Treadmill."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.const import CONF_ADDRESS, CONF_NAME

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.data_entry_flow import FlowResult


class TreadmillFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Mobvoi Treadmill."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        """Handle the bluetooth discovery step."""
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()

        self._discovery_info = discovery_info

        self.context["title_placeholders"] = {
            "name": discovery_info.name,
        }

        return await self.async_step_user()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        # If triggered by discovery
        if self._discovery_info:
            if user_input is not None:
                return self.async_create_entry(
                    title=self._discovery_info.name,
                    data={
                        CONF_NAME: self._discovery_info.name,
                        CONF_ADDRESS: self._discovery_info.address,
                    },
                )

            return self.async_show_form(
                step_id="user",
                description_placeholders={"name": self._discovery_info.name},
            )

        # If manually triggered
        errors: dict[str, str] = {}

        if user_input is not None:
            address = user_input[CONF_ADDRESS]
            # Find the device info again to be sure
            discovered = async_discovered_service_info(self.hass)
            discovery_info = next(
                (info for info in discovered if info.address == address), None
            )

            if discovery_info:
                await self.async_set_unique_id(discovery_info.address)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=discovery_info.name,
                    data={
                        CONF_NAME: discovery_info.name,
                        CONF_ADDRESS: discovery_info.address,
                    },
                )
            errors["base"] = "cannot_connect"

        # List devices
        discovered = async_discovered_service_info(self.hass)
        treadmills = [
            info
            for info in discovered
            if info.name and info.name.startswith("Mobvoi")
        ]

        if not treadmills:
            return self.async_abort(reason="no_devices_found")

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ADDRESS): vol.In(
                        {
                            info.address: f"{info.name} ({info.address})"
                            for info in treadmills
                        }
                    )
                }
            ),
            errors=errors,
        )
