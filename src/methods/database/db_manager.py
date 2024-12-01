import aiosqlite
from typing import Any

DB_PATH = "src/databases/database.db"

class DbManager:

    @classmethod
    async def create_table(self):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute('''CREATE TABLE IF NOT EXISTS usernames(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                    username TEXT NOT NULL,
                                    status TEXT,
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    UNIQUE (username)
                                    )'''
                                  ) as cursor: pass
              
    @classmethod
    async def get_value(cls, key: Any, username:str):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(f'SELECT {key} FROM usernames WHERE username = {username}') as cursor:
                result = await cursor.fetchone()
                if not result:
                    return -1
                return result[0]
    @classmethod
    async def create_username(cls,username: str,status: str):
        async with aiosqlite.connect(DB_PATH) as db:
            query = '''
            INSERT OR IGNORE INTO usernames(
                "username", "status"
            ) 
            VALUES (?,?)
            '''
            await db.execute(query,(username,status,))
            await db.commit()
    @classmethod
    async def set_value(cls, username: str, key: Any, new_value: Any):
        async with aiosqlite.connect(DB_PATH) as db:
            if type(key) is int:
                await db.execute(f'UPDATE usernames SET {key}={new_value}, updated_at = CURRENT_TIMESTAMP WHERE username = {username}')
            else:
                await db.execute(f'UPDATE usernames SET {key}=?, updated_at = CURRENT_TIMESTAMP WHERE username = {username}',(new_value,))
            await db.commit()
    @classmethod
    async def del_usernames(cls):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(f'DELETE FROM usernames')
            await db.commit()
    @classmethod
    async def del_username(cls,username):        
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('DELETE FROM usernames WHERE username = ?',(username,))
            await db.commit()

    @classmethod
    async def get_latest_records(cls,parametr , status:str=None, ):
        query = '''
        SELECT * FROM usernames
        WHERE status = ?
        ORDER BY created_at DESC
        LIMIT ?;
        '''
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(query, (status,parametr,)) as cursor:
                rows = await cursor.fetchall()
                return rows
            
    @classmethod
    async def get_all_records(cls,):
        async with aiosqlite.connect(DB_PATH) as db:
                # Выполняем запрос для получения всех записей из таблицы
                query = "SELECT * FROM usernames"
                async with db.execute(query) as cursor:
                    # Получаем имена столбцов из cursor.description
                    columns = [description[0] for description in cursor.description]
                    # Получаем все строки
                    rows = await cursor.fetchall()
                    return rows, columns


