# Brisbane Bin Schedule

Home Assistant custom integration for Brisbane City Council waste collection schedules, installable through [HACS](https://hacs.xyz/).

## Installation

1. In HACS, open **Integrations**, choose the three-dot menu, select **Custom repositories**, and add this repository URL as an **Integration**.
2. Download **Brisbane Bin Schedule** and restart Home Assistant.
3. Add it from **Settings > Devices & services > Add integration**.
4. Enter the suburb, street name, and street number. The street can be entered with or without its suffix, such as `Hyde` or `Hyde Rd`.

The integration uses Brisbane City Council's public Open Data Bin Collection Calendar dataset, so no API key is required.

## Dashboard card

Copy `www/brisbane-bin-schedule-card.js` to your Home Assistant `/config/www/` directory and add `/local/brisbane-bin-schedule-card.js` as a Lovelace resource with resource type **JavaScript module**. Then add this card, replacing the entity IDs with the entities created for your address:

```yaml
type: custom:brisbane-bin-schedule-card
title: Our bins
next_entity: sensor.next_collection
bins_entity: sensor.bins_due
```

The next collection sensor exposes the next collection date, collection weekday, zone, and upcoming records. The `Bins due` sensor identifies General waste, Recycling, or Green waste for that date.

## API

The integration calls the Brisbane City Council Open Data collection-days endpoint using the configured address:

`https://data.brisbane.qld.gov.au/api/explore/v2.1/catalog/datasets/waste-collection-days-collection-days/records`