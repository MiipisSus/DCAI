import PySide2.QtGui
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import os
import re
import discord
import asyncio
from discord.ext import commands
from discord.ui import *
from func.server_config import *
from func.send_chat import Chat
from GUI_main import MainForm as ManageWindow
import traceback
import aiohttp
import requests
import io
import sys
        
class DiscordBot(commands.Bot):
    bot_instances = {}
    
    def __init__(self, path):
        intents = discord.Intents.all()
        self.settings = init_configs(os.path.join('configs', path))
        self.path = path
        self.embed_color = self.settings[STYLE.__name__][STYLE.EMBED_COLOR]
        self.Chat = Chat(path, self.settings)
        self.token = self.settings[BOT_SETTING.__name__][BOT_SETTING.BOT_TOKEN]
        asyncio.ensure_future(self.get_bot_id())
        
        super(DiscordBot, self).__init__(intents = intents)

    async def get_bot_id(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://discord.com/api/v10/users/@me", headers={"Authorization": f"Bot {self.token}"}):
                app_info = await self.application_info()
                DiscordBot.bot_instances[str(app_info.id)] = self
        
    async def on_ready(self):
        print(f"目前登入身份 ==> {self.user}")
        if self.settings[BOT_SETTING.__name__][BOT_SETTING.STATUS] != "":
            await self.change_presence(activity=discord.Game(name=self.settings[BOT_SETTING.__name__][BOT_SETTING.STATUS]))
        if self.settings[BOT_SETTING.__name__][BOT_SETTING.AVATAR_PATH] != "":
            image_url = "https://characterai.io/i/80/static/avatars/" + self.settings[BOT_SETTING.__name__][BOT_SETTING.AVATAR_PATH]
            response = requests.get(image_url)
            if response.status_code == 200:
                image_file = io.BytesIO(response.content)
            await self.user.edit(avatar=image_file.read())
            
        await self.check_ini()
        await self.check_bot_list()

    async def check_ini(self):
        #檢查database是否已建立
        if not self.settings[DATA_PATH.__name__][DATA_PATH.DATABASE_CREATE]:
            await self.Chat.create_database()
            app_info = await self.application_info()
            admin = await self.Chat.search_database(ADMIN.__name__, [ADMIN.PRIVILAGE.name], {ADMIN.USER_ID.name: app_info.owner.id})
            if not admin:
                await self.Chat.insert_database(ADMIN.__name__, {ADMIN.USER_ID.name: app_info.owner.id,
                                                                ADMIN.PRIVILAGE.name: True})
            modify_configs(self.path, DATA_PATH.__name__, DATA_PATH.DATABASE_CREATE.name, "True")
        chara_name = await self.Chat.get_pycai_chara_info()
        modify_configs(self.path, PYCAI_SETTING.__name__, PYCAI_SETTING.CHAR_NAME.name, chara_name)
        
    async def check_bot_list(self):
        for bot_id, bot in DiscordBot.bot_instances.items():
            if bot != self:
                exist = await self.Chat.search_database(BOT.__name__, None, {BOT.BOT_ID.name: bot_id})
                if not exist and bot.settings[PROGRAM_SETTING.__name__][PROGRAM_SETTING.BOT_GROUP_CHAT]:
                    chara_name = await bot.Chat.get_pycai_chara_info()
                    if not exist:
                        await self.Chat.insert_database(BOT.__name__, {BOT.BOT_ID.name: bot.user.id,
                                                                    BOT.BOT_NAME.name: str(bot.user),
                                                                    BOT.CHARA_NAME.name: chara_name})
                elif exist and not bot.settings[PROGRAM_SETTING.__name__][PROGRAM_SETTING.BOT_GROUP_CHAT]:
                    await self.Chat.delete_database(BOT.__name__, {BOT.BOT_ID.name: bot.user.id})
    
    def get_bot_instance(self, dst_bot_id):
        return DiscordBot.bot_instances.get(str(dst_bot_id))
    
    async def send_bot_chat(self, src_bot_id, dst_bot_id, text, channel_id):
        recv_bot = self.get_bot_instance(dst_bot_id)
        await recv_bot.recv_bot_chat(src_bot_id, text, channel_id)
        return
    
    async def recv_bot_chat(self, dst_bot_id, text, channel_id):
        cog_main = self.get_cog("Main")
        await cog_main.process_bot_chat(dst_bot_id, text, channel_id)
        return
    
    async def load(self, ctx, extension):
        self.load_extension(f"cogs.{extension}")
        await ctx.send(f"**[Log] Loaded {extension} done.**")

    async def unload(self, ctx, extension):
        self.unload_extension(f"cogs.{extension}")
        await ctx.send(f"**[Log] Unloaded {extension} done.\n(Please wait for bot rebooting...)**")

    async def reload(self, ctx, extension):
        self.reload_extension(f"cogs.{extension}")
        await ctx.send(f"**[Log] ReLoaded {extension} done.**")

    async def shutdown(self):
        await self.close()

    async def reboot(self):
        for filename in os.listdir(os.path.join("./cogs")):
            if filename.endswith(".py"):
                self.reload_extension(f"cogs.{filename[:-3]}")
        
    def load_extensions(self):
        for filename in os.listdir(os.path.join("./cogs")):
            if filename.endswith(".py"):
                cog_path = f"cogs.{filename[:-3]}"
                self.load_extension(cog_path)
                
    async def run_bot(self):
        await self.start(self.token)

class BotThread(QThread):
    def run(self):
        self.bots = []
        tasks = []
        folder_path = 'configs'
        all_files = os.listdir(folder_path)
        ini_files = [file for file in all_files if re.match('.*\.ini$', file)]

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        for bot_inifile in ini_files:
            try:
                bot = DiscordBot(bot_inifile)
                bot.load_extensions()
                self.bots.append(bot)
            except Exception as e:
                print(traceback.print_exc())
                print(f"Error running bot '{bot_inifile}': {e}")

        for bot in self.bots:
            future = asyncio.ensure_future(bot.run_bot())
            tasks.append(future)
                
        # Wait for all tasks to complete
        self.loop.run_until_complete(asyncio.gather(*tasks))
    
    def close_all_bots(self):
        asyncio.set_event_loop(self.loop)
        for bot in self.bots:
            asyncio.ensure_future(bot.shutdown())
            
        self.bots.clear()
    
    def stop(self):
        self.close_all_bots()
        self.wait()

class TrayIconApp(QWidget):
    def __init__(self, bot_thread: BotThread):
        super().__init__()
        self.hide()
        self.bot_thread = bot_thread
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("QT_GUI/images/chat_AI_bot.svg"))

        menu = QMenu(self)

        manage_action = QAction("管理機器人", self)
        manage_action.triggered.connect(self.show_manage_window)
        menu.addAction(manage_action)
        
        reboot_action = QAction("重新啟動機器人", self)
        reboot_action.triggered.connect(self.reboot_thread)
        menu.addAction(reboot_action)
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.exit_application)
        menu.addAction(exit_action)

        self.tray_icon.setContextMenu(menu)

        self.tray_icon.show()

        self.manage_window = ManageWindow()

    def show_manage_window(self):
        self.manage_window.show()
    
    def reboot_thread(self):
        self.bot_thread.stop()
        self.bot_thread.quit()
        bot_thread = BotThread()
        self.bot_thread = bot_thread
        bot_thread.start()
        
    def exit_application(self):
        self.bot_thread.stop()
        self.bot_thread.quit()
        QCoreApplication.quit()
            
if __name__ == "__main__":
    app = QApplication()
    bot_thread = BotThread()
    bot_thread.start()
    tray_icon_app = TrayIconApp(bot_thread)
    
    database_folder = 'database'
    if not os.path.exists(database_folder):
        os.makedirs(database_folder)
    configs_folder = 'configs'
    if not os.path.exists(configs_folder):
        os.makedirs(configs_folder)
    
    sys.exit(app.exec_())