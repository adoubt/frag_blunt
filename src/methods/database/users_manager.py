import aiosqlite
from typing import Any
DB_PATH = "src/databases/database.db"
class UsersDatabase:

    @classmethod
    async def create_table(self):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                    f'''CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY,
                                                        is_banned INTEGER,
                                                        is_admin INTEGER,
                                                        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''') as cursor:
                pass

    @classmethod
    async def get_all(cls):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(f'SELECT * FROM users') as cursor:
                result = await cursor.fetchall()
                if not result:
                    return []
                return result

    @classmethod
    async def get_all_banned(cls):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(f'SELECT * FROM users WHERE is_banned=1') as cursor:
                result = await cursor.fetchall()
                if not result:
                    return []
                return result

    @classmethod
    async def get_user(cls, user_id: int):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(f'SELECT * FROM users WHERE user_id = {user_id}') as cursor:
                result = await cursor.fetchone()
                if not result:
                    return -1
                return result

    @classmethod
    async def create_user(
        cls,
        user_id: int,
        is_banned: int = 0,
        is_admin: int = 0,
    ):
        async with aiosqlite.connect(DB_PATH) as db:
            query = '''
            INSERT INTO users(
                "user_id", "is_banned", "is_admin"
            ) 
            VALUES (?, ?, ?)
            '''
            await db.execute(
                query,
                (user_id,is_banned, is_admin,)
            )
            await db.commit()


    @classmethod
    async def get_value(cls, user_id: int, key: Any):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(f'SELECT {key} FROM users WHERE user_id = {user_id}') as cursor:
                result = await cursor.fetchone()
                if not result:
                    return -1
                return result[0]

    @classmethod
    async def set_value(cls, user_id: int, key: Any, new_value: Any):
        async with aiosqlite.connect(DB_PATH) as db:
            if type(key) is int:
                await db.execute(f'UPDATE users SET {key}={new_value} WHERE user_id={user_id}')
            else:
                await db.execute(f'UPDATE users SET {key}=? WHERE user_id={user_id}',(new_value,))
            await db.commit()

    @classmethod        
    async def del_users(cls):
        async with aiosqlite.connect(DB_PATH) as db:
            
            await db.execute(f'DELETE from users')
            await db.commit()

    @classmethod
    async def add_points(cls, user_id: int, points: int):
        await cls.set_value(user_id, 'balance', (await cls.get_value(user_id, 'balance')) + points)

    @classmethod
    async def is_banned(cls, user_id: int):
        return await cls.get_value(user_id, 'is_banned')

    @classmethod
    async def is_admin(cls, user_id: int):
        return (await cls.get_value(user_id, 'is_admin')) == 1

