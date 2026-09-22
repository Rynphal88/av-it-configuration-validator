"""Generate the Unit 3 architecture blueprint as PNG and SVG."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "design" / "architecture"
OUT.mkdir(parents=True, exist_ok=True)


def box(ax, x, y, w, h, title, detail, fill="#EAF2F8", edge="#1F4E78"):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.012",
        linewidth=1.5, edgecolor=edge, facecolor=fill,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h * 0.64, title, ha="center", va="center",
            fontsize=10, fontweight="bold", color="#111111")
    ax.text(x + w / 2, y + h * 0.30, detail, ha="center", va="center",
            fontsize=7.5, color="#222222", wrap=True)
    return patch


def arrow(ax, start, end, color="#4A4A4A", style="-"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=12,
                                 linewidth=1.4, color=color, linestyle=style,
                                 connectionstyle="arc3,rad=0.0"))


fig, ax = plt.subplots(figsize=(11, 8.5), dpi=220)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

ax.text(0.5, 0.975, "Read Only AV IT Configuration Validation Architecture",
        ha="center", va="top", fontsize=16, fontweight="bold", color="#111111")
ax.text(0.5, 0.945, "ASEL X32 bounded proof of concept",
        ha="center", va="top", fontsize=10, color="#444444")

main_x, main_w, main_h = 0.34, 0.32, 0.092
ys = [0.82, 0.69, 0.56, 0.43, 0.30, 0.17]
labels = [
    ("Local Engineer Interface", "Select candidate file and approved baseline"),
    ("Input Integrity Module", "Type, size, readability and SHA 256 metadata"),
    ("Parser and Normalizer", "Supported path value records only; no execution"),
    ("Comparison and Rule Engine", "Baseline drift plus eight high risk invariants"),
    ("Severity and Explanation", "Rule defined severity with expected and observed evidence"),
    ("Report and Audit Module", "Human readable report, JSON result and audit metadata"),
]
for y, (title, detail) in zip(ys, labels):
    fill = "#E8F4EA" if title == "Report and Audit Module" else "#EAF2F8"
    box(ax, main_x, y, main_w, main_h, title, detail, fill=fill)

for y1, y2 in zip(ys[:-1], ys[1:]):
    arrow(ax, (0.5, y1), (0.5, y2 + main_h))

box(ax, 0.055, 0.47, 0.22, 0.10, "Approved Baseline Store",
    "Restricted, versioned and hash identified", fill="#FFF3CD", edge="#8A6D1D")
box(ax, 0.055, 0.34, 0.22, 0.10, "Versioned Rule Catalog",
    "Rule ID, field and rationale\nSeverity and test oracle", fill="#FFF3CD", edge="#8A6D1D")
arrow(ax, (0.275, 0.52), (main_x, 0.49), color="#8A6D1D")
arrow(ax, (0.275, 0.39), (main_x, 0.47), color="#8A6D1D")

box(ax, 0.725, 0.48, 0.22, 0.12, "Git and Continuous Integration",
    "Source, requirements and design\nTests, branches and traceable commits",
    fill="#F2EAF7", edge="#6F42A1")
arrow(ax, (0.725, 0.53), (0.66, 0.605), color="#6F42A1", style="--")
arrow(ax, (0.725, 0.53), (0.66, 0.215), color="#6F42A1", style="--")

ax.text(0.5, 0.105, "Human review and deployment approval",
        ha="center", va="center", fontsize=10, fontweight="bold", color="#7A1F1F")
arrow(ax, (0.5, 0.17), (0.5, 0.125), color="#7A1F1F")

boundary = FancyBboxPatch((0.10, 0.025), 0.80, 0.045,
                          boxstyle="round,pad=0.006,rounding_size=0.008",
                          linewidth=1.2, edgecolor="#7A1F1F", facecolor="#FCE8E6")
ax.add_patch(boundary)
ax.text(0.5, 0.048,
        "Safety boundary: no live console connection, no file modification and no automatic remediation",
        ha="center", va="center", fontsize=8.7, color="#7A1F1F")

ax.text(0.055, 0.625, "Reference data", fontsize=9, fontweight="bold", color="#5A4A10")
ax.text(0.725, 0.625, "Development governance", fontsize=9, fontweight="bold", color="#5A2C75")

fig.tight_layout(pad=0.5)
fig.savefig(OUT / "system-architecture.png", bbox_inches="tight")
fig.savefig(OUT / "system-architecture.svg", bbox_inches="tight")
plt.close(fig)
