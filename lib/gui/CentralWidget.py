import sys
import os
import tkinter as tk
from PySide2.QtCore import (
    Qt
)

from PySide2.QtWidgets import (
    QWidget,
    QApplication,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QTabWidget,
    QLineEdit,
    QLabel,
    QSpacerItem,
    QSpinBox,
    QDoubleSpinBox
)
from PySide2.QtGui import (
    QIcon
)

import lib.gui.commonFunctions as comFunc
import lib.core.projectFlags as projFlags
import lib.core.file_manipulation as file_manip

_PROJECT_FOLDER = os.path.normpath(os.path.realpath(__file__) + '/../../../')

_INT_SCREEN_WIDTH = tk.Tk().winfo_screenwidth()  # get the screen width
_INT_SCREEN_HEIGHT = tk.Tk().winfo_screenheight()  # get the screen height
_INT_WIN_WIDTH = 1024  # this variable is only for the if __name__ == "__main__"
_INT_WIN_HEIGHT = 512  # this variable is only for the if __name__ == "__main__"

_INT_MAX_STRETCH = 100000  # Spacer Max Stretch
_INT_BUTTON_MIN_WIDTH = 50  # Minimum Button Width


class WidgetCentral(QWidget):
    def __init__(self, w=512, h=512, minW=256, minH=256, maxW=512, maxH=512,
                 winTitle='My Window', iconPath=''):
        super().__init__()
        # ---------------------- #
        # ----- Set Window ----- #
        # ---------------------- #
        self.setWindowTitle(winTitle)  # Set Window Title
        self.setWindowIcon(QIcon(iconPath))  # Set Window Icon
        self.setGeometry(_INT_SCREEN_WIDTH / 4, _INT_SCREEN_HEIGHT / 4, w, h)  # Set Window Geometry
        self.setMinimumWidth(minW)  # Set Window Minimum Width
        self.setMinimumHeight(minH)  # Set Window Minimum Height
        if maxW is not None:
            self.setMaximumWidth(maxW)  # Set Window Maximum Width
        if maxH is not None:
            self.setMaximumHeight(maxH)  # Set Window Maximum Width

        self.vbox_main_layout = QVBoxLayout(self)  # Create the main vbox

        # -------------------- #
        # ---- QTabWidget ---- #
        # -------------------- #
        self.tabWidgetMain = QTabWidget()

        self.tabWidgetGeneral = WidgetTabGeneral()
        self.tabDownloadFromSentinelHub = WidgetTabDownloadFromSentinelHub()
        self.tabStorageImageBackendProcessing = WidgetTabStorageImageBackendProcessing()

    def setWidget(self):
        # Set buttons in hbox
        self.tabWidgetGeneral.setWidget()
        self.tabWidgetMain.addTab(self.tabWidgetGeneral, 'General')
        self.tabDownloadFromSentinelHub.setWidget()
        self.tabWidgetMain.addTab(self.tabDownloadFromSentinelHub, 'Download From Sentinel-Hub')
        self.tabStorageImageBackendProcessing.setWidget()
        self.tabWidgetMain.addTab(self.tabStorageImageBackendProcessing, 'Storage Image Backend Processing')

        hbox_tab = QHBoxLayout()  # Create Horizontal Layout
        hbox_tab.addWidget(self.tabWidgetMain)

        self.vbox_main_layout.addLayout(hbox_tab)

    # ------------------- #
    # ----- Actions ----- #
    # ------------------- #
    def setActions_(self):
        pass


class WidgetTabGeneral(QWidget):
    def __init__(self):
        super().__init__()

        # ---------------------- #
        # ----- Set Window ----- #
        # ---------------------- #
        self.vbox_main_layout = QVBoxLayout(self)  # Create the main vbox

        # ----------------------- #
        # ----- QPushButton ----- #
        # ----------------------- #
        self.button_Navigate = QPushButton()
        self.button_Navigate.setIcon(QIcon(projFlags.ICON_NAVIGATE_PATH))

        self.button_RestoreDefaults = QPushButton('Restore Defaults')
        # --------------------- #
        # ----- QLineEdit ----- #
        # --------------------- #
        self.lineEdit_Path = QLineEdit()
        self.lineEdit_Path.setEnabled(False)

        # ------------------------------ #
        # ----- Set Default Values ----- #
        # ------------------------------ #
        self._DEFAULT_STORAGE_PATH = projFlags.STR_STORAGE_DEFAULT_PATH

    # --------------------------- #
    # ----- Reuse Functions ----- #
    # --------------------------- #
    def setWidget(self):
        """
            A function to create the widget components into the main QWidget
            :return: Nothing
        """
        self.restoreDefaultValues()
        self.setEvents_()

        label_storage_path = QLabel('Storage Path:')

        hbox_storage_path = QHBoxLayout()
        hbox_storage_path.addWidget(label_storage_path)
        hbox_storage_path.addWidget(self.lineEdit_Path)
        hbox_storage_path.addWidget(self.button_Navigate)

        hbox_restore_defaults_button = QHBoxLayout()
        hbox_restore_defaults_button.addSpacerItem(QSpacerItem(projFlags.INT_MAX_STRETCH, 0))
        hbox_restore_defaults_button.addWidget(self.button_RestoreDefaults)

        self.vbox_main_layout.addLayout(hbox_storage_path)
        self.vbox_main_layout.addSpacerItem(QSpacerItem(0, projFlags.INT_MAX_STRETCH))
        self.vbox_main_layout.addLayout(hbox_restore_defaults_button)

    def restoreDefaultValues(self):
        # set default value
        self.lineEdit_Path.setText(self.getDefaultStoragePath())

    def setEvents_(self):
        self.button_RestoreDefaults.clicked.connect(self.restoreDefaultValues)
        self.button_Navigate.clicked.connect(self.actionNavigate)

    # ----------------------- #
    # ----- GET ACTIONS ----- #
    # ----------------------- #
    def actionNavigate(self):
        success, dirPath = comFunc.openDirectoryDialog(
            classRef=self,
            dialogName='Select a Directory',
            dialogOpenAt=self.getCurrentStoragePath(),
            dialogMultipleSelection=False)

        if success:
            self.lineEdit_Path.setText(file_manip.realPath(file_manip.normPath(dirPath)))

    # ------------------- #
    # ----- GETTERS ----- #
    # ------------------- #
    def getCurrentStoragePath(self):
        return self.lineEdit_Path.text()

    # ------------------------------ #
    # ----- GET DEFAULT VALUES ----- #
    # ------------------------------ #
    def getDefaultStoragePath(self):
        return self._DEFAULT_STORAGE_PATH


class WidgetTabDownloadFromSentinelHub(QWidget):
    def __init__(self):
        super().__init__()

        # ---------------------- #
        # ----- Set Window ----- #
        # ---------------------- #
        self.vbox_main_layout = QVBoxLayout(self)  # Create the main vbox

        # ----------------------- #
        # ----- QPushButton ----- #
        # ----------------------- #
        self.button_RestoreDefault = QPushButton('Restore Default')
        self.button_Config = QPushButton('Config')
        self.button_DownloadImages = QPushButton('Download Image(s)')

        # -------------------- #
        # ----- QSpinBox ----- #
        # -------------------- #
        self.spinBox_StartYear = QSpinBox()
        self.spinBox_StartYear.setMinimum(1990)
        self.spinBox_StartYear.setMaximum(file_manip.getCurrentYear())
        self.spinBox_StartYear.setAlignment(Qt.AlignCenter)
        self.spinBox_StartYear.setMaximumWidth(80)

        self.spinBox_StartMonth = QSpinBox()
        self.spinBox_StartMonth.setMinimum(1)
        self.spinBox_StartMonth.setMaximum(12)
        self.spinBox_StartMonth.setAlignment(Qt.AlignCenter)
        self.spinBox_StartMonth.setMaximumWidth(80)

        self.spinBox_StartDay = QSpinBox()
        self.spinBox_StartDay.setMinimum(1)
        self.spinBox_StartDay.setMaximum(31)
        self.spinBox_StartDay.setAlignment(Qt.AlignCenter)
        self.spinBox_StartDay.setMaximumWidth(80)

        self.spinBox_EndYear = QSpinBox()
        self.spinBox_EndYear.setMinimum(1990)
        self.spinBox_EndYear.setMaximum(file_manip.getCurrentYear())
        self.spinBox_EndYear.setAlignment(Qt.AlignCenter)
        self.spinBox_EndYear.setMaximumWidth(80)

        self.spinBox_EndMonth = QSpinBox()
        self.spinBox_EndMonth.setMinimum(1)
        self.spinBox_EndMonth.setMaximum(12)
        self.spinBox_EndMonth.setAlignment(Qt.AlignCenter)
        self.spinBox_EndMonth.setMaximumWidth(80)

        self.spinBox_EndDay = QSpinBox()
        self.spinBox_EndDay.setMinimum(1)
        self.spinBox_EndDay.setMaximum(31)
        self.spinBox_EndDay.setAlignment(Qt.AlignCenter)
        self.spinBox_EndDay.setMaximumWidth(80)

        self.spinBox_ChunkSize = QSpinBox()
        self.spinBox_ChunkSize.setSingleStep(1)

        # -------------------------- #
        # ----- QDoubleSpinBox ----- #
        # -------------------------- #
        self.doubleSpinBox_Resolution = QDoubleSpinBox()
        self.doubleSpinBox_Resolution.setDecimals(2)
        self.doubleSpinBox_Resolution.setSingleStep(0.05)
        self.doubleSpinBox_Resolution.setMaximumWidth(80)

        self.doubleSpinBox_MinLongitude = QDoubleSpinBox()
        self.doubleSpinBox_MinLongitude.setDecimals(2)
        self.doubleSpinBox_MinLongitude.setSingleStep(0.05)
        self.doubleSpinBox_MinLongitude.setMaximumWidth(80)

        self.doubleSpinBox_MinLatitude = QDoubleSpinBox()
        self.doubleSpinBox_MinLatitude.setDecimals(2)
        self.doubleSpinBox_MinLatitude.setSingleStep(0.05)
        self.doubleSpinBox_MinLatitude.setMaximumWidth(80)

        self.doubleSpinBox_MaxLongitude = QDoubleSpinBox()
        self.doubleSpinBox_MinLongitude.setDecimals(2)
        self.doubleSpinBox_MaxLongitude.setSingleStep(0.05)
        self.doubleSpinBox_MaxLongitude.setMaximumWidth(80)

        self.doubleSpinBox_MaxLatitude = QDoubleSpinBox()
        self.doubleSpinBox_MaxLatitude.setDecimals(2)
        self.doubleSpinBox_MaxLatitude.setSingleStep(0.05)
        self.doubleSpinBox_MaxLatitude.setMaximumWidth(80)

        # --------------------- #
        # ----- QLineEdit ----- #
        # --------------------- #

        # --------------------- #
        # ----- QComboBox ----- #
        # --------------------- #

        # ------------------------------ #
        # ----- Set Default Values ----- #
        # ------------------------------ #

    # --------------------------- #
    # ----- Reuse Functions ----- #
    # --------------------------- #
    def setWidget(self):
        """
            A function to create the widget components into the main QWidget
            :return: Nothing
        """
        self.restoreDefaultValues()
        self.setEvents_()

        labelEmpty = QLabel('')
        labelEmpty.setMinimumWidth(20)

        label_StartDate = QLabel('<b>Start Date:<\\b>')
        label_StartDate.setMinimumWidth(160)
        label_StartDate.setMaximumWidth(160)
        label_StartDate.setAlignment(Qt.AlignCenter)

        label_StartYear = QLabel('Start Year:')
        label_StartYear.setMinimumWidth(80)
        label_StartYear.setMaximumWidth(80)

        label_StartMonth = QLabel('Start Month:')
        label_StartMonth.setMinimumWidth(80)
        label_StartMonth.setMaximumWidth(80)

        label_StartDay = QLabel('Start Day:')
        label_StartDay.setMinimumWidth(80)
        label_StartDay.setMaximumWidth(80)

        label_EndDate = QLabel('<b>End Date:<\\b>')
        label_EndDate.setMinimumWidth(160)
        label_EndDate.setMaximumWidth(160)
        label_EndDate.setAlignment(Qt.AlignCenter)

        label_EndYear = QLabel('End Year:')
        label_EndYear.setMinimumWidth(80)
        label_EndYear.setMaximumWidth(80)

        label_EndMonth = QLabel('End Month:')
        label_EndMonth.setMinimumWidth(80)
        label_EndMonth.setMaximumWidth(80)

        label_EndDay = QLabel('End Day:')
        label_EndDay.setMinimumWidth(80)
        label_EndDay.setMaximumWidth(80)

        label_ChunkSize = QLabel('Chunk Size:')
        label_ChunkSize.setMinimumWidth(80)
        label_ChunkSize.setMinimumWidth(80)

        label_Resolution = QLabel('Resolution (meters):')
        label_MinLongitude = QLabel('Minimum Longitude:')
        label_MinLongitude = QLabel('Minimum Latitude:')
        label_MaxLongitude = QLabel('Maximum Longitude:')
        label_MaxLongitude = QLabel('Maximum Latitude:')

        hbox_StartYear = QHBoxLayout()
        hbox_StartYear.addWidget(label_StartYear)
        hbox_StartYear.addWidget(self.spinBox_StartYear)

        hbox_StartMonth = QHBoxLayout()
        hbox_StartMonth.addWidget(label_StartMonth)
        hbox_StartMonth.addWidget(self.spinBox_StartMonth)

        hbox_StartDay = QHBoxLayout()
        hbox_StartDay.addWidget(label_StartDay)
        hbox_StartDay.addWidget(self.spinBox_StartDay)

        vbox_StartDate = QVBoxLayout()
        vbox_StartDate.addWidget(label_StartDate)
        vbox_StartDate.addLayout(hbox_StartYear)
        vbox_StartDate.addLayout(hbox_StartMonth)
        vbox_StartDate.addLayout(hbox_StartDay)

        hbox_EndYear = QHBoxLayout()
        hbox_EndYear.addWidget(label_EndYear)
        hbox_EndYear.addWidget(self.spinBox_EndYear)

        hbox_EndMonth = QHBoxLayout()
        hbox_EndMonth.addWidget(label_EndMonth)
        hbox_EndMonth.addWidget(self.spinBox_EndMonth)

        hbox_EndDay = QHBoxLayout()
        hbox_EndDay.addWidget(label_EndDay)
        hbox_EndDay.addWidget(self.spinBox_EndDay)

        vbox_EndDate = QVBoxLayout()
        vbox_EndDate.addWidget(label_EndDate)
        vbox_EndDate.addLayout(hbox_EndYear)
        vbox_EndDate.addLayout(hbox_EndMonth)
        vbox_EndDate.addLayout(hbox_EndDay)

        hbox_DateOptions = QHBoxLayout()
        hbox_DateOptions.addLayout(vbox_StartDate)
        hbox_DateOptions.addWidget(labelEmpty)
        hbox_DateOptions.addLayout(vbox_EndDate)
        hbox_DateOptions.addSpacerItem(QSpacerItem(projFlags.INT_MAX_STRETCH, 0))

        hbox_ChunkSize = QHBoxLayout()
        hbox_ChunkSize.addWidget(label_ChunkSize)
        hbox_ChunkSize.addWidget(self.spinBox_ChunkSize)

        self.vbox_main_layout.addLayout(hbox_DateOptions)
        self.vbox_main_layout.addSpacerItem(QSpacerItem(0, projFlags.INT_MAX_STRETCH))

    def restoreDefaultValues(self):
        # set default value
        pass

    def setEvents_(self):
        pass

    # ------------------------------ #
    # ----- GET DEFAULT VALUES ----- #
    # ------------------------------ #


class WidgetTabStorageImageBackendProcessing(QWidget):
    def __init__(self):
        super().__init__()

        # ---------------------- #
        # ----- Set Window ----- #
        # ---------------------- #
        self.vbox_main_layout = QVBoxLayout(self)  # Create the main vbox

        # ----------------------- #
        # ----- QPushButton ----- #
        # ----------------------- #

        # -------------------- #
        # ----- QSpinBox ----- #
        # -------------------- #

        # -------------------------- #
        # ----- QDoubleSpinBox ----- #
        # -------------------------- #

        # --------------------- #
        # ----- QLineEdit ----- #
        # --------------------- #

        # --------------------- #
        # ----- QComboBox ----- #
        # --------------------- #

        # ------------------------------ #
        # ----- Set Default Values ----- #
        # ------------------------------ #

    # --------------------------- #
    # ----- Reuse Functions ----- #
    # --------------------------- #
    def setWidget(self):
        """
            A function to create the widget components into the main QWidget
            :return: Nothing
        """
        self.restoreDefaultValues()
        self.setEvents_()

    def restoreDefaultValues(self):
        # set default value
        pass

    def setEvents_(self):
        pass

    # ------------------------------ #
    # ----- GET DEFAULT VALUES ----- #
    # ------------------------------ #


# ******************************************************* #
# ********************   EXECUTION   ******************** #
# ******************************************************* #

def exec_app(w=512, h=512, minW=256, minH=256, maxW=512, maxH=512, winTitle='My Window', iconPath=''):
    myApp = QApplication(sys.argv)  # Set Up Application
    widgetWin = WidgetCentral(w=w, h=h, minW=minW, minH=minH, maxW=maxW, maxH=maxH,
                              winTitle=winTitle, iconPath=iconPath)  # Create MainWindow
    widgetWin.show()  # Show Window
    myApp.exec_()  # Execute Application
    sys.exit(0)  # Exit Application


if __name__ == "__main__":
    exec_app(w=1024, h=512, minW=512, minH=256, maxW=512, maxH=512,
             winTitle='WidgetTemplate', iconPath=_PROJECT_FOLDER + '/icon/crabsMLearning_32x32.png')
