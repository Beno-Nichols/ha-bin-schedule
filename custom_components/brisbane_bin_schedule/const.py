"""Constants for the Brisbane bin schedule integration."""

from homeassistant.const import Platform

DOMAIN = "brisbane_bin_schedule"
API_URL = "https://data.brisbane.qld.gov.au/api/explore/v2.1/catalog/datasets/waste-collection-days-collection-days/records"
PLATFORMS = [Platform.SENSOR]
CONF_SUBURB = "suburb"
CONF_STREET = "street"
CONF_STREET_NUMBER = "street_number"
CONF_API_KEY = "api_key"
DEFAULT_SCAN_INTERVAL = 86400