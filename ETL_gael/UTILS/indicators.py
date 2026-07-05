import pandas as pd


def calculate_indicators(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Calculate the main indicator:
    mean on-time submission rate by early-start group.
    """

    indicator = (
        df.groupby("start_group")
        .agg(
            assignment_count=("assignment_id", "count"),
            mean_hours_to_start=("hours_to_start", "mean"),
            mean_on_time_submission_rate=("submitted_on_time", "mean"),
            mean_completion_time_days=("completion_time_days", "mean"),
            mean_days_before_deadline=("days_before_deadline", "mean"),
        )
        .reset_index()
        .round(4)
    )

    early_rate = indicator.loc[
        indicator["start_group"] == "Early start (<= 24 hours)",
        "mean_on_time_submission_rate",
    ]

    late_rate = indicator.loc[
        indicator["start_group"] == "Late start (> 24 hours)",
        "mean_on_time_submission_rate",
    ]

    if len(early_rate) > 0 and len(late_rate) > 0:
        difference = float(early_rate.iloc[0] - late_rate.iloc[0])
    else:
        difference = None

    result = pd.DataFrame(
        [
            {
                "research_question": "Do students who start working on assignments within 24 hours of receiving them have a higher on-time submission rate than students who start later?",
                "indicator": "Mean on-time submission rate compared between early-start and late-start groups.",
                "early_start_rate": float(early_rate.iloc[0]) if len(early_rate) > 0 else None,
                "late_start_rate": float(late_rate.iloc[0]) if len(late_rate) > 0 else None,
                "difference_early_minus_late": round(difference, 4) if difference is not None else None,
                "total_assignments": int(len(df)),
                "interpretation": (
                    "Early-start students show a higher on-time submission rate."
                    if difference is not None and difference > 0
                    else "The observed difference does not support a higher early-start rate."
                ),
            }
        ]
    )

    print("[INDICATORS] Indicator table created")
    print(indicator.to_string(index=False))

    print("[INDICATORS] Main result created")
    print(result.to_string(index=False))

    return indicator, result
