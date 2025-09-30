import json
import re
import sys
from pathlib import Path

def clean_emojis(text: str) -> str:
    # Remove common emojis used in the notebook to keep tone professional
    return re.sub(r"[\U0001F300-\U0001FAFF]", "", text)

def strip_challenge(text: str) -> str:
    # Remove "Challenge" prompts and convert to brief narrative
    text = re.sub(r"\*\*?Challenge\*\*?:?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"(?i)challenge\s*[:]?", "", text)
    return text

def replace_headings(src: str) -> str:
    low = src.lower()
    def has_heading(keyword: str) -> bool:
        return re.search(r"^\s*#+\s*" + re.escape(keyword) + r"\b", src, flags=re.I | re.M) is not None
    # Targeted section rewrites
    if "### introduction" in low or "# setup and context" in low:
        return (
            "## Project Overview\n\n"
            "- Problem: Estimate residential property values in Boston using neighborhood, accessibility, and housing features.\n"
            "- Solution: Build a multivariable regression model, prepare features, evaluate fit, and iterate with transformations.\n"
            "- Impact: Support pricing, investment screening, and scenario analysis for real estate decisions.\n"
        )
    if "upgrade plotly" in low or "google colab" in low:
        return (
            "## Environment Note\n\n"
            "This project uses Plotly for interactive visuals. Manage package versions with your environment manager (e.g., pip)."
        )
    if "import statements" in low:
        return "## Dependencies\n\nImport core libraries used for data preparation, modeling, and visualization."
    if "notebook presentation" in low:
        return "## Display Settings\n\nTweak display precision for cleaner tables and summaries."
    if "load the data" in low:
        return (
            "## Load Data\n\n"
            "Load the Boston housing dataset from CSV. The first column contains row indices and is used as the index."
        )
    if "understand the boston house price dataset" in low or "dataset" in low and "characteristics" in low:
        return (
            "## Dataset Overview\n\n"
            "The dataset captures neighborhood metrics (e.g., crime rate, industry share), accessibility (highway access, river proximity), \n"
            "environmental factors (nitric oxides), and housing attributes (rooms, age, student–teacher ratio). The target is median home price."
        )
    if "preliminary data exploration" in low:
        return (
            "## Initial Exploration\n\n"
            "We profile the dataset: size, columns, and basic integrity checks (missing values, duplicates) to ensure reliable modeling."
        )
    if "descriptive statistics" in low:
        return (
            "## Descriptive Statistics\n\n"
            "Summarize key indicators that influence valuation (e.g., student–teacher ratio, rooms, price levels, river proximity)."
        )
    if "visualise the features" in low or "visualize the features" in low:
        return (
            "## Feature Distributions\n\n"
            "Explore distributions to spot skew, outliers, and modality. This informs transformations and model expectations."
        )
    if "house prices" in low:
        return (
            "### Target Variable: Price\n\n"
            "We review price distribution to understand scale and potential skew before modeling."
        )
    if "distance to employment" in low:
        return (
            "### Commute Distance (DIS)\n\n"
            "Shorter commutes often correlate with higher demand. Visualizing DIS helps gauge its distribution."
        )
    if "number of rooms" in low:
        return (
            "### Rooms (RM)\n\n"
            "Room count is a core driver of value. We inspect its distribution for range and spread."
        )
    if "access to highways" in low:
        return (
            "### Highway Access (RAD)\n\n"
            "Access can affect desirability and price; we assess its distribution."
        )
    if "next to the river" in low or "river" in low and "chas" in low:
        return (
            "### Proximity to the Charles River (CHAS)\n\n"
            "We compare counts by river proximity to see whether location near the river is common or rare."
        )
    if "understand the relationships" in low:
        return (
            "## Relationships Between Features\n\n"
            "We examine feature interactions to anticipate multicollinearity and non-linear effects."
        )
    if "run a pair plot" in low:
        return (
            "### Pair Plot\n\n"
            "Pairwise charts reveal linear trends, clusters, and potential interactions across predictors and the target."
        )
    if "jointplot" in low:
        return (
            "### Joint Plots for Key Pairs\n\n"
            "We zoom into selected relationships (e.g., DIS–NOX, INDUS–NOX, LSTAT–RM, LSTAT–PRICE, RM–PRICE) to inspect form and spread."
        )
    if "analyse the estimated values" in low or "analyze the estimated values" in low:
        return (
            "### Predicted Values and Residuals\n\n"
            "We evaluate model fit beyond R² by inspecting residuals for randomness, mean near zero, and low skew."
        )
    if "data transformations" in low:
        return (
            "### Log Transformation to Improve Fit\n\n"
            "If residuals show skew or heteroscedasticity, we apply a log transform to stabilize variance and improve linearity."
        )
    if "how does the log transformation work" in low:
        return (
            "#### Effect of Log Transformation\n\n"
            "Log compresses large values more than small ones, often producing a more symmetric distribution helpful for linear models."
        )
    if "regression using log prices" in low:
        return (
            "## Regression with Log Prices\n\n"
            "Refit using log-transformed prices, then compare fit and diagnostics to the original specification."
        )
    if "evaluating coefficients" in low or "coefficients" in low and "log prices" in low:
        return (
            "## Interpreting Coefficients (Log Prices)\n\n"
            "We examine coefficient signs and magnitudes to confirm expectations (e.g., RM positive, NOX negative) and interpret practical effects."
        )
    if "residual plots" in low:
        return (
            "## Residual Comparisons\n\n"
            "Compare residual patterns for linear vs. log-price models to assess improvements in symmetry and variance."
        )
    if "out of sample performance" in low or "compare out of sample" in low:
        return (
            "## Out-of-Sample Performance\n\n"
            "We compare R² (or other metrics) on the test set to validate generalization and choose the stronger model."
        )
    if "predict a property's value" in low or "predict a property" in low:
        return (
            "## Scenario-Based Valuation\n\n"
            "Using the fitted model, we estimate value for baseline (average) features and explore alternative scenarios by adjusting inputs."
        )
    if has_heading("Multivariable Regression"):
        return (
            "# Multivariable Regression\n\n"
            "We fit a linear model with multiple predictors to quantify how each feature contributes to property value."
        )
    if has_heading("Run Your First Regression"):
        return (
            "### Fit the Baseline Model\n\n"
            "Train a linear regression on the training set and review in-sample performance (e.g., R²)."
        )
    if has_heading("Evaluate the Coefficients"):
        return (
            "### Coefficient Sanity Check\n\n"
            "Confirm coefficient signs align with expectations (e.g., RM positive, NOX negative) and inspect magnitudes."
        )
    if "predict how much the average property" in low:
        return (
            "We estimate the value for an average property and convert log predictions back to dollar values for interpretation."
        )
    if "keeping the average values" in low and "value a property" in low:
        return (
            "We create a scenario by adjusting selected features while keeping others at their average to illustrate valuation impact."
        )
    return src

def rewrite_markdown(src: str) -> str:
    src = clean_emojis(src)
    src = replace_headings(src)
    src = strip_challenge(src)
    # Remove explicit course/university mentions
    src = re.sub(r"(?i)assignment|exercise|course|university", "", src)
    # Light touch: transitions are integrated into headings above where helpful
    # Clean up extra spaces/newlines
    src = re.sub(r"\n{3,}", "\n\n", src).strip() + "\n"
    return src

def rewrite_code(lines):
    out = []
    for line in lines:
        l = line
        if l.lstrip().startswith('#'):
            txt = l.strip()
            txt = re.sub(r"^#\s*TODO:.*", "# Import core libraries for analysis and modeling", txt)
            txt = re.sub(r"^#\s*Solution\b.*", "# Reference implementation for this step", txt)
            txt = re.sub(r"^#\s*Define Property Characteristics.*", "# Define property features for valuation", txt)
            txt = re.sub(r"^#\s*Set Property Characteristics.*", "# Set property features for the scenario", txt)
            txt = re.sub(r"^#\s*Make prediction.*", "# Generate prediction", txt)
            txt = re.sub(r"^#\s*Convert Log Prices.*", "# Convert log price back to dollar value", txt)
            txt = re.sub(r"^#\s*How close the property is to the river.*", "# CHAS indicates proximity to the Charles River (1=near, 0=far)", txt)
            # Remove course-like words in comments
            txt = re.sub(r"(?i)assignment|exercise|course|university", "", txt)
            l = ("# " + txt.lstrip('#').lstrip()).rstrip() + ("\n" if not txt.endswith("\n") else "")
        out.append(l)
    return out

def main(nb_path: Path):
    nb = json.loads(nb_path.read_text(encoding='utf-8'))
    changed = False
    # First pass: cell-level rewrites
    for cell in nb.get('cells', []):
        ctype = cell.get('cell_type')
        if ctype == 'markdown':
            src = ''.join(cell.get('source', []))
            new_src = rewrite_markdown(src)
            if new_src != src:
                cell['source'] = [new_src]
                changed = True
        elif ctype == 'code':
            src_lines = cell.get('source', [])
            new_lines = rewrite_code(src_lines)
            if new_lines != src_lines:
                cell['source'] = new_lines
                changed = True
    # Second pass: global cleanups (dedupe headings)
    mv_indices = []
    for i, cell in enumerate(nb.get('cells', [])):
        if cell.get('cell_type') == 'markdown':
            text = ''.join(cell.get('source', []))
            if re.search(r"^\s*#\s*Multivariable Regression\b", text, flags=re.I | re.M):
                mv_indices.append(i)
    if len(mv_indices) > 1:
        # Change the earliest to Project Overview to avoid duplicate main headers
        i0 = mv_indices[0]
        overview = (
            "## Project Overview\n\n"
            "- Problem: Estimate residential property values in Boston using neighborhood, accessibility, and housing features.\n"
            "- Solution: Build a multivariable regression model, prepare features, evaluate fit, and iterate with transformations.\n"
            "- Impact: Support pricing, investment screening, and scenario analysis for real estate decisions.\n"
        )
        if ''.join(nb['cells'][i0].get('source', [])) != overview:
            nb['cells'][i0]['source'] = [overview]
            changed = True
    # If the first two cells are both project overviews, convert the second to a concise model overview
    cells = nb.get('cells', [])
    if len(cells) >= 2:
        def cell_text(i):
            return ''.join(cells[i].get('source', [])) if cells[i].get('cell_type') == 'markdown' else ''
        if re.search(r"^\s*##\s*Project Overview\b", cell_text(0)) and re.search(r"^\s*##\s*Project Overview\b", cell_text(1)):
            model_overview = (
                "## Model Overview\n\n"
                "We fit a multivariable linear regression to quantify how features (rooms, accessibility, environment, neighborhood) relate to property prices, and use it for pricing and scenario analysis.\n"
            )
            if cell_text(1) != model_overview:
                cells[1]['source'] = [model_overview]
                changed = True
    # Minor cleanup: collapse duplicated phrasing
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'markdown':
            text = ''.join(cell.get('source', []))
            text2 = re.sub(r"Next, we profile[^.]*\.\s+We profile", "We profile", text)
            text2 = re.sub(r"Next, we examine[^.]*\.\s+We examine", "We examine", text2)
            text2 = re.sub(r"Next, we [^.]*\.\s+Next, we [^.]*\.", "We examine feature interactions to anticipate multicollinearity and non-linear effects.", text2)
            text2 = re.sub(r"Next, we refit[^.]*\.\s+We refit", "We refit", text2)
            if text2 != text:
                cell['source'] = [text2]
                changed = True
    if changed:
        nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f"Updated: {nb_path}")
    else:
        print("No changes detected")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python tools/rewrite_notebook.py <notebook.ipynb>")
        sys.exit(1)
    main(Path(sys.argv[1]))
