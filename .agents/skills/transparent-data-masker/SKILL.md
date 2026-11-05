---
name: transparent-data-masker
description: >-
  Enforces scientific transparency by ensuring any data filtering or masking logic 
  explicitly tracks, calculates, and logs the exact number of frames or rows dropped 
  for each specific exclusion criterion.
---

# Transparent Data Masker

## Overview
In scientific coding, silently dropping NaNs, filtering out artefacts, or applying masks without reporting the exact counts is a major source of irreproducibility. This skill enforces a strict rule for data preprocessing: any time filtering logic is written, it MUST include explicit tracking counters.

## Dependencies
- None.

## Quick Start
"Filter the calcium traces for periods where the mouse is moving and outside the shock zone."

## Workflow

### 1. Identify Exclusion Criteria
- List all independent reasons why data points (e.g., frames, rows, epochs) might be excluded. Example: NaNs, immobility, sensory artefact zone (shock zone), signal-to-noise ratio below threshold.

### 2. Build Independent Masks
- Construct a separate boolean mask for each criterion. Do not merge them into a single step without first having access to the independent boolean arrays.
- Example: `nan_mask`, `movement_mask`, `shock_mask`. Ensure `astype(bool)` is used on numpy arrays to avoid bitwise issues.

### 3. Track Dropped Counts
- Explicitly calculate the number of dropped frames/rows for *each* specific reason and store them as class attributes or log them.
- Example:
  ```python
  frames_dropped_nan = np.sum(nan_mask)
  frames_dropped_immobile = np.sum(~movement_mask)
  frames_dropped_shock = np.sum(shock_mask)
  ```

### 4. Apply Combined Mask
- Combine the masks into a single `valid_mask` and apply it to the data.

### 5. Report Transparency
- Ensure the tracked variables are easily accessible (e.g., saved in the output JSON, printed in the logs, or plotted as a pie chart in summary PDFs) so the user always knows exactly how much data was lost at each step.

## Common Mistakes
- **Silent Dropping**: Using `pandas.dropna()` or indexing `data[valid]` without first calculating and storing `len(data) - len(valid)`.
- **Merged Tracking**: Saying "1500 frames were dropped" without specifying that 1000 were NaNs and 500 were immobility. You must track each criterion independently.
