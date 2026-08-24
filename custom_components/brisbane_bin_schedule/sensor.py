"""Sensors for Brisbane bin collections."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, GENERAL_GREEN_IMAGE, GENERAL_RECYCLING_IMAGE
from .coordinator import BrisbaneBinScheduleCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            BrisbaneScheduleSensor(coordinator, entry, "next_collection", "Next collection"),
            BrisbaneScheduleSensor(coordinator, entry, "bins_due", "Bins due"),
        ]
    )


class BrisbaneScheduleSensor(CoordinatorEntity, SensorEntity):
    """Represent the next collection or its bin types."""

    def __init__(self, coordinator: BrisbaneBinScheduleCoordinator, entry, key, name):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_icon = "mdi:calendar-arrow-right" if key == "next_collection" else "mdi:trash-can-outline"

    @property
    def native_value(self):
        next_collection = self.coordinator.data.get("next")
        if not next_collection:
            return "No upcoming collection"
        if self._key == "next_collection":
            return next_collection["date"]
        next_date = next_collection["date"]
        return ", ".join(
            item["type"]
            for item in self.coordinator.data["collections"]
            if item["date"] == next_date
        )

    @property
    def device_class(self):
        return "date" if self._key == "next_collection" else None

    @property
    def extra_state_attributes(self):
        next_collection = self.coordinator.data.get("next")
        next_date = next_collection["date"] if next_collection else None
        bin_types = [
            item["type"]
            for item in self.coordinator.data.get("collections", [])
            if item["date"] == next_date
        ] if next_date else []
        image_url = (
            GENERAL_RECYCLING_IMAGE
            if any("Recycling" in item for item in bin_types)
            else GENERAL_GREEN_IMAGE
        )
        return {
            "upcoming": [
                {"date": item["date"].isoformat(), "bin": item["type"]}
                for item in self.coordinator.data.get("collections", [])[:10]
            ],
            "collection_day": self.coordinator.data.get("collection_day"),
            "zone": self.coordinator.data.get("zone"),
            "bin_types": bin_types,
            "bin_image": image_url,
        }