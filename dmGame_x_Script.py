# -*- coding: utf-8 -*-
# Author: bwl
# Create Date: 2020.07.21
import datetime
import pykeyboard
import win32con
import win32gui
import win32clipboard as wc
import pyperclip
from PIL import ImageGrab
import xlrd, xlwt
from time import sleep
import os
from pywinauto import application, handleprops
import time
import configparser
import sys
import logging
import threading
from pykeyboard import PyKeyboard
from win32com.client import Dispatch

dm = Dispatch('dm.dmsoft')

print(dm.ver())

# dm.moveto(50,50)
# dm.leftclick()

# print(dm.GetTime())
hwnd_title = dict()
def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

win32gui.EnumWindows(get_all_hwnd, 0)

for h, t in hwnd_title.items():
    if t != "":
        print(h,t)
print(dm.SetWindowTransparent(395046, 255))
print(dm.bindWindow(395046,'normal', 'normal', 'normal',0))
print(dm.moveto(0,0))
print(dm.leftclick())
sysPath = os.getcwd()
# print(dm.WaitKey(112,0))
dm.SetPath(sysPath)
clientX = 0;
clientY = 0;
x1 = 0;
x2 = 0;
y1 = 0;
y2 = 0;
width = 0;
height = 0;
print(dm.ClientToScreen(395046,clientX, clientY))
print(dm.GetClientSize(395046,width, height))
print(dm.GetForegroundFocus())
print(dm.GetClientRect(395046,x1, y1, x2, y2))
print(dm.GetWindowTitle(dm.GetForegroundFocus()))
print(dm.SendString(dm.GetForegroundFocus(),'111'))
print(dm.GetWindowProcessPath(395046))
foobarHwnd = dm.CreateFoobarEllipse(395046, 0, 0, 100, 200)
if  foobarHwnd > 0:
    dm.FoobarLock(foobarHwnd)
    dm.FoobarDrawText(foobarHwnd, 0,0,200,30,"测试","FF0000",1)
print(dm.moveto(100,100))
# print(dm.leftDown())
print(dm.moveto(1000,500))
# dm.Capture('')
# print(dm.GetWindowTitle(395046))
# print(dm.MoveWindow(395046, 100, 100))

def findImageXY(imagePath, dmObject):
    dmObject
    pass

class liufang_start:

    def gettliufangHwnd(self):
        for h, t in hwnd_title.items():
            if t == "Path of Exile":
                return h;


    if __name__ == '__main__':
        # 1：设置路径
        sysPath = os.getcwd()
        dm.SetPath(sysPath)
        # 2：获取进程
        lfHwnd = gettliufangHwnd()
        pass