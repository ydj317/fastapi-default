from datetime import datetime
from zoneinfo import ZoneInfo

timezone = ZoneInfo('Europe/Zurich')

class Datetime:
    @staticmethod
    def timestamp_to_string(timestamp_str: str) -> str:
        """
        타임스탬프 문자열을 'Y-m-d H:i:s' 포맷의 문자열로 변환
        """
        timestamp = int(timestamp_str)
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def string_to_timestamp(datetime_str: str) -> int:
        """
        'Y-m-d H:i:s' 포맷의 문자열을 타임스탬프(int)로 변환
        """
        dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        dt_kst = dt.replace(tzinfo=timezone)
        return int(dt_kst.timestamp())

    @staticmethod
    def now_timestamp() -> int:
        """
        현재 시간의 타임스탬프(int)를 반환
        """
        return int(datetime.now().timestamp())
