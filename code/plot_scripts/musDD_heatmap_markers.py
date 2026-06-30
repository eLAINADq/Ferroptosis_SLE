from __future__ import annotations

from pathlib import Path
import argparse

import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap

from common import MUSDD_CELLTYPE_ORDER, plt, read_source, save_figure


FIGURE_NAME = Path(__file__).stem


def plot() -> None:
    source = read_source(FIGURE_NAME, ["celltype", "gene", "marker_group", "marker_order", "scaled_mean_expression"])
    genes = source[["gene", "marker_order"]].drop_duplicates().sort_values("marker_order")["gene"].tolist()
    celltypes = [ct for ct in MUSDD_CELLTYPE_ORDER if ct in set(source["celltype"])]
    matrix = source.pivot(index="celltype", columns="gene", values="scaled_mean_expression").loc[celltypes, genes]

    cmap = LinearSegmentedColormap.from_list("warm_soft", ["#F7F7F7", "#FDDBC7", "#F4A582", "#D6604D", "#B2182B"])
    fig_w = 6.2
    fig_h = fig_w * (len(celltypes) / len(genes)) * 1.05
    fig = plt.figure(figsize=(fig_w, fig_h))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 0.025], left=0.15, right=0.90, bottom=0.25, top=0.90, wspace=0.02)
    ax = fig.add_subplot(gs[0, 0])
    cax = fig.add_subplot(gs[0, 1])
    im = ax.imshow(matrix.values, aspect="auto", cmap=cmap, vmin=0, vmax=1, interpolation="nearest")

    marker_groups = source[["gene", "marker_group", "marker_order"]].drop_duplicates().sort_values("marker_order")
    x_pos = 0
    for _, group in marker_groups.groupby("marker_group", sort=False):
        if x_pos > 0:
            ax.axvline(x_pos - 0.5, color="white", lw=0.8)
        x_pos += len(group)

    ax.set_xticks(range(len(genes)))
    ax.set_xticklabels(genes, rotation=45, ha="right", fontsize=6, fontstyle="italic")
    ax.set_yticks(range(len(celltypes)))
    ax.set_yticklabels(celltypes, fontsize=6.5)
    ax.tick_params(axis="both", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    cb = fig.colorbar(im, cax=cax)
    cb.set_label("Scaled mean\nexpression", fontsize=5.5, labelpad=4)
    cb.set_ticks([0, 0.5, 1])
    cb.ax.tick_params(labelsize=5, length=1.5, width=0.3)
    cb.outline.set_linewidth(0.3)
    save_figure(fig, FIGURE_NAME)


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    plot()
