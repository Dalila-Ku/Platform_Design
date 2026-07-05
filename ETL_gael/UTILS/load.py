from pathlib import Path

import pandas as pd


def load_csv(df: pd.DataFrame, output_path: Path) -> None:
    """Save a DataFrame as CSV."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[LOAD] {len(df)} rows saved to {output_path}")


def load_json(result: pd.DataFrame, output_path: Path) -> None:
    """Save the main result as JSON."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_json(output_path, orient="records", indent=2, force_ascii=False)
    print(f"[LOAD] JSON result saved to {output_path}")


def load_excel(
    assignments: pd.DataFrame,
    indicator: pd.DataFrame,
    result: pd.DataFrame,
    output_path: Path,
) -> None:
    """Export the final ETL report to Excel with multiple sheets."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        assignments.to_excel(writer, sheet_name="Final Dataset", index=False)
        indicator.to_excel(writer, sheet_name="Indicator", index=False)
        result.to_excel(writer, sheet_name="Main Result", index=False)

    print(f"[LOAD] Excel report saved to {output_path}")
