"""Pytest config — adds the fixture root to sys.path so pytest can find
the app package."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))