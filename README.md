# Centriole Nearest Neighbor Index (NNI) Analysis

A Python-based analysis script for quantifying centriole spatial organization using the **Nearest Neighbor Index (NNI)**.

The script analyzes X–Y centriole coordinates obtained using the **TrackMate plugin in ImageJ/Fiji**, calculates nearest-neighbor distances and NNI values, assigns a descriptive spatial pattern, and generates summary tables and plots.

## What the Script Does

For each CSV file in the selected folder, the script:

1. Detects the `POSITION_X` and `POSITION_Y` columns automatically.
2. Calculates the nearest-neighbor distance for each detected centriole.
3. Calculates the mean nearest-neighbor distance.
4. Estimates the expected nearest-neighbor distance under complete spatial randomness (CSR).
5. Calculates the Nearest Neighbor Index (NNI).
6. Classifies the spatial pattern as clustered, random, or dispersed.
7. Saves a scatter plot of centriole positions.
8. Saves a histogram of nearest-neighbor distances.
9. Generates a summary CSV file for all analyzed files.

## Requirements

The script requires Python 3 and the following packages:

```text
pandas
numpy
matplotlib
scikit-learn
```

They can be installed using:

```bash
pip install pandas numpy matplotlib scikit-learn
```

## Input Data

Centriole X–Y coordinates should be obtained using the **TrackMate plugin in ImageJ/Fiji** and exported as CSV files.

The CSV files must contain:

```text
POSITION_X
POSITION_Y
```

The script automatically searches for the row containing these column headers and supports comma- or semicolon-separated CSV files.

Each CSV file is analyzed independently.

## Set the Input Folder

Before running the script, change only the folder path in the settings section:

```python
# ========= 1) SETTINGS: CHANGE ONLY THIS =========
# Example:
# folder = Path("/Users/username/Desktop/centriole_data")
folder = Path("insert your CSV folder path here")
# ================================================
```

Replace:

```text
insert your CSV folder path here
```

with the path to the folder containing your CSV files.

For example:

```python
folder = Path("/Users/username/Desktop/centriole_data")
```

## Running the Analysis

After setting the folder path, run the Python script normally in your preferred Python environment.

The script automatically detects all `.csv` files in the selected folder and analyzes them in batch.

## NNI Calculation

The Nearest Neighbor Index is calculated as:

```text
NNI = observed mean nearest-neighbor distance / expected mean nearest-neighbor distance
```

The expected mean nearest-neighbor distance under complete spatial randomness is calculated as:

```text
Expected NN distance = 0.5 / sqrt(N / A)
```

where:

- `N` is the number of detected points.
- `A` is the area estimated from the bounding box of the detected X–Y coordinates.

The script uses the following descriptive classifications:

```text
NNI < 0.8       clustered
0.8–1.2         random
NNI > 1.2       dispersed
```

## Output

The script creates a summary file:

```text
NNI_results.csv
```

with the following columns:

| Column | Description |
|---|---|
| `cell` | Input CSV filename |
| `n_dots` | Number of detected points |
| `mean_NN_um` | Mean nearest-neighbor distance |
| `expected_random_NN_um` | Expected mean nearest-neighbor distance under CSR |
| `NNI` | Nearest Neighbor Index |
| `pattern` | Clustered, random, or dispersed classification |

The script also creates a folder named:

```text
plots
```

inside the input CSV folder.

For each CSV file, two plots are saved:

```text
*_scatter.png
*_NN_hist.png
```

The scatter plot shows the X–Y distribution of detected centrioles, and the histogram shows the distribution of nearest-neighbor distances.

## Methodological Note

The analyzed area is estimated using the **bounding box of the detected centriole coordinates**:

```text
Area = (maximum X - minimum X) × (maximum Y - minimum Y)
```

Therefore, the area used in the NNI calculation is based on the spatial extent of the detected points and does not represent a manually measured cell boundary.

The `0.8` and `1.2` NNI thresholds are used as descriptive classification thresholds in this analysis.

## Example Folder Structure

```text
centriole-nni-analysis/
├── README.md
├── LICENSE
├── nni_analysis.py
└── centriole_data/
    ├── cell_01.csv
    ├── cell_02.csv
    ├── cell_03.csv
    ├── NNI_results.csv
    └── plots/
        ├── cell_01_scatter.png
        ├── cell_01_NN_hist.png
        ├── cell_02_scatter.png
        └── cell_02_NN_hist.png
```

## License

This project is distributed under the **MIT License**. See the `LICENSE` file for details.

## Citation

If this code is used in published work, please cite the associated publication and/or archived software release when available.
