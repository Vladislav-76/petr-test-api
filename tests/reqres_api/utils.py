from datetime import datetime, timedelta


def is_almost_now(iso_time):
    iso_time = datetime.fromisoformat(iso_time)
    time_now = datetime.now(tz=iso_time.tzinfo)
    return iso_time > time_now - timedelta(minutes=5)
