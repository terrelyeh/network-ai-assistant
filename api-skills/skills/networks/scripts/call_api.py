#!/usr/bin/env python3
"""Delegates to shared call_api implementation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))
from _shared.manage_system.call_api import main  # noqa: E402

if __name__ == "__main__":
    main()
