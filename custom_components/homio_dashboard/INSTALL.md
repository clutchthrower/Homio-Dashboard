# Homio Dashboard Installation

This integration is installed via HACS and includes ALL dependencies!

## Post-Installation Configuration

After installing the integration and adding it via the Integrations page, you need to configure a few things in your Home Assistant:

### 1. Enable Packages (for helpers)

Add to your `configuration.yaml`:

```yaml
homeassistant:
  packages: !include_dir_named custom_components/homio_dashboard/packages
```

### 2. Load Homio Theme

Add to your `configuration.yaml`:

```yaml
frontend:
  themes: !include_dir_merge_named custom_components/homio_dashboard/themes
```

### 3. Add Template Sensors

Add to your `configuration.yaml`:

```yaml
template: !include custom_components/homio_dashboard/sensors.yaml
```

### 4. Restart Home Assistant

All JavaScript resources are automatically loaded by the integration:
- ✅ button-card (bundled)
- ✅ layout-card-modified (bundled)
- ✅ my-slider-v2 (bundled)

No external HACS installations needed!

### 5. Restart Again

After making configuration changes, restart Home Assistant.

### 6. Select Homio Theme

1. Click your profile (bottom left)
2. Select "Homio" from the theme dropdown

### 7. Add Room Images

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
