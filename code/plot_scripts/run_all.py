from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPTS = [
    "human_UMAP_celltypes.py",
    "human_UMAP_condition_overlay.py",
    "human_dotplot_markers.py",
    "human_death_pathways.py",
    "human_pyro_vs_ferro_scatter.py",
    "human_ferroptosis_by_celltype.py",
    "human_UMAP_quantification.py",
    "musDD_UMAP_celltypes.py",
    "musDD_heatmap_markers.py",
    "musDD_UMAP_condition_overlay.py",
    "musDD_death_pathways.py",
    "musDD_ferroptosis_by_celltype.py",
]


def main() -> None:
    here = Path(__file__).resolve().parent
    env = os.environ.copy()
    env.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    mpl_cache = Path(tempfile.gettempdir()) / "journal_submission_matplotlib_cache"
    mpl_cache.mkdir(parents=True, exist_ok=True)
    env.setdefault("MPLCONFIGDIR", str(mpl_cache))
    for script in SCRIPTS:
        subprocess.run([sys.executable, str(here / script)], check=True, env=env)


if __name__ == "__main__":
    main()
