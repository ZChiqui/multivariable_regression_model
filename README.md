# Multivariable Regression & Valuation Model

A portfolio‑style data analytics project that estimates Boston residential property values using multivariable linear regression.

## Problem – Solution – Impact
- Problem: Estimate home values from neighborhood, accessibility, environmental, and housing attributes.
- Solution: Prepare the Boston housing dataset, explore distributions and relationships, fit a multivariable regression, evaluate residuals, and refine with a log‑price specification.
- Impact: Support pricing, investment screening, and scenario‑based valuation by adjusting feature inputs (e.g., rooms, highway access, river proximity).

## What’s Inside
- `Multivariable_Regression_and_Valuation_Model_(start) (1).ipynb` – Main notebook with the project narrative and analysis.
- `tools/` – Helper scripts (optional) used to inspect and rewrite notebook text (no impact on modeling):
  - `tools/inspect_nb.py` – Prints a compact summary of notebook cells.
  - `tools/rewrite_notebook.py` – Converts educational prompts to a portfolio narrative (already applied).

## Data
- Input file: `boston.csv` (expected in the project root).
- Target: `PRICE` (median home price). The notebook also creates `REAL = PRICE * 1000` for dollar scaling in visuals.
- Typical features include: `CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, B, LSTAT`.

## Environment Setup
- Python 3.10+ recommended.
- Create a virtual environment and install dependencies:

```
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate # macOS/Linux
pip install -r requirements.txt
```

## Run the Notebook
```
jupyter lab
```
Open `Multivariable_Regression_and_Valuation_Model_(start) (1).ipynb` and run cells top‑to‑bottom. Ensure `boston.csv` is present.

## Modeling Workflow
- Exploration: size/columns checks, missing values/duplicates, descriptive stats, distributions, and pair/joint plots.
- Baseline model: multivariable linear regression; coefficient sanity checks and residual analysis.
- Refinement: log‑transform the target to improve linearity/variance stability; re‑evaluate fit and residuals.
- Validation: compare out‑of‑sample performance to choose the preferred specification.
- Scenario valuation: estimate baseline (average) value and scenario‑based prices by adjusting selected features.

## Extending the Project
- Add cross‑validation and regularization (Ridge/Lasso/ElasticNet).
- Include interaction terms or non‑linear transforms for key predictors.
- Calibrate business‑friendly KPIs (e.g., price deltas per room or per commute distance quartile).

## Notes
- The notebook narrative has been rewritten for a professional portfolio tone without changing the underlying code.
- Plotly is optional for interactive charts; manage versions via your environment if needed.

