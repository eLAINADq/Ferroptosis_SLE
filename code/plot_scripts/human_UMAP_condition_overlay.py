from __future__ import annotations

from pathlib import Path
import argparse

from matplotlib.lines import Line2D

from common import CONDITION_PALETTE, add_umap_arrows, plt, read_source, save_figure, set_umap_limits


FIGURE_NAME = Path(__file__).stem


def plot() -> None:
    source = read_source(FIGURE_NAME, ["UMAP1", "UMAP2", "condition"])
    fig, ax = plt.subplots(figsize=(4, 3))
    rng = source.sample(frac=1, random_state=42)
    colors = rng["condition"].map(CONDITION_PALETTE)
    ax.scatter(rng["UMAP1"], rng["UMAP2"], c=colors, s=1.2, alpha=0.70, linewidths=0, edgecolors="none", rasterized=True)
    set_umap_limits(ax, source)
    add_umap_arrows(ax)
    handles = []
    for condition in ["HC", "SLE"]:
        n_cells = int((source["condition"] == condition).sum())
        handles.append(Line2D([0], [0], marker="o", linestyle="none", markerfacecolor=CONDITION_PALETTE[condition], markeredgecolor="none", markersize=6, label=f"{condition} (n={n_cells:,})"))
    ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False)
    save_figure(fig, FIGURE_NAME)


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    plot()
