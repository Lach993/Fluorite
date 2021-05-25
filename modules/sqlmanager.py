import aiosqlite
import time
dbname = "main.db"
forever = int(time.time())
async def init():
    async with aiosqlite.connect(dbname) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS stats
                    (   uuid text, 
                        star int, 
                        kills int, 
                        deaths int, 
                        finalKills int, 
                        finalDeaths int, 
                        level int, 
                        wins int, 
                        bedsBroken int, 
                        time int
                        ) ''')


        await db.execute('''CREATE TABLE IF NOT EXISTS users
                    (   uuid text, 
                        name text,
                        time int
                        )''')

        await db.execute('''CREATE TABLE IF NOT EXISTS cosmetics
                    (   uuid text, 
                        tophat int,
                        wings int,
                        time int
                        )''')

        await db.execute('''CREATE TABLE IF NOT EXISTS capes
                    (   uuid text, 
                        cape text, 
                        time int
                        )''')

        await db.execute('''CREATE TABLE IF NOT EXISTS stone
                    (   uuid text, 
                        num int,
                        time int
                        )''')

        await db.execute('''CREATE TABLE IF NOT EXISTS playing
                    (   uuid text, 
                        time int
                        )''')  
        
        await db.execute('''CREATE TABLE IF NOT EXISTS bedwars
                    (   uuid text, 
                        prefix text,
                        suffix text,
                        tab text,
                        above text, 
                        time int)''')
        
        await db.execute('''CREATE TABLE IF NOT EXISTS discord
                    (   uuid text,
                        id int,
                        time int)''')
        
        with open("cape.png", "br") as fp:
            b = fp.read()
        await db.execute("""insert into capes (uuid, cape, time) VALUES (?, ?, 1621863239)""", ["f1c3965e278f457c8e05c41852eb8314", b])
        await db.execute("""insert into capes (uuid, cape, time) VALUES (?, ?, 1621863239)""", ["443baadc5349495aa735a7d31c684042", b])
        await db.execute("""insert into discord (uuid, id, time) VALUES (?, ?, 1621863239)""", ["f1c3965e278f457c8e05c41852eb8314", 292134677936865280])
        await db.commit()

class sqlbase:
    def __init__(self):
        self.timeout: int
        self.insertQuery: str
        self.fetchQuery: str

    def get_time(self) -> int:
        return int(time.time())

    def calc_time_difference(self, now) -> int:
        return int(now - self.timeout)

    def get_time_difference(self) -> int:
        return int(self.calc_time_difference(self.get_time()))
    
    async def _insert(self, parms: list, query:str = None):
        if query == None:
            query = self.insertQuery
        parms = tuple(parms)
        async with aiosqlite.connect(dbname) as db:
            await db.execute(self.insertQuery, parms)
            await db.commit()

    async def _fetchone(self, parms: list, query:str = None):
        if query == None:
            query = self.fetchQuery
        query += " ORDER BY time ASC LIMIT 1"
        db = await aiosqlite.connect(dbname)
        parms = tuple(parms)
        cursor = await db.execute(query, parms)
        row = await cursor.fetchone()
        await cursor.close()
        await db.close()
        return row

    async def _fetchall(self, parms: list, query:str = None):
        if query == None:
            query = self.fetchQuery
        db = await aiosqlite.connect(dbname)
        parms = tuple(parms)
        print(parms)
        cursor = await db.execute(query, parms)
        rows = await cursor.fetchall()
        await cursor.close()
        await db.close()
        return rows

    async def _check(self, parms: list, query:str = None) -> bool:
        if query == None:
            query = self.fetchQuery
        parms = tuple(parms)
        ret = await self._fetchall(parms, query)
        return bool(ret)
    
    def _append_time(self, query: list) -> list:
        query.append(self.get_time())
        return query
    def _append_time_difference(self, query: list) -> list:
        query.append(self.get_time_difference())
        return query
    async def _fetchlatest(self, parms, query: list = None):
        if query == None:
            query = self.fetchQuery
        query += " ORDER BY time DESC LIMIT 1"
        db = await aiosqlite.connect(dbname)
        parms = tuple(parms)
        cursor = await db.execute(query, parms)
        row = await cursor.fetchone()
        await cursor.close()
        await db.close()
        return row
    
    def clean_uuid(self, uuid) -> str:
        if isinstance(uuid, (list, tuple)):
            uuid = uuid[0]
        return uuid

    def nested_sum(self, L):
        return sum( self.nested_sum(x) if isinstance(x, (list, tuple)) else x for x in L )

class users(sqlbase):
    def __init__(self):
        self.timeout = 1209600
        self.insertQuery = "INSERT INTO users (uuid, name, time) VALUES (?, ?, ?)"
        self.fetchQuery = "SELECT uuid FROM users WHERE name==? AND time>=?"

    async def insert(self, uuid:str, name:str):
        parms = [uuid, name]
        parms = self._append_time(parms)
        return await self._insert(parms)

    async def fetchone(self, name:str):
        parms = [name]
        parms = self._append_time_difference(parms)
        return await self._fetchone(parms)

    async def fetchall(self, name:str):
        parms = [name]
        parms = self._append_time_difference(parms)
        return await self._fetchall(parms)

    async def check(self, name:str) -> bool:
        parms = [name]
        parms = self._append_time_difference(parms)
        return await self._check(parms)

    async def fetchlatest(self, name:str):
        parms = [name]
        parms = self._append_time_difference(parms)
        return await self._fetchlatest(parms)

class cape(sqlbase):
    def __init__(self):
        self.timeout = forever
        self.insertQuery = "INSERT INTO capes (uuid, cape, time) VALUES (?, ?, ?)"
        self.fetchQuery = "SELECT cape FROM capes WHERE uuid==? AND time>=?"

    async def insert(self, uuid:str, bytes:str):
        parms = [uuid, bytes]
        parms = self._append_time(parms)
        return await self._insert(parms)

    async def fetchone(self, name:str):
        parms = [name]
        parms = self._append_time_difference(parms)
        return await self._fetchone(parms)

    async def fetchall(self, name:str):
        parms = [name]
        parms = self._append_time_difference(parms)
        return await self._fetchall(parms)

    async def check(self, name:str) -> bool:
        parms = [name]
        parms = self._append_time_difference(parms)
        return await self._check(parms)
    
    async def fetchlatest(self, name:str):
        parms = [name]
        parms = self._append_time_difference(parms)
        return await self._fetchlatest(parms)

class bedwars(sqlbase):
    def __init__(self):
        self.timeout = forever
        self.insertQuery = "INSERT INTO bedwars (uuid, prefix, suffix, tab, above, time) VALUES (?, ?, ?, ?, ?, ?)"
        self.fetchQuery = "SELECT prefix, suffix, tab, above FROM bedwars WHERE uuid==? AND time>=?"

    async def insert(self, uuid:str, prefix: str, suffix: str, tab: str, above:str):
        parms = [uuid, prefix, suffix, tab, above]
        parms = self._append_time(parms)
        return await self._insert(parms)

    async def fetchone(self, uuid:str):
        parms = [uuid]
        parms = self._append_time_difference(parms)
        return await self._fetchone(parms)

    async def fetchall(self, uuid:str):
        parms = [uuid]
        parms = self._append_time_difference(parms)
        return await self._fetchall(parms)

    async def check(self, uuid:str) -> bool:
        parms = [uuid]
        parms = self._append_time_difference(parms)
        print(parms)
        return await self._check(parms)
    
    async def fetchlatest(self, uuid:str):
        parms = [uuid]
        parms = self._append_time_difference(parms)
        print(parms)
        return await self._fetchlatest(parms)

class cosmetics(sqlbase):
    def __init__(self):
        self.timeout = forever
        self.insertQuery = "INSERT INTO cosmetics (uuid, tophat, wings, time) VALUES (?, ?, ?, ?)"
        self.fetchQuery = "SELECT tophat, wings FROM cosmetics WHERE uuid==? AND time>=?"

    async def insert(self, uuid:str, tophat:int, wings:int):
        parms = [self.clean_uuid(uuid), int(tophat), int(wings)]
        parms = self._append_time(parms)
        print(parms)
        return await self._insert(parms)

    async def fetchone(self, uuid:str):
        parms = [uuid]
        parms = self._append_time_difference(parms)
        return await self._fetchone(parms)

    async def fetchall(self, uuid:str):
        parms = [uuid]
        parms = self._append_time_difference(parms)
        return await self._fetchall(parms)

    async def check(self, uuid:str) -> bool:
        parms = [uuid]
        parms = self._append_time_difference(parms)
        return await self._check(parms)
        
    async def fetchlatest(self, uuid:str):
        parms = [uuid]
        parms = self._append_time_difference(parms)
        print(parms)
        return await self._fetchlatest(parms)

class stone(sqlbase):
    def __init__(self):
        self.timeout = forever
        self.insertQuery = "INSERT INTO stone (uuid, num, time) VALUES (?, ?, ?)"
        self.fetchQuery = "SELECT num FROM stone WHERE uuid==? AND time>=?"

    async def insert(self, uuid:str, num:int):
        parms = [self.clean_uuid(uuid), num]
        parms = self._append_time(parms)
        print(parms)
        return await self._insert(parms)

    async def fetchone(self, uuid:str):
        parms = [self.clean_uuid(uuid)]
        parms = self._append_time_difference(parms)
        return await self._fetchone(parms)

    async def fetchall(self, uuid:str):
        parms = [self.clean_uuid(uuid)]
        parms = self._append_time_difference(parms)
        return await self._fetchall(parms)

    async def check(self, uuid:str) -> bool:
        parms = [self.clean_uuid(uuid)]
        parms = self._append_time_difference(parms)
        return await self._check(parms)
    
    async def countall(self, uuid:str) -> int:
        """NON STANDARD - just implemented to make the main file look nicer"""
        uuid = self.clean_uuid(uuid)
        if await self.check(uuid):
            c = await self.fetchall(uuid)
            return self.nested_sum(c)
        return 0
        
    async def fetchlatest(self, uuid:str):
        parms = [uuid]
        parms = self._append_time_difference(parms)
        print(parms)
        return await self._fetchlatest(parms)      