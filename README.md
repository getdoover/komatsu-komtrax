# Komatsu Komtrax

<img src="https://companieslogo.com/img/orig/6301.T-2d727627.png?t=1720244490&download=true" alt="App Icon" style="max-width: 100px;">

**Integrates with Komatsu Komtrax API for equipment monitoring**

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/getdoover/komatsu-komtrax)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/getdoover/komatsu-komtrax/blob/main/LICENSE)

[Getting Started](#getting-started) | [Configuration](#configuration) | [Developer](https://github.com/getdoover/komatsu-komtrax/blob/main/DEVELOPMENT.md) | [Need Help?](#need-help)

<br/>

## Overview

The Komatsu Komtrax processor provides seamless integration with Komatsu's Komtrax telematics system, enabling real-time monitoring of construction and mining equipment. This processor connects to the Komatsu Komtrax API (ISO-15143-3 / AEMP 2.0 standard) to fetch equipment data including location, operating hours, fuel levels, and engine status.

With this integration, fleet managers can monitor their Komatsu equipment directly within the Doover platform, receiving consolidated views of equipment health and operational metrics. The processor automatically polls the Komtrax API and updates the device UI with the latest equipment information.

The processor also supports configurable alert thresholds for low fuel and excessive idle hours, helping operators identify equipment that needs attention. All equipment data is displayed through an intuitive UI with color-coded status indicators for quick visual assessment.

### Features

- Real-time equipment monitoring via Komtrax API integration
- ISO-15143-3 / AEMP 2.0 telematics standard compliance
- GPS location tracking for equipment
- Operating hours and idle hours monitoring with color-coded ranges
- Fuel level monitoring with low fuel alerts
- Engine status and fault code display
- Configurable alert thresholds
- Support for monitoring single or multiple equipment units
- Command support for force sync and alert clearing

<br/>

## Getting Started

### Prerequisites

1. **Komatsu Komtrax Account** - You need an active Komtrax account with API access enabled
2. **API Key** - Obtain an API key from your Komatsu dealer or Komtrax portal
3. **Equipment Registration** - Your equipment must be registered in the Komtrax system

### Installation

1. Add the Komatsu Komtrax processor to your Doover deployment
2. Configure the API key and endpoint in the processor settings
3. Optionally specify a specific equipment ID to monitor

### Quick Start

1. Navigate to your Doover deployment settings
2. Add the Komatsu Komtrax processor
3. Enter your Komtrax API key in the configuration
4. Save and deploy - the processor will automatically start fetching equipment data

<br/>

## Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| **Komtrax API Endpoint** | Base URL for the Komatsu Komtrax API (ISO-15143-3 / AEMP 2.0) | `https://api.komtrax.komatsu.com/v1` |
| **API Key** | Authentication key for the Komtrax API | *Required* |
| **Equipment ID** | Optional: Specific equipment ID to monitor. Leave blank for all equipment. | *(empty)* |
| **Low Fuel Alert Percent** | Alert when fuel level drops below this percentage | `20.0` |
| **Excessive Idle Hours Alert** | Alert when idle hours exceed this threshold | `100.0` |

### Example Configuration

```json
{
  "komtrax_api_endpoint": "https://api.komtrax.komatsu.com/v1",
  "api_key": "your-api-key-here",
  "equipment_id": "KOM-12345",
  "low_fuel_alert_percent": 20.0,
  "excessive_idle_hours_alert": 100.0
}
```

<br/>

## UI Elements

This processor provides the following UI elements organized into four sections:

### Equipment Information

| Element | Description |
|---------|-------------|
| **Equipment ID** | The unique identifier for the monitored equipment |
| **Model** | The Komatsu equipment model (e.g., PC200-8) |
| **GPS Location** | Current latitude and longitude coordinates |

### Operating Metrics

| Element | Description | Ranges |
|---------|-------------|--------|
| **Operating Hours** | Total engine operating hours | New (0-1000, green), Normal (1000-5000, blue), High (5000-10000, orange), Service Due (10000+, red) |
| **Idle Hours** | Total engine idle hours | Low (0-500, green), Moderate (500-2000, orange), High (2000+, red) |
| **Fuel Level (%)** | Current fuel tank level percentage | Empty (0-10, red), Low (10-25, orange), Normal (25-75, green), Full (75-100, blue) |

### Engine Status

| Element | Description |
|---------|-------------|
| **Engine State** | Current engine status (Running, Idle, Off, etc.) |
| **Active Fault Codes** | Any active diagnostic trouble codes or "None" |

### Connection

| Element | Description |
|---------|-------------|
| **Status** | Connection status (Connected, Error, Not Configured, Unknown) |
| **Last Communication** | Timestamp of the last successful data update |

<br/>

## How It Works

1. **Initialization** - When the processor starts, it initializes UI components and loads configuration including API endpoint, API key, and equipment ID from the deployment settings.

2. **Scheduled Polling** - On scheduled triggers (when no message is present), the processor calls the Komtrax API to fetch the latest equipment data using Bearer token authentication.

3. **Data Processing** - Equipment data received from the API or via channel messages is parsed according to the ISO-15143-3 / AEMP 2.0 format, extracting location, operating metrics, and status information.

4. **UI Update** - The processor updates all UI components with the latest values, including color-coded ranges for operating hours, idle hours, and fuel levels.

5. **Alert Monitoring** - Fault codes from the equipment are displayed in the Active Fault Codes field, allowing operators to quickly identify issues.

6. **Command Handling** - The processor responds to commands including `force_sync` (immediate API fetch), `clear_alerts` (clear displayed alerts), and `update_config` (runtime configuration changes).

<br/>

## Integrations

This processor works with:

- **Komatsu Komtrax** - Primary telematics data source via ISO-15143-3 / AEMP 2.0 API
- **Doover Platform** - Displays equipment data through the Doover UI framework
- **Doover Channels** - Receives equipment data and commands via channel messages
- **Doover Scheduling** - Supports scheduled triggers for periodic API polling

<br/>

## Need Help?

- Email: support@doover.com
- [Doover Documentation](https://docs.doover.com)
- [App Developer Documentation](https://github.com/getdoover/komatsu-komtrax/blob/main/DEVELOPMENT.md)

<br/>

## Version History

### v0.1.0 (Current)
- Initial release
- Komatsu Komtrax API integration (ISO-15143-3 / AEMP 2.0)
- Real-time equipment monitoring
- GPS location tracking
- Operating hours and idle hours monitoring
- Fuel level monitoring with configurable alerts
- Engine status and fault code display
- Command support (force_sync, clear_alerts, update_config)

<br/>

## License

This app is licensed under the [Apache License 2.0](https://github.com/getdoover/komatsu-komtrax/blob/main/LICENSE).
