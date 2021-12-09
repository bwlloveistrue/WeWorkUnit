# -*- coding: utf-8 -*-
"""
        实现一款桌面宠物
"""
import os, cfg, sys, random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui

class DesktopPet(QWidget):

    def __init__(self, parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()
        self.pet_images, iconpath = self.randomLoadPetImages()
        quit_action = QAction('退出', self, triggered=(self.quit))
        quit_action.setIcon(QIcon(iconpath))
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(iconpath))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()
        self.image = QLabel(self)
        self.setImage(self.pet_images[0][0])
        self.is_follow_mouse = False
        self.mouse_drag_pos = self.pos()
        self.resize(128, 128)
        self.randomPosition()
        self.show()
        self.is_running_action = False
        self.action_images = []
        self.action_pointer = 0
        self.action_max_len = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomAct)
        self.timer.start(500)

    def randomAct(self):
        if not self.is_running_action:
            self.is_running_action = True
            self.action_images = random.choice(self.pet_images)
            self.action_max_len = len(self.action_images)
            self.action_pointer = 0
        self.runFrame()

    def runFrame(self):
        if self.action_pointer == self.action_max_len:
            self.is_running_action = False
            self.action_pointer = 0
            self.action_max_len = 0
        self.setImage(self.action_images[self.action_pointer])
        self.action_pointer += 1

    def setImage(self, image):
        self.image.setPixmap(QPixmap.fromImage(image))

    def randomLoadPetImages(self):
        pet_name = random.choice(list(cfg.PET_ACTIONS_MAP.keys()))
        actions = cfg.PET_ACTIONS_MAP[pet_name]
        pet_images = []
        for action in actions:
            pet_images.append([self.loadImage(os.path.join(cfg.ROOT_DIR, pet_name, 'shime' + item + '.png')) for item in action])

        iconpath = os.path.join(cfg.ROOT_DIR, pet_name, 'shime1.png')
        return (pet_images, iconpath)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton:
            if self.is_follow_mouse:
                self.move(event.globalPos() - self.mouse_drag_pos)
                event.accept()

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def loadImage(self, imagepath):
        image = QImage()
        image.load(imagepath)
        return image

    def randomPosition(self):
        screen_geo = QDesktopWidget().screenGeometry()
        pet_geo = self.geometry()
        width = (screen_geo.width() - pet_geo.width()) * random.random()
        height = (screen_geo.height() - pet_geo.height()) * random.random()
        self.move(width, height)

    def quit(self):
        self.close()
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec_())
# okay decompiling pet.pyc
