from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from GUI.main_configs import Ui_Form
from GUI import qtrc
from func.server_config import *
import sys
import asyncio
import configparser
from characterai import PyAsyncCAI
import aiohttp
import aiosqlite
import os
import webbrowser


class DeleteButton(QWidget):
    delete_row_signal = Signal()
    
    def __init__(self):
        super(DeleteButton, self).__init__()
        btn = QPushButton()
        btn.setFixedSize(20, 20)
        btn.setStyleSheet('''
        QPushButton::hover
        {
            background-color: rgb(222, 221, 218);
        }''')
        btn.setIcon(QIcon(u":/images/images/deletePushButton.svg"))
        btn.setIconSize(QSize(14, 16))
        btn.clicked.connect(lambda: self.delete_row_signal.emit())
        layout = QGridLayout()
        layout.addWidget(btn, 0, 0, Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 1, 0)
        self.setLayout(layout)
    
    
class MainForm(QWidget, Ui_Form):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.hide_timer = QTimer(self)
        #tab1
        self.avatar_path = ""
        self.DiscordBotTokenLineEdit.installEventFilter(self)
        self.characterAITokenLineEdit.installEventFilter(self)
        self.ExportHintLabel.setHidden(True)
        self.translateConfigWidget.setEnabled(False)
        self.APIKeyLineEdit.setEnabled(False)
        self.APIKeyDescriptionTextEdit.viewport().setCursor(Qt.ArrowCursor)
        self.translateModeComboBox.setCurrentIndex(0)
        self.targetLanguageComboBox.setCurrentIndex(0)
        self.enable_apikey()
        #tab2
        self.datapath = None
        self.admin_list = []
        self.delete_admin_list = []
        self.updateAdminHintLabel.setHidden(True)
        header = self.adminInfoTableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.resizeSection(2, 5)
        #tab3
        self.tab_3.setEnabled(False)
        self.updateVocabHintLabel.setHidden(True)
        header = self.vocabInfoTableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.init_signal()
    
    def closeEvent(self, event: QCloseEvent):
        event.ignore()
        self.hide()
        
    def init_signal(self):
        #tab1
        self.chooseColorPushButton.clicked.connect(self.show_colorDialog)
        self.enableTranslaterCheckBox.stateChanged.connect(self.translateConfigWidget.setEnabled)
        self.translateModeComboBox.currentIndexChanged.connect(self.enable_apikey)
        self.clearPushButton.clicked.connect(self.clean_config)
        self.characterAITokenLineEdit.textChanged.connect(self.show_input_style)
        self.DiscordBotTokenLineEdit.textChanged.connect(self.show_input_style)
        self.characterAITokenLineEdit.editingFinished.connect(self.on_editing_finished)
        self.DiscordBotTokenLineEdit.editingFinished.connect(self.on_editing_finished)
        self.characterIDLineEdit.editingFinished.connect(self.on_editing_finished)
        self.exportConfigButton.clicked.connect(self.export_config)
        self.importConfigButton.clicked.connect(self.import_config)
        self.characterAITokenHintPushButton.clicked.connect(self.open_web)
        self.characterIDHintPushButton.clicked.connect(self.open_web)
        self.DiscordBotTokenHintPushButton.clicked.connect(self.open_web)
        #tab2
        self.refreshAdminPushButton.clicked.connect(self.show_admin_list)
        self.updateAdminPushButton.clicked.connect(self.delete_admin_database)
        self.restoreAdminPushButton.clicked.connect(self.fill_admin_table)
    
    def open_web(self):
        if self.sender() in (self.characterIDHintPushButton, self.characterAITokenHintPushButton):
            webbrowser.open_new("https://hackmd.io/@grenn0113/BJXOGRh_a")
        elif self.sender() == self.DiscordBotTokenHintPushButton:
            webbrowser.open_new("https://hackmd.io/@grenn0113/Hkffw62O6")
        
    def on_editing_finished(self):
        if self.sender() == self.characterAITokenLineEdit:
            QTimer.singleShot(0, lambda: self.run_async_task(self.get_pycai_user_info()))
            QTimer.singleShot(0, lambda: self.run_async_task(self.get_pycai_chara_info()))
        elif self.sender() == self.DiscordBotTokenLineEdit:
            QTimer.singleShot(0, lambda: self.run_async_task(self.check_bot_token()))
        elif self.sender() == self.characterIDLineEdit:
            QTimer.singleShot(0, lambda: self.run_async_task(self.get_pycai_chara_info()))
    
    def run_async_task(self, func):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(func)
    
    def show_admin_list(self):
        QTimer.singleShot(0, lambda: self.run_async_task(self.update_admin_list()))
    
    def delete_admin_database(self):
        QTimer.singleShot(0, lambda: self.run_async_task(self.remove_users()))
        
    async def update_admin_list(self):
        try:
            self.admin_list.clear()
            datapath = "database/" + self.botNameLabel.text() + ".db"
            if os.path.exists(datapath):
                self.datapath = datapath
                admin_list = await self.get_admin_list()
                for user in admin_list:
                    if user[1]:
                        user_name = await self.get_username_by_id(user[0])
                        if user_name:
                            self.admin_list.append((user[0], user_name))

            self.fill_admin_table()
                
        except Exception as e:
            print(e)
            
    def fill_admin_table(self):
        self.adminInfoTableWidget.setRowCount(0)
        for row, table in enumerate(self.admin_list):
            self.adminInfoTableWidget.setRowCount(row + 1)
            user_id = QTableWidgetItem(table[0])
            user_name = QTableWidgetItem(table[1])
            delete_btn = DeleteButton()
            delete_btn.delete_row_signal.connect(self.update_delete_list)
            self.adminInfoTableWidget.setItem(row, 0, user_id)
            self.adminInfoTableWidget.setItem(row, 1, user_name)
            self.adminInfoTableWidget.setCellWidget(row, 2, delete_btn)
        
    def update_delete_list(self):
        delete_btn = self.sender()
        row = self.adminInfoTableWidget.indexAt(delete_btn.pos()).row()
        
        if self.adminInfoTableWidget.rowCount() == 1:
            self.updateAdminHintLabel.setText("管理員需至少保留一名！")
            self.updateAdminHintLabel.setProperty("state", "red")
            self.updateAdminHintLabel.style().polish(self.updateAdminHintLabel)
            self.updateAdminHintLabel.setHidden(False)
            self.hide_timer.singleShot(3000, lambda: self.updateAdminHintLabel.setHidden(True))
            return
        user_id = self.adminInfoTableWidget.item(row, 0).text()
        if user_id:
            self.delete_admin_list.append(user_id)
            self.adminInfoTableWidget.removeRow(row)
    
    def enable_apikey(self):
        if self.translateModeComboBox.currentIndex() == 1:
            self.APIKeyDescriptionTextEdit.setText('Open AI翻譯口語化能力強、彈性高。\nAPI本身需收費，並且翻譯處理時間稍微久一點，有些繁中用語翻譯不夠到位。')
        elif self.translateModeComboBox.currentIndex() == 2:
            self.APIKeyDescriptionTextEdit.setText('Azure AI translater翻譯較機械化，翻譯品質與Google Translation類似。\nAPI本身有免費額度，翻譯處理速度快。')
        else:
            self.APIKeyDescriptionTextEdit.setText('Google Translator翻譯較機械化，面對口語翻譯處理能力低。\n程式採用Google Trans因此無須提供API，然而流量過高可能導致請求被攔截，遇此情況請重新刷新。')
        if self.translateModeComboBox.currentIndex() != 0:
            self.APIKeyLineEdit.setEnabled(True)
        else:
            self.APIKeyLineEdit.setEnabled(False)
    
    def show_input_style(self, obj=None):
        if not isinstance(obj, QLineEdit):
            obj = self.sender()
        if obj.text() == "":
            obj.setProperty("state", "red")
            obj.style().polish(obj)
        else:
            obj.setProperty("state", None)
            obj.style().polish(obj)
            
    def show_colorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            style_sheet = f"QLabel {{ color: {color.name()}; }}"
            self.colorCodeLabel.setStyleSheet(style_sheet)
            self.colorCodeLabel.setText(color.name())
            
    def clean_config(self):
        for lineEdit in self.tab.findChildren(QLineEdit):
            lineEdit.clear()
        for cbb in self.tab.findChildren(QComboBox):
            cbb.setCurrentIndex(0)
        for chk in self.tab.findChildren(QCheckBox):
            chk.setChecked(False)
        self.colorCodeLabel.setText("")
        self.createrIDLabel.setText("")
        self.discordBotStatusLabel.setText("")
        self.characterNameLabel.setText("")
        self.botNameLabel.setText("檔案名稱")
        self.botNameLabel.setProperty("state", "")
        self.botNameLabel.style().polish(self.botNameLabel)
        
    def check_config(self):
        flag = False
        if self.DiscordBotTokenLineEdit.text() == "" or \
            self.characterAITokenLineEdit.text() == "":
            self.ExportHintLabel.setText("請輸入Token!")
        elif self.createrIDLabel.text() == "":
            self.ExportHintLabel.setText("CAI Token輸入有誤！")
        elif self.discordBotStatusLabel.text().lower() == "disabled":
            self.ExportHintLabel.setText("Discord Bot輸入有誤！")
        elif self.characterIDLineEdit.text() == "":
            self.ExportHintLabel.setText("請輸入Character ID!")
        elif self.characterNameLabel.text() == "":
            self.ExportHintLabel.setText("該Character ID 不存在！")
        elif self.translateModeComboBox.currentIndex() != 0 and self.APIKeyLineEdit.text() == "":
            self.ExportHintLabel.setText("請輸入API Key!")
        else:
            flag = True
        
        if flag:
            return True
        else:
            self.ExportHintLabel.setProperty("state", "red")
            self.ExportHintLabel.style().polish(self.ExportHintLabel)
            self.ExportHintLabel.setHidden(False)
            self.hide_timer.singleShot(3000, lambda: self.ExportHintLabel.setHidden(True))
            return False
    
    def export_config(self):
        check = self.check_config()
        if not check:
            return
        else:
            self.generate_config()
            
    def import_config(self):
        #get file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "INI Files (*.ini);;All Files (*)", options=options)
        if not file_path:
            return
        #import
        config = configparser.ConfigParser()
        config.read(file_path)
        self.clean_config()
        self.botNameLabel.setText(file_path.split('/')[-1].rstrip(".ini"))
        self.botNameLabel.setProperty("state", "green")
        self.botNameLabel.style().polish(self.botNameLabel)
        
        self.characterAITokenLineEdit.setText(config.get("API_KEY", "pycai_apikey"))
        self.DiscordBotTokenLineEdit.setText(config.get("BOT_SETTING", "bot_token"))
        self.characterIDLineEdit.setText(config.get("PYCAI_SETTING", "char_id"))
        
        if config.get("PROGRAM_SETTING", "language") == "zh-tw":
            self.targetLanguageComboBox.setCurrentIndex(0)
        else:
            self.targetLanguageComboBox.setCurrentIndex(1)
            
        translate_mode = int(config.get("PROGRAM_SETTING", "src_translate_mode"))
        self.translateModeComboBox.setCurrentIndex(int(config.get("PROGRAM_SETTING", "src_translate_mode")))
        
        if translate_mode == TRANSLATE_MODE.OPENAI:
            self.APIKeyLineEdit.setText(config.get("API_KEY", "openai_apikey"))
        elif translate_mode == TRANSLATE_MODE.AZURE:
            self.APIKeyLineEdit.setText(config.get("API_KEY", "azure_key"))
            
        color = "#" + config.get("STYLE", "embed_color").lstrip("0x")
        style_sheet = f"QLabel {{ color: {color}; }}"
        self.colorCodeLabel.setStyleSheet(style_sheet)
        self.colorCodeLabel.setText(color)
        
        if config.getboolean("PROGRAM_SETTING", "individual_chat"):
            self.DMChannelChatCheckBox.setChecked(True)
        if config.getboolean("PROGRAM_SETTING", "channel_group_chat"):
            self.GroupChannelChatCheckBox.setChecked(True)
        if config.getboolean("PROGRAM_SETTING", "bot_group_chat"):
            self.BotChatCheckBox.setChecked(True)
        if config.get("BOT_SETTING", "avatar_path") != "":
            self.changeAvatarCheckBox.setChecked(True)
        
        QTimer.singleShot(0, lambda: self.run_async_task(self.get_pycai_user_info()))
        QTimer.singleShot(0, lambda: self.run_async_task(self.get_pycai_chara_info()))
        QTimer.singleShot(0, lambda: self.run_async_task(self.check_bot_token()))    
            
    def generate_config(self):
        config = configparser.ConfigParser()
        #api key
        openai_apikey = ""
        azure_key = ""
        if self.translateModeComboBox.currentIndex() == TRANSLATE_MODE.OPENAI:
            openai_apikey = self.APIKeyLineEdit.text()
        elif self.translateModeComboBox.currentIndex() == TRANSLATE_MODE.AZURE:
            azure_key = self.APIKeyLineEdit.text()
        if self.targetLanguageComboBox.currentIndex() == 0:
            language = "zh-tw"
        else:
            language = "en"
        if not self.changeAvatarCheckBox.isChecked():
            self.avatar_path = ""
        if self.colorCodeLabel.text() == "":
            self.color = "#FFFFFF"
        else:
            self.color = self.colorCodeLabel.text()
            
        config["API_KEY"] = {"openai_apikey": openai_apikey,
                             "pycai_apikey": self.characterAITokenLineEdit.text(),
                             "azure_key": azure_key}
        config["PYCAI_SETTING"] = {"creator_id": self.createrIDLabel.text(),
                                   "char_id": self.characterIDLineEdit.text(),
                                   "char_name": self.characterNameLabel.text()}
        config["OPENAI_SETTING"] = {"model": "gpt-3.5-turbo",
                                    "user": "user"}
        config["AZURE_SETTING"] = {"endpoint": "https://api.cognitive.microsofttranslator.com",
                                   "location": "eastasia"}
        config["DATA_PATH"] = {"database_create": "False"}
        config["BOT_SETTING"] = {"status": "",
                                 "bot_token": self.DiscordBotTokenLineEdit.text(),
                                 "avatar_path": self.avatar_path}
        config["STYLE"] = {"embed_color": "0x" + self.color.lstrip("#")}
        config["PROGRAM_SETTING"] = {"src_translate_mode": str(self.translateModeComboBox.currentIndex()),
                                     "dst_translate_mode": str(self.translateModeComboBox.currentIndex()),
                                     "bot_translate_mode": "0",
                                     "vocab": "False",
                                     "language": language,
                                     "individual_chat": str(self.DMChannelChatCheckBox.isChecked()),
                                     "channel_group_chat": str(self.GroupChannelChatCheckBox.isChecked()),
                                     "bot_group_chat": str(self.BotChatCheckBox.isChecked())}
        
        ini_name = self.characterNameLabel.text().replace(" ", "_").rstrip("_")
        
        file_path = "configs/" + ini_name + ".ini"
        with open(file_path, 'w') as config_file:
            config.write(config_file)
            
        self.botNameLabel.setText(ini_name)
        self.botNameLabel.setProperty("state", "green")
        self.botNameLabel.style().polish(self.botNameLabel)
        
        self.ExportHintLabel.setText("設定匯出成功！")
        self.ExportHintLabel.setProperty("state", "green")
        self.ExportHintLabel.style().polish(self.ExportHintLabel)
        self.ExportHintLabel.setHidden(False)
        self.hide_timer.singleShot(3000, lambda: self.ExportHintLabel.setHidden(True))
        
    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.FocusOut:
            if obj == self.DiscordBotTokenLineEdit or self.characterAITokenLineEdit:
                self.show_input_style(obj)
        return super().eventFilter(obj, event)
    
    async def get_pycai_chara_info(self):
        try:
            self.PYCAI_client = PyAsyncCAI(self.characterAITokenLineEdit.text())
            res = await self.PYCAI_client.character.info(self.characterIDLineEdit.text())
            chara_name = res["character"]["name"] #chara name
            chara_avatar_path = res["character"]["avatar_file_name"] #avatar file name
            self.characterNameLabel.setText(chara_name)
            self.avatar_path = chara_avatar_path
        except:
            self.characterNameLabel.setText("")
            
    async def check_bot_token(self):
        url = "https://discord.com/api/v10/users/@me"
        headers = {
            "Authorization": f"Bot {self.DiscordBotTokenLineEdit.text()}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    self.discordBotStatusLabel.setText("Enabled")
                    self.discordBotStatusLabel.setProperty("state", "green")
                    self.discordBotStatusLabel.style().polish(self.discordBotStatusLabel)
                else:
                    self.discordBotStatusLabel.setText("Disabled")
                    self.discordBotStatusLabel.setProperty("state", "red")
                    self.discordBotStatusLabel.style().polish(self.discordBotStatusLabel)
        
    async def get_pycai_user_info(self):
        try:
            self.PYCAI_client = PyAsyncCAI(self.characterAITokenLineEdit.text())
            user_info = await self.PYCAI_client.user.info()
            creator_id = user_info["user"]["user"]["id"]  #creator id
            self.createrIDLabel.setText(str(creator_id))
        except:
            self.createrIDLabel.setText("")
    
    async def get_username_by_id(self, user_id):
        try:
            bot_token = self.DiscordBotTokenLineEdit.text()
            url = f'https://discord.com/api/v10/users/{user_id}'
            headers = {
                'Authorization': f'Bot {bot_token}'
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        user_data = await response.json()
                        username = user_data['username']
                        return username
                    else:
                        return None
        except Exception as e:
            print(e)
            return None
            
    async def get_admin_list(self):
        async with aiosqlite.connect(self.datapath) as db:
            cursor = await db.cursor()
            query = "SELECT * FROM ADMIN"
            await cursor.execute(query)
            result = await cursor.fetchall()
            if isinstance(result, tuple):
                result = [result]
        return result
    
    async def remove_users(self):
        async with aiosqlite.connect(self.datapath) as db:
            cursor = await db.cursor()

            for user_id in self.delete_admin_list:
                await cursor.execute('''
                    DELETE FROM ADMIN
                    WHERE USER_ID = ?
                ''', (user_id,))

            await db.commit()
            self.delete_admin_list.clear()
            
        self.updateAdminHintLabel.setText("管理員名單更新成功！")
        self.updateAdminHintLabel.setProperty("state", "green")
        self.updateAdminHintLabel.style().polish(self.updateAdminHintLabel)
        self.updateAdminHintLabel.setHidden(False)
        self.hide_timer.singleShot(3000, lambda: self.updateAdminHintLabel.setHidden(True))
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainForm()
    main.show()
    sys.exit(app.exec_())