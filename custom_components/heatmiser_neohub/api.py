"""Heatmiser neoHub API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout
from numpy import number


class HeatmiserNeohubApiClientError(Exception):
    """Exception to indicate a general API error."""


class HeatmiserNeohubApiClientCommunicationError(
    HeatmiserNeohubApiClientError,
):
    """Exception to indicate a communication error."""


class HeatmiserNeohubApiClientAuthenticationError(
    HeatmiserNeohubApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise HeatmiserNeohubApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class HeatmiserNeohubApiClient:
    """Client for the Heatmiser websocket API."""

    def __init__(
        self,
        host: str,
        port: number,
        token: str,
        session: aiohttp.ClientSession,
    ) -> None:
        self._host = host
        self._port = port
        self._token = token
        self._session = session

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="get",
            url="https://jsonplaceholder.typicode.com/posts/1",
        )

    async def async_set_title(self, value: str) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="patch",
            url="https://jsonplaceholder.typicode.com/posts/1",
            data={"title": value},
            headers={"Content-type": "application/json; charset=UTF-8"},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise HeatmiserNeohubApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise HeatmiserNeohubApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise HeatmiserNeohubApiClientError(
                msg,
            ) from exception
