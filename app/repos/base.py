from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# 메타데이터를 alembic에서 사용할 수 있도록 export
metadata = Base.metadata