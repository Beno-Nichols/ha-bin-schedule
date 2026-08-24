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

The next collection sensor exposes the next collection date, collection weekday, zone, upcoming records, bin types, and a `bin_image` URL. The `Bins due` sensor identifies General waste, Recycling, or Green waste for that date.

## Day-before notification

Add an automation in Home Assistant and replace the notification service with your phone's notify service:

```yaml
alias: Bins out reminder
triggers:
	- trigger: time
		at: "07:00:00"
conditions:
	- condition: template
		value_template: >-
			{{ (states('sensor.next_collection') | as_datetime | as_local).date()
				 == (now() + timedelta(days=1)).date() }}
actions:
	- action: notify.mobile_app_your_phone
		data:
			title: Bins out tomorrow
			message: >-
				{{ state_attr('sensor.bins_due', 'bin_types') | join(', ') }} collection
				is tomorrow. Collection day: {{ state_attr('sensor.next_collection', 'collection_day') }}.
			data:
				image: "{{ state_attr('sensor.bins_due', 'bin_image') }}"
mode: single
```

The date sensor is the trigger source and the `bins_due` attributes provide both the bin image and bin names for the notification.

## API

The integration calls the Brisbane City Council Open Data Bin Collection Calendar endpoint using the configured address:

`https://data.brisbane.qld.gov.au/api/explore/v2.1/catalog/datasets/waste-collection-days-collection-days/records`