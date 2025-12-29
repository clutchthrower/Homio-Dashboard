"""The Homio Dashboard integration."""
from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
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

    # Register static paths and resources
    await _register_static_resources(hass)

    # Register the dashboard panel
    await _register_panel(hass, entry)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Remove the dashboard panel
    if DOMAIN in hass.data.get("lovelace", {}).get("dashboards", {}):
        hass.components.frontend.async_remove_panel(DOMAIN)

    return True


async def _copy_theme_to_config(hass: HomeAssistant) -> None:
    """Copy Homio theme to the standard Home Assistant themes directory."""
    integration_dir = Path(__file__).parent
    source_theme = integration_dir / "themes" / "homio"

    # Standard HA themes directory
    config_dir = Path(hass.config.config_dir)
    dest_themes_dir = config_dir / "themes"
    dest_theme = dest_themes_dir / "homio"

    try:
        # Create themes directory if it doesn't exist
        dest_themes_dir.mkdir(exist_ok=True)

        # Copy theme to standard location (overwrite if exists for updates)
        if source_theme.exists():
            if dest_theme.exists():
                shutil.rmtree(dest_theme)
            shutil.copytree(source_theme, dest_theme)
            _LOGGER.info(f"✅ Homio theme copied to {dest_theme}")
            _LOGGER.info("Theme will be available after restart. Select 'Homio' from your profile.")
        else:
            _LOGGER.warning(f"Source theme not found: {source_theme}")

    except Exception as e:
        _LOGGER.error(f"Failed to copy Homio theme: {e}")


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


async def _register_panel(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register the Homio Dashboard panel."""

    integration_dir = Path(__file__).parent
    dashboard_path = integration_dir / "lovelace" / "homio.yaml"

    # Create the Lovelace YAML dashboard
    hass.data["lovelace"]["dashboards"][DOMAIN] = LovelaceYAML(
        hass,
        DOMAIN,
        {
            "mode": "yaml",
            "title": "Homio",
            "icon": "mdi:star-plus-outline",
            "show_in_sidebar": True,
            "filename": str(dashboard_path),
        },
    )

    # Register the panel in the frontend
    await hass.data["lovelace"]["dashboards"][DOMAIN].async_load(False)

    _LOGGER.info(f"Homio Dashboard panel registered successfully")
