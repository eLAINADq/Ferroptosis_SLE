from __future__ import annotations

from pathlib import Path
import argparse

import numpy as np

from common import DEATH_COLORS, SINGLE_COL, clean_axes, plt, read_source, save_figure, sig_symbol


FIGURE_NAME = Path(__file__).stem


def plot() -> None:
    source = read_source(FIGURE_NAME, ["pathway", "cohens_d", "p_adj"])
    fig, ax = plt.subplots(figsize=(SINGLE_COL * 0.95, SINGLE_COL * 0.55))
    y = np.arange(len(source))
    colors = [DEATH_COLORS[pathway] for pathway in source["pathway"]]
    ax.barh(y, source["cohens_d"], height=0.58, color=colors, alpha=0.85, edgecolor="none")
    ax.axvline(0, color="#888888", lw=0.4)
    ax.set_yticks(y)
    ax.set_yticklabels(source["pathway"], fontsize=6.5)
    ax.set_xlabel("Effect size (Cohen's d)", fontsize=6.5)
    ax.invert_yaxis()
    x_range = float(source["cohens_d"].max() - source["cohens_d"].min()) or 1.0
    pad = x_range * 0.03
    for i, row in source.iterrows():
        star = sig_symbol(float(row["p_adj"]))
        x_val = float(row["cohens_d"])
        ax.text(x_val + pad if x_val >= 0 else x_val - pad, i, star, ha="left" if x_val >= 0 else "right", va="center", fontsize=5.5)
    ax.set_xlim(source["cohens_d"].min() - x_range * 0.15, source["cohens_d"].max() + x_range * 0.12)
    clean_axes(ax)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    save_figure(fig, FIGURE_NAME)


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    plot()
