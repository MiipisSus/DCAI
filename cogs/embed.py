import discord
from discord.ui import *
from discord.ext import commands
from func.server_config import *

class Styled_Embed(discord.Embed):
    def __init__(self, bot, embed_type, **kwargs):
        self.bot = bot
        super().__init__(title="", description = self.bot.user, color = self.bot.embed_color)
        self.init_embed_type(embed_type, **kwargs)

    def init_embed_type(self, embed_type, **kwargs):
        if embed_type == EMBED_TYPE.NAME_PROCESSING:
            self.title = "暱稱正在更新中，請稍後..."
        elif embed_type == EMBED_TYPE.NAME_COMPLETE:
            self.title = f"已將角色對{kwargs['old']}的暱稱修改為: {kwargs['new']}"
            self.description = kwargs['res']
        elif embed_type == EMBED_TYPE.NSFW_PROCESSING:
            self.title = "NSFW 提示訊息傳送中，請稍後..."
        elif embed_type == EMBED_TYPE.NSFW_COMPLETE:
            self.title = "NSFW 提示訊息已傳送完成"
            self.description = kwargs['res']
        elif embed_type == EMBED_TYPE.CLEAN_COMPLETE:
            self.title = f"已清除{kwargs['num']}篇角色的對話紀錄"
        elif embed_type == EMBED_TYPE.RESET_PROCESSING:
            self.title = "正在重置角色聊天紀錄..."
        elif embed_type == EMBED_TYPE.RESET_COMPLETE:
            self.title = "已重置角色的所有對話紀錄"
        elif embed_type == EMBED_TYPE.SHOW_INFO:
            self.description = f"**使用者名稱**: {kwargs['user_name']}\n\
                        請使用 **/list** 以取得所有命令"
            self.set_thumbnail(url = self.bot.user.avatar.url)
        elif embed_type == EMBED_TYPE.SHOW_LIST:
            self.title = "Command List"
        elif embed_type == EMBED_TYPE.NSFW_FILTER:
            self.title = "NSFW filter 阻擋了角色的回覆，請嘗試刷新或刪除訊息。"
        elif embed_type == EMBED_TYPE.EXECUTED_FLAG:
            self.title = "重要指令正在執行中，請稍後再試..."
        elif embed_type == EMBED_TYPE.REMOVE_LAST_MESSAGE:
            self.title = "訊息已被移除。"
        elif embed_type == EMBED_TYPE.REFRESH_LAST_MESSAGE:
            self.title = "產生新訊息中，請稍後..."
        elif embed_type == EMBED_TYPE.STATUS_COMPLETE:
            self.title = f"角色的狀態已更改為：{kwargs['status']}"
        elif embed_type == EMBED_TYPE.REBOOT_PROCESSING:
            self.title = "Bot正在重新啟動，請稍後..."
        elif embed_type == EMBED_TYPE.REBOOT_COMPLETE:
            self.title = "Bot已重新啟動"
        elif embed_type == EMBED_TYPE.RP_PROCESSING:
            self.title = "RP 提示訊息傳送中，請稍後..."
        elif embed_type == EMBED_TYPE.RP_COMPLETE:
            self.title = "RP 提示訊息已傳送完成"
            self.description = kwargs['res']
        elif embed_type == EMBED_TYPE.OOC_PROCESSING:
            self.title = "OOC 提示訊息傳送中，請稍後..."
        elif embed_type == EMBED_TYPE.OOC_COMPLETE:
            self.title = "OOC 提示訊息已傳送完成"
            self.description = kwargs['res']
        elif embed_type == EMBED_TYPE.ADMIN_COMPLETE:
            self.title = f"ADMIN 權限已賦予{kwargs['user']}"
        elif embed_type == EMBED_TYPE.CHECK_PRIVILAGE:
            self.title = "你沒有角色機器人管理員權限，請管理員使用 /admin 賦予權限"
        elif embed_type == EMBED_TYPE.SHOW_TASK:
            self.title = f"🕛 現在的時間是： {kwargs['time']}"
            self.description = kwargs['res']
            self.set_thumbnail(url = self.bot.user.avatar.url)
        elif embed_type == EMBED_TYPE.SHOW_EVENT:
            self.title = f"🎉 歡迎來到{kwargs['guild']}伺服器，{kwargs['user_name']}！"
            self.description = kwargs['res']
            self.set_thumbnail(url = self.bot.user.avatar.url)
        elif embed_type == EMBED_TYPE.TASK_COMPLETE:
            self.title = f"SCHEDULE 功能已於{kwargs['channel']}頻道開啟"
        elif embed_type == EMBED_TYPE.EVENT_COMPLETE:
            self.title = f"WELCOME 功能已於{kwargs['channel']}頻道開啟"
        elif embed_type == EMBED_TYPE.TASK_EVENT_DISABLED:
            self.title = f"{kwargs['func']} 功能已停用"
        elif embed_type == EMBED_TYPE.BOT_CHAT_EMBED:
            self.title = f"角色聊天 with: {kwargs['bot_name']}"
            self.add_field(name="Status", value=kwargs['status'], inline=True)
            if "topic" in kwargs:
                self.add_field(name="Topic", value=kwargs['topic'], inline=True)
            self.set_thumbnail(url = self.bot.user.avatar.url)
        elif embed_type == EMBED_TYPE.BOT_CHAT_DISABLED:
            self.title = f"該角色並未啟用 BOT CHAT 功能"
        elif embed_type == EMBED_TYPE.DM_NOT_AVALIABLE:
            self.title = f"該功能未在DM頻道開放使用"
            
def setup(bot: commands.Bot):
    pass