"""
Komatsu Komtrax Processor Configuration

Defines user-configurable parameters for the Komtrax integration,
including API settings and alert thresholds.
"""

from pathlib import Path

from pydoover import config


class KomatsuKomtraxConfig(config.Schema):
    """Configuration schema for Komatsu Komtrax processor."""

    def __init__(self):
        # API Configuration
        self.api_endpoint = config.String(
            "Komtrax API Endpoint",
            default="https://api.komtrax.komatsu.com/v1",
            description="Base URL for the Komatsu Komtrax API (ISO-15143-3 / AEMP 2.0)",
        )

        self.api_key = config.String(
            "API Key",
            description="Authentication key for the Komtrax API",
        )

        self.equipment_id = config.String(
            "Equipment ID",
            default="",
            description="Optional: Specific equipment ID to monitor. Leave blank for all equipment.",
        )

        # Alert Configuration
        self.fuel_alert_threshold = config.Number(
            "Low Fuel Alert Percent",
            default=20.0,
            description="Alert when fuel level drops below this percentage",
        )

        self.idle_hours_alert = config.Number(
            "Excessive Idle Hours Alert",
            default=100.0,
            description="Alert when idle hours exceed this threshold",
        )


def export():
    """Export the configuration schema to doover_config.json."""
    KomatsuKomtraxConfig().export(
        Path(__file__).parents[2] / "doover_config.json",
        "komatsu_komtrax",
    )


if __name__ == "__main__":
    export()
