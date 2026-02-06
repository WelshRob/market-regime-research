"""Measure range compression, overlap, and directional efficiency for FX data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
WINDOWS = (5, 10, 20)


def compute_overlap_ratio(current_high: pd.Series, current_low: pd.Series) -> pd.Series:
    """
    Compute overlap ratio between consecutive daily ranges.

    Overlap length is the intersection of today's range with yesterday's range.
    The ratio is overlap length divided by today's range length.
    """

    previous_high = current_high.shift(1)
    previous_low = current_low.shift(1)
    overlap_high = pd.concat([current_high, previous_high], axis=1).min(axis=1)
    overlap_low = pd.concat([current_low, previous_low], axis=1).max(axis=1)
    overlap_length = (overlap_high - overlap_low).clip(lower=0)
    today_range = (current_high - current_low).replace(0, pd.NA)
    return overlap_length / today_range


def compute_directional_efficiency(close: pd.Series, window: int) -> pd.Series:
    """
    Directional efficiency over a rolling window.

    Net displacement is the absolute change from the window start to end.
    Total movement is the sum of absolute day-to-day changes within the window.
    """

    net_displacement = (close - close.shift(window - 1)).abs()
    total_movement = close.diff().abs().rolling(window - 1).sum()
    return net_displacement / total_movement.replace(0, pd.NA)


def process_symbol(csv_path: Path) -> pd.DataFrame:
    """Load a CSV and compute compression, overlap, and efficiency metrics."""

    data = pd.read_csv(csv_path)

    # Daily range metrics
    data["Range"] = data["High"] - data["Low"]
    for window in WINDOWS:
        data[f"Range_MA_{window}"] = data["Range"].rolling(window).mean()

    # Compression ratios vs 20-day average range
    data["RangeCompression_5_vs_20"] = data["Range_MA_5"] / data["Range_MA_20"].replace(
        0, pd.NA
    )
    data["RangeCompression_10_vs_20"] = data["Range_MA_10"] / data["Range_MA_20"].replace(
        0, pd.NA
    )

    # Overlap ratio between consecutive daily ranges and rolling averages
    data["Overlap_Ratio"] = compute_overlap_ratio(data["High"], data["Low"])
    for window in (5, 10):
        data[f"Overlap_Ratio_MA_{window}"] = data["Overlap_Ratio"].rolling(window).mean()

    # Directional efficiency (net displacement vs total movement)
    for window in WINDOWS:
        data[f"DirectionalEfficiency_{window}"] = compute_directional_efficiency(
            data["Close"], window
        )

    return data


def main() -> None:
    """Run compression analysis for each CSV in the data directory."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for csv_path in sorted(DATA_DIR.glob("*_Daily.csv")):
        symbol = csv_path.stem.replace("_Daily", "")
        results = process_symbol(csv_path)
        output_path = OUTPUT_DIR / f"{symbol}_compression_analysis.csv"
        results.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()
