import discord
from discord.ext import tasks, commands
from discord.ui import *
from func.send_chat import Chat
from func.server_config import *
from cogs.embed import Styled_Embed

class Event(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.Chat : Chat = self.bot.Chat
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return
        channel_id, chat_id = await self.Chat.search_database(GUILD.__name__, [GUILD.EVENT_CHANNEL_ID.name, GUILD.NOTIFY_CHAT_ID.name], {GUILD.GUILD_ID.name: member.guild.id})
        if not channel_id:
            return
        channel = self.bot.get_channel(int(channel_id))
        async with channel.typing():
            res = await self.Chat.send_event_reminder(chat_id, member.name)
            embed = Styled_Embed(self.bot, EMBED_TYPE.SHOW_EVENT, guild = member.guild.name, user_name = member.mention, res = res)
            await channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Event(bot))