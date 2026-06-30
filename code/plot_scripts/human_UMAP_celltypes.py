from __future__ import annotations

from pathlib import Path
import argparse

import matplotlib.patheffects as patheffects

from common import CELLTYPE_ORDER, CELLTYPE_PALETTE, add_umap_arrows, ordered_present, plt, read_source, save_figure, set_umap_limits


FIGURE_NAME = Path(__file__).stem
ORDER = CELLTYPE_ORDER
MIN_LABEL_CELLS = 1


def plot() -> None:
    source = read_source(FIGURE_NAME, ["UMAP1", "UMAP2", "celltype_major"])
    celltypes = ordered_present(source["celltype_major"], ORDER)
    fig, ax = plt.subplots(figsize=(4, 3))
    for celltype in celltypes:
        sub = source[source["celltype_major"] == celltype]
        ax.scatter(sub["UMAP1"], sub["UMAP2"], s=1, alpha=0.7, c=CELLTYPE_PALETTE[celltype], label=celltype, edgecolors="none", rasterized=True)
    set_umap_limits(ax, source)
    add_umap_arrows(ax)
    for celltype in celltypes:
        sub = source[source["celltype_major"] == celltype]
        if len(sub) < MIN_LABEL_CELLS:
            continue
        ax.text(sub["UMAP1"].median(), sub["UMAP2"].median(), celltype, fontsize=4, fontweight="bold", ha="center", va="center", path_effects=[patheffects.withStroke(linewidth=1.5, foreground="white")])
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=6.5, markerscale=4)
    save_figure(fig, FIGURE_NAME)


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    plot()
