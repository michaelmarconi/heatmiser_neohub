"""Sensor platform for heatmiser_neohub."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import HeatmiserNeohubEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import HeatmiserNeohubDataUpdateCoordinator
    from .data import HeatmiserNeohubConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="heatmiser_neohub",
        name="Integration Sensor",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: HeatmiserNeohubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        HeatmiserNeohubSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class HeatmiserNeohubSensor(HeatmiserNeohubEntity, SensorEntity):
    """heatmiser_neohub Sensor class."""

    def __init__(
        self,
        coordinator: HeatmiserNeohubDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data.get("body")
