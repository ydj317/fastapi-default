from databases import Database
from app.core.settings import settings

database = Database(settings.database_url)


