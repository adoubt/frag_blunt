from src.methods.database.db_manager import DbManager
from src.methods.database.users_manager import UsersDatabase

async def init_databases() -> None:
    await DbManager.create_table()
    await UsersDatabase.create_table()