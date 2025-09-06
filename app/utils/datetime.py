from datetime import datetime
from zoneinfo import ZoneInfo

timezone = ZoneInfo("Asia/Seoul")


def timestamp_to_string(timestamp: int, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    타임스탬프를 'Y-m-d H:i:s' 포맷의 문자열로 변환
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime(format_str)


def string_to_timestamp(datetime_str: str) -> int:
    """
    'Y-m-d H:i:s' 포맷의 문자열을 타임스탬프(int)로 변환
    """
    dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    dt_kst = dt.replace(tzinfo=timezone)
    return int(dt_kst.timestamp())


def now_timestamp() -> int:
    """
    현재 시간의 타임스탬프(int)를 반환
    """
    return int(datetime.now().timestamp())

def now_datetime(format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    return timestamp_to_string(int(datetime.now().timestamp()))
