---
name: scientific-pdf-dashboard
description: >-
  Standardizes the generation of multi-page scientific reports from JSON metrics. 
  Enforces memory management, aesthetic rules (e.g. percentages over raw counts), 
  and consistent layout architectures using matplotlib PdfPages.
---

# Scientific PDF Dashboard

## Overview
Generates complex, multi-page Matplotlib data visualization reports safely and aesthetically. Scientific pipelines often output massive JSON statistics; this skill dictates how to render them into a dashboard without exhausting system memory.

## Dependencies
- None.

## Quick Start
"Build a 5-page PDF summary dashboard for the spatial tuning batch results."

## Workflow

### 1. File & Data Orchestration
- Read the aggregated statistics from the source JSON.
- Open `matplotlib.backends.backend_pdf.PdfPages` to manage the output stream.

### 2. Aesthetic Standardization
- **Percentages:** Always use percentages (e.g., % of cells tuned) instead of raw counts for general plotting to ensure comparability across uneven sample sizes.
- **Color Palettes:** Avoid plain primary colors. Use carefully curated, harmonious colormaps that differentiate groups effectively.
- **Typography:** Ensure titles and axis labels are readable and professionally scaled.

### 3. Layout Architecture
- **Page 1 (Title / KPI):** Global metrics, total cells, significance thresholds, and top-level categorical breakdowns (e.g., pie charts of classifications).
- **Page 2+ (Distributions):** Histograms and violin/dumbbell plots of continuous metrics (e.g., Spatial Information, Coherence).
- **Final Pages (Examples):** Heatmaps or traces of the top N representative "best" cells to visually anchor the statistics.

### 4. Memory Management (CRITICAL)
- When generating hundreds of subplots across pages, Matplotlib will leak memory if figures are not explicitly closed.
- You MUST wrap figure generation in a strict lifecycle: `fig = plt.figure(...)`, `pdf.savefig(fig)`, `plt.close(fig)`.

## Common Mistakes
- **Memory Leaks:** Calling `plt.savefig` in a loop without `plt.close(fig)`. The process will crash from OOM on large datasets.
- **Raw Counts:** Plotting raw cell counts in histograms across days when the total number of recorded cells differs. Always normalize to percentages or densities.
