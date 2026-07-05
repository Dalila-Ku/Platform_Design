import numpy as np
import pandas as pd


RANDOM_SEED = 42


def generate_assignment_log(
    tasks: pd.DataFrame,
    users: pd.DataFrame,
    n_records: int = 250
) -> pd.DataFrame:
    """
    Generate a synthetic assignment interaction log from the platform skeleton.

    The GitHub platform already provides real structure: tasks, dates, status,
    priority, difficulty and users. Since the system is still in beta and does
    not yet contain hundreds of real interactions, this module expands those
    records into a controlled synthetic dataset for the final ETL demonstration.
    """

    rng = np.random.default_rng(RANDOM_SEED)
    rows = []

    for i in range(n_records):
        task = tasks.iloc[i % len(tasks)]
        user = users.iloc[i % len(users)]

        assignment_date = task["assignment_date"]
        if pd.isna(assignment_date):
            assignment_date = pd.Timestamp("2026-05-01")

        # Spread the sample records through time.
        assignment_date = assignment_date + pd.Timedelta(days=int(i // len(tasks)))

        priority = str(task.get("priority", "medium")).lower()
        difficulty = str(task.get("difficulty", "medium")).lower()

        # 55% of students start early, 45% start late.
        starts_early = rng.random() < 0.55

        if starts_early:
            hours_to_start = int(rng.integers(1, 24))
            on_time_probability = 0.82
        else:
            hours_to_start = int(rng.integers(25, 96))
            on_time_probability = 0.52

        # Higher priority / difficulty slightly reduces probability of finishing on time.
        if priority in ["high", "critical"]:
            on_time_probability -= 0.05

        if difficulty in ["hard", "very_hard"]:
            on_time_probability -= 0.05

        on_time_probability = float(np.clip(on_time_probability, 0.10, 0.95))
        submitted_on_time = bool(rng.random() < on_time_probability)

        due_date = assignment_date + pd.Timedelta(days=int(rng.integers(5, 22)))
        start_date = assignment_date + pd.Timedelta(hours=hours_to_start)

        if submitted_on_time:
            completed_date = due_date - pd.Timedelta(days=int(rng.integers(0, 4)))
        else:
            completed_date = due_date + pd.Timedelta(days=int(rng.integers(1, 8)))

        rows.append(
            {
                "assignment_id": i + 1,
                "source_task_id": task["id"],
                "student_id": user["id"],
                "student_name": user["full_name"],
                "assignment_title": task["title"],
                "priority": priority,
                "difficulty": difficulty,
                "assignment_date": assignment_date,
                "start_date": start_date,
                "due_date": due_date,
                "completed_date": completed_date,
                "status": "done",
                "hours_to_start": hours_to_start,
                "submitted_on_time": submitted_on_time,
            }
        )

    df = pd.DataFrame(rows)
    print(f"[SYNTHETIC] Generated {len(df)} assignment interaction records")
    print(f"[SYNTHETIC] Source platform tasks used: {len(tasks)}")
    print(f"[SYNTHETIC] Source platform users used: {len(users)}")

    return df
