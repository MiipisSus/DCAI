import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord import option
from func.server_config import *
from func.send_chat import Chat
from func.msg_regex import remove_ooc
from cogs.embed import Styled_Embed
from bot import DiscordBot
from discord.ui import *
import asyncio
import traceback

class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        print(discord.__version__)
        self.send_ooc_counter = 20
        self.bot: DiscordBot = bot
        self.execute_cmd = {}
        self.fix_button_flag = {}
        self.ooc_count = {}
        self.bot.loop.create_task(self.init_config())
    
    def cog_unload(self):
        super().cog_unload()
    
    #config initialize
    async def init_config(self):
        self.settings = self.bot.settings
        self.Chat: Chat = self.bot.Chat
        self.path = self.bot.path
        self.embed_color = self.settings[STYLE.__name__][STYLE.EMBED_COLOR]
        try:
            await self.Chat.update_database(CHANNEL.__name__, {CHANNEL.LAST_MESSAGE_ID.name: None}, None)
            await self.Chat.update_database(INDIVIDUALS.__name__, {INDIVIDUALS.LAST_MESSAGE_ID.name: None}, None)
        except:
            pass
        
    #func
    def check_flag(self, id):
        if id not in self.ooc_count:
            self.ooc_count[id] = 0
        if id not in self.fix_button_flag:
            self.fix_button_flag[id] = False
    
    async def check_last_msg_id(self, channel, user, chat_type):
        if chat_type == CHAT_TYPE.GROUP:
            last_message_id = await self.Chat.search_database(CHANNEL.__name__, 
                                                                [CHANNEL.LAST_MESSAGE_ID.name], 
                                                                {CHANNEL.CHANNEL_ID.name: channel.id})
        else:
            last_message_id = await self.Chat.search_database(INDIVIDUALS.__name__, 
                                                                [INDIVIDUALS.LAST_MESSAGE_ID.name], 
                                                                {INDIVIDUALS.USER_ID.name: user.id})
        if last_message_id:
            last_message = await channel.fetch_message(last_message_id)
            if any(isinstance(child, discord.components.Button) for row in last_message.components for child in row.children):
                await last_message.edit(view = None)
                self.fix_button_flag[channel.id] = False
            else:
                self.fix_button_flag[channel.id] = True
                
    async def update_last_msg_id(self, channel, user, msg_id, chat_type):
        if chat_type == CHAT_TYPE.GROUP:
            await self.Chat.update_database(CHANNEL.__name__, {CHANNEL.LAST_MESSAGE_ID.name: msg_id}, {CHANNEL.CHANNEL_ID.name: channel.id})
        else:
            await self.Chat.update_database(INDIVIDUALS.__name__, {INDIVIDUALS.LAST_MESSAGE_ID.name: msg_id}, {INDIVIDUALS.USER_ID.name: user.id})
            
    async def clean_last_msg_id(self, channel, user, chat_type):
        if chat_type == CHAT_TYPE.GROUP:
            last_message_id = await self.Chat.search_database(CHANNEL.__name__, 
                                                                [CHANNEL.LAST_MESSAGE_ID.name], 
                                                                {CHANNEL.CHANNEL_ID.name: channel.id})
        else:
            last_message_id = await self.Chat.search_database(INDIVIDUALS.__name__, 
                                                                [INDIVIDUALS.LAST_MESSAGE_ID.name], 
                                                                {INDIVIDUALS.USER_ID.name: user.id})
        if last_message_id:
            last_message = await channel.fetch_message(last_message_id)
            await last_message.edit(view = None)
        
        await self.update_last_msg_id(channel, user, None, chat_type)

    async def check_admin(self, user_id):
        admin = await self.Chat.search_database(ADMIN.__name__, [ADMIN.PRIVILAGE.name], {ADMIN.USER_ID.name: user_id})
        return admin
    
    async def cmd_name(self, author, channel, guild, new, chat_type):
        res = await self.Chat.send_Name_reminder(author, channel, guild, new, chat_type)
        return res
    
    async def cmd_NSFW(self, guild, user, channel, chat_type):
        res = await self.Chat.send_NSFW_reminder(guild, user, channel, chat_type)
        return res
    
    async def cmd_clean(self, num, id, chat_type):
        await self.Chat.clean_chat_history(int(num), id, chat_type)
    
    async def cmd_reset(self, id, chat_type):
        await self.Chat.reset_chat(id, chat_type)
        
    async def cmd_info(self, author, channel, chat_type):
        if chat_type == CHAT_TYPE.GROUP:
            user_name = await self.Chat.search_database(MEMBERS.__name__, 
                                                        [MEMBERS.USER_NAME.name], 
                                                        {MEMBERS.GUILD_ID.name: channel.id, MEMBERS.USER_ID.name: author.id})
        else:
            user_name = await self.Chat.search_database(INDIVIDUALS.__name__,
                                                        [INDIVIDUALS.USER_NAME.name],
                                                        {INDIVIDUALS.USER_ID.name: author.id})
        return user_name
    
    async def cmd_create_chat(self, src_text, src_bot_id, dst_bot_id, channel_id, ooc_text):
        #啟用新的bot_chat_id
        bot_chat_id = await self.Chat.initial_new_chat(src_bot_id, CHAT_TYPE.BOT)
        exist = await self.Chat.search_database(BOT_CHAT.__name__, None, {BOT_CHAT.CHANNEL_ID.name: channel_id, BOT_CHAT.BOT_ID.name: dst_bot_id})
        if not exist:
            await self.Chat.insert_database(BOT_CHAT.__name__,{BOT_CHAT.BOT_CHAT_ID.name: bot_chat_id,
                                                               BOT_CHAT.BOT_ID.name: dst_bot_id,
                                                               BOT_CHAT.CHANNEL_ID.name: channel_id})
        else:
            await self.Chat.update_database(BOT_CHAT.__name__, {BOT_CHAT.BOT_CHAT_ID.name: bot_chat_id},
                                                               {BOT_CHAT.BOT_ID.name: dst_bot_id, BOT_CHAT.CHANNEL_ID.name: channel_id})
        dst_bot = self.bot.get_bot_instance(dst_bot_id)
        bot_chat_id = await dst_bot.Chat.initial_new_chat(dst_bot_id, CHAT_TYPE.BOT)
        if not exist:
            await dst_bot.Chat.insert_database(BOT_CHAT.__name__,{BOT_CHAT.BOT_CHAT_ID.name: bot_chat_id,
                                                               BOT_CHAT.BOT_ID.name: src_bot_id,
                                                               BOT_CHAT.CHANNEL_ID.name: channel_id})
        else:
            await dst_bot.Chat.update_database(BOT_CHAT.__name__, {BOT_CHAT.BOT_CHAT_ID.name: bot_chat_id},
                                                               {BOT_CHAT.BOT_ID.name: src_bot_id, BOT_CHAT.CHANNEL_ID.name: channel_id})
        #傳送給自己的chat_id
        res, res_translated, safety_flag = await self.Chat.bot_chat_recv(dst_bot_id, channel_id, src_text, ooc_text)
        res = remove_ooc(res)
        res_translated = remove_ooc(res_translated)
        
        return res, res_translated, safety_flag
    
    async def process_bot_chat(self, dst_bot_id, text, channel_id):
        src_bot_id = self.bot.user.id
        channel = self.bot.get_channel(int(channel_id))
        async with channel.typing():
            res, res_translated, safety_flag = await self.Chat.bot_chat_recv(dst_bot_id, channel_id, text)
            if safety_flag:
                embed = Styled_Embed(self.bot, EMBED_TYPE.NSFW_FILTER)
            await channel.send(res_translated, embed = embed if safety_flag else None, view = BotChatButton(self, src_bot_id, dst_bot_id, channel_id, res))
   
    async def cmd_ooc(self, text, guild, user, channel, chat_type):
        text = await self.Chat.translate_send(text, None)
        text = f"(ooc: {text})"
        res, flag = await self.Chat.send_RP_reminder(guild, user, channel, text, chat_type)
        return res
    
    #cmd   
    @commands.slash_command(name = "name", description = "改變角色對自己的稱呼")
    async def name(self, interaction: discord.Interaction, name):
        try:
            channel, user, guild = interaction.channel, interaction.user, interaction.guild
            embed = Styled_Embed(self.bot, EMBED_TYPE.NAME_PROCESSING)
            await interaction.response.defer()
            msg = await interaction.followup.send(embed = embed)
            if isinstance(interaction.channel, discord.TextChannel):
                chat_type = CHAT_TYPE.GROUP 
                id = channel.id
            else:
                chat_type = CHAT_TYPE.INDIVIDUAL
                id = user.id
            
            await self.check_last_msg_id(channel, user, chat_type)
            res = await self.cmd_name(user, channel, guild, name, chat_type)
            await self.update_last_msg_id(channel, user, msg.id, chat_type)
            
            embed.init_embed_type(EMBED_TYPE.NAME_COMPLETE, old = interaction.user.name, new = name, res = res)
            await msg.edit(embed = embed, view = ChatButton(self, id, chat_type
                                                            , embed_res=EMBED_TYPE.NAME_COMPLETE, old = interaction.user.name, new = name))
        except Exception as e:
            print(traceback.print_exc())
            print(e)

    @commands.slash_command(name = "nsfw", description = "關閉NSFW過濾器")
    async def NSFW(self, interaction: discord.Interaction):
        try:
            channel, user, guild = interaction.channel, interaction.user, interaction.guild
            embed = Styled_Embed(self.bot, EMBED_TYPE.NSFW_PROCESSING)
            await interaction.response.defer()
            msg = await interaction.followup.send(embed = embed)
            if isinstance(interaction.channel, discord.TextChannel):
                chat_type = CHAT_TYPE.GROUP 
                id = channel.id
            else:
                chat_type = CHAT_TYPE.INDIVIDUAL
                id = user.id

            await self.check_last_msg_id(channel, user, chat_type)
            res = await self.cmd_NSFW(guild, user, channel, chat_type)
            await self.update_last_msg_id(channel, user, msg.id, chat_type)
            
            embed.init_embed_type(EMBED_TYPE.NSFW_COMPLETE, res = res)
            await msg.edit(embed = embed, view = ChatButton(self, id, chat_type, embed_res=EMBED_TYPE.NSFW_COMPLETE))
        except Exception as e:
            print(e)
        
    @commands.slash_command(name = "clean", description = "刪除指定數量的聊天紀錄")
    async def clean(self, interaction: discord.Interaction, msg_num):
        try:
            channel, user = interaction.channel, interaction.user
            if isinstance(interaction.channel, discord.TextChannel):
                chat_type = CHAT_TYPE.GROUP 
                id = channel.id
            else:
                chat_type = CHAT_TYPE.INDIVIDUAL
                id = user.id
            await self.cmd_clean(msg_num, id, chat_type)
            await self.clean_last_msg_id(channel, user, chat_type)
            embed = Styled_Embed(self.bot, EMBED_TYPE.CLEAN_COMPLETE, num = msg_num)
            await interaction.response.send_message(embed = embed)
        except Exception as e:
            print(e)
        
    @commands.slash_command(name = "reset", description = "重置角色聊天紀錄")
    async def reset(self, interaction: discord.Interaction):
        try:
            channel, user = interaction.channel, interaction.user
            await interaction.response.defer()
            embed = Styled_Embed(self.bot, EMBED_TYPE.RESET_PROCESSING)
            msg = await interaction.followup.send(embed=embed)
            if isinstance(interaction.channel, discord.TextChannel):
                chat_type = CHAT_TYPE.GROUP 
                id = channel.id
            else:
                chat_type = CHAT_TYPE.INDIVIDUAL
                id = user.id
            await self.cmd_reset(id, chat_type)
            await self.clean_last_msg_id(channel, user, chat_type)
            embed.init_embed_type(EMBED_TYPE.RESET_COMPLETE)
            await msg.edit(embed = embed)
        except Exception as e:
            print(e)
            
    @commands.slash_command(name = "info", description = "取得Bot基本資訊與目前使用名稱")
    async def info(self, interaction: discord.Interaction):
        try:
            chat_type = CHAT_TYPE.GROUP if isinstance(interaction.channel, discord.TextChannel) else CHAT_TYPE.INDIVIDUAL
            user_name = await self.cmd_info(interaction.user, interaction.channel, chat_type)
            embed = Styled_Embed(self.bot, EMBED_TYPE.SHOW_INFO, user_name = user_name)
            await interaction.response.send_message(embed = embed, ephemeral=True)
        except Exception as e:
            print(e)
    
    @commands.slash_command(name = "list", description = "取得命令清單")
    async def list(self, interaction: discord.Interaction):
        try:
            admin = await self.check_admin(interaction.user.id)
            embed = Styled_Embed(self.bot, EMBED_TYPE.SHOW_LIST)
            chat_type = CHAT_TYPE.GROUP if isinstance(interaction.channel, discord.TextChannel) else CHAT_TYPE.INDIVIDUAL
            await interaction.response.send_message(content = "", view=CommandSelectMenu(self, chat_type, admin)
                                                    , embed=embed, ephemeral=True)
        except Exception as e:
            print(e)
    
    @commands.slash_command(name = "ooc", description = "提醒角色設定/故事走向/其他")
    async def ooc(self, interaction: discord.Interaction, text):
        channel, user, guild = interaction.channel, interaction.user, interaction.guild
        await interaction.response.defer()
        embed = Styled_Embed(self.bot, EMBED_TYPE.OOC_PROCESSING)
        msg = await interaction.followup.send(embed=embed)
        if isinstance(interaction.channel, discord.TextChannel):
            chat_type = CHAT_TYPE.GROUP 
            id = channel.id
        else:
            chat_type = CHAT_TYPE.INDIVIDUAL
            id = user.id
        
        await self.check_last_msg_id(channel, user, chat_type)
        res = await self.cmd_ooc(text, guild, user, channel, chat_type)
        await self.update_last_msg_id(channel, user, msg.id, chat_type)
        
        embed.init_embed_type(EMBED_TYPE.OOC_COMPLETE, res = res)
        await msg.edit(embed = embed, view = ChatButton(self, id, chat_type, embed_res=EMBED_TYPE.OOC_COMPLETE))
    
    @commands.slash_command(name = "rp", description = "開始與角色的故事扮演")
    async def rp(self, interaction: discord.Interaction):
        chat_type = CHAT_TYPE.GROUP if isinstance(interaction.channel, discord.TextChannel) else CHAT_TYPE.INDIVIDUAL
        await interaction.response.send_modal(RPInput_Modal(self, interaction.user, interaction.channel, interaction.guild, chat_type))
            
    @commands.slash_command(name = "status", description = "變更狀態（管理員）")
    async def status(self, interaction: discord.Interaction, status):
        try:
            admin = await self.check_admin(interaction.user.id)
            if not admin:
                embed = Styled_Embed(self.bot, EMBED_TYPE.CHECK_PRIVILAGE)
                await interaction.response.send_message(embed = embed, ephemeral=True)
                return
            embed = Styled_Embed(self.bot, EMBED_TYPE.STATUS_COMPLETE, status = status)
            modify_configs(self.path, BOT_SETTING.__name__, BOT_SETTING.STATUS.name, status)
            await self.bot.change_presence(activity=discord.Game(name=status))
            await interaction.response.send_message(embed = embed, ephemeral=True)
        except Exception as e:
            print(e)
                
    @commands.slash_command(name = "reboot", description = "重啟Bot（管理員）")
    async def reboot(self, interaction: discord.Interaction):
        try:
            admin = await self.check_admin(interaction.user.id)
            if not admin:
                embed = Styled_Embed(self.bot, EMBED_TYPE.CHECK_PRIVILAGE)
                await interaction.response.send_message(embed = embed, ephemeral=True)
                return
            embed = Styled_Embed(self.bot, EMBED_TYPE.REBOOT_PROCESSING)
            await interaction.response.defer(ephemeral=True)
            msg = await interaction.followup.send(embed = embed, ephemeral=True)
            await self.bot.reboot()
            embed.init_embed_type(EMBED_TYPE.REBOOT_COMPLETE)
            await msg.edit(embed = embed)
        except Exception as e:
            print(e)
    
    @commands.slash_command(name = "admin", description = "指定其他使用者為管理員（管理員）")
    @option(name = "user", descriptions = "請選擇欲指定的管理員...", input_type = discord.User)
    async def admin(self, interaction: discord.Interaction, user: discord.User):
        if isinstance(interaction.channel, discord.DMChannel):
            embed = Styled_Embed(self.bot, EMBED_TYPE.DM_NOT_AVALIABLE)
            interaction.response.send_message(embed=embed, ephemeral=True)
            return
        try:
            admin = await self.check_admin(interaction.user.id)
            if not admin:
                embed = Styled_Embed(self.bot, EMBED_TYPE.CHECK_PRIVILAGE)
                await interaction.response.send_message(embed = embed, ephemeral=True)
                return
            admin = await self.check_admin(user.id)
            if not admin:
                await self.Chat.insert_database(ADMIN.__name__, {ADMIN.USER_ID.name: user.id, ADMIN.PRIVILAGE.name: True})
                embed = Styled_Embed(self.bot, EMBED_TYPE.ADMIN_COMPLETE, user = user.name)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            print(e)
    
    @commands.slash_command(name = "event", description = "在特定頻道啟用訊息功能")
    @option(name = "type", description = "選擇啟用功能", choices = ["報時功能（早上/中午/晚上）", "歡迎新成員訊息功能"])
    @option(name = "state", description = "選擇功能狀態", choices = ["啟用", "禁用"])
    async def event(self, interaction: discord.Interaction, type: str, state: str):
        if isinstance(interaction.channel, discord.DMChannel):
            embed = Styled_Embed(self.bot, EMBED_TYPE.DM_NOT_AVALIABLE)
            interaction.response.send_message(embed=embed, ephemeral=True)
            return
        try:   
            admin = await self.check_admin(interaction.user.id)
            if not admin:
                embed = Styled_Embed(self.bot, EMBED_TYPE.CHECK_PRIVILAGE)
                await interaction.response.send_message(embed = embed, ephemeral=True)
                return
            if type == "報時功能（早上/中午/晚上）":
                if state == "啟用":
                    await interaction.response.send_message(view=ChannelSelectMenu(self, "schedule"), ephemeral=True)
                else:
                    await self.Chat.update_database(GUILD.__name__, {GUILD.TASK_CHANNEL_ID.name: None}, {GUILD.GUILD_ID.name: interaction.guild.id})
                    embed = Styled_Embed(self.bot, EMBED_TYPE.TASK_EVENT_DISABLED, func = type)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                if state == "啟用":
                    await interaction.response.send_message(view=ChannelSelectMenu(self, "welcome"), ephemeral=True)
                else:
                    await self.Chat.update_database(GUILD.__name__, {GUILD.EVENT_CHANNEL_ID.name: None}, {GUILD.GUILD_ID.name: interaction.guild.id})
                    embed = Styled_Embed(self.bot, EMBED_TYPE.TASK_EVENT_DISABLED, func = type)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    
        except Exception as e:
            print(e)
            
    async def get_bot_list(self, ctx: discord.AutocompleteContext):
        if not ctx.interaction.guild:
            return []
        avaliable_bot_list = []
        bot_list = await self.Chat.search_database(BOT.__name__, [BOT.BOT_NAME.name, BOT.BOT_ID.name], None)
        for bot in bot_list:
            avaliable = await ctx.interaction.guild.fetch_member(int(bot[1]))
            if avaliable:
                avaliable_bot_list.append(bot[0])
        return avaliable_bot_list
    
    async def get_story_list(self, ctx: discord.AutocompleteContext):
        bot_name = ctx.options["bot_name"]
        bot_id = await self.Chat.search_database(BOT.__name__, [BOT.BOT_ID.name], {BOT.BOT_NAME.name: bot_name})
        started = await self.Chat.search_database(BOT_CHAT.__name__, None, 
                                                  {BOT_CHAT.BOT_ID.name: bot_id, BOT_CHAT.CHANNEL_ID.name: ctx.interaction.channel.id})
        if started:
            return ["重置", "繼續"]
        else:
            return ["開始"]
        
    
    async def get_topic_list(self, ctx: discord.AutocompleteContext):
        choice = ctx.options["story"]
        if choice in ("重置", "開始"):
            return ["詳細設定（RP）", "簡單設定（OOC）", "略過"]
        else:
            bot_name = ctx.options["bot_name"]
            bot_id = await self.Chat.search_database(BOT.__name__, [BOT.BOT_ID.name], {BOT.BOT_NAME.name: bot_name})
            start = await self.Chat.search_database(BOT_CHAT.__name__, [BOT_CHAT.STATE.name], 
                                                    {BOT_CHAT.BOT_ID.name: bot_id, BOT_CHAT.CHANNEL_ID.name: ctx.interaction.channel.id})
            start_name = self.bot.user.name if start else bot_name
            return [f"從{start_name}的最後一則訊息繼續："]
    
    @commands.slash_command(name = "chat", description = "開始與其他角色的聊天")
    @option(name = "bot_name", description = "選擇其他角色", autocomplete = get_bot_list)
    @option(name = "story", description = "重置/繼續", autocomplete = get_story_list)
    @option(name = "topic", description = "選擇使用Role Play Topic（角色設定故事）", autocomplete = get_topic_list)
    async def create_chat(self, interaction: discord.Interaction, bot_name: str, story: str, topic: str):
        if self.settings[PROGRAM_SETTING.__name__][PROGRAM_SETTING.BOT_GROUP_CHAT]:
            embed = Styled_Embed(self.bot, EMBED_TYPE.BOT_CHAT_DISABLED)
            interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if isinstance(interaction.channel, discord.DMChannel):
            embed = Styled_Embed(self.bot, EMBED_TYPE.DM_NOT_AVALIABLE)
            interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if story in ("重置", "開始"):
            async with interaction.channel.typing():
                src_bot_id = self.bot.user.id
                src_chara_name = self.settings[PYCAI_SETTING.__name__][PYCAI_SETTING.CHAR_NAME]
                channel_id = interaction.channel.id
                dst_bot_id, dst_chara_name = await self.Chat.search_database(BOT.__name__, [BOT.BOT_ID.name, BOT.CHARA_NAME.name],
                                                                                    {BOT.BOT_NAME.name: bot_name})
                if topic == "詳細設定（RP）":
                    await interaction.response.send_modal(RPInput_Modal(self, None, interaction.channel, None, chat_type=CHAT_TYPE.BOT, src_bot_id = src_bot_id,
                                                                        dst_bot_id=dst_bot_id, src_chara_name = src_chara_name, dst_chara_name = dst_chara_name,
                                                                        channel_id = channel_id))
                elif topic == "簡單設定（OOC）":
                    await interaction.response.send_modal(TextInput_Modal(self, "ooc", None, interaction.channel, None, CHAT_TYPE.BOT, src_bot_id = src_bot_id,
                                                                        dst_bot_id=dst_bot_id, src_chara_name = src_chara_name, dst_chara_name = dst_chara_name,
                                                                        channel_id = channel_id, start = True))
                else:
                    
                        embed = Styled_Embed(self.bot, EMBED_TYPE.BOT_CHAT_EMBED, bot_name = bot_name, status = "on", topic = "on")
                        await interaction.response.send_message(embed=embed)
                        src_text = f"(ooc: The character you will chat with is {dst_chara_name}\n\
                                    Please be careful not to actively use ooc, just follow my ooc instructions\n\
                                    Story start!)"
                        dst_text = f"(ooc: The character you will chat with is {src_chara_name}\n\
                                    Please be careful not to actively use ooc, just follow my ooc instructions\n\
                                    Story start!)"
                        res, res_translated, safety_flag = await self.cmd_create_chat(src_text, src_bot_id, dst_bot_id, interaction.channel.id, dst_text)
                        if safety_flag:
                            embed = Styled_Embed(self.bot, EMBED_TYPE.NSFW_FILTER)
                        view = BotChatButton(self, src_bot_id, dst_bot_id, channel_id, res, dst_text)
                        await interaction.followup.send(res_translated, embed = embed if safety_flag else None, view = view)
        else:
            embed = Styled_Embed(self.bot, EMBED_TYPE.BOT_CHAT_EMBED, bot_name = bot_name, status = "on")
            await interaction.response.send_message(embed = embed)
            src_bot_id = self.bot.user.id
            dst_bot_id = await self.Chat.search_database(BOT.__name__, [BOT.BOT_ID.name],{BOT.BOT_NAME.name: bot_name})
            channel_id = interaction.channel.id
            state, send_text = await self.Chat.search_database(BOT_CHAT.__name__, [BOT_CHAT.STATE.name, BOT_CHAT.LAST_MESSAGE_TEXT.name],
                                                               {BOT_CHAT.BOT_ID.name: dst_bot_id, BOT_CHAT.CHANNEL_ID.name: channel_id})
            dst_bot = self.bot.get_bot_instance(dst_bot_id)
            if state:
                await self.Chat.update_database(BOT_CHAT.__name__, {BOT_CHAT.STATE.name: False}, 
                                                {BOT_CHAT.BOT_ID.name: dst_bot_id, BOT_CHAT.CHANNEL_ID.name: channel_id})
                await self.bot.send_bot_chat(src_bot_id, dst_bot_id, send_text, channel_id)
            else:
                await dst_bot.Chat.update_database(BOT_CHAT.__name__, {BOT_CHAT.STATE.name: False},
                                                {BOT_CHAT.BOT_ID.name: dst_bot_id, BOT_CHAT.CHANNEL_ID.name: channel_id})
                send_text = await dst_bot.Chat.search_database(BOT_CHAT.__name__, [BOT_CHAT.LAST_MESSAGE_TEXT.name],
                                                               {BOT_CHAT.BOT_ID.name: dst_bot_id, BOT_CHAT.CHANNEL_ID.name: channel_id})
                await self.process_bot_chat(dst_bot_id, send_text, channel_id)
                
        return
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        elif message.author.bot:
            return
        user = message.author
        channel = message.channel
        guild = message.guild
        self.check_flag(channel.id)
        
        if isinstance(message.channel, discord.DMChannel):
            try:
                if not self.settings[PROGRAM_SETTING.__name__][PROGRAM_SETTING.INDIVIDUAL_CHAT]:
                    return
                
                async with message.channel.typing():
                    #查找該User最後一則message id
                    await self.check_last_msg_id(channel, user, CHAT_TYPE.INDIVIDUAL)
                        
                    response, flag = await self.Chat.send_chat(message.clean_content, guild, channel, user, self.bot.user, CHAT_TYPE.INDIVIDUAL)
                embed = Styled_Embed(self.bot, EMBED_TYPE.NSFW_FILTER)
                #Fix Continuously Send Message View
                if self.fix_button_flag[channel.id]:
                    view = None
                    self.fix_button_flag[channel.id] = False
                else:
                    view = ChatButton(self, user.id, CHAT_TYPE.INDIVIDUAL)
                    
                res = await asyncio.wait_for(message.reply(f"{response}", 
                                                            view = view, 
                                                            embed = embed if flag else None), timeout = 10)
                    
                #更新最後一則message id
                await self.update_last_msg_id(channel, user, res.id, CHAT_TYPE.INDIVIDUAL)
                    
            except asyncio.TimeoutError:
                message.reply("**[Log] Proccessing timeout, please try again, sorry!**")
            except Exception as e:
                print(traceback.print_exc())
                print(e)
                
        elif self.bot.user.mentioned_in(message) and isinstance(message.channel, discord.TextChannel):
            if not self.settings[PROGRAM_SETTING.__name__][PROGRAM_SETTING.CHANNEL_GROUP_CHAT]:
                return
            try:
                async with message.channel.typing():
                    #查找該Guild最後一則message id
                    await self.check_last_msg_id(channel, user, CHAT_TYPE.GROUP)

                    response, flag = await self.Chat.send_chat(message.clean_content, guild, channel, user, self.bot.user, CHAT_TYPE.GROUP)
                    
                embed = Styled_Embed(self.bot, EMBED_TYPE.NSFW_FILTER)
                if self.fix_button_flag[channel.id]:
                    view = None
                    self.fix_button_flag[channel.id] = False
                else:
                    view = ChatButton(self, channel.id, CHAT_TYPE.GROUP)
                    
                res = await asyncio.wait_for(message.reply(f"{response}", 
                                                            view = view, 
                                                            embed = embed if flag else None), timeout = 10)
                
                '''self.ooc_count[channel.id] += 1
                if self.ooc_count[channel.id] >= DEFINE_OOC_COUNT:
                    await self.Chat.send_ooc_reminder(channel.id)
                    self.ooc_count[channel.id] = 0'''
                    
                #更新最後一則message id
                await self.update_last_msg_id(channel, user, res.id, CHAT_TYPE.GROUP)
            except asyncio.TimeoutError:
                message.reply("**[Log] Proccessing timeout, please try again, sorry!**")
            except Exception as e:
                print(traceback.print_exc())
                print(e)
            
class BotChatButton(discord.ui.View):
    def __init__(self, parent: Main, src_bot_id, dst_bot_id, channel_id, send_text = None, ooc = None):
        super().__init__(timeout = 100000)
        self.parent = parent
        self.src_bot_id = src_bot_id
        self.dst_bot_id = dst_bot_id
        self.channel_id = channel_id
        self.send_text = send_text
        self.ooc = ooc if ooc else ""
    
    @discord.ui.button(custom_id="oocButton", label="", style=discord.ButtonStyle.secondary, emoji="💡")
    async def ooc_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        original_msg = await interaction.channel.fetch_message(interaction.message.id)
        try:
            await interaction.response.send_modal(TextInput_Modal(self.parent, "ooc", None, None, None, CHAT_TYPE.BOT, src_bot_id = self.src_bot_id,
                                                                dst_bot_id = self.dst_bot_id, src_chara_name = None, dst_chara_name = None,
                                                                channel_id = self.channel_id))
        except Exception as e:
            print(traceback.print_exc())
    
    @discord.ui.button(custom_id="refreshButton", label="", style=discord.ButtonStyle.secondary, emoji="🔄")
    async def refresh_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        original_msg = await interaction.channel.fetch_message(interaction.message.id)
        embed = Styled_Embed(self.parent.bot, EMBED_TYPE.REFRESH_LAST_MESSAGE)
        await original_msg.edit(embed = embed, view = None)
        await interaction.response.defer()
        try:
            response, response_translated, flag = await self.parent.Chat.refresh_chat(self.dst_bot_id, self.channel_id, CHAT_TYPE.BOT)
            if response == None:
                response = ""
            if flag:
                embed.init_embed_type(EMBED_TYPE.NSFW_FILTER)
            self.send_text = response
            await self.parent.Chat.update_database(BOT_CHAT.__name__, {BOT_CHAT.LAST_MESSAGE_TEXT.name: f"{self.ooc}\n{response}"},
                                                   {BOT_CHAT.BOT_ID.name: self.dst_bot_id, BOT_CHAT.CHANNEL_ID.name: self.channel_id})
            await original_msg.edit(f"{response_translated}", embed = embed if flag else None, view = self)
        except Exception as e:
            print(traceback.print_exc())
    
    @discord.ui.button(custom_id="continueButton", label="", style=discord.ButtonStyle.secondary, emoji="➡️")
    async def continue_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            await self.parent.Chat.update_database(BOT_CHAT.__name__, {BOT_CHAT.STATE.name: False},
                                                   {BOT_CHAT.BOT_ID.name: self.dst_bot_id, BOT_CHAT.CHANNEL_ID.name: self.channel_id})
            original_msg = await interaction.channel.fetch_message(interaction.message.id)
            if not self.send_text:
                self.send_text = original_msg.content
            await original_msg.edit(view=None)
            await interaction.response.defer()
            await self.parent.bot.send_bot_chat(self.src_bot_id, self.dst_bot_id, f"{self.ooc}\n{self.send_text}", self.channel_id)
        except Exception as e:
            print(e)
            
        
class ChatButton(discord.ui.View):
    def __init__(self, parent: Main, id, chat_type, embed_res = None, **kwargs):
        super().__init__(timeout = 100000)
        self.parent = parent
        self.id = id
        self.chat_type = chat_type
        self.embed_res = embed_res
        self.kwargs = kwargs
    
    @discord.ui.button(custom_id="removeButton", label="", style=discord.ButtonStyle.secondary, emoji="❌")
    async def remove_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.parent.Chat.clean_chat_history(2, self.id, self.chat_type)
        await self.parent.clean_last_msg_id(interaction.channel, interaction.user, self.chat_type)
        embed = Styled_Embed(self.parent.bot, EMBED_TYPE.REMOVE_LAST_MESSAGE)
        original_msg = await interaction.channel.fetch_message(interaction.message.id)
        await original_msg.edit(content="", embed=embed, view=None)
        
    @discord.ui.button(custom_id="refreshButton", label="", style=discord.ButtonStyle.secondary, emoji="🔄")
    async def refresh_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        original_msg = await interaction.channel.fetch_message(interaction.message.id)
        embed = Styled_Embed(self.parent.bot, EMBED_TYPE.REFRESH_LAST_MESSAGE)
        await original_msg.edit(embed = embed, view = None)
        await interaction.response.defer()
        try:
            response, flag = await self.parent.Chat.refresh_chat(self.id, chat_type= self.chat_type)
            if response == None:
                response = ""
            if self.embed_res:
                if flag:
                    embed_2 = Styled_Embed(EMBED_TYPE.NSFW_FILTER)
                if self.embed_res == EMBED_TYPE.NAME_COMPLETE:
                    embed.init_embed_type(self.embed_res, new = self.kwargs["new"], old = self.kwargs["old"], res = response)
                else:
                    embed.init_embed_type(self.embed_res, res = response)
                await original_msg.edit(embeds = [embed, embed_2] if flag else [embed], view=self)
            else:
                if flag:
                    embed.init_embed_type(EMBED_TYPE.NSFW_FILTER)
                await original_msg.edit(f"{response}", embed = embed if flag else None, view = self)
            
        except Exception as e:
            print(traceback.print_exc())
            
    @discord.ui.button(custom_id="continueButton", label="", style=discord.ButtonStyle.secondary, emoji="➡️")
    async def continue_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            user, channel, guild = interaction.user, interaction.channel, interaction.guild
            if self.chat_type == CHAT_TYPE.GROUP:
                async with channel.typing():
                    await self.parent.check_last_msg_id(channel, user, self.chat_type)
                    response, flag = await self.parent.Chat.send_RP_reminder(guild, user, channel, "(Continue)", self.chat_type)
                    if response == None:
                        response = ""
                    if flag:
                        embed = Styled_Embed(self.parent.bot, EMBED_TYPE.NSFW_FILTER)
                    res = await interaction.followup.send(f"{response}", embed = embed if flag else None, view = ChatButton(self.parent, self.id, self.chat_type))
                    await self.parent.update_last_msg_id(channel, user, res.id, self.chat_type)
            else:
                await channel.trigger_typing()
                await self.parent.check_last_msg_id(channel, user, self.chat_type)
                response, flag = await self.parent.Chat.send_RP_reminder(guild, user, channel, "(Continue)", self.chat_type)
                if response == None:
                    response = ""
                if flag:
                    embed = Styled_Embed(self.parent.bot, EMBED_TYPE.NSFW_FILTER)
                res = await interaction.followup.send(f"{response}", embed = embed if flag else None, view = ChatButton(self.parent, self.id, self.chat_type))
                await self.parent.update_last_msg_id(channel, user, res.id, self.chat_type)
            
        except Exception as e:
            print(e)


class CommandList(discord.ui.Select):
    def __init__(self, parent: Main, chat_type, admin = False):
        options = [
            discord.SelectOption(value="info", label="Bot資訊", description="取得Bot基本資訊與目前使用名稱", default=False),
            discord.SelectOption(value="name", label="修改暱稱", description="改變角色對自己的稱呼", default=False),
            discord.SelectOption(value="clean", label="清除歷史", description="刪除指定數量的聊天紀錄", default=False),
            discord.SelectOption(value="reset", label="重置聊天", description="重置角色聊天紀錄", default=False),
            discord.SelectOption(value="NSFW", label="NSFW", description="關閉NSFW過濾器", default=False),
            discord.SelectOption(value="RP", label="Role Play", description="開始與角色的故事扮演", default=False),
            discord.SelectOption(value="ooc", label="角色提示", description="提醒角色設定/故事走向/其他", default=False)
            ]
        if admin:
            options.extend([discord.SelectOption(value="status", label="變更狀態", description="更改角色上線狀態", default=False),
                            discord.SelectOption(value="reboot", label="重啟Bot", description="重新啟動Bot\n", default=False),
                            discord.SelectOption(value="admin", label="管理權限", description="指定其他使用者為管理員", default=False)])
        self.chat_type = chat_type
        self.parent = parent
        super().__init__(placeholder = "選擇欲執行的命令...", max_values = 1, min_values = 1,
                         options = options)
    
    async def callback(self, interaction: Interaction):
        user, channel, guild = interaction.user, interaction.channel, interaction.guild
        if self.values[0] == "RP":
            await interaction.response.send_modal(RPInput_Modal(self.parent, user, channel, guild, self.chat_type))
        if self.values[0] in ("name", "clean", "status", "ooc"):
            await interaction.response.send_modal(TextInput_Modal(self.parent, self.values[0], user, channel, guild, self.chat_type))
        elif self.values[0] == "info":
            await interaction.response.defer(ephemeral=True)
            user_name = await self.parent.cmd_info(interaction.user, interaction.channel, self.chat_type)
            embed = Styled_Embed(self.parent.bot, EMBED_TYPE.SHOW_INFO, user_name = user_name)
            await interaction.followup.send(embed = embed, ephemeral=True)
        elif self.values[0] == "reset":
            await interaction.response.defer()
            id = channel.id if self.chat_type == CHAT_TYPE.GROUP else user.id
            await self.parent.cmd_reset(id, self.chat_type)
            await self.parent.clean_last_msg_id(channel, user, self.chat_type)
            embed = Styled_Embed(self.parent.bot, EMBED_TYPE.RESET_COMPLETE)
            await interaction.followup.send(embed = embed)
        elif self.values[0] == "NSFW":
            await interaction.response.defer()
            embed = Styled_Embed(self.parent.bot, EMBED_TYPE.NSFW_PROCESSING)
            id = channel.id if self.chat_type == CHAT_TYPE.GROUP else user.id
            msg = await interaction.followup.send(embed = embed)
            await self.parent.check_last_msg_id(channel, user, self.chat_type)
            res = await self.parent.cmd_NSFW(guild, user, channel, self.chat_type)
            await self.parent.update_last_msg_id(channel, user, msg.id, self.chat_type)
            embed.init_embed_type(EMBED_TYPE.NSFW_COMPLETE, res = res)
            await msg.edit(embed = embed, view = ChatButton(self.parent, id, self.chat_type, embed_res=EMBED_TYPE.NSFW_COMPLETE))
        elif self.values[0] == "admin":
            await interaction.response.send_message(view=UserSelectMenu(self.parent), ephemeral=True)

        
class CommandSelectMenu(discord.ui.View):
    def __init__(self, parent, chat_type, admin):
        super().__init__(timeout=100000)
        self.parent = parent
        self.add_item(CommandList(parent, chat_type, admin))


class UserSelectMenu(discord.ui.View):
    def __init__(self, parent: Main):
        self.parent = parent
        super().__init__(timeout=100000)
        
    @discord.ui.user_select(placeholder="請選擇欲指定的管理員...", min_values=1, max_values=1)
    async def callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        admin = await self.parent.check_admin(select.values[0].id)
        if not admin:
            await self.parent.Chat.insert_database(ADMIN.__name__, {ADMIN.USER_ID.name: select.values[0].id, ADMIN.PRIVILAGE.name: True})
        embed = Styled_Embed(self.parent.bot, EMBED_TYPE.ADMIN_COMPLETE, user = select.values[0].name)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class ChannelSelectMenu(discord.ui.View):
    def __init__(self, parent: Main, cmd_type):
        self.parent = parent
        self.cmd_type = cmd_type
        super().__init__(timeout=100000)
    
    @discord.ui.channel_select(placeholder="請選擇欲指定的頻道...（僅能選擇一個）", min_values=1, max_values=1)
    async def callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        guild_exist = await self.parent.Chat.search_database(GUILD.__name__, None, {GUILD.GUILD_ID.name: interaction.guild.id})
        if not guild_exist:
            await self.parent.Chat.insert_database(GUILD.__name__, {GUILD.GUILD_ID.name: interaction.guild.id,
                                                        GUILD.ACCESS.name: True})
        if self.cmd_type == "schedule":
            await self.parent.Chat.update_database(GUILD.__name__, {GUILD.TASK_CHANNEL_ID.name: select.values[0].id}, {GUILD.GUILD_ID.name: interaction.guild.id})
        else:
            await self.parent.Chat.update_database(GUILD.__name__, {GUILD.EVENT_CHANNEL_ID.name: select.values[0].id}, {GUILD.GUILD_ID.name: interaction.guild.id})
        embed = Styled_Embed(self.parent.bot, EMBED_TYPE.TASK_COMPLETE, channel = select.values[0].name)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        chat_id = await self.parent.Chat.search_database(GUILD.__name__, [GUILD.NOTIFY_CHAT_ID.name], {GUILD.GUILD_ID.name: interaction.guild.id})
        if not chat_id:
            chat_id = await self.parent.Chat.initial_new_chat(interaction.guild.id, CHAT_TYPE.NOTIFY)
            await self.parent.Chat.update_database(GUILD.__name__, {GUILD.NOTIFY_CHAT_ID.name: chat_id}, {GUILD.GUILD_ID.name: interaction.guild.id})
    
class TextInput_Modal(discord.ui.Modal):
    def __init__(self, parent: Main, cmd_type, user = None, channel = None, guild = None, chat_type = None, **kwargs) -> None:
        self.parent = parent
        self.cmd_type = cmd_type
        self.user = user
        self.channel = channel
        self.guild = guild
        self.chat_type = chat_type
        self.kwargs = kwargs
        self.placeholder = {
            "name": "請輸入新的稱呼...", 
            "clean": "請輸入欲刪除的聊天紀錄數量...(最多50則)",
            "status": "請輸入欲變更的狀態...",
            "ooc": "請輸入提示訊息..."}
        self.text_input = discord.ui.InputText(
            label = cmd_type,
            style = discord.InputTextStyle.short if cmd_type != "ooc" else discord.InputTextStyle.long,
            placeholder = self.placeholder[cmd_type],
        )
        super().__init__(self.text_input, title="")
        
    async def callback(self, interaction: discord.Interaction):
        if self.cmd_type == "clean":
            try:
                await interaction.response.defer()
                user_input = int(self.children[0].value)
                if user_input > 50:
                    user_input = 50
                id = self.channel.id if self.chat_type == CHAT_TYPE.GROUP else self.user.id
                await self.parent.cmd_clean(user_input, id, self.chat_type)
                await self.parent.clean_last_msg_id(self.channel, self.user, self.chat_type)
                embed = Styled_Embed(self.parent.bot, EMBED_TYPE.CLEAN_COMPLETE, num = user_input)
                await interaction.followup.send(embed = embed)
            except Exception as e:
                print(e)
        elif self.cmd_type == "name":
            new_name = self.children[0].value
            try:
                await interaction.response.defer()
                id = self.channel.id if self.chat_type == CHAT_TYPE.GROUP else self.user.id
                embed = Styled_Embed(self.parent.bot, EMBED_TYPE.NAME_PROCESSING)
                msg = await interaction.followup.send(embed = embed)
                await self.parent.check_last_msg_id(self.channel, self.user, self.chat_type)
                res = await self.parent.cmd_name(self.user, self.channel, self.guild, new_name, self.chat_type)
                await self.parent.update_last_msg_id(self.channel, self.user, msg.id, self.chat_type)
                embed.init_embed_type(EMBED_TYPE.NAME_COMPLETE, old = self.user.name, new = new_name, res = res)
                await msg.edit(embed=embed, view = ChatButton(self.parent, id, self.chat_type, embed_res=EMBED_TYPE.NAME_COMPLETE))
            except Exception as e:
                print(e)
        elif self.cmd_type == "status":
            status = self.children[0].value
            try:
                await interaction.response.defer(ephemeral=True)
                embed = Styled_Embed(self.parent.bot, EMBED_TYPE.STATUS_COMPLETE, status = status)
                modify_configs(self.parent.path, BOT_SETTING.__name__, BOT_SETTING.STATUS.name, status)
                await self.parent.bot.change_presence(activity=discord.Game(name=status))
                await interaction.followup.send(embed = embed, ephemeral=True)
            except Exception as e:
                print(e)
        elif self.cmd_type == "ooc":
            text = self.children[0].value
            if self.chat_type == CHAT_TYPE.BOT:
                src_bot_id, dst_bot_id, src_chara_name , dst_chara_name, channel_id= self.kwargs['src_bot_id'], self.kwargs['dst_bot_id'],\
                                                        self.kwargs['src_chara_name'], self.kwargs['dst_chara_name'], self.kwargs['channel_id']
                text = await self.parent.Chat.translate_send(text, None, CHAT_TYPE.BOT)
                if 'start' in self.kwargs:
                    embed = Styled_Embed(self.parent.bot, EMBED_TYPE.BOT_CHAT_EMBED, bot_name = dst_chara_name, status = "on", topic = "off")
                    await interaction.response.send_message(embed=embed)
                    async with interaction.channel.typing():
                        src_text = f"(ooc: The character you will chat with is {dst_chara_name}\n\
                                    Please be careful not to actively use ooc, just follow my ooc instructions)\n\
                                    (ooc: {text}\nStory start!)"
                        dst_text = f"(ooc: The character you will chat with is {src_chara_name}\n\
                                    Please be careful not to actively use ooc, just follow my ooc instructions)\n\
                                    (ooc: {text}\nStory start!)"
                        res, res_translated, safety_flag = await self.parent.cmd_create_chat(src_text, src_bot_id, dst_bot_id, self.channel.id, dst_text)
                    if safety_flag:
                        embed = Styled_Embed(self.parent.bot, EMBED_TYPE.NSFW_FILTER)
                    view = BotChatButton(self.parent, src_bot_id, dst_bot_id, channel_id, res, ooc = dst_text)
                    await interaction.followup.send(res_translated, embed=embed if safety_flag else None, view=view)
                else:
                    await interaction.response.defer()
                    original_msg = await interaction.channel.fetch_message(interaction.message.id)
                    await original_msg.edit(view=None)
                    ooc_text = f"(ooc: {text})"
                    async with interaction.channel.typing():
                        res, res_translated, safety_flag = await self.parent.Chat.bot_chat_recv(dst_bot_id, channel_id, ooc_text, ooc_text)
                    await self.parent.Chat.update_database(BOT_CHAT.__name__, {BOT_CHAT.LAST_MESSAGE_TEXT.name: f"{ooc_text}\n{res}"},
                                                           {BOT_CHAT.BOT_ID.name: dst_bot_id, BOT_CHAT.CHANNEL_ID.name: channel_id})
                    if safety_flag:
                        embed = Styled_Embed(self.parent.bot, EMBED_TYPE.NSFW_FILTER)
                    view = BotChatButton(self.parent, src_bot_id, dst_bot_id, channel_id, res, ooc = ooc_text)
                    await interaction.followup.send(res_translated, embed=embed if safety_flag else None, view=view)
            
            else:
                await interaction.response.defer()
                embed = Styled_Embed(self.parent.bot, EMBED_TYPE.OOC_PROCESSING)
                msg = await interaction.followup.send(embed=embed)
                id = self.channel.id if self.chat_type == CHAT_TYPE.GROUP else self.user.id
                await self.parent.check_last_msg_id(self.channel, self.user, self.chat_type)
                res = await self.parent.cmd_ooc(text, self.guild, self.user, self.channel, self.chat_type)
                await self.parent.update_last_msg_id(self.channel, self.user, msg.id, self.chat_type)
                embed.init_embed_type(EMBED_TYPE.OOC_COMPLETE, res = res)
                await msg.edit(embed=embed, view = ChatButton(self.parent, id, self.chat_type, embed_res=EMBED_TYPE.OOC_COMPLETE))
        else:
            return
        
class RPInput_Modal(discord.ui.Modal):
    def __init__(self, parent: Main, user = None, channel = None, guild = None, chat_type = CHAT_TYPE.GROUP, **kwargs) -> None:
        self.parent = parent
        self.user = user
        self.channel = channel
        self.guild = guild
        self.kwargs = kwargs
        self.chat_type = chat_type
        title = ("故事主題", "主要情節", "故事起始（可不填）", "故事目標（可不填）", "額外設定（可不填）")
        placeholder = ("請輸入你想扮演的故事主題...", "請輸入你想該故事的主要情節...", 
                       "請輸入故事開始的時間點或劇情...", "請輸入你想達成的目標...",
                       "請輸入該故事的額外設定...")
        self.topic_input = discord.ui.InputText(
            label = title[0],
            style = discord.InputTextStyle.short,
            placeholder = placeholder[0],
        )
        self.plot_input = discord.ui.InputText(
            label = title[1],
            style = discord.InputTextStyle.long,
            placeholder = placeholder[1],
        )
        self.start_input = discord.ui.InputText(
            label = title[2],
            style = discord.InputTextStyle.long,
            placeholder = placeholder[2],
            required = False
        )
        self.goal_input = discord.ui.InputText(
            label = title[3],
            style = discord.InputTextStyle.long,
            placeholder = placeholder[3],
            required = False
        )
        self.extra_input = discord.ui.InputText(
            label = title[4],
            style = discord.InputTextStyle.long,
            placeholder = placeholder[4],
            required = False
        )
        super().__init__(self.topic_input, self.plot_input, self.start_input, self.goal_input, self.extra_input, title = "")
        
    async def callback(self, interaction: discord.Interaction):
        text = f"Hey, I want to start a role play with the following settings: \n\
                    The topic about the story is: {self.children[0].value}\n\
                    The main plot about the story is: {self.children[1].value}\n"
        if self.children[2].value != "":
            text += f"The plot will start with: {self.children[2].value}\n"
        if self.children[3].value != "":
            text += f"The goal I want to arrived with the story is: {self.children[3].value}\n"
        if self.children[4].value != "":
            text += f"And PLEASE remember these role setting: {self.children[4].value}\n"
        text += "If you have any questions, please let me know, thank you!"
            
        if self.chat_type == CHAT_TYPE.BOT:
            src_bot_id, dst_bot_id, src_chara_name , dst_chara_name, channel_id = self.kwargs['src_bot_id'], self.kwargs['dst_bot_id'],\
                                                                self.kwargs['src_chara_name'], self.kwargs['dst_chara_name'],\
                                                                self.kwargs['channel_id']
            text = await self.parent.Chat.translate_send(text, None, CHAT_TYPE.BOT)
            embed = Styled_Embed(self.parent.bot, EMBED_TYPE.BOT_CHAT_EMBED, bot_name = dst_chara_name, status = "on", topic = "on")
            await interaction.response.send_message(embed=embed)
            async with interaction.channel.typing():
                src_text = f"(ooc: The character you will chat with is {dst_chara_name}\n\
                            Please be careful not to actively use ooc, just follow my ooc instructions)\n\
                            (ooc: {text}\nStory start!)"
                dst_text = f"(ooc: The character you will chat with is {src_chara_name}\n\
                            Please be careful not to actively use ooc, just follow my ooc instructions)\n\
                            (ooc: {text}\nStory start!)"
                res, res_translated, safety_flag = await self.parent.cmd_create_chat(src_text, src_bot_id, dst_bot_id, self.channel.id, dst_text)
            if safety_flag:
                embed = Styled_Embed(self.parent.bot, EMBED_TYPE.NSFW_FILTER)
            view = BotChatButton(self.parent, src_bot_id, dst_bot_id, channel_id, res, ooc = dst_text)
            await interaction.followup.send(res_translated, embed=embed if safety_flag else None, view=view)
            
        else:
            embed = Styled_Embed(self.parent.bot, EMBED_TYPE.RP_PROCESSING)
            await interaction.response.defer()
            msg = await interaction.followup.send(embed=embed)
            id = self.channel.id if self.chat_type == CHAT_TYPE.GROUP else self.user.id
            await self.parent.check_last_msg_id(self.channel, self.user, self.chat_type)
            res = await self.parent.cmd_ooc(text, self.guild, self.user, self.channel, self.chat_type)
            await self.parent.update_last_msg_id(self.channel, self.user, msg.id, self.chat_type)
            
            embed.init_embed_type(EMBED_TYPE.RP_COMPLETE, res = res)
            await msg.edit(embed=embed, view = ChatButton(self.parent, id, self.chat_type, EMBED_TYPE.RP_COMPLETE))
            return  

def setup(bot: commands.Bot):
    bot.add_cog(Main(bot))
    
