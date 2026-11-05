---
name: statistical-batch-orchestrator
description: >-
  Standardizes how single-cell/single-trial analytical engines are scaled to 
  population levels. Enforces parallelization, generalized null-distribution 
  shuffling, multiple-comparisons correction (e.g. FDR), and discrete 
  categorical classification.
---

# Statistical Batch Orchestrator

## Overview
Moving from a single-cell or single-trial metric to a population-level analysis requires strict statistical rigor. This skill provides an instruction template for wrapping single-iteration logic into a scalable, statistically sound batch processor.

## Dependencies
- None.

## Quick Start
"Wrap the spatial tuning engine to process all cells, apply FDR correction on the shuffles, and classify them."

## Workflow

### 1. Parallelization
- Never loop over cells sequentially if they are computationally heavy. Utilize `joblib.Parallel` or Python's `multiprocessing` to distribute the single-cell engine calls.

### 2. Generalized Null Distributions (Shuffling)
- Do NOT assume a standard Gaussian null. 
- Implement an appropriate generalized shuffling protocol based on the biological data (e.g., Circular Shifts for continuous time series, Block Bootstrapping for temporal correlations, or label permutations).
- Return an empirical p-value for each unit/cell compared against its own null distribution.

### 3. Multiple-Comparisons Correction
- When testing multiple units (e.g., 200 cells), the false positive rate inflates. 
- You MUST aggregate all naive empirical p-values and apply a multiple comparisons correction. 
- Use Benjamini-Hochberg FDR (q-values) as the default for exploratory populations, or Bonferroni for highly strict criteria.

### 4. Categorical Output Assignment
- Define strict thresholds (e.g., `q < 0.05`).
- Output a discrete classification for each unit (e.g., "Tuned" vs "Untuned", or "Room-Tuned" vs "Arena-Tuned" vs "Conjunctive").
- Append these classifications alongside the q-values into a structured JSON/dictionary output for downstream plotting.

## Common Mistakes
- **Applying thresholds to Naive P-values**: Never classify a population of cells based on uncorrected p-values. Always aggregate and correct them first.
- **Breaking temporal structure in shuffles**: Shuffling time series data points independently destroys autocorrelation. Always use Circular Shifts or Block Bootstraps for biological time series.
