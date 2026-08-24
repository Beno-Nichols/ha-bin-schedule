"""Normalize Brisbane waste collection payloads."""

from __future__ import annotations

from datetime import date, datetime
import re

DATE_KEYS = ("collection_date", "pickup_date", "service_date", "next_date", "date")
TYPE_KEYS = ("waste_type", "bin_type", "waste", "type", "name", "flag")
BIN_DATE_FIELDS = {
    "next_red_bin": "General waste",
    "next_yellow_bin": "Recycling",
    "next_green_bin": "Green waste",
}
WEEKDAYS = {name: index for index, name in enumerate(("MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"))}


def _date_value(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None
    value = value.strip()
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        pass
    for fmt in ("%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    return None


def _label(value):
    text = re.sub(r"[_-]+", " ", str(value)).strip()
    replacements = {"general": "General waste", "recycling": "Recycling", "green": "Green waste"}
    return replacements.get(text.lower(), text.title())


def _next_weekday(day_name, today=None):
    today = today or date.today()
    weekday = WEEKDAYS.get(str(day_name).upper().strip())
    if weekday is None:
        return None
    return today.fromordinal(today.toordinal() + (weekday - today.weekday()) % 7)


def parse_schedule(payload):
    """Extract collection records from the API's nested response formats."""
    records = []

    def visit(value):
        if isinstance(value, dict):
            for field, bin_type in BIN_DATE_FIELDS.items():
                bin_date = _date_value(value.get(field))
                if bin_date:
                    records.append({"date": bin_date, "type": bin_type})
            found_date = next((_date_value(value[key]) for key in DATE_KEYS if key in value), None)
            found_type = next((value[key] for key in TYPE_KEYS if key in value), "Bin")
            if found_date:
                records.append({"date": found_date, "type": _label(found_type)})
            collection_day = value.get("collection_day")
            if collection_day and not found_date and not any(value.get(field) for field in BIN_DATE_FIELDS):
                next_date = _next_weekday(collection_day)
                if next_date:
                    records.append({"date": next_date, "type": "Collection day"})
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(payload)
    unique = {(item["date"], item["type"]): item for item in records}
    collections = sorted(unique.values(), key=lambda item: item["date"])
    today = date.today()
    upcoming = [item for item in collections if item["date"] >= today]
    results = payload.get("results", []) if isinstance(payload, dict) else []
    first_result = next((value for value in results if isinstance(value, dict)), {})
    return {
        "collections": upcoming,
        "next": upcoming[0] if upcoming else None,
        "collection_day": first_result.get("collection_day"),
        "zone": first_result.get("zone"),
    }