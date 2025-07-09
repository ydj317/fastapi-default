from abc import ABC, abstractmethod
from databases import Database
import sqlalchemy
from datetime import datetime
from sqlalchemy import and_, or_, func

class BaseRepo(ABC):
    def __init__(self, db: Database):
        self.db = db

    @property
    @abstractmethod
    def table(self) -> sqlalchemy.Table:
        """서브클래스가 구현해야 할 SQLAlchemy Table"""
        pass

    def _has_column(self, column_name: str) -> bool:
        return column_name in self.table.c

    def _now(self):
        return datetime.now()

    async def create(self, **values):
        if self._has_column("created_at") and "created_at" not in values:
            values["created_at"] = self._now()
        query = self.table.insert().values(**values)
        return await self.db.execute(query)

    async def get_all(self):
        query = self.table.select()
        rows = await self.db.fetch_all(query)
        return [dict(row) for row in rows]

    async def get_by_id(self, id: int):
        query = self.table.select().where(self.table.c.id == id)
        row = await self.db.fetch_one(query)
        return dict(row) if row else None

    async def update_by_id(self, id: int, **values):
        if self._has_column("updated_at"):
            values["updated_at"] = self._now()
        query = self.table.update().where(self.table.c.id == id).values(**values)
        return await self.db.execute(query)

    async def delete_by_id(self, id: int):
        query = self.table.delete().where(self.table.c.id == id)
        return await self.db.execute(query)

    async def get_by_where(
            self,
            where: dict = None,
            limit: int = 10,
            page: int = 1,
            order_by: list = None
    ):
        """
        조건 기반으로 데이터를 조회하고 페이징, 정렬, 총 개수까지 반환합니다.

        Args:
            where (dict): 조회 조건. 연산자 포함 가능.
                예:
                    {
                        "username": {"like": "%admin%"},
                        "age": {">": 18},
                        "or": [
                            {"status": "active"},
                            {"status": "pending"}
                        ]
                    }

            limit (int): 페이지당 항목 수 (기본값: 10)
            page (int): 페이지 번호 (1부터 시작)
            order_by (list): 정렬 조건 (튜플 리스트).
                예: [("created_at", "desc"), ("id", "asc")]

        Returns:
            dict: {
                "total": 전체 결과 수,
                "items": [결과 리스트 (dict)]
            }
        """

        query = self.table.select()
        count_query = self.table.select().with_only_columns([func.count()])

        def build_conditions(w: dict):
            """
            where 딕셔너리를 기반으로 SQLAlchemy 조건 리스트 생성
            """
            conds = []

            for key, condition in w.items():
                if key == "or" and isinstance(condition, list):
                    # OR 조건 지원
                    or_conds = []
                    for or_item in condition:
                        or_conds.append(and_(*build_conditions(or_item)))
                    conds.append(or_(*or_conds))
                    continue

                column = self.table.c.get(key)
                if column is None:
                    continue  # 존재하지 않는 컬럼은 무시

                if not isinstance(condition, dict):
                    # 기본 = 조건
                    conds.append(column == condition)
                else:
                    # 연산자 처리
                    for op, val in condition.items():
                        if op == "=":
                            conds.append(column == val)
                        elif op == "!=":
                            conds.append(column != val)
                        elif op == ">":
                            conds.append(column > val)
                        elif op == "<":
                            conds.append(column < val)
                        elif op == ">=":
                            conds.append(column >= val)
                        elif op == "<=":
                            conds.append(column <= val)
                        elif op == "in" and isinstance(val, list):
                            conds.append(column.in_(val))
                        elif op == "not_in" and isinstance(val, list):
                            conds.append(~column.in_(val))
                        elif op == "like":
                            conds.append(column.like(val))
                        elif op == "ilike":
                            conds.append(column.ilike(val))
            return conds

        # 조건 적용
        if where:
            where_conditions = build_conditions(where)
            if where_conditions:
                query = query.where(and_(*where_conditions))
                count_query = count_query.where(and_(*where_conditions))

        # 정렬 처리
        if order_by:
            order_clauses = []
            for col_name, direction in order_by:
                col = self.table.c.get(col_name)
                if col is not None:
                    if direction.lower() == "desc":
                        order_clauses.append(col.desc())
                    else:
                        order_clauses.append(col.asc())
            if order_clauses:
                query = query.order_by(*order_clauses)

        # 페이징 처리
        offset = (page - 1) * limit
        query = query.limit(limit).offset(offset)

        # 데이터 조회
        rows = await self.db.fetch_all(query)
        total = await self.db.fetch_val(count_query)

        return {
            "total": total,
            "items": [dict(row) for row in rows]
        }
