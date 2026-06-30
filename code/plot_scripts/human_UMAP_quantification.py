from __future__ import annotations

from pathlib import Path
import argparse

import numpy as np

from common import CONDITION_PALETTE, DOUBLE_COL, EPITHELIAL_TYPES, CELLTYPE_ORDER, plt, read_source, save_figure


FIGURE_NAME = Path(__file__).stem


def plot() -> None:
    source = read_source(FIGURE_NAME, ["UMAP1", "UMAP2", "condition", "celltype_major", "Ferroptosis_susceptibility"])
    fig = plt.figure(figsize=(DOUBLE_COL * 0.95, 89 / 25.4))
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 0.05], width_ratios=[1, 1, 1.2], hspace=0.25, wspace=0.3)
    ax_hc = fig.add_subplot(gs[0, 0])
    ax_sle = fig.add_subplot(gs[0, 1])
    ax_bar = fig.add_subplot(gs[0, 2])
    ax_cbar = fig.add_subplot(gs[1, :2])

    scores = source["Ferroptosis_susceptibility"]
    vmin = scores.quantile(0.02)
    vmax = scores.quantile(0.98)
    x_range = source["UMAP1"].max() - source["UMAP1"].min()
    y_range = source["UMAP2"].max() - source["UMAP2"].min()
    xlim = (source["UMAP1"].min() - 0.02 * x_range, source["UMAP1"].max() + 0.02 * x_range)
    ylim = (source["UMAP2"].min() - 0.02 * y_range, source["UMAP2"].max() + 0.02 * y_range)

    sc_handle = None
    for ax, condition in [(ax_hc, "HC"), (ax_sle, "SLE")]:
        sub = source[source["condition"] == condition]
        sc_handle = ax.scatter(sub["UMAP1"], sub["UMAP2"], c=sub["Ferroptosis_susceptibility"], cmap="RdBu_r", s=0.2, alpha=0.6, vmin=vmin, vmax=vmax, rasterized=True)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(condition, fontsize=8, fontweight="bold", color=CONDITION_PALETTE[condition])
        ax.set_aspect("equal")
        for spine in ax.spines.values():
            spine.set_visible(False)
    cbar = fig.colorbar(sc_handle, cax=ax_cbar, orientation="horizontal")
    cbar.set_label("Ferroptosis susceptibility", fontsize=6)
    cbar.ax.tick_params(labelsize=5)

    threshold = scores.quantile(0.75)
    celltypes = [ct for ct in CELLTYPE_ORDER if ct in set(source["celltype_major"]) and ct in EPITHELIAL_TYPES]
    x = np.arange(len(celltypes))
    width = 0.35
    values = {}
    for condition in ["HC", "SLE"]:
        out = []
        for celltype in celltypes:
            sub = source[(source["condition"] == condition) & (source["celltype_major"] == celltype)]
            out.append(float((sub["Ferroptosis_susceptibility"] >= threshold).mean() * 100) if len(sub) else 0.0)
        values[condition] = out
    ax_bar.bar(x - width / 2, values["HC"], width, color=CONDITION_PALETTE["HC"], alpha=0.8, label="HC")
    ax_bar.bar(x + width / 2, values["SLE"], width, color=CONDITION_PALETTE["SLE"], alpha=0.8, label="SLE")
    labels = ["EEC" if ct == "Enteroendocrine" else ct for ct in celltypes]
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(labels, rotation=45, ha="right", fontsize=6)
    ax_bar.set_ylabel("Ferroptosis-high (%)", fontsize=7)
    ax_bar.legend(fontsize=5, loc="upper right", frameon=False)
    ax_bar.spines["top"].set_visible(False)
    ax_bar.spines["right"].set_visible(False)
    save_figure(fig, FIGURE_NAME)


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    plot()
