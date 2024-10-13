from func.server_config import *
import aiosqlite
import asyncio
import os, re,traceback

async def fix():
    folder_path = 'database'
    all_files = os.listdir(folder_path)
    for path in all_files:
        path = "database/" + path
        await update_database_schema(path)
        #result = await search_database(path, GUILD.__name__, [GUILD.TASK_CHANNEL_ID.name, GUILD.NOTIFY_CHAT_ID.name], None)
        #await create_database(path)

async def update_database_schema(path):
    async with aiosqlite.connect(path) as db:
        try:
            cursor = await db.cursor()

            # 重命名表和列
            query_rename = 'ALTER TABLE BOT RENAME TO BOT_CHAT;'
            query_rename_column = 'ALTER TABLE CHANNEL RENAME COLUMN GUILD_ID TO CHANNEL_ID;'

            # 在 CHANNEL 表中新增 GUILD_ID 列
            #query_add_column = 'ALTER TABLE BOT ADD COLUMN CHARA_NAME TEXT;'
            quert_drop_column = 'ALTER TABLE BOT_CHAT DROP COLUMN CHARA_NAME;'

            # 创建 GUILD 表
            query_create_table = '''
                CREATE TABLE IF NOT EXISTS GUILD (
                    GUILD_ID TEXT PRIMARY KEY,
                    TASK_CHANNEL_ID TEXT,
                    ACCESS BOOLEAN
                );
            '''

            # 逐个执行 SQL 语句
            #await cursor.execute(query_rename)
            #await cursor.execute(query_rename_column)
            #await cursor.execute(query_add_column)
            await cursor.execute(quert_drop_column)
            #await cursor.execute(query_create_table)

            await db.commit()
        except Exception as e:
            print(f"Error updating database schema: {e}")
            
async def search_database(path, table: str, columns: list, conditions: dict):
        try:
            async with aiosqlite.connect(path) as db:
                cursor = await db.cursor()

                if columns:
                    columns_str = ', '.join(columns)
                else:
                    columns_str = '*'
                    
                if conditions:
                    conditions_str = ' AND '.join(f"{key} = ?" for key in conditions.keys())
                    query = f"SELECT {columns_str} FROM {table} WHERE {conditions_str}"
                    values = tuple(conditions.values())
                else:
                    query = f"SELECT {columns_str} FROM {table}"
                    values = ()

                await cursor.execute(query, values)
                result = await cursor.fetchall()
                
                if not result and columns and conditions:
                    # 若未找到結果且指定了columns和conditions，則返回[None, None]
                    result = [None for _ in columns]
                elif len(result) == 1:
                    result = result[0]
                else:
                    # 將結果進行格式轉換
                    result = [item[0] if isinstance(item, tuple) and len(item) == 1 else item for item in result]

                # 若結果是包含單一元素的元組，直接取該元素
                if isinstance(result, tuple) and len(result) == 1:
                    result = result[0]
                    
                return result
            
        except Exception as e:
            print(traceback.print_exc())

async def create_database(path):
    try:
        async with aiosqlite.connect(path) as db:
            cursor = await db.cursor()

            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS BOT (
                    BOT_ID INT PRIMARY KEY,
                    BOT_NAME TEXT,
                    CHARA_NAME TEXT
                );
            ''')

            await db.commit()
    except Exception as e:
        print(e)
        
asyncio.run(fix())