from pathlib import Path

from UTILS.extract_platform import extract_platform_data
from UTILS.generate_synthetic import generate_assignment_log
from UTILS.transform import clean_sources, transform_assignments
from UTILS.indicators import calculate_indicators
from UTILS.load import load_csv, load_json, load_excel


BASE_DIR = Path(__file__).parent

OUTPUT_DATASET = BASE_DIR / "outputs" / "gael_final_assignment_dataset.csv"
OUTPUT_INDICATOR = BASE_DIR / "outputs" / "gael_indicator_summary.csv"
OUTPUT_RESULT_JSON = BASE_DIR / "outputs" / "gael_indicator_result.json"
OUTPUT_REPORT = BASE_DIR / "outputs" / "gael_etl_report.xlsx"


if __name__ == "__main__":
    print("=" * 70)
    print("PROJECT #08 — GAEL ETL FINAL PIPELINE")
    print("=" * 70)

    # EXTRACT
    tasks_raw, users_raw = extract_platform_data(BASE_DIR)

    # CLEAN
    tasks_clean, users_clean = clean_sources(tasks_raw, users_raw)

    # SYNTHETIC EXPANSION FROM PLATFORM SOURCES
    assignment_log = generate_assignment_log(tasks_clean, users_clean, n_records=250)

    # TRANSFORM
    final_dataset = transform_assignments(assignment_log)

    # INDICATORS
    indicator_summary, main_result = calculate_indicators(final_dataset)

    # LOAD
    load_csv(final_dataset, OUTPUT_DATASET)
    load_csv(indicator_summary, OUTPUT_INDICATOR)
    load_json(main_result, OUTPUT_RESULT_JSON)
    load_excel(final_dataset, indicator_summary, main_result, OUTPUT_REPORT)

    print("=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)
