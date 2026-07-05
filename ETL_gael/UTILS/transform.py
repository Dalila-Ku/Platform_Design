import numpy as np
import pandas as pd


def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to snake_case."""

    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


def clean_sources(
    tasks_raw: pd.DataFrame,
    users_raw: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clean raw platform sources before synthetic expansion."""

    tasks = _clean_columns(tasks_raw)
    users = _clean_columns(users_raw)

    before_tasks = len(tasks)
    before_users = len(users)

    tasks = tasks.drop_duplicates()
    users = users.drop_duplicates()

    print(f"[CLEAN] Removed task duplicates: {before_tasks} -> {len(tasks)}")
    print(f"[CLEAN] Removed user duplicates: {before_users} -> {len(users)}")

    for df_name, df in [("tasks", tasks), ("users", users)]:
        text_cols = df.select_dtypes(include="object").columns

        for col in text_cols:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({"": np.nan, "nan": np.nan, "None": np.nan})

        print(f"[CLEAN] Standardized text columns in {df_name}: {list(text_cols)}")

    for col in ["assignment_date", "start_date", "due_date", "completed_date"]:
        if col in tasks.columns:
            tasks[col] = pd.to_datetime(tasks[col], errors="coerce")
            print(f"[CLEAN] Parsed {col}. Missing values: {tasks[col].isna().sum()}")

    if "id" not in tasks.columns:
        tasks["id"] = range(1, len(tasks) + 1)
        print("[CLEAN] Created missing tasks.id")

    if "id" not in users.columns:
        users["id"] = range(1, len(users) + 1)
        print("[CLEAN] Created missing users.id")

    if "full_name" not in users.columns:
        users["full_name"] = "Student " + users["id"].astype(str)
        print("[CLEAN] Created missing users.full_name")

    print(f"[CLEAN] Completed: tasks={len(tasks)} rows, users={len(users)} rows")
    return tasks, users


def transform_assignments(assignments: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich the synthetic assignment log."""

    df = assignments.copy()

    before = len(df)

    df = df.drop_duplicates(subset=["assignment_id"])
    df = df.dropna(
        subset=[
            "assignment_id",
            "student_id",
            "assignment_date",
            "start_date",
            "due_date",
            "completed_date",
        ]
    )

    print(f"[TRANSFORM] Removed invalid/duplicate assignment records: {before} -> {len(df)}")

    for col in ["assignment_date", "start_date", "due_date", "completed_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    df["hours_to_start"] = (
        df["start_date"] - df["assignment_date"]
    ).dt.total_seconds() / 3600

    df["early_start"] = df["hours_to_start"] <= 24

    df["start_group"] = np.where(
        df["early_start"],
        "Early start (<= 24 hours)",
        "Late start (> 24 hours)",
    )

    df["submitted_on_time"] = df["completed_date"] <= df["due_date"]

    df["completion_time_days"] = (
        df["completed_date"] - df["assignment_date"]
    ).dt.total_seconds() / 86400

    df["days_vs_deadline"] = (
        df["completed_date"] - df["due_date"]
    ).dt.total_seconds() / 86400

    df["days_before_deadline"] = -df["days_vs_deadline"]

    df = df[df["hours_to_start"] >= 0].copy()

    print("[TRANSFORM] Derived columns created:")
    print("[TRANSFORM] early_start, start_group, submitted_on_time, completion_time_days, days_vs_deadline")
    print(f"[TRANSFORM] Final analytical records: {len(df)}")

    return df
