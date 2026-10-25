#!/usr/bin/env python3
"""Run the command-line interface from a source checkout.

Equivalent to ``python -m hyperliquid_liquidation`` and to the
``hyperliquid-liquidation`` command installed by ``pip install .``.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from hyperliquid_liquidation.main import main  # noqa: E402

if __name__ == "__main__":
    main()
