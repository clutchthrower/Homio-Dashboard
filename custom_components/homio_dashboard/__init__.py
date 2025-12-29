"""The Homio Dashboard integration."""
from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path

from homeassistant.components.frontend import add_extra_js_url, async_remove_panel
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.lovelace import _register_panel
from homeassistant.components.lovelace.dashboard import LovelaceYAML
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, VERSION

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Homio Dashboard component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Homio Dashboard from a config entry."""

    # Copy theme to standard themes directory for easy use
    await _copy_theme_to_config(hass)

    # Copy packages to standard packages directory
    await _copy_packages_to_config(hass)

    # Create template sensors (no YAML include needed!)
    await _create_template_sensors(hass)

    # Create helper entities (no YAML include needed!)
    await _create_helper_entities(hass)

    # Register static paths and resources
    await _register_static_resources(hass)

    # Register the dashboard panel
    await _setup_dashboard_panel(hass, entry)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Remove the dashboard from lovelace
    lovelace_data = hass.data.get("lovelace")
    if lovelace_data and hasattr(lovelace_data, "dashboards") and DOMAIN in lovelace_data.dashboards:
        # Remove from dashboards dict
        if hasattr(lovelace_data, "dashboards"):
            lovelace_data.dashboards.pop(DOMAIN, None)
        else:
            lovelace_data["dashboards"].pop(DOMAIN, None)

    return True


async def _copy_theme_to_config(hass: HomeAssistant) -> None:
    """Copy Homio theme to the standard Home Assistant themes directory."""
    integration_dir = Path(__file__).parent
    source_theme = integration_dir / "themes" / "homio"

    # Standard HA themes directory
    config_dir = Path(hass.config.config_dir)
    dest_themes_dir = config_dir / "themes"
    dest_theme = dest_themes_dir / "homio"

    def _copy_theme():
        """Copy theme files (runs in executor)."""
        try:
            # Create themes directory if it doesn't exist
            dest_themes_dir.mkdir(exist_ok=True)

            # Copy theme to standard location (overwrite if exists for updates)
            if source_theme.exists():
                if dest_theme.exists():
                    shutil.rmtree(dest_theme)
                shutil.copytree(source_theme, dest_theme)
                return True
            else:
                _LOGGER.warning(f"Source theme not found: {source_theme}")
                return False
        except Exception as e:
            _LOGGER.error(f"Failed to copy Homio theme: {e}")
            return False

    try:
        success = await hass.async_add_executor_job(_copy_theme)
        if success:
            _LOGGER.info(f"✅ Homio theme copied to {dest_theme}")
    except Exception as e:
        _LOGGER.error(f"Failed to copy Homio theme: {e}")


async def _copy_packages_to_config(hass: HomeAssistant) -> None:
    """Copy Homio packages to the standard Home Assistant packages directory."""
    integration_dir = Path(__file__).parent
    source_packages = integration_dir / "packages"

    # Standard HA packages directory
    config_dir = Path(hass.config.config_dir)
    dest_packages_dir = config_dir / "packages"
    dest_package = dest_packages_dir / "homio"

    def _copy_packages():
        """Copy package files (runs in executor)."""
        try:
            # Create packages directory if it doesn't exist
            dest_packages_dir.mkdir(exist_ok=True)

            # Copy packages to standard location (overwrite if exists for updates)
            if source_packages.exists():
                if dest_package.exists():
                    shutil.rmtree(dest_package)
                shutil.copytree(source_packages, dest_package)
                return True
            else:
                _LOGGER.warning(f"Source packages not found: {source_packages}")
                return False
        except Exception as e:
            _LOGGER.error(f"Failed to copy Homio packages: {e}")
            return False

    try:
        success = await hass.async_add_executor_job(_copy_packages)
        if success:
            _LOGGER.info(f"✅ Homio packages copied to {dest_package}")
    except Exception as e:
        _LOGGER.error(f"Failed to copy Homio packages: {e}")


async def _create_template_sensors(hass: HomeAssistant) -> None:
    """Create Homio template sensors programmatically (no YAML needed!)."""
    try:
        # Create Current Date sensor
        hass.states.async_set(
            "sensor.homio_current_date",
            "",
            {
                "friendly_name": "Current Date",
                "icon": "mdi:calendar",
            }
        )

        # Create Current Time sensor
        hass.states.async_set(
            "sensor.homio_current_time",
            "",
            {
                "friendly_name": "Current Time",
                "icon": "mdi:clock",
            }
        )

        # Set up periodic updates
        async def update_sensors(now=None):
            """Update the template sensors."""
            from datetime import datetime
            now = datetime.now()

            # Format date: "Monday 29th December 2025"
            day = now.day
            suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
            date_str = now.strftime(f"%A {day}{suffix} %B %Y")

            # Format time: "14:30"
            time_str = now.strftime("%H:%M")

            hass.states.async_set("sensor.homio_current_date", date_str)
            hass.states.async_set("sensor.homio_current_time", time_str)

        # Update immediately
        await update_sensors()

        # Update every minute
        from homeassistant.helpers.event import async_track_time_interval
        from datetime import timedelta
        async_track_time_interval(hass, update_sensors, timedelta(minutes=1))

        _LOGGER.info("✅ Homio template sensors created (sensor.homio_current_date, sensor.homio_current_time)")

    except Exception as e:
        _LOGGER.error(f"Failed to create Homio sensors: {e}")


async def _create_helper_entities(hass: HomeAssistant) -> None:
    """Create Homio helper entities programmatically (no YAML needed!)."""
    try:
        # Create input_boolean helpers
        hass.states.async_set(
            "input_boolean.homio_mobile_navigation",
            "off",
            {
                "friendly_name": "Mobile Navigation",
                "icon": "mdi:menu",
            }
        )

        hass.states.async_set(
            "input_boolean.homio_heating_control",
            "off",
            {
                "friendly_name": "Heating Control",
                "icon": "mdi:radiator",
            }
        )

        hass.states.async_set(
            "input_boolean.homio_hot_water_control",
            "off",
            {
                "friendly_name": "Hot Water Control",
                "icon": "mdi:water-boiler",
            }
        )

        # Create input_number helper
        hass.states.async_set(
            "input_number.homio_thermostat_target_temperature",
            "20",
            {
                "friendly_name": "Homio Thermostat Target Temperature",
                "icon": "mdi:thermometer",
                "unit_of_measurement": "°C",
                "min": 7,
                "max": 24,
                "step": 0.5,
            }
        )

        _LOGGER.info("✅ Homio helper entities created (3 input_booleans, 1 input_number)")

    except Exception as e:
        _LOGGER.error(f"Failed to create Homio helpers: {e}")


async def _register_static_resources(hass: HomeAssistant) -> None:
    """Register static paths and frontend resources."""
    integration_dir = Path(__file__).parent
    www_dir = integration_dir / "www"

    # Register the entire www directory for static file serving
    await hass.http.async_register_static_paths(
        [StaticPathConfig(f"/{DOMAIN}", str(www_dir), cache_headers=False)]
    )
    _LOGGER.info(f"Registered static path: /{DOMAIN} -> {www_dir}")

    # JavaScript files to load as frontend resources
    js_files = [
        "button-card/button-card.js",
        "community/layout-card-modified/layout-card-modified.js",
        "community/light-slider/my-slider-v2.js",
    ]

    # Register each JavaScript file as a frontend resource
    for file_path in js_files:
        full_path = www_dir / file_path
        if full_path.exists():
            # Add to frontend resources with version for cache busting
            resource_url = f"/{DOMAIN}/{file_path}?v={VERSION}"
            add_extra_js_url(hass, resource_url, es5=False)
            _LOGGER.info(f"Registered JS resource: {resource_url}")
        else:
            _LOGGER.warning(f"JS file not found: {full_path}")


async def _setup_dashboard_panel(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register the Homio Dashboard panel."""

    integration_dir = Path(__file__).parent
    dashboard_path = integration_dir / "lovelace" / "homio.yaml"

    dashboard_config = {
        "mode": "yaml",
        "title": "Homio",
        "icon": "mdi:star-plus-outline",
        "show_in_sidebar": True,
        "filename": str(dashboard_path),
        "require_admin": False,
    }

    # Get lovelace data
    lovelace_data = hass.data.get("lovelace")
    if not lovelace_data:
        _LOGGER.error("Lovelace data not available")
        return

    # Create the Lovelace YAML dashboard
    dashboard = LovelaceYAML(hass, DOMAIN, dashboard_config)

    # Use attribute access instead of dictionary access
    if hasattr(lovelace_data, "dashboards"):
        lovelace_data.dashboards[DOMAIN] = dashboard
    else:
        # Fallback for older HA versions
        lovelace_data["dashboards"][DOMAIN] = dashboard

    # Load the dashboard YAML config (this is critical for proper routing!)
    try:
        await dashboard.async_load(False)
        _LOGGER.info("Dashboard YAML loaded successfully")
    except Exception as e:
        _LOGGER.error(f"Failed to load dashboard YAML: {e}")
        raise

    # Register the panel in the frontend sidebar (this makes the icon show up!)
    _register_panel(hass, DOMAIN, "yaml", dashboard_config, False)

    _LOGGER.info(f"Homio Dashboard panel registered successfully")
