from database import db

users = db.users()
info = db.information()
info_sync = db.information_sync()
users_sync = db.users_sync()
async def initialize():
    await users.db_init()
    await info.db_init()