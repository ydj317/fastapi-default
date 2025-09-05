from databases import Database

async def get_database(database_url: str, min_size: str, max_size: str):
    database = Database(
        database_url,
        min_size=min_size,
        max_size=max_size,
    )

    await database.connect()
    print("✅ Database connected")
    try:
        yield database
    finally:
        await database.disconnect()
        print("🔌 Database disconnected")


