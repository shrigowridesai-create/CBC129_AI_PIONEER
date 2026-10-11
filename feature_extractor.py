from datetime import datetime, date
from typing import List, Dict, Any
import pytz

from ..core.intervals import TimeInterval, calculate_buffer_minutes, overlaps_lunch

# Grounded scheduling features plus the recently-added edge-case indicators.
# The project dataset was extended with: no_common_time_slot,
# critical_participant_unavailable, and multiple_similar_alternatives.
FEATURE_COLUMNS = [
    "duration_minutes",
    "priority_level",
    "num_participants",
    "day_of_week",
    "start_hour_utc",
    "max_tz_difference_hrs",
    "calendar_load_ratio",
    "min_buffer_before_min",
    "min_buffer_after_min",
    "consecutive_meetings",
    "lunch_overlap_ratio",
    "no_common_time_slot",
    "critical_participant_unavailable",
    "multiple_similar_alternatives"
]

PRIORITY_MAP = {
    "LOW": 1.0,
    "MEDIUM": 2.0,
    "HIGH": 3.0,
    "CRITICAL": 4.0
}


def extract_slot_features(
    candidate: TimeInterval,
    participants_info: List[Dict[str, Any]],
    duration_minutes: int,
    priority: str = "MEDIUM"
) -> Dict[str, float]:
    """
    Extracts an 11-dimensional tabular feature vector for a candidate meeting slot.
    
    Guarantees:
    - Zero data leakage: All features computed strictly from data known at request time.
    - Grounded: Every feature directly originates from the Problem Statement 51 spec
      or established calendar attendance literature (NESA / Kaggle benchmarks).
    """
    num_participants = max(len(participants_info), 1)
    
    lunch_overlaps = 0
    buffers_before = []
    buffers_after = []
    consecutives = []
    tz_offsets_hours = []
    total_busy_minutes = 0.0
    total_available_work_minutes = 0.0

    target_date = candidate.start.date()

    for p in participants_info:
        tz_str = p.get("timezone", "UTC")
        try:
            user_tz = pytz.timezone(tz_str)
        except Exception:
            user_tz = pytz.UTC

        # 1. Timezone offset in hours
        try:
            offset_sec = user_tz.utcoffset(candidate.start).total_seconds()
            tz_offsets_hours.append(offset_sec / 3600.0)
        except Exception:
            tz_offsets_hours.append(0.0)

        # 2. Lunch overlap ratio
        lunch_s = p.get("lunch_start_hour", 12)
        lunch_e = p.get("lunch_end_hour", 13)
        if overlaps_lunch(candidate, tz_str, lunch_s, lunch_e):
            lunch_overlaps += 1

        # 3. Buffer and consecutive fatigue
        busy_intervals: List[TimeInterval] = p.get("busy_intervals", [])
        buf_before, buf_after, consec = calculate_buffer_minutes(candidate, busy_intervals)
        buffers_before.append(buf_before)
        buffers_after.append(buf_after)
        consecutives.append(consec)

        # 4. Daily calendar load ratio (busy minutes today vs total working minutes today)
        work_s = p.get("work_start_hour", 9)
        work_e = p.get("work_end_hour", 17)
        work_minutes = max((work_e - work_s) * 60.0, 60.0)
        total_available_work_minutes += work_minutes

        # Sum busy interval durations for today
        for b in busy_intervals:
            if b.start.date() == target_date or b.end.date() == target_date:
                total_busy_minutes += b.duration_minutes

    # Derived feature computations
    max_tz_diff = max(tz_offsets_hours) - min(tz_offsets_hours) if tz_offsets_hours else 0.0
    load_ratio = total_busy_minutes / max(total_available_work_minutes, 60.0)
    clamped_load_ratio = min(max(load_ratio, 0.0), 1.0)
    lunch_ratio = lunch_overlaps / num_participants
    start_hour_utc = candidate.start.hour + candidate.start.minute / 60.0

    required_participants = [p for p in participants_info if p.get("is_required", True)]
    required_busy_overlaps = 0
    for p in required_participants:
        busy_intervals: List[TimeInterval] = p.get("busy_intervals", [])
        if any(b.start < candidate.end and b.end > candidate.start for b in busy_intervals):
            required_busy_overlaps += 1

    no_common_time_slot = float(
        1.0 if (
            len(required_participants) > 1
            and required_busy_overlaps >= max(1, len(required_participants) // 2)
        ) or (len(required_participants) > 2 and clamped_load_ratio > 0.8)
        else 0.0
    )

    critical_participant_unavailable = float(1.0 if required_busy_overlaps > 0 else 0.0)
    multiple_similar_alternatives = float(
        1.0 if len(participants_info) >= 5 and max_tz_diff <= 2.0 and clamped_load_ratio < 0.45 else 0.0
    )

    return {
        "duration_minutes": float(duration_minutes),
        "priority_level": float(PRIORITY_MAP.get(priority.upper(), 2.0)),
        "num_participants": float(num_participants),
        "day_of_week": float(candidate.start.weekday()),
        "start_hour_utc": float(round(start_hour_utc, 2)),
        "max_tz_difference_hrs": float(round(max_tz_diff, 2)),
        "calendar_load_ratio": float(round(clamped_load_ratio, 3)),
        "min_buffer_before_min": float(min(buffers_before)) if buffers_before else 180.0,
        "min_buffer_after_min": float(min(buffers_after)) if buffers_after else 180.0,
        "consecutive_meetings": float(max(consecutives)) if consecutives else 0.0,
        "lunch_overlap_ratio": float(round(lunch_ratio, 3)),
        "no_common_time_slot": no_common_time_slot,
        "critical_participant_unavailable": critical_participant_unavailable,
        "multiple_similar_alternatives": multiple_similar_alternatives
    }
