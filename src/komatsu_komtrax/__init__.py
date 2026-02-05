from pydoover.docker import run_app

from .application import KomatsuKomtraxApplication
from .app_config import KomatsuKomtraxConfig

def main():
    """
    Run the application.
    """
    run_app(KomatsuKomtraxApplication(config=KomatsuKomtraxConfig()))
