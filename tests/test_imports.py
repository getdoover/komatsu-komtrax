"""
Basic tests for an application.

This ensures all modules are importable and that the config is valid.
"""

def test_import_app():
    from komatsu_komtrax.application import KomatsuKomtraxApplication
    assert KomatsuKomtraxApplication

def test_config():
    from komatsu_komtrax.app_config import KomatsuKomtraxConfig

    config = KomatsuKomtraxConfig()
    assert isinstance(config.to_dict(), dict)

def test_ui():
    from komatsu_komtrax.app_ui import KomatsuKomtraxUI
    assert KomatsuKomtraxUI

def test_state():
    from komatsu_komtrax.app_state import KomatsuKomtraxState
    assert KomatsuKomtraxState