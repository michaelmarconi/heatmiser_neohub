"""Adds config flow for HeatmiserNeohub."""

from __future__ import annotations

from typing import TYPE_CHECKING

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_TOKEN
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    HeatmiserNeohubApiClient,
    HeatmiserNeohubApiClientAuthenticationError,
    HeatmiserNeohubApiClientCommunicationError,
    HeatmiserNeohubApiClientError,
)
from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from numpy import number


class HeatmiserNeohubFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for HeatmiserNeohub."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    host=user_input[CONF_HOST],
                    port=user_input[CONF_PORT],
                    token=user_input[CONF_TOKEN],
                )
            except HeatmiserNeohubApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except HeatmiserNeohubApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except HeatmiserNeohubApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title="Heatmiser neoHub",
                    # title=user_input[CONF_USERNAME],  # TODO: nuke
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default=(user_input or {}).get(CONF_HOST, ""),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Required(
                        CONF_PORT,
                        default=(user_input or {}).get(CONF_HOST, ""),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.NUMBER,
                        ),
                    ),
                    vol.Required(
                        CONF_TOKEN,
                        default=(user_input or {}).get(CONF_HOST, ""),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_credentials(self, host: str, port: number, token: str) -> None:
        """Validate credentials."""
        client = HeatmiserNeohubApiClient(
            host=host,
            port=port,
            token=token,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
