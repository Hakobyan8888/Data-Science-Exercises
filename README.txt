PANDAS AND MATPLOTLIB EXERCISES

solutions.py contains the solutions to Exercises 0, 1, 3, and 6.
solutions.ipynb contains the same solutions with executed results and charts.
outputs/ contains the charts, generated data, and numerical results.

Run with a normal Python installation:
    python -m pip install -r requirements.txt
    python solutions.py

Exercise 0: Three synthetic practice CSVs are included in data/:
    student_grades.csv: 20 students with Math, Physics, and CS grades (0-20).
    monthly_sales.csv: 12 months in 2025, four product categories, sales in EUR.
    survey_responses.csv: 30 respondents with preferred product categories.
These are generated examples, not the missing original assignment datasets.
Run solutions.py to load these files and create their charts, or use:
    python solutions.py --csv-dir PATH_TO_CSV_FOLDER
Plots depend on the supplied data; the generic solution plots numeric columns
by row and their means, or category frequencies for a nonnumeric CSV.

Exercise 1: Grades are integers from 0 through 20 inclusive. The Average column
uses only Math, Physics, and CS. Equal averages are ordered by student number.
Both requested plots and the top three students appear in the saved figure.

Exercise 3: Sales are whole euros from 5,000 through 50,000 inclusive. The
MultiIndex is (month, store). The best store/category pair is based on its sum
over all 12 months. The monthly line plot sums all stores and categories.

Exercise 6: The default input is a synthetic grayscale image, as allowed by the
exercise. To use a real image:
    python solutions.py --image image.png
Pixel values are converted to uint8 on the 0-255 scale before thresholding.
The brightest region is defined as the 16 x 16 square with the highest mean
brightness, or a smaller square for images smaller than 16 pixels. Row and
column coordinates are zero-based. The threshold comparison is strictly >128.

All randomly generated examples use seed 42 for reproducibility.
The CSV examples use a JavaScript random generator, independently of the
NumPy examples in Exercises 1, 3, and 6. To regenerate them with the bundled
Node environment, run: node generate_example_csvs.mjs
The saved chart PNGs can be opened directly and used for the requested screenshots.
