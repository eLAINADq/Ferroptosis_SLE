from __future__ import annotations

import os
import tempfile
from pathlib import Path

MPL_CACHE_DIR = Path(tempfile.gettempdir()) / "journal_submission_matplotlib_cache"
MPL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE_DIR))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PACKAGE_ROOT / "source_data"
FIGURE_DIR = PACKAGE_ROOT / "figures"

MM2INCH = 1 / 25.4
SINGLE_COL = 89 * MM2INCH
DOUBLE_COL = 183 * MM2INCH
OUTPUT_DPI = 600

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 7,
        "axes.titlesize": 8,
        "axes.labelsize": 7,
        "xtick.labelsize": 6,
        "ytick.labelsize": 6,
        "legend.fontsize": 6,
        "legend.title_fontsize": 7,
        "axes.linewidth": 0.5,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "xtick.major.size": 2,
        "ytick.major.size": 2,
        "lines.linewidth": 0.75,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.dpi": OUTPUT_DPI,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
        "figure.dpi": 150,
    }
)

CELLTYPE_ORDER = [
    "Stem/TA",
    "Enterocytes",
    "Goblet",
    "Enteroendocrine",
    "Tuft",
    "M cells",
    "CD8+ T cells",
    "CD4+ T cells",
    "T cells (other)",
    "Innate lymphocytes",
    "B cells",
    "Plasma",
    "Myeloid",
    "Stromal",
]

MUSDD_CELLTYPE_ORDER = [
    "Stem/TA",
    "Enterocytes",
    "Goblet",
    "Enteroendocrine",
    "Tuft",
    "CD8+ T cells",
    "CD4+ T cells",
    "B cells",
    "Plasma",
    "Myeloid",
]

EPITHELIAL_TYPES = {"Stem/TA", "Enterocytes", "Goblet", "Enteroendocrine", "Tuft"}

CELLTYPE_PALETTE = {
    "Stem/TA": "#E8A838",
    "Enterocytes": "#D95F02",
    "Goblet": "#66A61E",
    "Enteroendocrine": "#A6761D",
    "Tuft": "#E7298A",
    "M cells": "#BBBBBB",
    "CD8+ T cells": "#1B9E77",
    "CD4+ T cells": "#7570B3",
    "T cells (other)": "#A6CEE3",
    "Innate lymphocytes": "#17BECF",
    "B cells": "#1F78B4",
    "Plasma": "#E31A1C",
    "Myeloid": "#FF7F00",
    "Stromal": "#999999",
}

CONDITION_PALETTE = {"HC": "#4DBBD5", "SLE": "#E64B35"}

DEATH_COLORS = {
    "Apoptosis": "#91D1C2",
    "Necroptosis": "#8491B4",
    "Pyroptosis": "#F39B7F",
    "Ferroptosis": "#E64B35",
}


def read_source(name: str, required: list[str]) -> pd.DataFrame:
    path = DATA_DIR / f"{name}.csv"
    source = pd.read_csv(path)
    missing = [column for column in required if column not in source.columns]
    if missing:
        raise ValueError(f"{path} is missing required columns: {', '.join(missing)}")
    return source


def save_figure(fig: plt.Figure, name: str) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_DIR / f"{name}.png", dpi=OUTPUT_DPI)
    fig.savefig(FIGURE_DIR / f"{name}.pdf", format="pdf")
    plt.close(fig)


def ordered_present(values: pd.Series, order: list[str]) -> list[str]:
    present = set(values.astype(str))
    return [item for item in order if item in present]


def parse_bool(value: object) -> bool:
    text = str(value).strip().lower()
    if text in {"true", "1"}:
        return True
    if text in {"false", "0"}:
        return False
    raise ValueError(f"Cannot parse boolean value: {value}")


def sig_symbol(p_value: float) -> str:
    if p_value < 0.001:
        return "***"
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return ""


def set_umap_limits(ax: plt.Axes, source: pd.DataFrame) -> None:
    xm = (source["UMAP1"].max() - source["UMAP1"].min()) * 0.06
    ym = (source["UMAP2"].max() - source["UMAP2"].min()) * 0.06
    ax.set_xlim(source["UMAP1"].min() - xm, source["UMAP1"].max() + xm)
    ax.set_ylim(source["UMAP2"].min() - ym, source["UMAP2"].max() + ym)
    ax.set_aspect("equal")
    ax.set_frame_on(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")


def add_umap_arrows(ax: plt.Axes) -> None:
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    xr = xlim[1] - xlim[0]
    yr = ylim[1] - ylim[0]
    x0 = xlim[0] + xr * 0.035
    y0 = ylim[0] + yr * 0.035
    dx = xr * 0.10
    dy = yr * 0.10
    ax.annotate("", xy=(x0 + dx, y0), xytext=(x0, y0), arrowprops={"arrowstyle": "-|>", "lw": 0.8, "color": "black"})
    ax.annotate("", xy=(x0, y0 + dy), xytext=(x0, y0), arrowprops={"arrowstyle": "-|>", "lw": 0.8, "color": "black"})
    ax.text(x0 + dx * 0.5, y0 - yr * 0.04, "UMAP1", fontsize=6, ha="center")
    ax.text(x0 - xr * 0.04, y0 + dy * 0.5, "UMAP2", fontsize=6, ha="center", rotation=90)


def clean_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def format_count(value: float) -> str:
    value = int(value)
    if value >= 1000:
        return f"{value / 1000:.1f}k"
    return str(value)
