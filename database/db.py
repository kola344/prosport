import aiosqlite
import sqlite3

class information_sync:
    def __init__(self):
        self.db = sqlite3.connect('database/db.db')
        self.cursor = self.db.cursor()

    def get_informations(self):
        self.cursor.execute("SELECT * FROM information")
        data = self.cursor.fetchall()
        return [{"id": i[0], "info": i[1], "description": i[2]} for i in data]

class users_sync:
    def __init__(self):
        self.db = sqlite3.connect('database/db.db')
        self.cursor = self.db.cursor()

    def unlock_messages(self, user_id):
        self.cursor.execute(f'UPDATE users SET lock_messages = 0 WHERE id = ?', (user_id,))
        self.db.commit()

class users:
    def __init__(self):
        self.db = None

    async def db_init(self):
        self.db = await aiosqlite.connect('database/db.db')

    async def add_user(self, user_id):
        await self.db.execute(f'INSERT INTO users VALUES (?, ?)', (user_id, 0))
        await self.db.commit()

    async def update_last_message(self, user_id, last_message):
        await self.db.execute(f'UPDATE users SET last_message = ? WHERE user_id = ?', (user_id, last_message))
        await self.db.commit()

    async def get_last_message(self, user_id):
        async with self.db.execute('SELECT last_message FROM users WHERE id = ?', (user_id,)) as cursor:
            data = await cursor.fetchone()
            return data[0]

    async def lock_messages(self, user_id):
        await self.db.execute(f'UPDATE users SET lock_messages = ? WHERE id = ?', (1, user_id))
        await self.db.commit()

    async def unlock_messages(self, user_id):
        await self.db.execute(f'UPDATE users SET lock_messages = ? WHERE id = ?', (0, user_id))
        await self.db.commit()

class information:
    def __init__(self):
        self.db = None

    async def db_init(self):
        self.db = await aiosqlite.connect('database/db.db')

    async def add_information(self):
        await self.db.execute(f'INSERT INTO information(info, description) VALUES(?, ?)', ('Информация', 'Описание'))
        await self.db.commit()

    async def get_informations(self):
        async with self.db.execute('SELECT * FROM information') as cursor:
            data = await cursor.fetchall()
            return [{"id": i[0], "info": i[1], "description": i[2]} for i in data]

    async def update_info(self, info_id, info):
        await self.db.execute(f'UPDATE information SET info = ? WHERE id = ?', (info, info_id))
        await self.db.commit()

    async def update_description(self, info_id, description):
        await self.db.execute(f'UPDATE information SET description = ? WHERE id = ?', (description, info_id))
        await self.db.commit()

    async def delete_info(self, info_id):
        await self.db.execute(f'DELETE FROM information WHERE id = ?', (info_id, ))
        await self.db.commit()

    async def truncate(self):
        await self.db.execute('DELETE FROM information')
        await self.db.commit()