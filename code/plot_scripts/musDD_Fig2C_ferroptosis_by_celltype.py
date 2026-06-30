from __future__ import annotations

from pathlib import Path
import argparse

import numpy as np

from common import SINGLE_COL, clean_axes, parse_bool, plt, read_source, save_figure, sig_symbol


FIGURE_NAME = Path(__file__).stem


def plot() -> None:
    source = read_source(FIGURE_NAME, ["celltype", "cohens_d", "is_epithelial", "p_adj"])
    fig, ax = plt.subplots(figsize=(SINGLE_COL * 0.95, SINGLE_COL * 0.65))
    y = np.arange(len(source))
    colors = ["#E64B35" if parse_bool(v) else "#4DBBD5" for v in source["is_epithelial"]]
    ax.barh(y, source["cohens_d"], color=colors, alpha=0.85, edgecolor="none", height=0.6)
    ax.axvline(0, color="#888888", lw=0.4)
    ax.set_yticks(y)
    ax.set_yticklabels(source["celltype"], fontsize=6)
    ax.set_xlabel("Effect size (Cohen's d)\nFerroptosis susceptibility, SLE vs HC", fontsize=6)
    ax.invert_yaxis()
    x_range = float(source["cohens_d"].max() - source["cohens_d"].min()) or 1.0
    pad = x_range * 0.03
    for i, row in source.iterrows():
        star = sig_symbol(float(row["p_adj"]))
        if not star:
            continue
        x_val = float(row["cohens_d"])
        ax.text(x_val + pad if x_val >= 0 else x_val - pad, i, star, fontsize=5.5, ha="left" if x_val >= 0 else "right", va="center")
    ax.set_xlim(source["cohens_d"].min() - x_range * 0.12, source["cohens_d"].max() + x_range * 0.12)
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor="#E64B35", edgecolor="none", label="Epithelial"),
        plt.Rectangle((0, 0), 1, 1, facecolor="#4DBBD5", edgecolor="none", label="Immune"),
    ]
    ax.legend(handles=legend_handles, loc="lower left", fontsize=5, frameon=False)
    clean_axes(ax)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    save_figure(fig, FIGURE_NAME)


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    plot()
