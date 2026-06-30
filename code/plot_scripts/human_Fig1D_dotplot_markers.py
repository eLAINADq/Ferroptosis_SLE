from __future__ import annotations

from pathlib import Path
import argparse

import matplotlib.gridspec as gridspec
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

from common import CELLTYPE_ORDER, format_count, plt, read_source, save_figure


FIGURE_NAME = Path(__file__).stem


def plot() -> None:
    source = read_source(FIGURE_NAME, ["celltype", "gene", "marker_group", "marker_order", "scaled_mean_expression", "fraction_expressing_pct", "celltype_n"])
    genes = source[["gene", "marker_order"]].drop_duplicates().sort_values("marker_order")["gene"].tolist()
    celltypes = [ct for ct in CELLTYPE_ORDER if ct in set(source["celltype"])]
    x_pos = {gene: i for i, gene in enumerate(genes)}
    y_pos = {celltype: i for i, celltype in enumerate(celltypes)}

    fig = plt.figure(figsize=(9.2, 3.0))
    gs = gridspec.GridSpec(1, 3, width_ratios=[1.0, 0.11, 0.30], left=0.08, right=0.98, bottom=0.20, top=0.78, wspace=0.03)
    ax = fig.add_subplot(gs[0, 0])
    bar_ax = fig.add_subplot(gs[0, 1], sharey=ax)
    leg_ax = fig.add_subplot(gs[0, 2])
    leg_ax.axis("off")

    sizes = source["fraction_expressing_pct"] / 100 * 170 + 8
    ax.scatter(
        source["gene"].map(x_pos),
        source["celltype"].map(y_pos),
        s=sizes,
        c=source["scaled_mean_expression"],
        cmap="Reds",
        vmin=0,
        vmax=1,
        edgecolors="#777777",
        linewidths=0.25,
    )
    ax.set_xticks(range(len(genes)))
    ax.set_xticklabels(genes, rotation=90, fontsize=5.5, fontstyle="italic")
    ax.set_yticks(range(len(celltypes)))
    ax.set_yticklabels(celltypes, fontsize=6)
    ax.set_xlim(-0.8, len(genes) - 0.2)
    ax.set_ylim(len(celltypes) - 0.5, -0.9)
    ax.tick_params(length=0)

    for marker_group, group_df in source[["marker_group", "gene", "marker_order"]].drop_duplicates().groupby("marker_group", sort=False):
        group_genes = group_df.sort_values("marker_order")["gene"].tolist()
        x0 = x_pos[group_genes[0]] - 0.35
        x1 = x_pos[group_genes[-1]] + 0.35
        y = -0.75
        ax.plot([x0, x0, x1, x1], [y + 0.15, y, y, y + 0.15], color="black", lw=0.8, clip_on=False)
        ax.text((x0 + x1) / 2, y - 0.25, marker_group, ha="center", va="bottom", rotation=90, fontsize=6, clip_on=False)

    counts = source[["celltype", "celltype_n"]].drop_duplicates().set_index("celltype").loc[celltypes, "celltype_n"]
    bar_ax.barh(range(len(celltypes)), counts.values, color="#E6E6E6", edgecolor="black", height=0.62)
    bar_ax.set_xlim(0, counts.max() * 1.25)
    bar_ax.set_xticks([])
    bar_ax.tick_params(left=False, labelleft=False)
    for i, value in enumerate(counts.values):
        bar_ax.text(value + counts.max() * 0.06, i, format_count(value), va="center", fontsize=5)
    for spine in bar_ax.spines.values():
        spine.set_visible(False)

    legend_sizes = [20, 40, 60, 80, 100]
    handles = [plt.scatter([], [], s=pct / 100 * 170 + 8, color="#777777", edgecolors="#777777", label=f"{pct}") for pct in legend_sizes]
    leg_ax.legend(handles=handles, title="Fraction of cells\nin group (%)", loc="upper left", frameon=False, scatterpoints=1, ncol=5, fontsize=5, title_fontsize=5, handletextpad=0.2, columnspacing=0.5)

    cax = leg_ax.inset_axes([0.05, 0.02, 0.78, 0.12])
    sm = ScalarMappable(norm=Normalize(vmin=0, vmax=1), cmap="Reds")
    cb = fig.colorbar(sm, cax=cax, orientation="horizontal")
    cb.set_label("Mean expression\nin group", fontsize=5, labelpad=1)
    cb.ax.tick_params(labelsize=5, length=1.5)

    save_figure(fig, FIGURE_NAME)


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    plot()
