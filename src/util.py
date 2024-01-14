import isodate


def pt_time_to_seconds(pt_time: str) -> float:
    return isodate.parse_duration(pt_time).total_seconds()
