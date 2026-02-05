"""
Komatsu Komtrax Processor Application

This processor integrates with the Komatsu Komtrax telematics API (ISO-15143-3 / AEMP 2.0)
for equipment monitoring. It can:
- Poll the Komtrax API to fetch equipment data
- Receive inbound equipment data via channel messages
- Update device UI with equipment status, location, and operational metrics
- Track equipment health and maintenance alerts
"""

import logging
from datetime import datetime, timezone

import httpx

from pydoover.cloud.processor import ProcessorBase

from .app_ui import KomatsuKomtraxUI

log = logging.getLogger()


class KomatsuKomtraxProcessor(ProcessorBase):
    """Processor for Komatsu Komtrax equipment monitoring integration."""

    def setup(self):
        """Initialize the processor and set up UI components."""
        log.info("Setting up Komatsu Komtrax processor")

        # Initialize UI components
        self.ui = KomatsuKomtraxUI()
        self.ui_manager.add_children(*self.ui.fetch())

        # Get config from deployment
        self.api_endpoint = self.get_agent_config("api_endpoint") or "https://api.komtrax.komatsu.com/v1"
        self.api_key = self.get_agent_config("api_key")
        self.equipment_id = self.get_agent_config("equipment_id")

    def process(self):
        """
        Process incoming messages or scheduled triggers.

        Handles:
        - Equipment data from channel messages
        - Commands (force_sync, clear_alerts)
        - Scheduled API polling
        """
        log.info("Processing Komatsu Komtrax event")

        # Check if we have a message to process
        if self.message is not None:
            data = self.message.data
            log.info(f"Processing message: {data}")

            # Handle different message types
            if isinstance(data, dict):
                # Check if this is a command
                command = data.get("command")
                if command:
                    self._handle_command(command, data)
                else:
                    # Assume it's equipment data
                    self._process_equipment_data(data)
        else:
            # No message - this is likely a scheduled invocation
            # Try to fetch data from the API
            log.info("No message - attempting API fetch")
            if self.api_key:
                self._fetch_and_process_equipment_data()
            else:
                log.warning("API key not configured, cannot fetch data")
                self.ui.connection_status.update("Not Configured")

        # Push UI updates
        self.ui_manager.push()

    def close(self):
        """Clean up resources after processing."""
        log.info("Closing Komatsu Komtrax processor")

    def _handle_command(self, command: str, data: dict):
        """Handle control commands."""
        log.info(f"Handling command: {command}")

        if command == "force_sync":
            if self.api_key:
                self._fetch_and_process_equipment_data()
            else:
                log.warning("Cannot force sync - API key not configured")

        elif command == "clear_alerts":
            log.info("Clearing alerts")
            self.ui.active_alerts.update("None")

        elif command == "update_config":
            # Allow runtime config updates
            if "api_endpoint" in data:
                self.api_endpoint = data["api_endpoint"]
            if "api_key" in data:
                self.api_key = data["api_key"]
            if "equipment_id" in data:
                self.equipment_id = data["equipment_id"]
            log.info("Configuration updated")

    def _fetch_and_process_equipment_data(self):
        """Fetch equipment data from the Komtrax API and process it."""
        try:
            equipment_data = self._fetch_equipment_data()
            if equipment_data:
                self._process_equipment_data(equipment_data)
                self.ui.connection_status.update("Connected")
        except Exception as e:
            log.error(f"Error fetching equipment data: {e}")
            self.ui.connection_status.update("Error")

    def _fetch_equipment_data(self) -> dict | None:
        """
        Fetch equipment data from the Komtrax API.

        Uses ISO-15143-3 (AEMP 2.0) telematics API standard.

        Returns:
            Equipment data dictionary or None on failure
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # Build endpoint URL
        if self.equipment_id:
            url = f"{self.api_endpoint}/equipment/{self.equipment_id}"
        else:
            url = f"{self.api_endpoint}/equipment"

        log.info(f"Fetching equipment data from {url}")

        # Use synchronous httpx for ProcessorBase (non-async)
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            log.error(f"HTTP error from Komtrax API: {e.response.status_code}")
            raise
        except httpx.RequestError as e:
            log.error(f"Request error to Komtrax API: {e}")
            raise

    def _process_equipment_data(self, data: dict):
        """
        Process equipment data and update UI.

        Expected data format (ISO-15143-3 / AEMP 2.0 compatible):
        {
            "equipment_id": "KOM-12345",
            "model": "PC200-8",
            "serial_number": "12345",
            "location": {"latitude": 35.6762, "longitude": 139.6503},
            "operating_hours": 5432.5,
            "idle_hours": 1234.2,
            "fuel_level_percent": 75,
            "engine_status": "running",
            "fault_codes": [],
            "last_communication": "2026-02-05T10:30:00Z"
        }
        """
        log.info(f"Processing equipment data: {data.get('equipment_id', 'unknown')}")

        # Update UI components
        self.ui.equipment_id.update(data.get("equipment_id", "N/A"))
        self.ui.model.update(data.get("model", "N/A"))

        # Location
        location = data.get("location", {})
        if location:
            lat = location.get("latitude", 0)
            lon = location.get("longitude", 0)
            self.ui.location.update(f"{lat:.4f}, {lon:.4f}")

        # Operating metrics
        operating_hours = data.get("operating_hours")
        if operating_hours is not None:
            self.ui.operating_hours.update(operating_hours)

        idle_hours = data.get("idle_hours")
        if idle_hours is not None:
            self.ui.idle_hours.update(idle_hours)

        fuel_level = data.get("fuel_level_percent")
        if fuel_level is not None:
            self.ui.fuel_level.update(fuel_level)

        # Engine status
        engine_status = data.get("engine_status", "unknown")
        self.ui.engine_status.update(engine_status.title())

        # Fault codes / alerts
        fault_codes = data.get("fault_codes", [])
        if fault_codes:
            self.ui.active_alerts.update(", ".join(str(c) for c in fault_codes))
        else:
            self.ui.active_alerts.update("None")

        # Connection status
        last_comm = data.get("last_communication")
        if last_comm:
            self.ui.last_communication.update(last_comm)
            self.ui.connection_status.update("Connected")
        else:
            self.ui.connection_status.update("Unknown")

        log.info(f"UI updated for equipment {data.get('equipment_id', 'unknown')}")
