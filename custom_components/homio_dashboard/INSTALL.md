# Homio Dashboard Installation - 100% Install & Go!

This integration is installed via HACS and includes ALL dependencies with ZERO configuration.yaml changes required!

## Installation Steps

### 1. Install via HACS

1. Go to HACS → Integrations
2. Click "Custom repositories"
3. Add this repository URL: `https://github.com/clutchthrower/Homio-Dashboard`
4. Select category: **Integration**
5. Search for "Homio Dashboard"
6. Click "Download"
7. **Restart Home Assistant**

### 2. Add the Integration

1. Go to Settings → Devices & Services → Integrations
2. Click "+ ADD INTEGRATION"
3. Search for "Homio Dashboard"
4. Click "Submit"
5. **Restart Home Assistant again**

**That's it!** The integration automatically configures everything:

- ✅ **JavaScript dependencies** (button-card, layout-card-modified, my-slider-v2) - auto-loaded
- ✅ **Homio theme** - auto-copied to `/config/themes/homio/`
- ✅ **Helper packages** - auto-copied to `/config/packages/homio/`
- ✅ **Template sensors** (sensor.homio_current_date, sensor.homio_current_time) - auto-created
- ✅ **Sidebar panel** - auto-registered with icon (⭐+)

**NO configuration.yaml changes needed!**

### 3. Select Homio Theme

1. Click your profile (bottom left)
2. Select "Homio" from the theme dropdown

### 4. Add Room Images

Add your room background images to:
```
custom_components/homio_dashboard/www/images/Homio/rooms/
```

For example: `custom_components/homio_dashboard/www/images/Homio/rooms/lounge.jpg`

The integration already includes 19 icon assets that are automatically available at `/homio_dashboard/images/Homio/icons/`.

### 8. Access the Dashboard

Click the Homio icon (⭐+) in your sidebar to access your dashboard!

## Customization

Edit the dashboard configuration at:
```
custom_components/homio_dashboard/lovelace/homio.yaml
```

Replace example entities with your own entities.

## Support

For issues, visit: https://github.com/iamtherufus/Homio
