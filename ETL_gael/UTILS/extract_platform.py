from pathlib import Path

import pandas as pd


TASKS_URL = "https://raw.githubusercontent.com/Dalila-Ku/Platform_Design/main/db_files/dalila/data/tasks_sample.csv"
USERS_URL = "https://raw.githubusercontent.com/Dalila-Ku/Platform_Design/main/db_files/esau/data/users.csv"


def _read_csv(source_name: str, github_url: str, fallback_path: Path) -> pd.DataFrame:
    """Read a CSV source from GitHub. Use local fallback if GitHub is unavailable."""

    try:
        print(f"[EXTRACT] Connecting to {source_name}: {github_url}")
        df = pd.read_csv(github_url)
        print(f"[EXTRACT] {source_name}: {len(df)} rows read from GitHub")
        return df

    except Exception as error:
        print(f"[EXTRACT] WARNING: could not read {source_name} from GitHub")
        print(f"[EXTRACT] Reason: {type(error).__name__}: {error}")
        print(f"[EXTRACT] Using local fallback: {fallback_path}")
        df = pd.read_csv(fallback_path)
        print(f"[EXTRACT] {source_name}: {len(df)} rows read from fallback")
        return df


def extract_platform_data(base_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Extract data from two shared-platform sources."""

    tasks_path = base_dir / "data" / "tasks_sample_seed.csv"
    users_path = base_dir / "data" / "users_seed.csv"

    tasks_raw = _read_csv("tasks_sample.csv", TASKS_URL, tasks_path)
    users_raw = _read_csv("users.csv", USERS_URL, users_path)

    print(f"[EXTRACT] Completed: tasks={len(tasks_raw)} rows, users={len(users_raw)} rows")
    return tasks_raw, users_raw
