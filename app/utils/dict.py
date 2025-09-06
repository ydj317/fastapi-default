from sqlalchemy import Table
from app.utils.datetime import now_datetime

def filter_to_table_columns(data: dict, table: Table):
    # 테이블 컬럼 이름 집합
    table_columns = {col.name for col in table.columns}

    # dict에서 테이블 컬럼과 교집합만 추출
    filtered = {k: v for k, v in data.items() if k in table_columns}

    return filtered