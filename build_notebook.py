"""Build a self-contained, executed notebook using only the standard library."""

import ast
import base64
import contextlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
source = (ROOT / "solutions.py").read_text(encoding="utf-8")
lines = source.splitlines(keepends=True)
tree = ast.parse(source)
functions = {node.name: "".join(lines[node.lineno - 1:node.end_lineno])
             for node in tree.body if isinstance(node, ast.FunctionDef)}
setup = source[:source.index("def exercise_0")]
setup = setup.replace("Path(__file__).resolve().parent", "Path.cwd()")

cells = []
results = []
namespace = {"__name__": "__notebook__"}


def markdown(text):
    cells.append({"cell_type": "markdown", "metadata": {},
                  "source": text.splitlines(keepends=True)})


def code(text, figures=()):
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        exec(compile(text, "<notebook>", "exec"), namespace)
    stdout = capture.getvalue()
    results.append(stdout)
    outputs = []
    if stdout:
        outputs.append({"output_type": "stream", "name": "stdout",
                        "text": stdout.splitlines(keepends=True)})
    for filename in figures:
        data = base64.b64encode((ROOT / "outputs" / filename).read_bytes()).decode("ascii")
        outputs.append({"output_type": "display_data", "metadata": {},
                        "data": {"image/png": data,
                                 "text/plain": [f"Saved chart: {filename}"]}})
    cells.append({"cell_type": "code", "metadata": {},
                  "execution_count": sum(c["cell_type"] == "code" for c in cells) + 1,
                  "source": text.splitlines(keepends=True), "outputs": outputs})


markdown("# Pandas and Matplotlib — exercise solutions\n\n"
         "Solutions for Exercises **0, 1, 3, and 6** from the supplied screenshots. "
         "Random examples use seed 42. All results below were executed.\n\n"
         "Run this notebook from its folder. Install `numpy`, `pandas`, and `matplotlib` "
         "if necessary. Charts and data are saved in `outputs/`. "
         "The code also works in `solutions.py`. When rerunning a chart cell in Jupyter, "
         "open its saved PNG or use `display(Image(filename='outputs/FILE.png'))` "
         "after importing `Image` from `IPython.display`.")
code(setup)
markdown("## Exercise 0 — From CSV to Matplotlib\n\n"
         "Three synthetic practice datasets are included in `data/`: grades for "
         "20 students, monthly sales for four categories, and 30 survey responses. "
         "These examples replace the unavailable original CSVs for practice. "
         "This code reads each CSV placed in `data/` and plots its "
         "numeric series and numeric means. For a CSV with only text, it plots "
         "the most common values in its first column. Adapt the chart to the "
         "meaning and units of the actual data when those files are available.")
code(functions["exercise_0"] + "\n\ncsv_tables = exercise_0(Path.cwd() / 'data')\n",
     [f"exercise_0_{path.stem}.png" for path in sorted((ROOT / "data").glob("*.csv"))])
markdown("## Exercise 1 — Student Grades Analysis\n\n"
         "`integers(0, 21)` includes both 0 and 20. Each student's average uses "
         "only the three subjects. The bar chart uses subject means across all "
         "20 students; the histogram uses the 20 individual averages and 10 bins. "
         "Ties in the top three are ordered by student number.")
code(functions["exercise_1"] + "\n\ngrades, top_3, subject_means = exercise_1()\n",
     ["exercise_1_grades.png"])
markdown("## Exercise 3 — Retail Sales Dashboard\n\n"
         "The matrix has axes `(month, store, category)` and shape `(12, 5, 4)`. "
         "Sales are whole euros from EUR 5,000 through EUR 50,000 inclusive. "
         "Reshaping to `(60, 4)` preserves month/store order for the MultiIndex. "
         "The best pair is the store/category combination with the greatest "
         "annual total. Monthly evolution is the total across every store and category.")
code(functions["exercise_3"] + "\n\nsales_matrix, sales, store_category, store_totals, category_totals = exercise_3()\n",
     ["exercise_3_sales_dashboard.png"])
markdown("## Exercise 6 — Image Processing with NumPy + Pandas + Matplotlib\n\n"
         "A synthetic grayscale image is used, as allowed by the exercise. "
         "Its pixel matrix is a Pandas DataFrame. `mean(axis=1)` gives a mean "
         "for each row and `mean(axis=0)` a mean for each column.\n\n"
         "**Brightest region:** the contiguous 16 × 16 square with the highest "
         "mean brightness (a smaller square for tiny images). The brightest "
         "row, column, and first maximum pixel are also reported. Coordinates "
         "are zero-based and region endpoints are inclusive.\n\n"
         "Thresholding uses the exact rule **pixel > 128 → 255; otherwise → 0**. "
         "For a real image, call `exercise_6('image.png')`; normalized PNG values "
         "are converted to the 0–255 scale before thresholding.")
code(functions["exercise_6"] + "\n\nimage, pixels, row_means, column_means, thresholded = exercise_6()\n",
     ["exercise_6_image_processing.png"])

notebook = {"nbformat": 4, "nbformat_minor": 5, "cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python",
                                         "name": "python3"},
                         "language_info": {"name": "python", "version": "3.12"}}}
for index, cell in enumerate(cells):
    cell["id"] = f"exercise-cell-{index:02d}"
(ROOT / "solutions.ipynb").write_text(json.dumps(notebook, indent=1), encoding="utf-8")
(ROOT / "outputs" / "results.txt").write_text("\n".join(results), encoding="utf-8")
print("Created executed solutions.ipynb and outputs/results.txt")
