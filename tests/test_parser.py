from datetime import date, timedelta

from custom_components.brisbane_bin_schedule.schedule import parse_schedule


def test_parse_nested_schedule_records():
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    payload = {"data": {"waste_flags": [{"collection_date": tomorrow, "waste_type": "general"}]}}

    result = parse_schedule(payload)

    assert result["next"] == {"date": date.today() + timedelta(days=1), "type": "General waste"}


def test_parse_ignores_past_records():
    payload = {"items": [{"date": "01/01/2020", "bin_type": "recycling"}]}

    assert parse_schedule(payload)["collections"] == []


def test_parse_collection_day():
    result = parse_schedule({"results": [{"collection_day": "TUESDAY", "zone": "ZONE 2", "next_red_bin": "2026-08-25", "next_yellow_bin": "2026-09-01", "next_green_bin": "2026-09-08"}]})

    assert result["collection_day"] == "TUESDAY"
    assert result["next"]["type"] == "General waste"
    assert len(result["collections"]) == 3