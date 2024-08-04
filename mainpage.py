import sys
import os
import subprocess
import json
import asyncio

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPlainTextEdit, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot,QStringListModel,QObject,QTranslator,QUrl,Qt, QTimer
from PyQt5.QtGui import QDesktopServices, QPixmap
from frontpage import Ui_MainWindow
from tools.i18n.i18n import I18nAuto
from bilibiliApi import BilibiliApi
import logging
from config import config

logging.basicConfig(level=logging.INFO)

i18n = I18nAuto()

list_language = {
    i18n("Chinese"): "中文",
    i18n("English"): "英文",
    i18n("Japanese"): "日文",
    i18n("Chinese and English"): "中英混合",
    i18n("Japanese and English"): "日英混合",
    i18n("Multilingual"): "多语种混合",
}

save_language={
    "中文":"Chinese",
    "英文":"English",
    "日文":"Japanese",
    "中英混合":"Chinese and English",
    "日英混合":"Japanese and English",
    "多语种混合":"Multilingual",

}

#new
class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass


class ServerThread(QThread):
    def __init__(self, bilibili_api, room_id):
        super().__init__()
        self.bilibili_api = bilibili_api
        self.room_id = room_id

    def run(self):
        try:
            self.bilibili_api.start_connection(self.room_id)
        except Exception as e:
            logging.error(f"启动连接时发生错误: {e}")

    def stop(self):
        try:
            self.bilibili_api.stop_connection()
        except Exception as e:
            logging.error(f"停止连接时发生错误: {e}")

class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        #self.app = app  # 保存app实例
        self.setupUi(self)
        self.server_thread = None
        self.translator = QTranslator()
        #self.current_language = ""

        # Find the QPlainTextEdit widget
        self.console_output = self.findChild(QPlainTextEdit, 'plainTextEdit')
        self.console_output.setReadOnly(True)

        # Set up EmittingStream and redirect stdout and stderr
        self.emitting_stream = EmittingStream()
        self.emitting_stream.textWritten.connect(self.update_console_output)
        sys.stdout = self.emitting_stream
        sys.stderr = self.emitting_stream

        # Set up logging to also go through emitting stream
        logger = logging.getLogger()
        handler = logging.StreamHandler(self.emitting_stream)
        logger.addHandler(handler)

        # Connect buttons to slots
        self.pushButton_1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButton_4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        #apply button
        self.apply_button_1 = self.findChild(QtWidgets.QPushButton, 'pushButton_12')
        self.apply_button_2 = self.findChild(QtWidgets.QPushButton, 'pushButton_5')
        self.apply_button_3 = self.findChild(QtWidgets.QPushButton, 'pushButton_7')
        self.apply_button_4 = self.findChild(QtWidgets.QPushButton, 'pushButton_8')
        self.apply_button_1.clicked.connect(self.save_parameters)
        self.apply_button_2.clicked.connect(self.save_parameters)
        self.apply_button_3.clicked.connect(self.save_parameters)
        self.apply_button_4.clicked.connect(self.save_parameters)

        # homepage setting
        self.pushButton.clicked.connect(self.toggle_server)
        self.ID_code_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit_3')
        self.SESSDATA_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit_10')
        self.bili_jct_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit_11')
        self.buvid3_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit_12')
        self.pushButton_9.clicked.connect(self.test_TTS)

        # model page setting
        self.populate_comboBox_6()
        self.populate_comboBox_5()
        # Connect QSlider and QDoubleSpinBox
        self.horizontalSlider_2.valueChanged.connect(self.slider_value_changed)
        self.doubleSpinBox.valueChanged.connect(self.spinbox_value_changed)
        self.horizontalSlider_3.valueChanged.connect(self.slider2_value_changed)
        self.doubleSpinBox_2.valueChanged.connect(self.spinbox2_value_changed)
        self.populate_comboBoxes()
        self.pushButton_10.clicked.connect(self.on_refresh_clicked)
        self.pushButton_11.clicked.connect(self.open_file_path)
        #set
        self.gpt_model_combo = self.findChild(QtWidgets.QComboBox, 'comboBox_6')
        self.sovits_model_combo = self.findChild(QtWidgets.QComboBox, 'comboBox_5')
        self.reference_audio_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit_6')
        self.audio_subtitle_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit_4')
        self.top_k_spin = self.findChild(QtWidgets.QSpinBox, 'spinBox')
        self.top_p_spin = self.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox')
        self.temperature_spin = self.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox_2')
        self.reference_language_combo = self.findChild(QtWidgets.QComboBox, 'comboBox_2')
        self.cutting_method_combo = self.findChild(QtWidgets.QComboBox, 'comboBox_4')
        self.output_language_combo = self.findChild(QtWidgets.QComboBox, 'comboBox_7')

        #comment page setting
        self.checkbox = self.findChild(QtWidgets.QCheckBox, 'checkBox')
        self.checkcomment = self.findChild(QtWidgets.QCheckBox, 'checkBox_2')
        self.checkSC = self.findChild(QtWidgets.QCheckBox, 'checkBox_3')
        self.checkgift = self.findChild(QtWidgets.QCheckBox, 'checkBox_4')
        self.checkmember = self.findChild(QtWidgets.QCheckBox, 'checkBox_5')
        self.list_view=self.findChild(QtWidgets.QListView, 'listView')
        self.block_words_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.pushButton_6.clicked.connect(self.add_block_word)
        self.pushButton_13.clicked.connect(self.delete_block_word)
        self.comment_format_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit_5')
        self.SC_format_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit_7')
        self.gift_format_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit_8')
        self.member_format_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit_9')

        #About page setting
        self.system_language_combo=self.findChild(QtWidgets.QComboBox, 'comboBox_3')
        # 创建字符串列表模型
        self.model = QStringListModel()
        self.list_view.setModel(self.model)


        #load parameters
        self.load_parameters()
        #set bilibiliapi
        self.bilibili_api = BilibiliApi(self.SESSDATA_line.text(),self.bili_jct_line.text(),self.buvid3_line.text())
        self.bilibili_api.connection_established.connect(self.on_server_started)
        self.bilibili_api.connection_closed.connect(self.on_server_stopped)

        # Enable link interaction for label_23
        self.label_23.setTextFormat(Qt.RichText)
        self.label_23.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.label_23.setOpenExternalLinks(False)
        self.label_23.linkActivated.connect(self.open_link)

        # Enable link interaction for label_24
        self.label_24.setTextFormat(Qt.RichText)
        self.label_24.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.label_24.setOpenExternalLinks(False)
        self.label_24.linkActivated.connect(self.open_link)

    def open_link(self, url):
        QDesktopServices.openUrl(QUrl(url))

    #system language
    def change_language(self, language):
        try:
            if language == "English" or language == "英文":
                qm_file ="translations/QTproject_en_GB.qm"
            elif language == "中文" or language == "Chinese":
                qm_file ="translations/QTproject_zh_CN.qm"
            else:
                print(f"Unsupported language: {language}")
                return

            if not os.path.exists(qm_file):
                print(f"Translation file not found: {qm_file}")
                return

            if not self.translator.load(qm_file):
                print(f"Failed to load translation file: {qm_file}")
                return

            app.installTranslator(self.translator)
            self.retranslateUi(self)  # 调用自动生成的retranslateUi方法更新UI
        except Exception as e:
            print(f"Error changing language: {e}")


    #apply button def
    def save_parameters(self):
        #global parameters_changed
        serverstate=self.pushButton.text()
        self.change_language(self.system_language_combo.currentText())
        self.pushButton.setText(serverstate)
        parameters = {
            #homepage
            "ID_code":self.ID_code_line.text(),
            "SESSDATA": self.SESSDATA_line.text(),
            "bili_jct": self.bili_jct_line.text(),
            "buvid3": self.buvid3_line.text(),
            #modelpage
            "GPT_Model": self.gpt_model_combo.currentText(),
            "SoVITS_Model": self.sovits_model_combo.currentText(),
            "refer_wav_path": self.reference_audio_line.text(),
            "prompt_text": self.audio_subtitle_line.text(),
            "top_k": self.top_k_spin.value(),
            "top_p": self.top_p_spin.value(),
            "temperature": self.temperature_spin.value(),
            "prompt_language": self.reference_language_combo.currentText(),
            "how_to_cut": self.cutting_method_combo.currentText(),
            "text_language": self.output_language_combo.currentText(),
            #commentpage
            "Comment_format":self.comment_format_line.text(),
            "SC_format":self.SC_format_line.text(),
            "gift_format":self.gift_format_line.text(),
            "member_format":self.member_format_line.text(),
            "Punctuation_filter":self.checkbox.isChecked(),
            "Comment_switch": self.checkcomment.isChecked(),
            "SC_switch": self.checkSC.isChecked(),
            "Gift_switch": self.checkgift.isChecked(),
            "Member_switch": self.checkmember.isChecked(),
            "Block_Words": self.block_words,

            #aboutpage
            "System_language":self.system_language_combo.currentText(),
        }
        with open('parameters.json', 'w') as f:
            json.dump(parameters, f, indent=4)
        config.parameters_changed = True
        config.gpt_path="GPT_weights/" + parameters["GPT_Model"]
        config.sovits_path="SoVITS_weights/" + parameters["SoVITS_Model"]
        parameters["prompt_language"] = list_language[parameters["prompt_language"]]
        parameters["text_language"] = list_language[parameters["text_language"]]
        config.parameters=parameters

        hidden_keys=["SESSDATA","bili_jct","buvid3"]

        formatted_parameters = "\n".join([f"{key}: {value}" for key, value in parameters.items() if key not in hidden_keys])

        self.show_message("Apply Successful", f"Parameters saved successfully:\n\n{formatted_parameters}")


    def load_parameters(self):
        if os.path.exists('parameters.json'):
            with open('parameters.json', 'r') as f:
                parameters = json.load(f)
        else:
            parameters = {
                "ID_code": "",
                "SESSDATA": "",
                "bili_jct": "",
                "buvid3": "",
                "GPT_Model": "otto-e10.ckpt",
                "SoVITS_Model": "otto_e39_s1638.pth",
                "refer_wav_path": "example\otto_路上停车的问题太多了啊，所以我现在得做这个市区管理了啊.wav",
                "prompt_text": "路上停车的问题太多了啊，所以我现在得做这个市区管理了啊。",
                "top_k": 5,
                "top_p": 1.0,
                "temperature": 1.0,
                "prompt_language": "Chinese",
                "how_to_cut": "No slice",
                "text_language": "Multilingual",
                "Comment_format": "$USER said: $TEXT.",
                "SC_format": "$USER send a super chat: $TEXT.",
                "gift_format": "Thank you $USER for sending $COUNT $GIFT.",
                "member_format": "$USER renewed $MEMBER for $COUNT months. thank you.",
                "Punctuation_filter": False,
                "Comment_switch": True,
                "SC_switch": True,
                "Gift_switch": True,
                "Member_switch": True,
                "System_language": "English"
            }

        # home load
        self.ID_code_line.setText(parameters.get("ID_code", ""))
        self.SESSDATA_line.setText(parameters.get("SESSDATA", ""))
        self.bili_jct_line.setText(parameters.get("bili_jct", ""))
        self.buvid3_line.setText(parameters.get("buvid3", ""))
        # model load
        self.gpt_model_combo.setCurrentText(parameters.get("GPT_Model", ""))
        self.sovits_model_combo.setCurrentText(parameters.get("SoVITS_Model", ""))
        self.reference_audio_line.setText(parameters.get("refer_wav_path", ""))
        self.audio_subtitle_line.setText(parameters.get("prompt_text", ""))
        self.top_k_spin.setValue(parameters.get("top_k", 5))
        self.top_p_spin.setValue(parameters.get("top_p", 1.0))
        self.temperature_spin.setValue(parameters.get("temperature", 1.0))
        self.reference_language_combo.setCurrentText(parameters.get("prompt_language", ""))
        self.cutting_method_combo.setCurrentText(parameters.get("how_to_cut", "No slice"))
        self.output_language_combo.setCurrentText(parameters.get("text_language", ""))
        # comment load
        self.comment_format_line.setText(parameters.get("Comment_format", ""))
        self.SC_format_line.setText(parameters.get("SC_format", ""))
        self.gift_format_line.setText(parameters.get("gift_format", ""))
        self.member_format_line.setText(parameters.get("member_format", ""))
        self.checkbox.setChecked(parameters.get("Punctuation_filter", False))
        self.checkcomment.setChecked(parameters.get("Comment_switch", True))
        self.checkSC.setChecked(parameters.get("SC_switch", True))
        self.checkgift.setChecked(parameters.get("Gift_switch", True))
        self.checkmember.setChecked(parameters.get("Member_switch", True))
        # about
        self.system_language_combo.setCurrentText(parameters.get("System_language", "English"))
        self.change_language(parameters["System_language"])

        # 检查 Block_Words 是否存在且不为空
        block_words = parameters.get("Block_Words")
        if block_words:  # 这将检查 block_words 是否为 None 或空列表
            self.block_words = block_words
        else:  # 初始化屏蔽词列表
            self.block_words = []

        self.model.setStringList(self.block_words)
        self.complete_loading()

        language = parameters['System_language']

        if language == 'English':
            print("""###################################################
 Click the "About" button to view the user manual

 Quick Start
 Open Chrome browser and log in Bilibili account
 Open Developer Tools, find the Application
 On the left, find: Storage/Cookies
 Select any Bilibili domain, find the Value 
 Copy them into the software and enter the ID code

 IMPORTANT: DON'T FORGET CLICK the Apply button!!!

 After saving, click Start Server to connect

 For other browser users, please see user manual                                                                     
###################################################""")
        elif language == 'Chinese':
            print("""###################################################
 软件详细功能介绍请点击 "关于" 按钮查阅用户手册
 快速上手
 打开Chrome浏览器并登录B站账号
 打开开发者工具, 找到Application选项卡
 在左侧找到: Storage/Cookies
 选中任一b站域名，在右侧找到对应三项Value并复制进软件
 输入直播间码后请点击保存设置按钮

 不要忘按保存设置！会报错！

 保存后点击Start Server连接即可   
 其他浏览器用户请见:                                                                   
 https://nemo2011.github.io/bilibili-api/#/get-credential    
###################################################""")



    #show message def
    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    #home page def
    def update_console_output(self, text):
        self.console_output.appendPlainText(text)

    def toggle_server(self):
        if self.pushButton.text() == "Start Server":
            self.start_server()
        else:
            self.stop_server()

    def test_TTS(self):
        try:
            if config.parameters["System_language"]=="Chinese":
                print("中文测试")
                danmaku_event = {
                    'data': {
                        'info': [
                            [], '测试弹幕内容', [12345, '测试用户114']
                        ]
                    }
                }
                self.bilibili_api.handle_event(danmaku_event, 'danmaku')
                logging.info("处理测试弹幕事件完成")

                gift_event = {
                    'data': {
                        'data': {
                            'uname': '测试用户514',
                            'giftName': '辣条',
                            'num': 5
                        }
                    }
                }
                self.bilibili_api.handle_event(gift_event, 'gift')
                logging.info("处理测试礼物事件完成")

                super_chat_event = {
                    'data': {
                        'data': {
                            'user_info': {
                                'uname': '测试用户1919'
                            },
                            'message': '这是一个超级留言',
                            'price': 100
                        }
                    }
                }
                self.bilibili_api.handle_event(super_chat_event, 'super_chat')
                logging.info("处理测试超级留言事件完成")

                guard_buy_event = {
                    'data': {
                        'data': {
                            'username': '测试用户810',
                            'guard_level': 3,
                            'num': 1,
                            'gift_name': '舰长'
                        }
                    }
                }
                self.bilibili_api.handle_event(guard_buy_event, 'guard_buy')
                logging.info("处理测试上舰事件完成")
            elif config.parameters["System_language"]=="English":
                print('English Test')
                danmaku_event = {
                    'data': {
                        'info': [
                            [], 'This is a comment inference', [12345, 'Test user543']
                        ]
                    }
                }
                self.bilibili_api.handle_event(danmaku_event, 'danmaku')
                logging.info("Test Comment Send")

                gift_event = {
                    'data': {
                        'data': {
                            'uname': 'Test user1145',
                            'giftName': 'Gift name',
                            'num': 5
                        }
                    }
                }
                self.bilibili_api.handle_event(gift_event, 'gift')
                logging.info("Test Gift Inference")

                super_chat_event = {
                    'data': {
                        'data': {
                            'user_info': {
                                'uname': 'Test User321'
                            },
                            'message': 'This is a super chat',
                            'price': 100
                        }
                    }
                }
                self.bilibili_api.handle_event(super_chat_event, 'super_chat')
                logging.info("SC Send")

                guard_buy_event = {
                    'data': {
                        'data': {
                            'username': 'Test user123',
                            'guard_level': 3,
                            'num': 1,
                            'gift_name': 'fans club'
                        }
                    }
                }
                self.bilibili_api.handle_event(guard_buy_event, 'guard_buy')
                logging.info("member test")


        except Exception as e:
            logging.error(f"ERROR: {e}")

    def start_server(self):
        self.pushButton.setText("Starting...")
        self.pushButton.setEnabled(False)
        self.server_thread = ServerThread(self.bilibili_api, self.ID_code_line.text())
        self.server_thread.start()

    def stop_server(self):
        self.pushButton.setText("Stopping...")
        self.pushButton.setEnabled(False)
        if self.server_thread:
            self.server_thread.stop()

    @pyqtSlot()
    def on_server_started(self):
        self.pushButton.setText("Stop Server")
        self.pushButton.setEnabled(True)

    @pyqtSlot()
    def on_server_stopped(self):
        self.pushButton.setText("Start Server")
        self.pushButton.setEnabled(True)
        self.server_thread = None

    #model page def
    def on_refresh_clicked(self):
        self.populate_comboBoxes()
        self.show_message("Refresh Successful", "Model list has been refreshed successfully.")

    def populate_comboBoxes(self):
        self.update_comboBox(self.comboBox_5, 'SoVITS_weights')
        self.update_comboBox(self.comboBox_6, 'GPT_weights')

    def update_comboBox(self, comboBox, folder_name):
        folder_path = os.path.join(os.path.dirname(__file__), folder_name)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
            comboBox.clear()
            comboBox.addItems(files)

    def slider_value_changed(self, value):
        spinbox_value = value / 100
        self.doubleSpinBox.blockSignals(True)
        self.doubleSpinBox.setValue(spinbox_value)
        self.doubleSpinBox.blockSignals(False)

    def spinbox_value_changed(self, value):
        slider_value = int(value * 100)
        self.horizontalSlider_2.blockSignals(True)
        self.horizontalSlider_2.setValue(slider_value)
        self.horizontalSlider_2.blockSignals(False)

    def slider2_value_changed(self, value):
        spinbox_value = value / 100
        self.doubleSpinBox_2.blockSignals(True)
        self.doubleSpinBox_2.setValue(spinbox_value)
        self.doubleSpinBox_2.blockSignals(False)

    def spinbox2_value_changed(self, value):
        slider_value = int(value * 100)
        self.horizontalSlider_3.blockSignals(True)
        self.horizontalSlider_3.setValue(slider_value)
        self.horizontalSlider_3.blockSignals(False)

    def populate_comboBox_6(self):
        folder_path = os.path.join(os.path.dirname(__file__), 'GPT_weights')
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
            self.comboBox_6.addItems(files)

    def populate_comboBox_5(self):
        folder_path = os.path.join(os.path.dirname(__file__), 'SoVITS_weights')
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
            self.comboBox_5.addItems(files)

    def open_file_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if sys.platform == "win32":
            os.startfile(current_dir)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", current_dir])
        else:
            subprocess.Popen(["xdg-open", current_dir])

    #comment page def
    def add_block_word(self):
        # 获取输入的屏蔽词
        block_word = self.block_words_line.text().strip()
        # 检查输入是否为空
        if not block_word:
            self.show_message("Input Error", "Block word cannot be empty.")
            return
        if block_word in self.block_words:
            self.show_message("Input Error", "Block word already in the list.")
            self.block_words_line.clear()
            return
        # 添加屏蔽词到列表并更新模型
        self.block_words.append(block_word)
        self.model.setStringList(self.block_words)
        # 清空输入框
        self.block_words_line.clear()

    def delete_block_word(self):
        # 获取当前选中的项
        selected_indexes = self.list_view.selectedIndexes()
        # 检查输入是否为空
        if not selected_indexes:
            self.show_message("Selection Error", "Please select a block word to delete.")
            return
        # 获取选中的项的索引
        index = selected_indexes[0].row()

        # 从列表中删除选中的项
        del self.block_words[index]

        # 更新模型
        self.model.setStringList(self.block_words)

    def complete_loading(self):
        #print("mainpage")
        current_directory = os.getcwd()
        #print(f"Current directory: {current_directory}")
        flag_path = os.path.join(current_directory, "loading_complete.flag")
        with open(flag_path, "w") as f:
            f.write("Loading complete")
        #print(f"Flag file created at: {flag_path}")
        #print("show mainwindow")


if __name__ == "__main__":
    print("run main")
    global app
    app = QApplication(sys.argv)
    print("run loading")
    mainWindow = MainApp()

    mainWindow.show()
    sys.exit(app.exec_())

