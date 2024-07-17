import sys
import os
import subprocess
import json
import asyncio

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPlainTextEdit
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot,QStringListModel,QObject
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
        self.setupUi(self)
        self.server_thread = None

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
        self.list_view=self.findChild(QtWidgets.QListView, 'listView')
        self.block_words_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.pushButton_6.clicked.connect(self.add_block_word)
        self.pushButton_13.clicked.connect(self.delete_block_word)
        self.comment_format_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit_5')
        self.SC_format_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit_7')
        self.gift_format_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit_8')
        self.member_format_line = self.findChild(QtWidgets.QLineEdit, 'lineEdit_9')
        # 创建字符串列表模型
        self.model = QStringListModel()
        self.list_view.setModel(self.model)


        #load parameters
        self.load_parameters()
        #set bilibiliapi
        self.bilibili_api = BilibiliApi(self.SESSDATA_line.text(),self.bili_jct_line.text(),self.buvid3_line.text())
        self.bilibili_api.connection_established.connect(self.on_server_started)
        self.bilibili_api.connection_closed.connect(self.on_server_stopped)

    #apply button def
    def save_parameters(self):
        #global parameters_changed
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
            "Block_Words": self.block_words,
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
            #home load
            self.ID_code_line.setText(parameters.get("ID_code", ""))
            self.SESSDATA_line.setText(parameters.get("SESSDATA", ""))
            self.bili_jct_line.setText(parameters.get("bili_jct", ""))
            self.buvid3_line.setText(parameters.get("buvid3", ""))
            #model load
            self.gpt_model_combo.setCurrentText(parameters.get("GPT_Model", ""))
            self.sovits_model_combo.setCurrentText(parameters.get("SoVITS_Model", ""))
            self.reference_audio_line.setText(parameters.get("refer_wav_path", ""))
            self.audio_subtitle_line.setText(parameters.get("prompt_text", ""))
            self.top_k_spin.setValue(parameters.get("top_k", 0))
            self.top_p_spin.setValue(parameters.get("top_p", 0.0))
            self.temperature_spin.setValue(parameters.get("temperature", 0.0))
            self.reference_language_combo.setCurrentText(parameters.get("prompt_language", ""))
            self.cutting_method_combo.setCurrentText(parameters.get("how_to_cut", ""))
            self.output_language_combo.setCurrentText(parameters.get("text_language", ""))
            #comment load
            self.comment_format_line.setText(parameters.get("Comment_format",""))
            self.SC_format_line.setText(parameters.get("SC_format", ""))
            self.gift_format_line.setText(parameters.get("gift_format", ""))
            self.member_format_line.setText(parameters.get("member_format", ""))
            # 检查 Block_Words 是否存在且不为空
            block_words = parameters.get("Block_Words")
            if block_words:  # 这将检查 block_words 是否为 None 或空列表
                self.block_words = block_words
            else:# 初始化屏蔽词列表
                self.block_words = []

            self.model.setStringList(self.block_words)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainApp()
    mainWindow.show()
    sys.exit(app.exec_())
