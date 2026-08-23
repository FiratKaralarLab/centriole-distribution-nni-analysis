import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from pathlib import Path

# ========= 1) SETTINGS: CHANGE ONLY THIS =========
# Example:
# folder = Path("/Users/username/Desktop/centriole_data")
folder = Path("insert your CSV folder path here")
# ================================================


def load_spots_csv(csv_path):
    """
    Robust loader for spots in CSV.
    Finds the header row containing POSITION_X and POSITION_Y automatically.
    Handles comma or semicolon separators.
    """
    preview = pd.read_csv(csv_path, header=None, nrows=30, sep=None, engine="python")

    header_row = None
    for i in range(preview.shape[0]):
        row = preview.iloc[i].astype(str).tolist()
        if any("POSITION_X" in x for x in row) and any("POSITION_Y" in x for x in row):
            header_row = i
            break

    if header_row is None:
        raise ValueError(f"Header with POSITION_X/POSITION_Y not found in {csv_path.name}")

    df = pd.read_csv(csv_path, header=header_row, sep=None, engine="python")

    # Convert to numeric safely (handles unit rows etc.)
    for col in ["POSITION_X", "POSITION_Y"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    pts = df[["POSITION_X", "POSITION_Y"]].dropna().values
    return pts


def analyze_points(pts):
    """
    Returns: nn_distances, mean_nn, expected_random_nn, nni, label
    """
    if len(pts) < 3:
        return None

    nbrs = NearestNeighbors(n_neighbors=2).fit(pts)
    dists, _ = nbrs.kneighbors(pts)
    nn = dists[:, 1]  # nearest neighbor distance for each point

    mean_nn = float(nn.mean())

    # area estimate using bounding box (no cell boundary needed)
    xmin, ymin = pts.min(axis=0)
    xmax, ymax = pts.max(axis=0)
    area = float((xmax - xmin) * (ymax - ymin))

    n = len(pts)
    expected = 0.5 / np.sqrt(n / area)  # expected mean NN under CSR
    nni = mean_nn / expected

    if nni < 0.8:
        label = "clustered"
    elif nni > 1.2:
        label = "dispersed"
    else:
        label = "random"

    return nn, mean_nn, expected, float(nni), label


def save_plots(csv_path, pts, nn, nni):
    """
    Saves two plots per cell:
    1) scatter of dot positions
    2) histogram of NN distances
    """
    outdir = csv_path.parent / "plots"
    outdir.mkdir(exist_ok=True)

    # Scatter plot
    plt.figure(figsize=(5, 5))
    plt.scatter(pts[:, 0], pts[:, 1], s=12)
    plt.gca().set_aspect("equal")
    plt.title(f"{csv_path.stem} | NNI={nni:.2f}")
    plt.xlabel("X (µm)")
    plt.ylabel("Y (µm)")
    plt.tight_layout()
    plt.savefig(outdir / f"{csv_path.stem}_scatter.png", dpi=300)
    plt.close()

    # NN histogram
    plt.figure(figsize=(6, 4))
    plt.hist(nn, bins=25)
    plt.title(f"NN distance histogram: {csv_path.stem}")
    plt.xlabel("Nearest-neighbor distance (µm)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(outdir / f"{csv_path.stem}_NN_hist.png", dpi=300)
    plt.close()


# ========= 2) RUN BATCH =========

csv_files = sorted(folder.glob("*.csv"))
print(f"Folder: {folder}")
print(f"CSV files found: {len(csv_files)}")

rows = []

for f in csv_files:
    try:
        pts = load_spots_csv(f)
        res = analyze_points(pts)

        if res is None:
            print(f"{f.name}: skipped (need >=3 points)")
            continue

        nn, mean_nn, expected, nni, label = res

        # Save plots
        save_plots(f, pts, nn, nni)

        # Save row
        rows.append([f.stem, len(pts), mean_nn, expected, nni, label])

        print(f"{f.name}: n={len(pts)} mean_NN={mean_nn:.3f} NNI={nni:.3f} -> {label}")

    except Exception as e:
        print(f"{f.name}: ERROR -> {e}")

out = pd.DataFrame(rows, columns=[
    "cell", "n_dots", "mean_NN_um", "expected_random_NN_um", "NNI", "pattern"
])

# Save results table
out_path = folder / "NNI_results.csv"
out.to_csv(out_path, index=False)

print("\nSummary:")
print(out)
print(f"\nSaved table: {out_path}")
print(f"Saved plots in: {folder / 'plots'}")
