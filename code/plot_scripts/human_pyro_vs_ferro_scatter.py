from __future__ import annotations

from pathlib import Path
import argparse

from matplotlib.lines import Line2D

from common import CELLTYPE_PALETTE, DOUBLE_COL, parse_bool, plt, read_source, save_figure


FIGURE_NAME = Path(__file__).stem


def plot() -> None:
    source = read_source(FIGURE_NAME, ["celltype", "pyro_d", "ferro_d", "is_epi"])
    fig, ax = plt.subplots(figsize=(DOUBLE_COL * 0.45, DOUBLE_COL * 0.42))
    for _, row in source.iterrows():
        is_epi = parse_bool(row["is_epi"])
        marker = "s" if is_epi else "o"
        color = CELLTYPE_PALETTE.get(row["celltype"], "#666666")
        ax.scatter(row["pyro_d"], row["ferro_d"], c=color, marker=marker, s=28, edgecolor="white", linewidth=0.4)
        ax.text(row["pyro_d"] + 0.015, row["ferro_d"] + 0.015, row["celltype"], fontsize=5)
    ax.axhline(0, color="#888888", lw=0.4)
    ax.axvline(0, color="#888888", lw=0.4)
    ax.set_xlabel("Cohen's d (Pyroptosis)", fontsize=7)
    ax.set_ylabel("Cohen's d (Ferroptosis)", fontsize=7)
    handles = [
        Line2D([0], [0], marker="s", color="w", markerfacecolor="#777777", markersize=5, label="Epithelial"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#777777", markersize=5, label="Immune"),
    ]
    ax.legend(handles=handles, frameon=False, fontsize=5, loc="lower right")
    save_figure(fig, FIGURE_NAME)


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    plot()
