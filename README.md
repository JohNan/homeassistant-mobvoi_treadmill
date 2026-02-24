# Mobvoi Treadmill Home Assistant Integration

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]][license]
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)

This is a custom integration for Home Assistant to control and monitor Mobvoi Treadmills via Bluetooth Low Energy (BLE). It uses the [`pymvtreadmill`](https://pypi.org/project/pymvtreadmill/) library.

## Features

The integration provides the following sensors:

*   **Speed:** Current speed in km/h.
*   **Inclination:** Current inclination in %.
*   **Distance:** Distance covered in the current session (meters).
*   **Total Distance:** Total distance covered by the treadmill (meters).
*   **Last Run Distance:** Distance of the last run (meters).

And a binary sensor:

*   **Running:** Indicates if the treadmill is currently running.

## Installation

### HACS (Recommended)

1.  Open HACS in Home Assistant.
2.  Go to **Integrations**.
3.  Click the three dots in the top right corner and select **Custom repositories**.
4.  Add the URL of this repository: `https://github.com/JohNan/homeassistant-mobvoi_treadmill`.
5.  Select **Integration** as the category.
6.  Click **Add**.
7.  Find **Mobvoi Treadmill** in the list and click **Download**.
8.  Restart Home Assistant.

### Manual

1.  Download the latest release.
2.  Extract the `custom_components/mobvoi_treadmill` folder to your Home Assistant `custom_components` directory.
3.  Restart Home Assistant.

## Configuration

This integration supports config flow, meaning it can be configured directly from the Home Assistant UI.

1.  Ensure your Home Assistant host has a working Bluetooth adapter.
2.  Go to **Settings** -> **Devices & Services**.
3.  Click **+ ADD INTEGRATION**.
4.  Search for **Mobvoi Treadmill**.
5.  If your treadmill is powered on and within Bluetooth range, it should be discovered automatically.
    *   The integration looks for Bluetooth devices with names starting with "Mobvoi".
6.  Select your device and click **Submit**.

**Note:** You need a Bluetooth adapter configured in Home Assistant for this integration to work.

## Supported Devices

*   Mobvoi Home Treadmill (and potentially others with Bluetooth names starting with "Mobvoi").

## Credits

This integration is based on the work of the [`pymvtreadmill`](https://pypi.org/project/pymvtreadmill/) library.

[releases]: https://github.com/JohNan/homeassistant-mobvoi_treadmill/releases
[releases-shield]: https://img.shields.io/github/v/release/JohNan/homeassistant-mobvoi_treadmill.svg?style=for-the-badge
[license]: ./LICENSE
[license-shield]: https://img.shields.io/github/license/JohNan/homeassistant-mobvoi_treadmill.svg?style=for-the-badge
