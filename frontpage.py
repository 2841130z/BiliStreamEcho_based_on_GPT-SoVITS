# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontdesign.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(945, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(945, 450))
        MainWindow.setMaximumSize(QtCore.QSize(945, 450))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 911, 421))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_1 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_1.setObjectName("pushButton_1")
        self.horizontalLayout.addWidget(self.pushButton_1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.verticalLayout_13.addLayout(self.horizontalLayout)
        self.stackedWidget = QtWidgets.QStackedWidget(self.layoutWidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.page)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout()
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_16 = QtWidgets.QLabel(self.page)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_6.addWidget(self.label_16)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.page)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_6.addWidget(self.lineEdit_3)
        self.pushButton = QtWidgets.QPushButton(self.page)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_6.addWidget(self.pushButton)
        self.verticalLayout_19.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_13 = QtWidgets.QLabel(self.page)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_4.addWidget(self.label_13)
        self.lineEdit_10 = QtWidgets.QLineEdit(self.page)
        self.lineEdit_10.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.horizontalLayout_4.addWidget(self.lineEdit_10)
        self.verticalLayout_10.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_21 = QtWidgets.QLabel(self.page)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_8.addWidget(self.label_21)
        self.lineEdit_11 = QtWidgets.QLineEdit(self.page)
        self.lineEdit_11.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.horizontalLayout_8.addWidget(self.lineEdit_11)
        self.verticalLayout_10.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_22 = QtWidgets.QLabel(self.page)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_9.addWidget(self.label_22)
        self.lineEdit_12 = QtWidgets.QLineEdit(self.page)
        self.lineEdit_12.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.horizontalLayout_9.addWidget(self.lineEdit_12)
        self.verticalLayout_10.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.pushButton_9 = QtWidgets.QPushButton(self.page)
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_10.addWidget(self.pushButton_9)
        self.pushButton_12 = QtWidgets.QPushButton(self.page)
        self.pushButton_12.setObjectName("pushButton_12")
        self.horizontalLayout_10.addWidget(self.pushButton_12)
        self.verticalLayout_10.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_7.addLayout(self.verticalLayout_10)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.page)
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout_7.addWidget(self.plainTextEdit)
        self.verticalLayout_19.addLayout(self.horizontalLayout_7)
        self.gridLayout_6.addLayout(self.verticalLayout_19, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.modelselect = QtWidgets.QHBoxLayout()
        self.modelselect.setObjectName("modelselect")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.pushButton_10 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_10.setObjectName("pushButton_10")
        self.verticalLayout_15.addWidget(self.pushButton_10)
        self.pushButton_11 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_11.setObjectName("pushButton_11")
        self.verticalLayout_15.addWidget(self.pushButton_11)
        self.modelselect.addLayout(self.verticalLayout_15)
        self.label_9 = QtWidgets.QLabel(self.page_2)
        self.label_9.setObjectName("label_9")
        self.modelselect.addWidget(self.label_9)
        self.comboBox_6 = QtWidgets.QComboBox(self.page_2)
        self.comboBox_6.setObjectName("comboBox_6")
        self.modelselect.addWidget(self.comboBox_6)
        self.label_10 = QtWidgets.QLabel(self.page_2)
        self.label_10.setObjectName("label_10")
        self.modelselect.addWidget(self.label_10)
        self.comboBox_5 = QtWidgets.QComboBox(self.page_2)
        self.comboBox_5.setObjectName("comboBox_5")
        self.modelselect.addWidget(self.comboBox_5)
        self.verticalLayout_7.addLayout(self.modelselect)
        self.referdetail_2 = QtWidgets.QHBoxLayout()
        self.referdetail_2.setObjectName("referdetail_2")
        self.label_6 = QtWidgets.QLabel(self.page_2)
        self.label_6.setObjectName("label_6")
        self.referdetail_2.addWidget(self.label_6)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.referdetail_2.addWidget(self.lineEdit_6)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.referdetail_2.addLayout(self.verticalLayout_14)
        self.verticalLayout_7.addLayout(self.referdetail_2)
        self.referdetail = QtWidgets.QHBoxLayout()
        self.referdetail.setObjectName("referdetail")
        self.label_7 = QtWidgets.QLabel(self.page_2)
        self.label_7.setObjectName("label_7")
        self.referdetail.addWidget(self.label_7)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.referdetail.addWidget(self.lineEdit_4)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.referdetail.addLayout(self.verticalLayout_4)
        self.verticalLayout_7.addLayout(self.referdetail)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.modeldetail = QtWidgets.QHBoxLayout()
        self.modeldetail.setObjectName("modeldetail")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.page_2)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.page_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.page_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.modeldetail.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalSlider = QtWidgets.QSlider(self.page_2)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setProperty("value", 5)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout_2.addWidget(self.horizontalSlider)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.page_2)
        self.horizontalSlider_2.setMaximum(100)
        self.horizontalSlider_2.setSingleStep(5)
        self.horizontalSlider_2.setPageStep(10)
        self.horizontalSlider_2.setProperty("value", 100)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.verticalLayout_2.addWidget(self.horizontalSlider_2)
        self.horizontalSlider_3 = QtWidgets.QSlider(self.page_2)
        self.horizontalSlider_3.setMaximum(100)
        self.horizontalSlider_3.setSingleStep(5)
        self.horizontalSlider_3.setProperty("value", 100)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.verticalLayout_2.addWidget(self.horizontalSlider_3)
        self.modeldetail.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.spinBox = QtWidgets.QSpinBox(self.page_2)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(100)
        self.spinBox.setProperty("value", 5)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout_3.addWidget(self.spinBox)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.page_2)
        self.doubleSpinBox.setMaximum(1.0)
        self.doubleSpinBox.setSingleStep(0.05)
        self.doubleSpinBox.setProperty("value", 1.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.verticalLayout_3.addWidget(self.doubleSpinBox)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.page_2)
        self.doubleSpinBox_2.setMaximum(1.0)
        self.doubleSpinBox_2.setSingleStep(0.05)
        self.doubleSpinBox_2.setProperty("value", 1.0)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.verticalLayout_3.addWidget(self.doubleSpinBox_2)
        self.modeldetail.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2.addLayout(self.modeldetail)
        self.cutlayout = QtWidgets.QHBoxLayout()
        self.cutlayout.setObjectName("cutlayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.page_2)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.label_8 = QtWidgets.QLabel(self.page_2)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_5.addWidget(self.label_8)
        self.label_4 = QtWidgets.QLabel(self.page_2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.cutlayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.comboBox_2 = QtWidgets.QComboBox(self.page_2)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.verticalLayout_6.addWidget(self.comboBox_2)
        self.comboBox_4 = QtWidgets.QComboBox(self.page_2)
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.verticalLayout_6.addWidget(self.comboBox_4)
        self.comboBox_7 = QtWidgets.QComboBox(self.page_2)
        self.comboBox_7.setObjectName("comboBox_7")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.verticalLayout_6.addWidget(self.comboBox_7)
        self.cutlayout.addLayout(self.verticalLayout_6)
        self.horizontalLayout_2.addLayout(self.cutlayout)
        self.pushButton_5 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout_7, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.page_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_17 = QtWidgets.QLabel(self.page_3)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_16.addWidget(self.label_17)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.page_3)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.verticalLayout_16.addWidget(self.lineEdit_5)
        self.label_18 = QtWidgets.QLabel(self.page_3)
        self.label_18.setObjectName("label_18")
        self.verticalLayout_16.addWidget(self.label_18)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.page_3)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.verticalLayout_16.addWidget(self.lineEdit_7)
        self.label_19 = QtWidgets.QLabel(self.page_3)
        self.label_19.setObjectName("label_19")
        self.verticalLayout_16.addWidget(self.label_19)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.page_3)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.verticalLayout_16.addWidget(self.lineEdit_8)
        self.label_20 = QtWidgets.QLabel(self.page_3)
        self.label_20.setObjectName("label_20")
        self.verticalLayout_16.addWidget(self.label_20)
        self.lineEdit_9 = QtWidgets.QLineEdit(self.page_3)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.verticalLayout_16.addWidget(self.lineEdit_9)
        self.gridLayout_4.addLayout(self.verticalLayout_16, 0, 0, 1, 1)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_11 = QtWidgets.QLabel(self.page_3)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_3.addWidget(self.label_11)
        self.lineEdit = QtWidgets.QLineEdit(self.page_3)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.pushButton_6 = QtWidgets.QPushButton(self.page_3)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_3.addWidget(self.pushButton_6)
        self.pushButton_13 = QtWidgets.QPushButton(self.page_3)
        self.pushButton_13.setObjectName("pushButton_13")
        self.horizontalLayout_3.addWidget(self.pushButton_13)
        self.verticalLayout_9.addLayout(self.horizontalLayout_3)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_12 = QtWidgets.QLabel(self.page_3)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_8.addWidget(self.label_12)
        self.listView = QtWidgets.QListView(self.page_3)
        self.listView.setObjectName("listView")
        self.verticalLayout_8.addWidget(self.listView)
        self.verticalLayout_9.addLayout(self.verticalLayout_8)
        self.gridLayout_4.addLayout(self.verticalLayout_9, 0, 2, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.page_3)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_4.addWidget(self.checkBox, 1, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.page_3)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_4.addWidget(self.pushButton_7, 1, 2, 1, 1)
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.page_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_14 = QtWidgets.QLabel(self.page_4)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_5.addWidget(self.label_14)
        self.comboBox_3 = QtWidgets.QComboBox(self.page_4)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.horizontalLayout_5.addWidget(self.comboBox_3)
        self.pushButton_8 = QtWidgets.QPushButton(self.page_4)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_5.addWidget(self.pushButton_8)
        self.verticalLayout_11.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_23 = QtWidgets.QLabel(self.page_4)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_11.addWidget(self.label_23)
        self.label_24 = QtWidgets.QLabel(self.page_4)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_11.addWidget(self.label_24)
        self.verticalLayout_11.addLayout(self.horizontalLayout_11)
        self.gridLayout_5.addLayout(self.verticalLayout_11, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_4)
        self.verticalLayout_13.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.horizontalSlider.valueChanged['int'].connect(self.spinBox.setValue) # type: ignore
        self.spinBox.valueChanged['int'].connect(self.horizontalSlider.setValue) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BiliStreamEcho"))
        self.pushButton_1.setText(_translate("MainWindow", "Home"))
        self.pushButton_2.setText(_translate("MainWindow", "Model"))
        self.pushButton_3.setText(_translate("MainWindow", "Comment"))
        self.pushButton_4.setText(_translate("MainWindow", "About"))
        self.label_16.setText(_translate("MainWindow", "  ID code"))
        self.pushButton.setText(_translate("MainWindow", "Start Server"))
        self.label_13.setText(_translate("MainWindow", " SESSDATA"))
        self.label_21.setText(_translate("MainWindow", " bili_jct"))
        self.label_22.setText(_translate("MainWindow", "  buvid3 "))
        self.pushButton_9.setText(_translate("MainWindow", "Test TTS"))
        self.pushButton_12.setText(_translate("MainWindow", "Apply"))
        self.pushButton_10.setText(_translate("MainWindow", "Refresh"))
        self.pushButton_11.setText(_translate("MainWindow", "File Path"))
        self.label_9.setText(_translate("MainWindow", "       GPT_Model"))
        self.label_10.setText(_translate("MainWindow", "        SoVITS_Model"))
        self.label_6.setText(_translate("MainWindow", "   Reference Audio  "))
        self.label_7.setText(_translate("MainWindow", "   Audio Subtitle   "))
        self.label.setToolTip(_translate("MainWindow", "toolTip test"))
        self.label.setText(_translate("MainWindow", "   top_k"))
        self.label_2.setText(_translate("MainWindow", "   top_p"))
        self.label_3.setText(_translate("MainWindow", "temperature"))
        self.label_5.setText(_translate("MainWindow", " Reference_Language "))
        self.label_8.setText(_translate("MainWindow", " Cutting_Method "))
        self.label_4.setText(_translate("MainWindow", " Output_Language "))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Chinese"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "English"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "Japanese"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "Chinese and English"))
        self.comboBox_2.setItemText(4, _translate("MainWindow", "Japanese and English"))
        self.comboBox_2.setItemText(5, _translate("MainWindow", "Multilingual"))
        self.comboBox_4.setItemText(0, _translate("MainWindow", "No slice"))
        self.comboBox_4.setItemText(1, _translate("MainWindow", "Slice once every 4 sentences"))
        self.comboBox_4.setItemText(2, _translate("MainWindow", "Cut per 50 characters"))
        self.comboBox_4.setItemText(3, _translate("MainWindow", "Slice by Chinese punct"))
        self.comboBox_4.setItemText(4, _translate("MainWindow", "Slice by English punct"))
        self.comboBox_4.setItemText(5, _translate("MainWindow", "Slice by every punct"))
        self.comboBox_7.setItemText(0, _translate("MainWindow", "Chinese"))
        self.comboBox_7.setItemText(1, _translate("MainWindow", "English"))
        self.comboBox_7.setItemText(2, _translate("MainWindow", "Japanese"))
        self.comboBox_7.setItemText(3, _translate("MainWindow", "Chinese and English"))
        self.comboBox_7.setItemText(4, _translate("MainWindow", "Japanese and English"))
        self.comboBox_7.setItemText(5, _translate("MainWindow", "Multilingual"))
        self.pushButton_5.setText(_translate("MainWindow", "Apply"))
        self.label_17.setText(_translate("MainWindow", "When receiving a comment:"))
        self.label_18.setText(_translate("MainWindow", "When receiving a super chat:"))
        self.label_19.setText(_translate("MainWindow", "When receiving a gift:"))
        self.label_20.setText(_translate("MainWindow", "When a user joins as a member:"))
        self.label_11.setText(_translate("MainWindow", "Block Words"))
        self.pushButton_6.setText(_translate("MainWindow", "ADD"))
        self.pushButton_13.setText(_translate("MainWindow", "DELETE"))
        self.label_12.setText(_translate("MainWindow", "Block Words List"))
        self.checkBox.setText(_translate("MainWindow", "Punctuation filter"))
        self.pushButton_7.setText(_translate("MainWindow", "Apply"))
        self.label_14.setText(_translate("MainWindow", " System_Language "))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "English"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "Chinese"))
        self.pushButton_8.setText(_translate("MainWindow", "Apply"))
        self.label_23.setText(_translate("MainWindow", "                       中文教程"))
        self.label_24.setText(_translate("MainWindow", "                     English Tutorial"))
