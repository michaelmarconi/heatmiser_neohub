"""Custom types for heatmiser_neohub."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import HeatmiserNeohubApiClient
    from .coordinator import HeatmiserNeohubDataUpdateCoordinator


type HeatmiserNeohubConfigEntry = ConfigEntry[HeatmiserNeohubData]


@dataclass
class HeatmiserNeohubData:
    """Data for the HeatmiserNeohub integration."""

    client: HeatmiserNeohubApiClient
    coordinator: HeatmiserNeohubDataUpdateCoordinator
    integration: Integration
