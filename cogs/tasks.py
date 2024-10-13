import discord
from discord.ext import tasks, commands
from discord.ui import *
from func.send_chat import Chat
from func.server_config import *
from func.msg_regex import clean_string
from cogs.embed import Styled_Embed
import datetime, pytz


class TaskTime(commands.Cog):
    tz = datetime.timezone(datetime.timedelta(hours=8))
    everyday_time = [
        datetime.time(hour = i, minute = 0, tzinfo = datetime.timezone(datetime.timedelta(hours = 8)))
        for i in (9, 12, 18, 23)
    ]
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.Chat: Chat = self.bot.Chat
        self.everyday.start()
    
    def get_taiwan_time(self):
        # 取得目前的本地時間
        local_time = datetime.datetime.now()

        # 取得目前的本地時區
        local_timezone = pytz.timezone('UTC')  # 使用協調世界時 (UTC) 作為初始時區
        local_time = local_timezone.localize(local_time)

        # 轉換為台灣時區
        taiwan_timezone = pytz.timezone('Asia/Taipei')
        taiwan_time = local_time.astimezone(taiwan_timezone)

        return taiwan_time

    @tasks.loop(time=everyday_time)
    async def everyday(self):
        channel_id_list = await self.Chat.search_database(GUILD.__name__, [GUILD.TASK_CHANNEL_ID.name, GUILD.NOTIFY_CHAT_ID.name], None)
        for channel_info in channel_id_list:
            if channel_info[0]:
                time = datetime.datetime.now(tz=self.tz).strftime('%H:%M')
                channel = self.bot.get_channel(int(channel_info[0]))
                async with channel.typing():
                    res = await self.Chat.send_task_reminder(channel_info[1], time)
                    res = clean_string(res)
                    embed = Styled_Embed(self.bot, EMBED_TYPE.SHOW_TASK, time = time, res = res)
                    await channel.send(embed=embed)
                
    @everyday.before_loop
    async def action_before(self):
        await self.bot.wait_until_ready()
        
    
def setup(bot: commands.Bot):
    bot.add_cog(TaskTime(bot))