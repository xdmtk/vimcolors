# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import subprocess

CURRENT_SELECTION = None
MAIN_WIN_GLOB = None


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        global MAIN_WIN_GLOB
        MAIN_WIN_GLOB = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(848, 796)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.theme_list = QtWidgets.QListWidget(self.centralWidget)
        self.theme_list.setGeometry(QtCore.QRect(10, 660, 691, 121))
        self.theme_list.setObjectName("theme_list")
        self.theme_view = QtWidgets.QLabel(self.centralWidget)
        self.theme_view.setGeometry(QtCore.QRect(10, 10, 831, 631))
        self.theme_view.setObjectName("theme_view")
        self.theme_view.setText("No theme selected")
        self.theme_view.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)
        self.load_button = QtWidgets.QPushButton(self.centralWidget)
        self.load_button.setGeometry(QtCore.QRect(710, 660, 131, 31))
        self.load_button.setObjectName("load_button")
        self.load_button.setEnabled(False)
        self.package_button = QtWidgets.QPushButton(self.centralWidget)
        self.package_button.setGeometry(QtCore.QRect(710, 690, 131, 31))
        self.package_button.setObjectName("package_button")
        self.revert_button = QtWidgets.QPushButton(self.centralWidget)
        self.revert_button.setGeometry(QtCore.QRect(710, 720, 131, 31))
        self.revert_button.setObjectName("revert_button")
        self.revert_button.setEnabled(False)
        self.delete_button = QtWidgets.QPushButton(self.centralWidget)
        self.delete_button.setGeometry(QtCore.QRect(710, 750, 131, 31))
        self.delete_button.setObjectName("delete_button")
        self.delete_button.setEnabled(False)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.theme_list.itemClicked.connect(self.onclick_theme_list)
        self.load_button.clicked.connect(self.onclick_load_button)
        self.package_button.clicked.connect(self.onclick_package_button)
        self.delete_button.clicked.connect(self.onclick_delete_button)
        self.revert_button.clicked.connect(self.onclick_revert_button)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.load_button.setText(_translate("MainWindow", "&Load"))
        self.package_button.setText(_translate("MainWindow", "&Package"))
        self.revert_button.setText(_translate("MainWindow", "&Revert"))
        self.delete_button.setText(_translate("MainWindow", "&Delete"))



        # Quick and dirty...
        USER = os.environ.get("USER")
        I3P_DIR = "/home/" + USER + "/.config/i3packager/"


        if not (os.path.isdir(I3P_DIR) and os.path.isfile(I3P_DIR + "config")):
            print("[-] Please run CLI application first to generate config file and directory")
            quit()

        theme_dir_listing = os.listdir(I3P_DIR)
        for dir in theme_dir_listing:
            if os.path.isdir(I3P_DIR + dir) and dir != ".last":
                self.theme_list.addItem(dir)

        for dir in theme_dir_listing:
            if dir == ".last":
                self.revert_button.setEnabled(True)

    def onclick_load_button(self):
        if CURRENT_SELECTION is None or CURRENT_SELECTION == "":
            fail_box = QtWidgets.QMessageBox()
            fail_box.setText("Please select a theme to load!")
            fail_box.exec_()
            return
        cur_dir = os.getcwd()
        subprocess.call(['python3', cur_dir + '/i3-package.py', 'load', '-t ', CURRENT_SELECTION, '-g'])
        qbox = QtWidgets.QMessageBox()
        qbox.setText("i3-theme-manager needs to kill the current i3 session to reload the applied theme. \n\n "
                     + "Kill current i3 session?")
        qbox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        retval = qbox.exec_()

        if retval == 1024:
            subprocess.call(['killall', 'i3'])


    def onclick_package_button(self):
        name_package = QtWidgets.QInputDialog()
        (package_name, ok) = name_package.getText(MAIN_WIN_GLOB, "Enter package name", "Enter package name")
        if ok is True:
            cur_dir = os.getcwd()
            subprocess.call(['python3', cur_dir + '/i3-package.py', 'package', '-o ', package_name])


            # Quick and dirty...
            USER = os.environ.get("USER")
            I3P_DIR = "/home/" + USER + "/.config/i3packager/"
            self.theme_list.clear()

            theme_dir_listing = os.listdir(I3P_DIR)
            for dir in theme_dir_listing:
                if os.path.isdir(I3P_DIR + dir) and dir != ".last":
                    self.theme_list.addItem(dir)



    def onclick_theme_list(self):
        global CURRENT_SELECTION
        selected_item = self.theme_list.selectedItems()[0]
        CURRENT_SELECTION = selected_item.text()
        self.load_button.setEnabled(True)
        self.delete_button.setEnabled(True)

        # Quick and dirty...
        USER = os.environ.get("USER")
        I3P_DIR = "/home/" + USER + "/.config/i3packager/"
        image = QtGui.QImage(I3P_DIR + selected_item.text() + '/' + selected_item.text() + '.png')
        image = QtGui.QPixmap.fromImage(image)
        self.theme_view.setPixmap(image.scaled(self.theme_view.width(),self.theme_view.height()))

    def onclick_delete_button(self):
        USER = os.environ.get("USER")
        I3P_DIR = "/home/" + USER + "/.config/i3packager/"

        qbox = QtWidgets.QMessageBox()
        qbox.setText("Delete selected theme '" + CURRENT_SELECTION + "' ?")
        qbox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        retval = qbox.exec_()

        if retval == 1024:
            subprocess.call(['rm', '-rf', I3P_DIR + CURRENT_SELECTION])
            self.theme_list.clear()

            theme_dir_listing = os.listdir(I3P_DIR)
            for dir in theme_dir_listing:
                if os.path.isdir(I3P_DIR + dir) and dir != ".last":
                    self.theme_list.addItem(dir)

            self.theme_view.clear()
            self.theme_view.setText("No theme selected")

    def onclick_revert_button(self):

        qbox = QtWidgets.QMessageBox()
        qbox.setText("Are you sure you want to revert to the last applied theme?")
        qbox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        retval = qbox.exec_()
        cur_dir = os.getcwd()

        if retval == 1024:
            subprocess.call(['python3', cur_dir + '/i3-package.py', 'revert', '-g'])

            qvbox = QtWidgets.QMessageBox()
            qvbox.setText("i3-theme-manager needs to kill the current i3 session to reload the applied theme. \n\n "
                         + "Kill current i3 session?")
            qvbox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            retval_v = qvbox.exec_()

            if retval_v == 1024:
                subprocess.call(['killall', 'i3'])

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

