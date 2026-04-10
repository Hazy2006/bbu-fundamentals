import json
from pathlib import Path

from repository import (
    MemoryRepository,
    TextFileRepository,
    BinaryFileRepository,
)

from services import Service
from ui import UI

if __name__ == "__main__":

    repo = BinaryFileRepository()

    print(f"Using Repository: {repo.__class__.__name__}")

    service = Service(repo)
    ui = UI(service)
    ui.start()
