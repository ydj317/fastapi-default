# 마이그레이션
```bash
alembic revision --autogenerate -m "first commit"  # 마이그레이션 파일 생성
alembic upgrade head #마이그레이션

alembic downgrade base # 롤백
alembic history # 마이그레이션 이력 확인

```