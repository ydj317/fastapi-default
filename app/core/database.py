from databases import Database
from app.core.settings import settings

database = Database(
    settings.database_url,
    min_size=5,
    max_size=20,
)


