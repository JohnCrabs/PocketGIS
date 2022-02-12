import sys
import os
import tkinter as tk
import cv2 as cv2

from OpenGL.GL import *

from PySide2.QtCore import (
    QBasicTimer
)

from PySide2.QtOpenGL import (
    QGLWidget
)

from PySide2.QtWidgets import (
    QApplication,
)

from PySide2.QtGui import (
    QIcon,
)


_PROJECT_FOLDER = os.path.normpath(os.path.realpath(__file__) + '/../../../')

_INT_SCREEN_WIDTH = tk.Tk().winfo_screenwidth()  # get the screen width
_INT_SCREEN_HEIGHT = tk.Tk().winfo_screenheight()  # get the screen height
_INT_WIN_WIDTH = 1024  # this variable is only for the if __name__ == "__main__"
_INT_WIN_HEIGHT = 512  # this variable is only for the if __name__ == "__main__"

_INT_MAX_STRETCH = 100000  # Spacer Max Stretch
_INT_BUTTON_MIN_WIDTH = 50  # Minimum Button Width


class WidgetTemplate(QGLWidget):
    def __init__(self, w=512, h=512, minW=256, minH=256, maxW=512, maxH=512,
                 winTitle='My Window', iconPath=''):
        super().__init__()
        self._timer = QBasicTimer()  # creating timer
        self._timer.start(1000 / 60, self)  # setting up timer ticks to 60 fps
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

        self.imgToView = None

    def initializeGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.imgToView is not None:
            # print(self.imgToView.shape)
            glColor3f(0.0, 0.0, 0.0)
            w = self.imgToView.shape[1]
            h = self.imgToView.shape[0]
            original_ratio = w / h
            designer_ratio = self.width() / self.height()
            if original_ratio > designer_ratio:
                designer_height = self.width() / original_ratio
                scale = designer_height / h
            else:
                designer_width = self.height() * original_ratio
                scale = designer_width / w

            if self.width() < self.height():
                if original_ratio == 1.0:
                    glRasterPos2f(-1.0, -0.5)
                elif original_ratio > 1.0:
                    pos = scale * h
                    pos = 1.0 - ((self.height() - pos) / self.height())
                    glRasterPos2f(-1.0, -pos)
                else:
                    pos = scale * w
                    pos = 1.0 - ((self.width() - pos) / self.width())
                    glRasterPos2f(-1.0, -pos)
            elif self.width() > self.height():
                if original_ratio == 1.0:
                    glRasterPos2f(-0.5, -1.0)
                elif original_ratio > 1.0:
                    pos = scale * h
                    pos = 1.0 - ((self.height() - pos) / self.height())
                    glRasterPos2f(-pos, -1.0)
                else:
                    pos = scale * w
                    pos = 1.0 - ((self.width() - pos) / self.width())
                    glRasterPos2f(-pos, -1.0)
            else:
                glRasterPos2f(-1.0, -1.0)

            glPixelZoom(scale, scale)
            glDrawPixels(w, h, GL_RGBA, GL_UNSIGNED_BYTE, self.imgToView)

        else:
            glColor3f(0.0, 0.0, 0.0)

    def resizeGL(self, w: int, h: int):
        glViewport(0, 0, w, h)
        glLoadIdentity()
        # Make the display area proportional to the size of the view
        glOrtho(-w / self.width(), w / self.width(), -h / self.height(), h / self.height(), -1.0, 1.0)

    def timerEvent(self, QTimerEvent):
        self.update()  # refreshing the widget

    def setImg(self, imgPath):
        img = cv2.imread(imgPath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.imgToView = img

    def clearImg(self):
        self.imgToView = None


# ******************************************************* #
# ********************   EXECUTION   ******************** #
# ******************************************************* #

def exec_app(w=512, h=512, minW=256, minH=256, maxW=512, maxH=512, winTitle='My Window', iconPath=''):
    myApp = QApplication(sys.argv)  # Set Up Application
    widgetWin = WidgetTemplate(w=w, h=h, minW=minW, minH=minH, maxW=maxW, maxH=maxH,
                               winTitle=winTitle, iconPath=iconPath)  # Create MainWindow
    widgetWin.show()  # Show Window
    myApp.exec_()  # Execute Application
    sys.exit(0)  # Exit Application


if __name__ == "__main__":
    exec_app(w=1024, h=512, minW=512, minH=256, maxW=512, maxH=512,
             winTitle='WidgetTemplate', iconPath=_PROJECT_FOLDER + '/icon/crabsMLearning_32x32.png')
