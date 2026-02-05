"""
Komatsu Komtrax Processor

Lambda handler entry point for the Komatsu Komtrax equipment monitoring processor.
"""

from .application import KomatsuKomtraxProcessor


def handler(event, context):
    """Lambda handler entry point for Komatsu Komtrax processor."""
    processor = KomatsuKomtraxProcessor(**event)
    processor.execute()
