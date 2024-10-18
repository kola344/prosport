import asyncio
from database.db import messages

async def test():
    db = messages()
    await db.db_init()
    new = messages()
    await new.db_init()
    print(await db.get_messages())
    print(await new.get_messages())


asyncio.run(test())