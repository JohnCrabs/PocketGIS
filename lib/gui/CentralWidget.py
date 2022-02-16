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
    QDoubleSpinBox,
    QListWidget,
    QListWidgetItem,
    QCheckBox,
    QTextEdit
)
from PySide2.QtGui import (
    QIcon
)

import lib.gui.commonFunctions as comFunc
import lib.core.common.projectFlags as projFlags
import lib.core.common.projectFuctions as projFunc
import lib.core.common.file_manipulation as file_manip
import lib.core.base.SentinelHubDownloader as shd
import lib.core.base.EvaluationScripts as evalScript
import lib.core.base.GeotiffProcessing as geoProc

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
        self.tabStorageImageVisualizing = WidgetTabStorageImageVisualizing()

    def setWidget(self):
        # Set buttons in hbox
        self.setActions_()

        self.tabWidgetGeneral.setWidget()
        self.tabWidgetMain.addTab(self.tabWidgetGeneral, 'General')
        self.tabDownloadFromSentinelHub.setWidget()
        self.tabWidgetMain.addTab(self.tabDownloadFromSentinelHub, 'Download From Sentinel-Hub')
        self.tabStorageImageBackendProcessing.setWidget()
        self.tabWidgetMain.addTab(self.tabStorageImageBackendProcessing, 'Storage Image Backend Processing')
        self.tabStorageImageVisualizing.setWidget()
        self.tabWidgetMain.addTab(self.tabStorageImageVisualizing, 'Image Visualizing')

        hbox_tab = QHBoxLayout()  # Create Horizontal Layout
        hbox_tab.addWidget(self.tabWidgetMain)

        self.vbox_main_layout.addLayout(hbox_tab)

    # ------------------- #
    # ----- Actions ----- #
    # ------------------- #
    def setActions_(self):
        self.tabDownloadFromSentinelHub.button_DownloadImages.clicked.connect(self.setButtonDownloadImagesClicked)
        self.tabStorageImageBackendProcessing.button_RefreshList.clicked.connect(self.setButtonRefreshListImage_BackendProcessing)
        self.tabStorageImageVisualizing.button_RefreshList.clicked.connect(self.setButtonRefreshListImage_Visualizing)

    def setButtonDownloadImagesClicked(self):
        instanceID = self.tabDownloadFromSentinelHub.getValueInstanceID()
        clientID = self.tabDownloadFromSentinelHub.getValueClientID()
        clientSecret = self.tabDownloadFromSentinelHub.getValueClientSecret()

        storagePath = self.tabWidgetGeneral.getCurrentStoragePath()
        startYear = self.tabDownloadFromSentinelHub.getValueStartYear()
        startMonth = self.tabDownloadFromSentinelHub.getValueStartMonth()
        startDay = self.tabDownloadFromSentinelHub.getValueStartDay()
        endYear = self.tabDownloadFromSentinelHub.getValueEndYear()
        endMonth = self.tabDownloadFromSentinelHub.getValueEndMonth()
        endDay = self.tabDownloadFromSentinelHub.getValueEndDay()
        chunkSize = self.tabDownloadFromSentinelHub.getValueChunkSize()
        minLatitude = round(self.tabDownloadFromSentinelHub.getValueMinLatitude(), 2)
        minLongitude = round(self.tabDownloadFromSentinelHub.getValueMinLongitude(), 2)
        maxLatitude = round(self.tabDownloadFromSentinelHub.getValueMaxLatitude(), 2)
        maxLongitude = round(self.tabDownloadFromSentinelHub.getValueMaxLongitude(), 2)
        resolution = self.tabDownloadFromSentinelHub.getValueResolution()

        listSelectedJSON = self.tabDownloadFromSentinelHub.getListSelectionJSON()

        sentinelHubDownloader = shd.SentinelHubDownloader()
        sentinelHubDownloader.setStoragePath(path=storagePath)
        sentinelHubDownloader.setSentinelHubConfiguration(
            instance_id=instanceID,
            client_id=clientID,
            client_secret=clientSecret
        )
        sentinelHubDownloader.setTimeSlots(
            startYear=startYear, startMonth=startMonth, startDay=startDay,
            endYear=endYear, endMonth=endMonth, endDay=endDay,
            n_chunks=chunkSize
        )
        sentinelHubDownloader.setAreaOfInterest(
            minLatitude=minLatitude, minLongitude=minLongitude,
            maxLatitude=maxLatitude, maxLongitude=maxLongitude,
            spatialResolution=resolution
        )

        sentinelHubDownloader.imgDownload(listSelectedJSON)

    def setButtonRefreshListImage_BackendProcessing(self):
        self.tabStorageImageBackendProcessing.setStoragePath(self.tabWidgetGeneral.getCurrentStoragePath())
        self.tabStorageImageBackendProcessing.setImageCollectionJSON()
        self.tabStorageImageBackendProcessing.setGeoDatabaseProcessing()

    def setButtonRefreshListImage_Visualizing(self):
        self.tabStorageImageVisualizing.setStoragePath(self.tabWidgetGeneral.getCurrentStoragePath())
        self.tabStorageImageVisualizing.setImageCollectionJSON()
        self.tabStorageImageVisualizing.setGeoDatabaseProcessing()


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

        self.widgetConfig = WidgetConfig(w=428, h=256,
                                         minW=428, minH=256,
                                         maxW=428, maxH=256,
                                         winTitle='Config', iconPath='')

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
        self.spinBox_StartYear.setMinimumHeight(20)

        self.spinBox_StartMonth = QSpinBox()
        self.spinBox_StartMonth.setMinimum(1)
        self.spinBox_StartMonth.setMaximum(12)
        self.spinBox_StartMonth.setAlignment(Qt.AlignCenter)
        self.spinBox_StartMonth.setMaximumWidth(80)
        self.spinBox_StartMonth.setMinimumHeight(20)

        self.spinBox_StartDay = QSpinBox()
        self.spinBox_StartDay.setMinimum(1)
        self.spinBox_StartDay.setMaximum(31)
        self.spinBox_StartDay.setAlignment(Qt.AlignCenter)
        self.spinBox_StartDay.setMaximumWidth(80)
        self.spinBox_StartDay.setMinimumHeight(20)

        self.spinBox_EndYear = QSpinBox()
        self.spinBox_EndYear.setMinimum(1990)
        self.spinBox_EndYear.setMaximum(file_manip.getCurrentYear())
        self.spinBox_EndYear.setAlignment(Qt.AlignCenter)
        self.spinBox_EndYear.setMaximumWidth(80)
        self.spinBox_EndYear.setMinimumHeight(20)

        self.spinBox_EndMonth = QSpinBox()
        self.spinBox_EndMonth.setMinimum(1)
        self.spinBox_EndMonth.setMaximum(12)
        self.spinBox_EndMonth.setAlignment(Qt.AlignCenter)
        self.spinBox_EndMonth.setMaximumWidth(80)
        self.spinBox_EndMonth.setMinimumHeight(20)

        self.spinBox_EndDay = QSpinBox()
        self.spinBox_EndDay.setMinimum(1)
        self.spinBox_EndDay.setMaximum(31)
        self.spinBox_EndDay.setAlignment(Qt.AlignCenter)
        self.spinBox_EndDay.setMaximumWidth(80)
        self.spinBox_EndDay.setMinimumHeight(20)

        self.spinBox_ChunkSize = QSpinBox()
        self.spinBox_ChunkSize.setSingleStep(1)
        self.spinBox_ChunkSize.setMinimum(1)
        self.spinBox_ChunkSize.setAlignment(Qt.AlignCenter)
        self.spinBox_ChunkSize.setMaximumWidth(80)
        self.spinBox_ChunkSize.setMinimumHeight(20)

        # -------------------------- #
        # ----- QDoubleSpinBox ----- #
        # -------------------------- #
        self.doubleSpinBox_Resolution = QDoubleSpinBox()
        self.doubleSpinBox_Resolution.setSuffix(' m')
        self.doubleSpinBox_Resolution.setDecimals(2)
        self.doubleSpinBox_Resolution.setSingleStep(0.05)
        self.doubleSpinBox_Resolution.setMaximumWidth(80)
        self.doubleSpinBox_Resolution.setMinimumHeight(20)
        self.doubleSpinBox_Resolution.setAlignment(Qt.AlignCenter)

        self.doubleSpinBox_MinLatitude = QDoubleSpinBox()
        self.doubleSpinBox_MinLatitude.setDecimals(2)
        self.doubleSpinBox_MinLatitude.setSingleStep(0.05)
        self.doubleSpinBox_MinLatitude.setMaximumWidth(80)
        self.doubleSpinBox_MinLatitude.setMinimumHeight(20)
        self.doubleSpinBox_MinLatitude.setAlignment(Qt.AlignCenter)

        self.doubleSpinBox_MinLongitude = QDoubleSpinBox()
        self.doubleSpinBox_MinLongitude.setDecimals(2)
        self.doubleSpinBox_MinLongitude.setSingleStep(0.05)
        self.doubleSpinBox_MinLongitude.setMaximumWidth(80)
        self.doubleSpinBox_MinLongitude.setMinimumHeight(20)
        self.doubleSpinBox_MinLongitude.setAlignment(Qt.AlignCenter)

        self.doubleSpinBox_MaxLatitude = QDoubleSpinBox()
        self.doubleSpinBox_MaxLatitude.setDecimals(2)
        self.doubleSpinBox_MaxLatitude.setSingleStep(0.05)
        self.doubleSpinBox_MaxLatitude.setMaximumWidth(80)
        self.doubleSpinBox_MaxLatitude.setMinimumHeight(20)
        self.doubleSpinBox_MaxLatitude.setAlignment(Qt.AlignCenter)

        self.doubleSpinBox_MaxLongitude = QDoubleSpinBox()
        self.doubleSpinBox_MinLongitude.setDecimals(2)
        self.doubleSpinBox_MaxLongitude.setSingleStep(0.05)
        self.doubleSpinBox_MaxLongitude.setMaximumWidth(80)
        self.doubleSpinBox_MaxLongitude.setMinimumHeight(20)
        self.doubleSpinBox_MaxLongitude.setAlignment(Qt.AlignCenter)

        # ----------------------- #
        # ----- QListWidget ----- #
        # ----------------------- #
        self.listWidget_SatelliteList = QListWidget()

        self.listWidget_BandList = QListWidget()

        self.dict_SatelliteJSON = {}

        # ------------------------------ #
        # ----- Set Default Values ----- #
        # ------------------------------ #
        self._DEFAULT_START_YEAR = projFlags.INT_START_YEAR_DEFAULT
        self._DEFAULT_START_MONTH = projFlags.INT_START_MONTH_DEFAULT
        self._DEFAULT_START_DAY = projFlags.INT_START_DAY_DEFAULT
        self._DEFAULT_END_YEAR = projFlags.INT_END_YEAR_DEFAULT
        self._DEFAULT_END_MONTH = projFlags.INT_END_MONTH_DEFAULT
        self._DEFAULT_END_DAY = projFlags.INT_END_DAY_DEFAULT

        self._DEFAULT_CHUNK_SIZE = projFlags.INT_CHUNK_SIZE_DEFAULT
        self._DEFAULT_RESOLUTION = projFlags.FLOAT_RESOLUTION_DEFAULT

        self._DEFAULT_MIN_LATITUDE = projFlags.FLOAT_MIN_LATITUDE_DEFAULT
        self._DEFAULT_MIN_LONGITUDE = projFlags.FLOAT_MIN_LONGITUDE_DEFAULT
        self._DEFAULT_MAX_LATITUDE = projFlags.FLOAT_MAX_LATITUDE_DEFAULT
        self._DEFAULT_MAX_LONGITUDE = projFlags.FLOAT_MAX_LONGITUDE_DEFAULT

        # --------------------------- #
        # ----- Set CLass Flags ----- #
        # --------------------------- #
        self._FLAG_SATELLITE_LIST_KEY = 'satellite-key'
        self._FLAG_BAND_LIST_KEY = 'band-key'

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

        self.setSatelliteJSON()
        self.setSatelliteList()

        self.widgetConfig.setWidget()

        # Label Start Date
        label_StartDate = QLabel('<b>Start Date:<\\b>')
        label_StartDate.setMinimumWidth(160)
        label_StartDate.setMaximumWidth(160)
        label_StartDate.setAlignment(Qt.AlignCenter)

        # Label Start Year
        label_StartYear = QLabel('Start Year:')
        label_StartYear.setMinimumWidth(80)
        label_StartYear.setMaximumWidth(80)

        # Label Start Month
        label_StartMonth = QLabel('Start Month:')
        label_StartMonth.setMinimumWidth(80)
        label_StartMonth.setMaximumWidth(80)

        # Label Start Day
        label_StartDay = QLabel('Start Day:')
        label_StartDay.setMinimumWidth(80)
        label_StartDay.setMaximumWidth(80)

        # Label End Date
        label_EndDate = QLabel('<b>End Date:<\\b>')
        label_EndDate.setMinimumWidth(160)
        label_EndDate.setMaximumWidth(160)
        label_EndDate.setAlignment(Qt.AlignCenter)

        # Label End Year
        label_EndYear = QLabel('End Year:')
        label_EndYear.setMinimumWidth(80)
        label_EndYear.setMaximumWidth(80)

        # Label End Month
        label_EndMonth = QLabel('End Month:')
        label_EndMonth.setMinimumWidth(80)
        label_EndMonth.setMaximumWidth(80)

        # Label End Day
        label_EndDay = QLabel('End Day:')
        label_EndDay.setMinimumWidth(80)
        label_EndDay.setMaximumWidth(80)

        # Label Chunk Size
        label_ChunkSize = QLabel('<b>Chunk Size:<\\b>')
        label_ChunkSize.setMinimumWidth(80)
        label_ChunkSize.setMaximumWidth(80)

        # Label Resolution
        label_Resolution = QLabel('<b>Resolution:<\\b>')
        label_Resolution.setMinimumWidth(80)
        label_Resolution.setMaximumWidth(80)

        # Label Bounding Box
        label_Set_Bounding_Box = QLabel('<b>Set Bounding Box (WGS84 - EPSG:4386):<\\b>')
        label_Set_Bounding_Box.setAlignment(Qt.AlignCenter)
        label_Set_Bounding_Box.setMinimumWidth(180)
        label_Set_Bounding_Box.setMaximumWidth(420)

        # Label Minimum Longitude
        label_MinLongitude = QLabel('Minimum Longitude:')
        label_MinLongitude.setMinimumWidth(130)
        label_MinLongitude.setMinimumWidth(130)

        # Label Minimum Latitude
        label_MinLatitude = QLabel('Minimum Latitude:')
        label_MinLatitude.setMinimumWidth(130)
        label_MinLatitude.setMinimumWidth(130)

        # Label Maximum Longitude
        label_MaxLongitude = QLabel('Maximum Longitude:')
        label_MaxLongitude.setMinimumWidth(130)
        label_MaxLongitude.setMinimumWidth(130)

        # Label Maximum Latitude
        label_MaxLatitude = QLabel('Maximum Latitude:')
        label_MaxLatitude.setMinimumWidth(130)
        label_MaxLatitude.setMinimumWidth(130)

        # Label Satellite List
        label_Satellite_List = QLabel('<b>Satellite List:<\\b>')
        label_Satellite_List.setMinimumWidth(130)
        label_Satellite_List.setMaximumWidth(130)

        # Label Band List
        label_Band_List = QLabel('<b>Band List:<\\b>')
        label_Band_List.setMinimumWidth(130)
        label_Band_List.setMaximumWidth(130)

        # Start Year
        hbox_StartYear = QHBoxLayout()
        hbox_StartYear.addWidget(label_StartYear)
        hbox_StartYear.addWidget(self.spinBox_StartYear)

        # Start Month
        hbox_StartMonth = QHBoxLayout()
        hbox_StartMonth.addWidget(label_StartMonth)
        hbox_StartMonth.addWidget(self.spinBox_StartMonth)

        # Start Day
        hbox_StartDay = QHBoxLayout()
        hbox_StartDay.addWidget(label_StartDay)
        hbox_StartDay.addWidget(self.spinBox_StartDay)

        # Start Date
        vbox_StartDate = QVBoxLayout()
        vbox_StartDate.addWidget(label_StartDate)
        vbox_StartDate.addLayout(hbox_StartYear)
        vbox_StartDate.addLayout(hbox_StartMonth)
        vbox_StartDate.addLayout(hbox_StartDay)

        # End Year
        hbox_EndYear = QHBoxLayout()
        hbox_EndYear.addWidget(label_EndYear)
        hbox_EndYear.addWidget(self.spinBox_EndYear)

        # End Month
        hbox_EndMonth = QHBoxLayout()
        hbox_EndMonth.addWidget(label_EndMonth)
        hbox_EndMonth.addWidget(self.spinBox_EndMonth)

        # End Day
        hbox_EndDay = QHBoxLayout()
        hbox_EndDay.addWidget(label_EndDay)
        hbox_EndDay.addWidget(self.spinBox_EndDay)

        # End Date
        vbox_EndDate = QVBoxLayout()
        vbox_EndDate.addWidget(label_EndDate)
        vbox_EndDate.addLayout(hbox_EndYear)
        vbox_EndDate.addLayout(hbox_EndMonth)
        vbox_EndDate.addLayout(hbox_EndDay)

        # Date Options
        hbox_DateOptions = QHBoxLayout()
        hbox_DateOptions.addLayout(vbox_StartDate)
        hbox_DateOptions.addWidget(QLabel('    '))
        hbox_DateOptions.addWidget(QLabel('    '))
        hbox_DateOptions.addLayout(vbox_EndDate)
        # hbox_DateOptions.addSpacerItem(QSpacerItem(projFlags.INT_MAX_STRETCH, 0))

        # Chunk Size
        hbox_ChunkSize = QHBoxLayout()
        hbox_ChunkSize.addWidget(label_ChunkSize)
        hbox_ChunkSize.addWidget(self.spinBox_ChunkSize)
        # hbox_ChunkSize.addSpacerItem(QSpacerItem(projFlags.INT_MAX_STRETCH, 0))

        # Minimum Longitude
        hbox_MinLongitude = QHBoxLayout()
        hbox_MinLongitude.addWidget(label_MinLongitude)
        hbox_MinLongitude.addWidget(self.doubleSpinBox_MinLongitude)

        # Minimum Latitude
        hbox_MinLatitude = QHBoxLayout()
        hbox_MinLatitude.addWidget(label_MinLatitude)
        hbox_MinLatitude.addWidget(self.doubleSpinBox_MinLatitude)

        # Minimum Bound:
        vbox_MinBound = QVBoxLayout()
        vbox_MinBound.addLayout(hbox_MinLatitude)
        vbox_MinBound.addLayout(hbox_MinLongitude)

        # Maximum Longitude
        hbox_MaxLongitude = QHBoxLayout()
        hbox_MaxLongitude.addWidget(label_MaxLongitude)
        hbox_MaxLongitude.addWidget(self.doubleSpinBox_MaxLongitude)

        # Maximum Latitude
        hbox_MaxLatitude = QHBoxLayout()
        hbox_MaxLatitude.addWidget(label_MaxLatitude)
        hbox_MaxLatitude.addWidget(self.doubleSpinBox_MaxLatitude)

        # Maximum Bound:
        vbox_MaxBound = QVBoxLayout()
        vbox_MaxBound.addLayout(hbox_MaxLatitude)
        vbox_MaxBound.addLayout(hbox_MaxLongitude)

        # Bounding Box
        hbox_BoundingBox = QHBoxLayout()
        hbox_BoundingBox.addLayout(vbox_MinBound)
        hbox_BoundingBox.addWidget(QLabel('    '))
        hbox_BoundingBox.addLayout(vbox_MaxBound)
        # hbox_BoundingBox.addSpacerItem(QSpacerItem(projFlags.INT_MAX_STRETCH, 0))

        # Final Bounding Box
        vbox_FinalBoundingBox = QVBoxLayout()
        vbox_FinalBoundingBox.addWidget(label_Set_Bounding_Box)
        vbox_FinalBoundingBox.addLayout(hbox_BoundingBox)

        # Resolution
        hbox_Resolution = QHBoxLayout()
        hbox_Resolution.addWidget(label_Resolution)
        hbox_Resolution.addWidget(self.doubleSpinBox_Resolution)
        # hbox_Resolution.addSpacerItem(QSpacerItem(projFlags.INT_MAX_STRETCH, 0))

        # Button
        hbox_Buttons = QHBoxLayout()
        hbox_Buttons.addWidget(self.button_Config)
        hbox_Buttons.addWidget(self.button_RestoreDefault)
        # hbox_Buttons.addSpacerItem(QSpacerItem(projFlags.INT_MAX_STRETCH, 0))
        hbox_Buttons.addWidget(self.button_DownloadImages)

        # ListsRightVbox
        vbox_ListsRightVbox = QVBoxLayout()
        vbox_ListsRightVbox.addWidget(label_Satellite_List)
        vbox_ListsRightVbox.addWidget(self.listWidget_SatelliteList)
        vbox_ListsRightVbox.addWidget(label_Band_List)
        vbox_ListsRightVbox.addWidget(self.listWidget_BandList)

        # LeftVBox
        vbox_LeftVBox = QVBoxLayout()
        vbox_LeftVBox.addLayout(hbox_DateOptions)
        vbox_LeftVBox.addWidget(QLabel(''))
        vbox_LeftVBox.addLayout(hbox_ChunkSize)
        vbox_LeftVBox.addWidget(QLabel(''))
        vbox_LeftVBox.addLayout(vbox_FinalBoundingBox)
        vbox_LeftVBox.addWidget(QLabel(''))
        vbox_LeftVBox.addLayout(hbox_Resolution)
        vbox_LeftVBox.addSpacerItem(QSpacerItem(0, projFlags.INT_MAX_STRETCH))

        # FinalHBox
        hbox_FinalHBox = QHBoxLayout()
        hbox_FinalHBox.addLayout(vbox_LeftVBox)
        hbox_FinalHBox.addWidget(QLabel('    '))
        hbox_FinalHBox.addLayout(vbox_ListsRightVbox)

        self.vbox_main_layout.addLayout(hbox_FinalHBox)
        self.vbox_main_layout.addLayout(hbox_Buttons)

    def restoreDefaultValues(self):
        # set default value
        self.spinBox_StartYear.setValue(self.getDefaultStartYear())
        self.spinBox_StartMonth.setValue(self.getDefaultStartMonth())
        self.spinBox_StartDay.setValue(self.getDefaultStartDay())
        self.spinBox_EndYear.setValue(self.getDefaultEndYear())
        self.spinBox_EndMonth.setValue(self.getDefaultEndMonth())
        self.spinBox_EndDay.setValue(self.getDefaultEndDay())
        self.spinBox_ChunkSize.setValue(self.getDefaultChunkSize())

        self.doubleSpinBox_Resolution.setValue(self.getDefaultResolution())
        self.doubleSpinBox_MinLatitude.setValue(self.getDefaultMinLatitude())
        self.doubleSpinBox_MinLongitude.setValue(self.getDefaultMinLongitude())
        self.doubleSpinBox_MaxLatitude.setValue(self.getDefaultMaxLatitude())
        self.doubleSpinBox_MaxLongitude.setValue(self.getDefaultMaxLongitude())

    def setEvents_(self):
        self.button_RestoreDefault.clicked.connect(self.restoreDefaultValues)
        self.button_Config.clicked.connect(self.setButtonConfigClicked)

        self.listWidget_SatelliteList.currentItemChanged.connect(self.setBandList)
        self.listWidget_SatelliteList.itemChanged.connect(self.setSatelliteItemChanged)

        self.listWidget_BandList.itemChanged.connect(self.setBandItemChanged)

    def setSatelliteJSON(self):
        for _key_ in evalScript.CONST_EVALUATION_DICTIONARY.keys():
            satListWidgetItem = QListWidgetItem(_key_)
            satListWidgetItem.setFlags(satListWidgetItem.flags() | Qt.ItemIsUserCheckable)
            satListWidgetItem.setCheckState(Qt.Unchecked)

            self.dict_SatelliteJSON[_key_] = {
                self._FLAG_SATELLITE_LIST_KEY: satListWidgetItem,
                self._FLAG_BAND_LIST_KEY: []
            }

            for _band_ in evalScript.CONST_EVALUATION_DICTIONARY[_key_][evalScript.SKEY_BANDS].keys():
                bandName = evalScript.CONST_EVALUATION_DICTIONARY[_key_][evalScript.SKEY_BANDS][_band_]
                listBandName = _band_
                if bandName is not None:
                    listBandName += ' - ' + bandName
                bandListWidgetItem = QListWidgetItem(listBandName)
                bandListWidgetItem.setFlags(bandListWidgetItem.flags() | Qt.ItemIsUserCheckable)
                bandListWidgetItem.setCheckState(Qt.Unchecked)
                self.dict_SatelliteJSON[_key_][self._FLAG_BAND_LIST_KEY].append(bandListWidgetItem)

    def setSatelliteList(self):
        listSize = self.listWidget_SatelliteList.count()
        for _index_ in range(0, listSize):
            self.listWidget_SatelliteList.takeItem(0)
        for _key_ in self.dict_SatelliteJSON.keys():
            self.listWidget_SatelliteList.addItem(self.dict_SatelliteJSON[_key_][self._FLAG_SATELLITE_LIST_KEY])
        self.listWidget_SatelliteList.setCurrentRow(0)

    def setBandList(self):
        listSize = self.listWidget_BandList.count()
        for _index_ in range(0, listSize):
            self.listWidget_BandList.takeItem(0)
        _key_ = self.listWidget_SatelliteList.currentItem().text()
        for _bandItem_ in self.dict_SatelliteJSON[_key_][self._FLAG_BAND_LIST_KEY]:
            self.listWidget_BandList.addItem(_bandItem_)
        self.setBandListItemsActive()

    def setSatelliteItemChanged(self, item):
        self.listWidget_SatelliteList.setCurrentItem(item)
        self.setBandListItemsActive()

    def setBandListItemsActive(self):
        _key_ = self.listWidget_SatelliteList.currentItem().text()
        _checkState_ = self.listWidget_SatelliteList.currentItem().checkState()
        for _bandItem_ in self.dict_SatelliteJSON[_key_][self._FLAG_BAND_LIST_KEY]:
            if _checkState_:
                _bandItem_.setFlags(~Qt.ItemIsSelectable)
            else:
                _bandItem_.setFlags(Qt.ItemIsSelectable)

    @staticmethod
    def setBandItemChanged(item):
        if item.checkState() == Qt.PartiallyChecked:
            item.setCheckState(Qt.Checked)

    def setButtonConfigClicked(self):
        self.widgetConfig.show()

    # ------------------------------ #
    # ----- GET DEFAULT VALUES ----- #
    # ------------------------------ #
    def getDefaultStartYear(self):
        return self._DEFAULT_START_YEAR

    def getDefaultStartMonth(self):
        return self._DEFAULT_START_MONTH

    def getDefaultStartDay(self):
        return self._DEFAULT_START_DAY

    def getDefaultEndYear(self):
        return self._DEFAULT_END_YEAR

    def getDefaultEndMonth(self):
        return self._DEFAULT_END_MONTH

    def getDefaultEndDay(self):
        return self._DEFAULT_END_DAY

    def getDefaultChunkSize(self):
        return self._DEFAULT_CHUNK_SIZE

    def getDefaultResolution(self):
        return self._DEFAULT_RESOLUTION

    def getDefaultMinLatitude(self):
        return self._DEFAULT_MIN_LATITUDE

    def getDefaultMinLongitude(self):
        return self._DEFAULT_MIN_LONGITUDE

    def getDefaultMaxLatitude(self):
        return self._DEFAULT_MAX_LATITUDE

    def getDefaultMaxLongitude(self):
        return self._DEFAULT_MAX_LONGITUDE

    # ------------------- #
    # ----- GETTERS ----- #
    # ------------------- #
    def getValueStartYear(self):
        return self.spinBox_StartYear.value()

    def getValueStartMonth(self):
        return self.spinBox_StartMonth.value()

    def getValueStartDay(self):
        return self.spinBox_StartDay.value()

    def getValueEndYear(self):
        return self.spinBox_EndYear.value()

    def getValueEndMonth(self):
        return self.spinBox_EndMonth.value()

    def getValueEndDay(self):
        return self.spinBox_EndDay.value()

    def getValueChunkSize(self):
        return self.spinBox_ChunkSize.value()

    def getValueResolution(self):
        return self.doubleSpinBox_Resolution.value()

    def getValueMinLatitude(self):
        return self.doubleSpinBox_MinLatitude.value()

    def getValueMinLongitude(self):
        return self.doubleSpinBox_MinLongitude.value()

    def getValueMaxLatitude(self):
        return self.doubleSpinBox_MaxLatitude.value()

    def getValueMaxLongitude(self):
        return self.doubleSpinBox_MaxLongitude.value()

    def getValueInstanceID(self):
        return self.widgetConfig.getInstanceID()

    def getValueClientID(self):
        return self.widgetConfig.getClientID()

    def getValueClientSecret(self):
        return self.widgetConfig.getClientSecret()

    def getListSelectionJSON(self):
        listSelectedJSON = {}
        for _key_ in self.dict_SatelliteJSON.keys():
            if self.dict_SatelliteJSON[_key_][self._FLAG_SATELLITE_LIST_KEY].checkState().__bool__():
                listSelectedJSON[_key_] = []
                for _band_ in self.dict_SatelliteJSON[_key_][self._FLAG_BAND_LIST_KEY]:
                    if _band_.checkState().__bool__():
                        listSelectedJSON[_key_].append(_band_.text().split(' - ')[0])
        return listSelectedJSON


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
        self.button_RefreshList = QPushButton('Refresh List')
        self.button_Execute = QPushButton('Execute')

        # ----------------------- #
        # ----- QListWidget ----- #
        # ----------------------- #

        self._listWidget_Dir = QListWidget()
        self._listWidget_AvailableProcesses = QListWidget()

        # --------------------- #
        # ----- QCheckBox ----- #
        # --------------------- #
        self._checkbox_ProcessOnlyUnprocessed = QCheckBox('Process only new files.')

        # ------------------------------ #
        # ----- Set Default Values ----- #
        # ------------------------------ #

        self._DKEY_PKEY_4_EVALUATION_DICT = 'pkey-for-evaluation-dict'
        self._DKEY_DIR_ITEM = 'directory-item'
        self._DKEY_PROCESS_ITEM = 'process-item'
        self._DKEY_SELECTED_PROCESSES = 'selected-processes'

        # ------------------------- #
        # ----- Set Variables ----- #
        # ------------------------- #
        self._storagePath = None
        self._geoProcessing = geoProc.GeotiffProcessing()
        self._ImageCollectionJSON = {}
        self._ProcessesJSON = {}

    # --------------------------- #
    # ----- Reuse Functions ----- #
    # --------------------------- #
    def setWidget(self):
        """
            A function to create the widget components into the main QWidget
            :return: Nothing
        """
        self.setEvents_()

        # Labels
        label_Directories = QLabel('<b>Geo-Database Directories:<\\b>')
        label_AvailableProcesses = QLabel('<b>Available Processes:<\\b>')

        # List vbox
        vbox_ListWidgets = QVBoxLayout()
        vbox_ListWidgets.addWidget(label_Directories)
        vbox_ListWidgets.addWidget(self._listWidget_Dir)
        vbox_ListWidgets.addWidget(label_AvailableProcesses)
        vbox_ListWidgets.addWidget(self._listWidget_AvailableProcesses)

        # Buttons
        hbox_Buttons = QHBoxLayout()
        hbox_Buttons.addWidget(self.button_RefreshList)
        hbox_Buttons.addWidget(self.button_Execute)

        self.vbox_main_layout.addLayout(vbox_ListWidgets)
        self.vbox_main_layout.addWidget(self._checkbox_ProcessOnlyUnprocessed)
        self.vbox_main_layout.addLayout(hbox_Buttons)

    def setEvents_(self):
        self._listWidget_Dir.currentRowChanged.connect(self.setProcessListWidget)
        self._listWidget_AvailableProcesses.itemChanged.connect(self.setProcessListItemChanged)

        self.button_Execute.clicked.connect(self.setButtonExecute)

    def setStoragePath(self, path):
        self._storagePath = path
        self._geoProcessing.setStoragePath(self._storagePath)

    def setImageCollectionJSON(self):
        self._geoProcessing.createImageCollectionJSON()
        self._ImageCollectionJSON = self._geoProcessing.getImageCollectionJSON()

    def setGeoDatabaseProcessing(self):
        self._listWidget_Dir.clear()
        for _key_ in self._ImageCollectionJSON.keys():
            dirWidgetItem = QListWidgetItem(_key_)
            self._listWidget_Dir.addItem(dirWidgetItem)
            self._ProcessesJSON[_key_] = {
                self._DKEY_PKEY_4_EVALUATION_DICT: '',
                self._DKEY_DIR_ITEM: dirWidgetItem,
                self._DKEY_PROCESS_ITEM: [],
                self._DKEY_SELECTED_PROCESSES: []

            }
            for _sat_key_ in evalScript.CONST_EVALUATION_DICTIONARY.keys():
                if _key_ == evalScript.CONST_EVALUATION_DICTIONARY[_sat_key_][evalScript.SKEY_PATH_NAME]:
                    self._ProcessesJSON[_key_][self._DKEY_PKEY_4_EVALUATION_DICT] = _sat_key_
                    for _process_ in evalScript.CONST_EVALUATION_DICTIONARY[_sat_key_][evalScript.SKEY_AVAILABLE_PROCESSES].keys():
                        processWidgetItem = QListWidgetItem(_process_)
                        processWidgetItem.setFlags(processWidgetItem.flags() | Qt.ItemIsUserCheckable)
                        processWidgetItem.setCheckState(Qt.Unchecked)
                        self._ProcessesJSON[_key_][self._DKEY_PROCESS_ITEM].append(processWidgetItem)
        self._listWidget_Dir.setCurrentRow(0)

    def setProcessListWidget(self, row):
        if self._listWidget_Dir.item(row):
            _key_ = self._listWidget_Dir.item(row).text()
            item_count = self._listWidget_AvailableProcesses.count()
            for _ in range(0, item_count):
                self._listWidget_AvailableProcesses.takeItem(0)
            for _process_ in self._ProcessesJSON[_key_][self._DKEY_PROCESS_ITEM]:
                self._listWidget_AvailableProcesses.addItem(_process_)

    def setProcessListItemChanged(self, item):
        _key_ = self._listWidget_Dir.currentItem().text()
        if item.checkState().__bool__():
            if item.text() not in self._ProcessesJSON[_key_][self._DKEY_SELECTED_PROCESSES]:
                self._ProcessesJSON[_key_][self._DKEY_SELECTED_PROCESSES].append(item.text())
        else:
            if item.text() in self._ProcessesJSON[_key_][self._DKEY_SELECTED_PROCESSES]:
                self._ProcessesJSON[_key_][self._DKEY_SELECTED_PROCESSES].remove(item.text())

    def setButtonExecute(self):
        processOnlyNewFiles = self._checkbox_ProcessOnlyUnprocessed.checkState().__bool__()
        for _key_ in self._ProcessesJSON.keys():
            _pkey_eval_ = self._ProcessesJSON[_key_][self._DKEY_PKEY_4_EVALUATION_DICT]
            _imageCollection = self._geoProcessing.getImageCollectionJSON()
            for _process_ in self._ProcessesJSON[_key_][self._DKEY_SELECTED_PROCESSES]:
                for _path_key_ in _imageCollection[_key_].keys():
                    full_path = _imageCollection[_key_][_path_key_][self._geoProcessing.getKey_FullPath()]
                    if 'RAW' in full_path:
                        currentFileNameJSON = projFunc.readCubePathMetadata(_path_key_)
                        currentFileNameJSON[projFlags.DKEY_PATH_BANDS] = 1
                        currentFileNameJSON[projFlags.DKEY_PATH_DATA_TYPE] = _process_
                        newFileName = projFunc.createImagePathName(
                            satStamp=currentFileNameJSON[projFlags.DKEY_PATH_SATELLITE],
                            bandNum=currentFileNameJSON[projFlags.DKEY_PATH_BANDS],
                            dataType=currentFileNameJSON[projFlags.DKEY_PATH_DATA_TYPE],
                            timeIntervalList=[currentFileNameJSON[projFlags.DKEY_PATH_DATE_START], currentFileNameJSON[projFlags.DKEY_PATH_DATE_END]],
                            bboxList=[currentFileNameJSON[projFlags.DKEY_PATH_LATITUDE_MIN], currentFileNameJSON[projFlags.DKEY_PATH_LONGITUDE_MIN],
                                      currentFileNameJSON[projFlags.DKEY_PATH_LATITUDE_MAX], currentFileNameJSON[projFlags.DKEY_PATH_LONGITUDE_MAX]],
                            crs=currentFileNameJSON[projFlags.DKEY_PATH_CRS],
                            size=[currentFileNameJSON[projFlags.DKEY_PATH_WIDTH], currentFileNameJSON[projFlags.DKEY_PATH_HEIGHT]]
                        ) + file_manip.pathFileSuffix(full_path)

                        o_full_path = file_manip.normPath(full_path + '/..') + newFileName
                        if processOnlyNewFiles:
                            if newFileName not in self._ImageCollectionJSON[_key_].keys():
                                evalScript.CONST_EVALUATION_DICTIONARY[_pkey_eval_][
                                    evalScript.SKEY_AVAILABLE_PROCESSES][_process_](full_path, o_full_path, _pkey_eval_)
                        else:
                            evalScript.CONST_EVALUATION_DICTIONARY[_pkey_eval_][evalScript.SKEY_AVAILABLE_PROCESSES][_process_](full_path, o_full_path, _pkey_eval_)

    # ------------------------------ #
    # ----- GET DEFAULT VALUES ----- #
    # ------------------------------ #


class WidgetTabStorageImageVisualizing(QWidget):
    def __init__(self):
        super().__init__()

        # ---------------------- #
        # ----- Set Window ----- #
        # ---------------------- #
        self.vbox_main_layout = QVBoxLayout(self)  # Create the main vbox

        self._Widget_Filter = WidgetFilter(
            w=640, h=512,
            minW=640, minH=512,
            maxW=640, maxH=512,
            winTitle='Set Filter', iconPath='')

        self._Widget_ShowImage = WidgetShowImage(
            w=512, h=512,
            minW=256, minH=256,
            maxW=512, maxH=512,
            winTitle='Show Image', iconPath='')

        # ----------------------- #
        # ----- QPushButton ----- #
        # ----------------------- #
        self.button_RefreshList = QPushButton('Refresh List')
        self._button_SetFilter = QPushButton('Set Filter')
        self._button_ShowImage = QPushButton('Show Image')

        # ----------------------- #
        # ----- QListWidget ----- #
        # ----------------------- #
        self._listWidget_Dir = QListWidget()
        # self._listWidget_Dir.setMaximumWidth(250)

        self._listWidget_FileList = QListWidget()
        # self._listWidget_FileList.setMaximumWidth(250)

        # -------------------- #
        # ----- QTextEdit----- #
        # -------------------- #
        self._textEdit_Metadata = QTextEdit()
        self._textEdit_Metadata.setEnabled(False)
        self._textEdit_Metadata.setText(self.setAndGetMetadata())
        self._textEdit_Metadata.setMinimumWidth(250)
        self._textEdit_Metadata.setMaximumWidth(250)

        # ------------------------- #
        # ----- Set Variables ----- #
        # ------------------------- #
        self._DKEY_PKEY_4_EVALUATION_DICT = 'pkey-for-evaluation-dict'
        self._DKEY_DIR_ITEM = 'directory-item'
        self._DKEY_DIR_FILES = 'directory-files'

        self._storagePath = None
        self._geoProcessing = geoProc.GeotiffProcessing()
        self._ImageCollectionJSON = {}
        self._DirFilesJSON = {}

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

        self._Widget_Filter.setWidget()
        self._Widget_ShowImage.setWidget()

        # Labels
        label_DirList = QLabel('<b>Geo-Database Directories:<\\b>')
        label_FileList = QLabel('<b>Available Files:<\\b>')
        label_Metadata = QLabel('<b>Metadata:<\\b>')

        # ListWidget
        vbox_ListWidget = QVBoxLayout()
        vbox_ListWidget.addWidget(label_DirList)
        vbox_ListWidget.addWidget(self._listWidget_Dir)
        vbox_ListWidget.addWidget(label_FileList)
        vbox_ListWidget.addWidget(self._listWidget_FileList)

        # vbox Metadata
        vbox_Metadata = QVBoxLayout()
        vbox_Metadata.addWidget(label_Metadata)
        vbox_Metadata.addWidget(self._textEdit_Metadata)

        # HBox_Final
        hbox_Final = QHBoxLayout()
        hbox_Final.addLayout(vbox_ListWidget)
        hbox_Final.addLayout(vbox_Metadata)

        # Buttons
        hbox_Buttons = QHBoxLayout()
        hbox_Buttons.addWidget(self.button_RefreshList)
        hbox_Buttons.addWidget(self._button_SetFilter)
        hbox_Buttons.addWidget(self._button_ShowImage)

        self.vbox_main_layout.addLayout(hbox_Final)
        self.vbox_main_layout.addLayout(hbox_Buttons)

    def restoreDefaultValues(self):
        # set default value
        pass

    def setEvents_(self):
        self._listWidget_Dir.currentRowChanged.connect(self.setFileListWidget)
        self._listWidget_FileList.currentRowChanged.connect(self.setFileListCurrentRowChange)

        self._button_SetFilter.clicked.connect(self.setButtonFilterClicked)
        self._button_ShowImage.clicked.connect(self.setButtonShowImage)

    def setStoragePath(self, path):
        self._storagePath = path
        self._geoProcessing.setStoragePath(self._storagePath)

    def setImageCollectionJSON(self):
        self._geoProcessing.createImageCollectionJSON()
        self._ImageCollectionJSON = self._geoProcessing.getImageCollectionJSON()

    def setGeoDatabaseProcessing(self):
        self._listWidget_Dir.clear()
        for _key_ in self._ImageCollectionJSON.keys():
            dirWidgetItem = QListWidgetItem(_key_)
            self._listWidget_Dir.addItem(dirWidgetItem)
            self._DirFilesJSON[_key_] = {
                self._DKEY_PKEY_4_EVALUATION_DICT: '',
                self._DKEY_DIR_ITEM: dirWidgetItem,
                self._DKEY_DIR_FILES: []

            }
            for _sat_key_ in evalScript.CONST_EVALUATION_DICTIONARY.keys():
                if _key_ == evalScript.CONST_EVALUATION_DICTIONARY[_sat_key_][evalScript.SKEY_PATH_NAME]:
                    self._DirFilesJSON[_key_][self._DKEY_PKEY_4_EVALUATION_DICT] = _sat_key_
            for _file_ in self._ImageCollectionJSON[_key_].keys():
                fileWidgetItem = QListWidgetItem(_file_)
                self._DirFilesJSON[_key_][self._DKEY_DIR_FILES].append(fileWidgetItem)

        if self._listWidget_Dir.count() > 0:
            self._listWidget_Dir.setCurrentRow(0)

    def setFileListWidget(self, row):
        if self._listWidget_Dir.item(row):
            _key_ = self._listWidget_Dir.item(row).text()
            item_count = self._listWidget_FileList.count()
            for _ in range(0, item_count):
                self._listWidget_FileList.takeItem(0)
            for _process_ in self._DirFilesJSON[_key_][self._DKEY_DIR_FILES]:
                self._listWidget_FileList.addItem(_process_)

            if self._listWidget_FileList.count() > 0:
                self._listWidget_FileList.setCurrentRow(0)

    def setFileListCurrentRowChange(self, row):
        if self._listWidget_Dir.currentItem() and self._listWidget_FileList.item(row):
            _dir_key_ = self._listWidget_Dir.currentItem().text()
            _file_key_ = self._listWidget_FileList.item(row).text()

            key_metadata = 'metadata'
            metadata = self.setAndGetMetadata(
                satelliteName=self._DirFilesJSON[_dir_key_][self._DKEY_PKEY_4_EVALUATION_DICT],
                imageType=self._ImageCollectionJSON[_dir_key_][_file_key_][key_metadata]['data-type'],
                startDate=self._ImageCollectionJSON[_dir_key_][_file_key_][key_metadata]['date-start'],
                endDate=self._ImageCollectionJSON[_dir_key_][_file_key_][key_metadata]['date-end'],
                crs=self._ImageCollectionJSON[_dir_key_][_file_key_][key_metadata]['crs'],
                minLat=self._ImageCollectionJSON[_dir_key_][_file_key_][key_metadata]['latitude-min'],
                minLon=self._ImageCollectionJSON[_dir_key_][_file_key_][key_metadata]['longitude-min'],
                maxLat=self._ImageCollectionJSON[_dir_key_][_file_key_][key_metadata]['latitude-max'],
                maxLon=self._ImageCollectionJSON[_dir_key_][_file_key_][key_metadata]['longitude-max'],
                imgWidth=self._ImageCollectionJSON[_dir_key_][_file_key_][key_metadata]['width'],
                imgHeight=self._ImageCollectionJSON[_dir_key_][_file_key_][key_metadata]['height'],
                imgBands=self._ImageCollectionJSON[_dir_key_][_file_key_][key_metadata]['bands'])

            self._textEdit_Metadata.setText(metadata)

        else:
            self._textEdit_Metadata.setText(self.setAndGetMetadata())

    def setButtonFilterClicked(self):
        self._Widget_Filter.show()

    def setButtonShowImage(self):
        self._Widget_ShowImage.show()

    @staticmethod
    def setAndGetMetadata(satelliteName='', imageType='',
                          startDate='', endDate='', crs='',
                          minLat='', minLon='', maxLat='', maxLon='',
                          imgWidth='', imgHeight='', imgBands=''):
        newLine = '<br>'
        o_str = f"<span style=\"color:black\"><b>Satellite: <\\b></span> <span style=\"color:green\"><b>{satelliteName}<\\b></span>{newLine}" \
                f"<span style=\"color:black\"><b>Type: <\\b></span> <span style=\"color:green\"><b>{imageType}<\\b></span>{newLine}" \
                f"<span style=\"color:black\"><b>Start Date: <\\b></span> <span style=\"color:green\"><b>{startDate}<\\b></span>{newLine}" \
                f"<span style=\"color:black\"><b>End Date: <\\b></span> <span style=\"color:green\"><b>{endDate}<\\b></span>{newLine}" \
                f"<span style=\"color:black\"><b>CRS: <\\b></span> <span style=\"color:green\"><b>{crs}<\\b></span>{newLine}" \
                f"<span style=\"color:black\"><b>Min Latitude: <\\b></span> <span style=\"color:green\"><b>{minLat}<\\b></span>{newLine}" \
                f"<span style=\"color:black\"><b>Min Longitude: <\\b></span> <span style=\"color:green\"><b>{minLon}<\\b></span>{newLine}" \
                f"<span style=\"color:black\"><b>Max Latitude: <\\b></span> <span style=\"color:green\"><b>{maxLat}<\\b></span>{newLine}" \
                f"<span style=\"color:black\"><b>Max Longitude: <\\b></span> <span style=\"color:green\"><b>{maxLon}<\\b></span>{newLine}" \
                f"<span style=\"color:black\"><b>Width: <\\b></span> <span style=\"color:green\"><b>{imgWidth}<\\b></span>{newLine}" \
                f"<span style=\"color:black\"><b>Height: <\\b></span> <span style=\"color:green\"><b>{imgHeight}<\\b></span>{newLine}" \
                f"<span style=\"color:black\"><b>Bands: <\\b></span> <span style=\"color:green\"><b>{imgBands}<\\b></span>"

        return o_str

    # ------------------------------ #
    # ----- GET DEFAULT VALUES ----- #
    # ------------------------------ #


class WidgetConfig(QWidget):
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

        # ------------------------- #
        # ----- Set Variables ----- #
        # ------------------------- #
        self._Instance_ID = ''
        self._Client_ID = ''
        self._Client_Secret = ''

        # ----------------------- #
        # ----- QPushButton ----- #
        # ----------------------- #
        self.button_Ok = QPushButton('Ok')
        self.button_Apply = QPushButton('Apply')
        self.button_Apply.setEnabled(False)
        self.button_ExportAsCSV = QPushButton('Export as CSV')
        self.button_Cancel = QPushButton('Cancel')

        # --------------------- #
        # ----- QLineEdit ----- #
        # --------------------- #
        self.lineEdit_Instance_ID = QLineEdit()
        self.lineEdit_Instance_ID.setAlignment(Qt.AlignCenter)

        self.lineEdit_Client_ID = QLineEdit()
        self.lineEdit_Client_ID.setAlignment(Qt.AlignCenter)

        self.lineEdit_Client_Secret = QLineEdit()
        self.lineEdit_Client_Secret.setAlignment(Qt.AlignCenter)

        # ------------------------------ #
        # ----- Set Default Values ----- #
        # ------------------------------ #
        self._DEFAULT_CREDENTIALS_FILE_PATH = projFlags.PROJECT_FOLDER + 'config/config.csv'
        self._DEFAULT_INSTANCE_ID_COLUMN = 'INSTANCE_ID'
        self._DEFAULT_CLIENT_ID_COLUMN = 'CLIENT_ID'
        self._DEFAULT_CLIENT_SECRET_COLUMN = 'CLIENT_SECRET'

    # --------------------------- #
    # ----- Reuse Functions ----- #
    # --------------------------- #
    def setWidget(self):
        """
            A function to create the widget components into the main QWidget
            :return: Nothing
        """
        self.setEvents_()
        self.setSavedCredentials()

        self.lineEdit_Instance_ID.setText(self._Instance_ID)
        self.lineEdit_Client_ID.setText(self._Client_ID)
        self.lineEdit_Client_Secret.setText(self._Client_Secret)

        # Labels
        label_Instance_ID = QLabel("<b>Instance ID:<\\b>")
        label_Instance_ID.setMinimumWidth(100)
        label_Client_ID = QLabel("<b>Client ID:<\\b>")
        label_Client_ID.setMinimumWidth(100)
        label_Client_Secret = QLabel("<b>Client Secret:<\\b>")
        label_Client_Secret.setMinimumWidth(100)

        # HBoxes
        hbox_Instance_ID = QHBoxLayout()
        hbox_Instance_ID.addWidget(label_Instance_ID)
        hbox_Instance_ID.addWidget(self.lineEdit_Instance_ID)

        hbox_Client_ID = QHBoxLayout()
        hbox_Client_ID.addWidget(label_Client_ID)
        hbox_Client_ID.addWidget(self.lineEdit_Client_ID)

        hbox_Client_Secret = QHBoxLayout()
        hbox_Client_Secret.addWidget(label_Client_Secret)
        hbox_Client_Secret.addWidget(self.lineEdit_Client_Secret)

        hbox_Buttons = QHBoxLayout()
        hbox_Buttons.addWidget(self.button_Ok)
        hbox_Buttons.addWidget(self.button_Apply)
        hbox_Buttons.addWidget(self.button_ExportAsCSV)
        hbox_Buttons.addWidget(self.button_Cancel)

        self.vbox_main_layout.addLayout(hbox_Instance_ID)
        self.vbox_main_layout.addLayout(hbox_Client_ID)
        self.vbox_main_layout.addLayout(hbox_Client_Secret)
        self.vbox_main_layout.addLayout(hbox_Buttons)

    def setEvents_(self):
        self.button_Ok.clicked.connect(self.setButtonOkClicked)
        self.button_Apply.clicked.connect(self.setButtonApplyClicked)
        self.button_ExportAsCSV.clicked.connect(self.setButtonExportAsCSVClicked)
        self.button_Cancel.clicked.connect(self.setButtonCancelClicked)

        self.lineEdit_Instance_ID.textChanged.connect(self.setTextChanged)
        self.lineEdit_Client_ID.textChanged.connect(self.setTextChanged)
        self.lineEdit_Client_Secret.textChanged.connect(self.setTextChanged)

    def setSavedCredentials(self):
        if file_manip.checkPathExistence(self._DEFAULT_CREDENTIALS_FILE_PATH):
            try:
                file_manip.checkAndCreateFolders(self._DEFAULT_CREDENTIALS_FILE_PATH)
                csvFile = file_manip.importCSV(self._DEFAULT_CREDENTIALS_FILE_PATH)
                self._Instance_ID = csvFile[self._DEFAULT_INSTANCE_ID_COLUMN].tolist()[0]
                self._Client_ID = csvFile[self._DEFAULT_CLIENT_ID_COLUMN].tolist()[0]
                self._Client_Secret = csvFile[self._DEFAULT_CLIENT_SECRET_COLUMN].tolist()[0]
            except (KeyError, ValueError):
                self._Instance_ID = ''
                self._Client_ID = ''
                self._Client_Secret = ''

    def setButtonApplyClicked(self):
        self._Instance_ID = self.lineEdit_Instance_ID.text()
        self._Client_ID = self.lineEdit_Client_ID.text()
        self._Client_Secret = self.lineEdit_Client_Secret.text()
        self.button_Apply.setEnabled(False)
        self.button_ExportAsCSV.setEnabled(True)

    def setButtonExportAsCSVClicked(self):
        list_csv = [[self._DEFAULT_INSTANCE_ID_COLUMN, self._DEFAULT_CLIENT_ID_COLUMN, self._DEFAULT_CLIENT_SECRET_COLUMN],
                    [self._Instance_ID, self._Client_ID, self._Client_Secret]]
        file_manip.exportCSV(self._DEFAULT_CREDENTIALS_FILE_PATH, list_csv)

    def setButtonOkClicked(self):
        self.setButtonApplyClicked()
        self.close()

    def setButtonCancelClicked(self):
        self.close()

    def setTextChanged(self):
        self.button_Apply.setEnabled(True)
        self.button_ExportAsCSV.setEnabled(False)

    def getInstanceID(self):
        return self._Instance_ID

    def getClientID(self):
        return self._Client_ID

    def getClientSecret(self):
        return self._Client_Secret

    def getCredentials(self):
        return self._Instance_ID, self._Client_ID, self._Client_Secret


class WidgetFilter(QWidget):
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

        # ------------------------- #
        # ----- Set Variables ----- #
        # ------------------------- #

        # ----------------------- #
        # ----- QPushButton ----- #
        # ----------------------- #
        self._button_Ok = QPushButton('Ok')
        self._button_Apply = QPushButton('Apply')
        self._button_Cancel = QPushButton('Cancel')

        # ----------------------- #
        # ----- QListWidget ----- #
        # ----------------------- #
        self._listWidget_Type = QListWidget()
        self._listWidget_Crs = QListWidget()

        # -------------------- #
        # ----- QSpinBox ----- #
        # -------------------- #
        self._spinBox_StartYear = QSpinBox()
        self._spinBox_StartYear.setMinimum(1990)
        self._spinBox_StartYear.setMaximum(file_manip.getCurrentYear())
        self._spinBox_StartYear.setAlignment(Qt.AlignCenter)
        self._spinBox_StartYear.setMaximumWidth(80)
        self._spinBox_StartYear.setMinimumHeight(20)

        self._spinBox_StartMonth = QSpinBox()
        self._spinBox_StartMonth.setMinimum(1)
        self._spinBox_StartMonth.setMaximum(12)
        self._spinBox_StartMonth.setAlignment(Qt.AlignCenter)
        self._spinBox_StartMonth.setMaximumWidth(80)
        self._spinBox_StartMonth.setMinimumHeight(20)

        self._spinBox_StartDay = QSpinBox()
        self._spinBox_StartDay.setMinimum(1)
        self._spinBox_StartDay.setMaximum(31)
        self._spinBox_StartDay.setAlignment(Qt.AlignCenter)
        self._spinBox_StartDay.setMaximumWidth(80)
        self._spinBox_StartDay.setMinimumHeight(20)

        self._spinBox_EndYear = QSpinBox()
        self._spinBox_EndYear.setMinimum(1990)
        self._spinBox_EndYear.setMaximum(file_manip.getCurrentYear())
        self._spinBox_EndYear.setAlignment(Qt.AlignCenter)
        self._spinBox_EndYear.setMaximumWidth(80)
        self._spinBox_EndYear.setMinimumHeight(20)

        self._spinBox_EndMonth = QSpinBox()
        self._spinBox_EndMonth.setMinimum(1)
        self._spinBox_EndMonth.setMaximum(12)
        self._spinBox_EndMonth.setAlignment(Qt.AlignCenter)
        self._spinBox_EndMonth.setMaximumWidth(80)
        self._spinBox_EndMonth.setMinimumHeight(20)

        self._spinBox_EndDay = QSpinBox()
        self._spinBox_EndDay.setMinimum(1)
        self._spinBox_EndDay.setMaximum(31)
        self._spinBox_EndDay.setAlignment(Qt.AlignCenter)
        self._spinBox_EndDay.setMaximumWidth(80)
        self._spinBox_EndDay.setMinimumHeight(20)

        self._spinBox_minBandSize = QSpinBox()
        self._spinBox_minBandSize.setMinimum(0)
        self._spinBox_minBandSize.setAlignment(Qt.AlignCenter)
        self._spinBox_minBandSize.setMaximumWidth(80)
        self._spinBox_minBandSize.setMinimumHeight(20)

        self._spinBox_maxBandSize = QSpinBox()
        self._spinBox_maxBandSize.setMinimum(0)
        self._spinBox_maxBandSize.setAlignment(Qt.AlignCenter)
        self._spinBox_maxBandSize.setMaximumWidth(80)
        self._spinBox_maxBandSize.setMinimumHeight(20)

        self._spinBox_minImageWidth = QSpinBox()
        self._spinBox_minImageWidth.setMinimum(0)
        self._spinBox_minImageWidth.setAlignment(Qt.AlignCenter)
        self._spinBox_minImageWidth.setMaximumWidth(80)
        self._spinBox_minImageWidth.setMinimumHeight(20)

        self._spinBox_maxImageWidth = QSpinBox()
        self._spinBox_maxImageWidth.setMinimum(0)
        self._spinBox_maxImageWidth.setAlignment(Qt.AlignCenter)
        self._spinBox_maxImageWidth.setMaximumWidth(80)
        self._spinBox_maxImageWidth.setMinimumHeight(20)

        self._spinBox_minImageHeight = QSpinBox()
        self._spinBox_minImageHeight.setMinimum(0)
        self._spinBox_minImageHeight.setAlignment(Qt.AlignCenter)
        self._spinBox_minImageHeight.setMaximumWidth(80)
        self._spinBox_minImageHeight.setMinimumHeight(20)

        self._spinBox_maxImageHeight = QSpinBox()
        self._spinBox_maxImageHeight.setMinimum(0)
        self._spinBox_maxImageHeight.setAlignment(Qt.AlignCenter)
        self._spinBox_maxImageHeight.setMaximumWidth(80)
        self._spinBox_maxImageHeight.setMinimumHeight(20)

        # -------------------------- #
        # ----- QDoubleSpinBox ----- #
        # -------------------------- #
        self._doubleSpinBox_MinimumLatitude = QDoubleSpinBox()
        self._doubleSpinBox_MinimumLatitude.setMinimum(-90)
        self._doubleSpinBox_MinimumLatitude.setMaximum(90)
        self._doubleSpinBox_MinimumLatitude.setAlignment(Qt.AlignCenter)
        self._doubleSpinBox_MinimumLatitude.setMaximumWidth(80)
        self._doubleSpinBox_MinimumLatitude.setMinimumHeight(20)

        self._doubleSpinBox_MinimumLongitude = QDoubleSpinBox()
        self._doubleSpinBox_MinimumLongitude.setMinimum(-180)
        self._doubleSpinBox_MinimumLongitude.setMaximum(180)
        self._doubleSpinBox_MinimumLongitude.setAlignment(Qt.AlignCenter)
        self._doubleSpinBox_MinimumLongitude.setMaximumWidth(80)
        self._doubleSpinBox_MinimumLongitude.setMinimumHeight(20)

        self._doubleSpinBox_MaximumLatitude = QDoubleSpinBox()
        self._doubleSpinBox_MaximumLatitude.setMinimum(-90)
        self._doubleSpinBox_MaximumLatitude.setMaximum(90)
        self._doubleSpinBox_MaximumLatitude.setAlignment(Qt.AlignCenter)
        self._doubleSpinBox_MaximumLatitude.setMaximumWidth(80)
        self._doubleSpinBox_MaximumLatitude.setMinimumHeight(20)

        self._doubleSpinBox_MaximumLongitude = QDoubleSpinBox()
        self._doubleSpinBox_MaximumLongitude.setMinimum(-180)
        self._doubleSpinBox_MaximumLongitude.setMaximum(180)
        self._doubleSpinBox_MaximumLongitude.setAlignment(Qt.AlignCenter)
        self._doubleSpinBox_MaximumLongitude.setMaximumWidth(80)
        self._doubleSpinBox_MaximumLongitude.setMinimumHeight(20)

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
        self.setEvents_()

        # Label
        label_Type = QLabel('<b>Available Type:<\\b>')
        label_Crs = QLabel('<b>Available CRS:<\\b>')
        label_Start_Date = QLabel('<b>Start Date:<\\b>')
        label_Start_Year = QLabel('Start Year:')
        label_Start_Month = QLabel('Start Month:')
        label_Start_Day = QLabel('Start Day:')
        label_End_Date = QLabel('<b>End Date:<\\b>')
        label_End_Year = QLabel('End Year:')
        label_End_Month = QLabel('End Month:')
        label_End_Day = QLabel('End Day:')
        label_Minimum_Latitude = QLabel('<b>Minimum Latitude:<\\b>')
        label_Minimum_Longitude = QLabel('<b>Minimum Longitude:<\\b>')
        label_Maximum_Latitude = QLabel('<b>Maximum Latitude:<\\b>')
        label_Maximum_Longitude = QLabel('<b>Maximum Longitude:<\\b>')
        label_MinBandNum = QLabel('<b>Minimum Bands:<\\b>')
        label_MaxBandNum = QLabel('<b>Maximum Bands:<\\b>')
        label_MinWidth = QLabel('<b>Minimum Width:<\\b>')
        label_MaxWidth = QLabel('<b>Maximum Width:<\\b>')
        label_MinHeight = QLabel('<b>Minimum Height:<\\b>')
        label_MaxHeight = QLabel('<b>Maximum Height:<\\b>')

        # Vbox_ListWidget
        vbox_ListWidget = QVBoxLayout()
        vbox_ListWidget.addWidget(label_Type)
        vbox_ListWidget.addWidget(self._listWidget_Type)
        vbox_ListWidget.addWidget(label_Crs)
        vbox_ListWidget.addWidget(self._listWidget_Crs)

        # Start Date
        hbox_StartYear = QHBoxLayout()
        hbox_StartYear.addWidget(label_Start_Year)
        hbox_StartYear.addWidget(self._spinBox_StartYear)

        hbox_StartMonth = QHBoxLayout()
        hbox_StartMonth.addWidget(label_Start_Month)
        hbox_StartMonth.addWidget(self._spinBox_StartMonth)

        hbox_StartDay = QHBoxLayout()
        hbox_StartDay.addWidget(label_Start_Day)
        hbox_StartDay.addWidget(self._spinBox_StartDay)

        vbox_StartDate = QVBoxLayout()
        vbox_StartDate.addWidget(label_Start_Date)
        vbox_StartDate.addLayout(hbox_StartYear)
        vbox_StartDate.addLayout(hbox_StartMonth)
        vbox_StartDate.addLayout(hbox_StartDay)

        # End Date
        hbox_EndYear = QHBoxLayout()
        hbox_EndYear.addWidget(label_End_Year)
        hbox_EndYear.addWidget(self._spinBox_EndYear)

        hbox_EndMonth = QHBoxLayout()
        hbox_EndMonth.addWidget(label_End_Month)
        hbox_EndMonth.addWidget(self._spinBox_EndMonth)

        hbox_EndDay = QHBoxLayout()
        hbox_EndDay.addWidget(label_End_Day)
        hbox_EndDay.addWidget(self._spinBox_EndDay)

        vbox_EndDate = QVBoxLayout()
        vbox_EndDate.addWidget(label_End_Date)
        vbox_EndDate.addLayout(hbox_EndYear)
        vbox_EndDate.addLayout(hbox_EndMonth)
        vbox_EndDate.addLayout(hbox_EndDay)

        # Date
        hbox_Date = QHBoxLayout()
        hbox_Date.addLayout(vbox_StartDate)
        hbox_Date.addLayout(vbox_EndDate)

        # Min Coordinates
        hbox_MinLatitude = QHBoxLayout()
        hbox_MinLatitude.addWidget(label_Minimum_Latitude)
        hbox_MinLatitude.addWidget(self._doubleSpinBox_MinimumLatitude)

        hbox_MinLongitude = QHBoxLayout()
        hbox_MinLongitude.addWidget(label_Minimum_Longitude)
        hbox_MinLongitude.addWidget(self._doubleSpinBox_MinimumLongitude)

        vbox_MinCoordinates = QVBoxLayout()
        vbox_MinCoordinates.addLayout(hbox_MinLatitude)
        vbox_MinCoordinates.addLayout(hbox_MinLongitude)

        # Max Coordinates
        hbox_MaxLatitude = QHBoxLayout()
        hbox_MaxLatitude.addWidget(label_Maximum_Latitude)
        hbox_MaxLatitude.addWidget(self._doubleSpinBox_MaximumLatitude)

        hbox_MaxLongitude = QHBoxLayout()
        hbox_MaxLongitude.addWidget(label_Maximum_Longitude)
        hbox_MaxLongitude.addWidget(self._doubleSpinBox_MaximumLongitude)

        vbox_MaxCoordinates = QVBoxLayout()
        vbox_MaxCoordinates.addLayout(hbox_MaxLatitude)
        vbox_MaxCoordinates.addLayout(hbox_MaxLongitude)

        # hbox_Coordinates
        hbox_Coordinates = QHBoxLayout()
        hbox_Coordinates.addLayout(vbox_MinCoordinates)
        hbox_Coordinates.addLayout(vbox_MaxCoordinates)

        # Min Image Size
        hbox_MinBand = QHBoxLayout()
        hbox_MinBand.addWidget(label_MinBandNum)
        hbox_MinBand.addWidget(self._spinBox_minBandSize)

        hbox_MinWidth = QHBoxLayout()
        hbox_MinWidth.addWidget(label_MinWidth)
        hbox_MinWidth.addWidget(self._spinBox_minImageWidth)

        hbox_MinHeight = QHBoxLayout()
        hbox_MinHeight.addWidget(label_MinHeight)
        hbox_MinHeight.addWidget(self._spinBox_minImageHeight)

        vbox_MinImageSize = QVBoxLayout()
        vbox_MinImageSize.addLayout(hbox_MinBand)
        vbox_MinImageSize.addLayout(hbox_MinWidth)
        vbox_MinImageSize.addLayout(hbox_MinHeight)

        # Max Image Size
        hbox_MaxBand = QHBoxLayout()
        hbox_MaxBand.addWidget(label_MaxBandNum)
        hbox_MaxBand.addWidget(self._spinBox_maxBandSize)

        hbox_MaxWidth = QHBoxLayout()
        hbox_MaxWidth.addWidget(label_MaxWidth)
        hbox_MaxWidth.addWidget(self._spinBox_maxImageWidth)

        hbox_MaxHeight = QHBoxLayout()
        hbox_MaxHeight.addWidget(label_MaxHeight)
        hbox_MaxHeight.addWidget(self._spinBox_maxImageHeight)

        vbox_MaxImageSize = QVBoxLayout()
        vbox_MaxImageSize.addLayout(hbox_MaxBand)
        vbox_MaxImageSize.addLayout(hbox_MaxWidth)
        vbox_MaxImageSize.addLayout(hbox_MaxHeight)

        # hbox Image Size
        hbox_ImageSize = QHBoxLayout()
        hbox_ImageSize.addLayout(vbox_MinImageSize)
        hbox_ImageSize.addLayout(vbox_MaxImageSize)

        # vbox_Final
        vbox_Final = QVBoxLayout()
        vbox_Final.addLayout(hbox_Date)
        vbox_Final.addLayout(hbox_Coordinates)
        vbox_Final.addLayout(hbox_ImageSize)
        vbox_Final.addSpacerItem(QSpacerItem(0, projFlags.INT_MAX_STRETCH))

        # Final HBox Layout
        hbox_Final = QHBoxLayout()
        hbox_Final.addLayout(vbox_ListWidget)
        hbox_Final.addLayout(vbox_Final)

        self.vbox_main_layout.addLayout(hbox_Final)

    def setEvents_(self):
        pass


class WidgetShowImage(QWidget):
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

        # ------------------------- #
        # ----- Set Variables ----- #
        # ------------------------- #

        # ----------------------- #
        # ----- QPushButton ----- #
        # ----------------------- #

        # --------------------- #
        # ----- QLineEdit ----- #
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
        self.setEvents_()

    def setEvents_(self):
        pass


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
