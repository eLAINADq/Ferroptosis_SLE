from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

mpl_cache = Path(tempfile.gettempdir()) / "journal_submission_matplotlib_cache"
mpl_cache.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(mpl_cache))
os.environ.setdefault("MPLBACKEND", "Agg")
