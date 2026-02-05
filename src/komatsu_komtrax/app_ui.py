"""
Komatsu Komtrax Processor UI Components

UI elements for displaying equipment monitoring data from
the Komatsu Komtrax telematics system.
"""

from pydoover import ui


class KomatsuKomtraxUI:
    """UI components for Komatsu Komtrax equipment monitoring."""

    def __init__(self):
        # Equipment Information
        self.equipment_info = ui.Submodule("equipment_info", "Equipment Information")
        self.equipment_id = ui.TextVariable("equipment_id", "Equipment ID")
        self.model = ui.TextVariable("model", "Model")
        self.location = ui.TextVariable("location", "GPS Location")
        self.equipment_info.add_children(self.equipment_id, self.model, self.location)

        # Operating Metrics
        self.metrics = ui.Submodule("operating_metrics", "Operating Metrics")
        self.operating_hours = ui.NumericVariable(
            "operating_hours",
            "Operating Hours",
            precision=1,
            ranges=[
                ui.Range("New", 0, 1000, ui.Colour.green),
                ui.Range("Normal", 1000, 5000, ui.Colour.blue),
                ui.Range("High", 5000, 10000, ui.Colour.orange),
                ui.Range("Service Due", 10000, 50000, ui.Colour.red),
            ],
        )
        self.idle_hours = ui.NumericVariable(
            "idle_hours",
            "Idle Hours",
            precision=1,
            ranges=[
                ui.Range("Low", 0, 500, ui.Colour.green),
                ui.Range("Moderate", 500, 2000, ui.Colour.orange),
                ui.Range("High", 2000, 10000, ui.Colour.red),
            ],
        )
        self.fuel_level = ui.NumericVariable(
            "fuel_level",
            "Fuel Level (%)",
            precision=0,
            ranges=[
                ui.Range("Empty", 0, 10, ui.Colour.red),
                ui.Range("Low", 10, 25, ui.Colour.orange),
                ui.Range("Normal", 25, 75, ui.Colour.green),
                ui.Range("Full", 75, 100, ui.Colour.blue),
            ],
        )
        self.metrics.add_children(self.operating_hours, self.idle_hours, self.fuel_level)

        # Engine Status
        self.engine = ui.Submodule("engine", "Engine Status")
        self.engine_status = ui.TextVariable("engine_status", "Engine State")
        self.active_alerts = ui.TextVariable("active_alerts", "Active Fault Codes")
        self.engine.add_children(self.engine_status, self.active_alerts)

        # Connection Status
        self.connection = ui.Submodule("connection", "Connection")
        self.connection_status = ui.TextVariable("connection_status", "Status")
        self.last_communication = ui.TextVariable("last_communication", "Last Communication")
        self.connection.add_children(self.connection_status, self.last_communication)

    def fetch(self):
        """Return all top-level UI components for registration."""
        return (
            self.equipment_info,
            self.metrics,
            self.engine,
            self.connection,
        )
