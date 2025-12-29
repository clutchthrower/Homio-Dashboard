# Homio Dashboard - 100% Install & Go!

## Quick Start

Homio Dashboard is a **complete Home Assistant custom integration** - a clean, minimal, YAML-based dashboard built with tablets in mind. Install via HACS, add the integration, and it's **ready to use with ZERO configuration.yaml changes!**

## What's Included & Auto-Configured

This integration bundles EVERYTHING and configures it automatically:

- ✅ button-card v7.0.1 (auto-loaded)
- ✅ Modified layout-card with extra CSS properties (auto-loaded)
- ✅ my-slider-v2 for light brightness control (auto-loaded)
- ✅ All Homio icon assets (19 SVG files included)
- ✅ Dashboard templates and themes (auto-copied to `/config/themes/homio/`)
- ✅ Helper configurations (auto-copied to `/config/packages/homio/`)
- ✅ Template sensors (auto-created programmatically)
- ✅ Sidebar panel (auto-created)

**ZERO external dependencies! ZERO configuration.yaml changes! Everything is bundled and auto-configured!**

## Installation Steps

### 1. Install via HACS

- Go to HACS → Integrations
- Click "Custom repositories"
- Add this repository URL: `https://github.com/clutchthrower/Homio-Dashboard`
- Select category: **Integration**
- Search for "Homio Dashboard"
- Click "Download"
- **Restart Home Assistant**

### 2. Add the Integration

- Go to Settings → Devices & Services → Integrations
- Click "+ ADD INTEGRATION"
- Search for "Homio Dashboard"
- Click "Submit"
- **Restart Home Assistant again**

### 3. Select Homio Theme

- Click your profile (bottom left)
- Select "Homio" from the theme dropdown
- **The Homio icon (⭐+) is now in your sidebar!**

### 4. Add Your Room Images

Add your room background images to:
```
custom_components/homio_dashboard/www/images/Homio/rooms/
```

Add .jpg files matching your room names (e.g., `lounge.jpg`, `bedroom.jpg`)

### 5. Customize Your Dashboard

Edit entities in:
```
custom_components/homio_dashboard/lovelace/homio.yaml
```

Replace example entities (sensor.living_room_temperature, light.hue_living_room_lamp, etc.) with your own.

## Features

- **Auto-loaded Resources**: JavaScript dependencies load automatically, no manual resource configuration needed
- **Single Install**: No need to manually copy files to www/ folder
- **Bundled Icons**: 19 Google Material icons included
- **Sidebar Integration**: Dashboard appears automatically in sidebar
- **Theme Included**: Homio theme bundled
- **Helpers Included**: All required input_boolean and input_number helpers

## Customization

- **Navigation Links**: Edit `custom_components/homio_dashboard/dashboards/templates/includes/homio_navigation_list.yaml`
- **Room Cards**: Customize in `custom_components/homio_dashboard/lovelace/homio.yaml`
- **Additional Icons**: Add SVG files to `custom_components/homio_dashboard/www/images/Homio/icons/`

## Support

For full documentation, examples, and support, visit the [GitHub repository](https://github.com/iamtherufus/Homio).
