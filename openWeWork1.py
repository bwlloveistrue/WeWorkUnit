# -*- coding: utf-8 -*-
# Author: bwl
# Create Date: 2020.07.21
import datetime
import sys
import traceback

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
import os
import logging
import threading

from xlutils import copy

k = pykeyboard.PyKeyboard()

class Pywin(object):
    """
    pywin framwork main class
    tool_name : 程序名称，支持带路径
    windows_name : 窗口名字
    """
    SLEEP_TIME = 1

    def __init__(self):
        """
        初始化方法，初始化一个app
        """
        self.app = application.Application()

    def run(self, tool_name):
        """
        启动应用程序
        """
        self.app.start(tool_name)
        time.sleep(1)

    def connect(self, window_name):
        """
        连接应用程序
        app.connect_(path = r"c:\windows\system32\notepad.exe")
        app.connect_(process = 2341)
        app.connect_(handle = 0x010f0c)
        """
        self.app.connect(title=window_name)
        time.sleep(1)

    def close(self, window_name):
        """
        关闭应用程序
        """
        self.app[window_name].close()
        time.sleep(1)

    def max_window(self, window_name):
        """
        最大化窗口
        """
        self.app[window_name].maximize()
        time.sleep(1)

    def menu_click(self, window_name, menulist):
        """
        菜单点击
        """
        self.app[window_name].MenuSelect(menulist)
        time.sleep(1)

    def input(self, window_name, controller, content):
        """
        输入内容
        """
        self.app[window_name][controller].type_keys(content)
        time.sleep(1)

    def click(self, window_name, controller):
        """
        鼠标左键点击
        example:
        下面两个功能相同,下面支持正则表达式
        app[u'关于“记事本”'][u'确定'].Click()
        app.window_(title_re = u'关于“记事本”').window_(title_re = u'确定').Click()
        """
        self.app[window_name][controller].Click()
        time.sleep(1)

    def double_click(self, window_name, controller, x=0, y=0):
        """
        鼠标左键点击(双击)
        """
        self.app[window_name][controller].DoubleClick(button="left", pressed="", coords=(x, y))
        time.sleep(1)

    def right_click(self, window_name, controller, order):
        """
        鼠标右键点击，下移进行菜单选择
        window_name : 窗口名
        controller：区域名
        order ： 数字，第几个命令
        """
        self.app[window_name][controller].RightClick()
        # for down in range(order):
        #         SendKeys.SendKeys('{DOWN}')
        #         time.sleep(0.5)
        # SendKeys.SendKeys('{ENTER}')
        time.sleep(1)

    def get_screenxy_from_bmp(self, main_bmp, son_bmp):
        # 获取屏幕上匹配指定截图的坐标->(x,y,width,height)
        from PIL import Image
        sleep(.5)
        img_main = Image.open(main_bmp)
        img_son = Image.open(son_bmp)
        datas_a = list(img_main.getdata())
        datas_b = list(img_son.getdata())
        for i, item in enumerate(datas_a):
            if i + 1 < len(datas_a) and datas_b[0] == item and datas_a[i + 1] == datas_b[1]:
                yx = divmod(i, img_main.size[0])
                main_start_pos = yx[1] + yx[0] * img_main.size[0]

                match_test = True
                for n in range(img_son.size[1]):
                    main_pos = main_start_pos + n * img_main.size[0]
                    son_pos = n * img_son.size[0]

                    if datas_b[son_pos:son_pos + img_son.size[0]] != datas_a[main_pos:main_pos + img_son.size[0]]:
                        match_test = False
                        break
                if match_test:
                    return (yx[1], yx[0], img_son.size[0], img_son.size[1])
        return False

    def getCopyText(self):
        wc.OpenClipboard()
        copy_text = wc.GetClipboardData(win32con.CF_TEXT)
        wc.CloseClipboard()
        return copy_text

    def inputText(self, text):
        # k.type_string('啊啊啊啊啊啊')  # 不能输入中文
        pyperclip.copy(text)
        k.press_key(k.control_key)
        k.tap_key('v')
        k.release_key(k.control_key)


class IniReader:
    """ 读取ini文件中的内容,返回值：str。
        指定config_name，param_name读取对应的值: read_config("TestSetting", "testType")
    """

    def __init__(self, CONFIG_INI, config_name, param_name):
        if os.path.exists(CONFIG_INI):
            self.ini_file = CONFIG_INI
        else:
            raise FileNotFoundError('文件不存在！')
        self.config_name = config_name
        self.param_name = param_name
        self._data = str()

    @property
    def data(self):
        config = configparser.ConfigParser()
        config.read(self.ini_file, encoding='UTF-8')
        self._data = config.get(self.config_name, self.param_name)
        return self._data


class My_Logger(object):
    """
    自定义日志类。日志分两类：
        1.总体日志，记录日志执行整体过程，存放在./log目录下，命名读取配置文件logFileName参数
        2.测试日志，记录测试执行过程中的详细日志。有两部分：
            （1）debug log，记录从浏览器打开到结束所有的详细过程，按./log/starttime//browser/runtime/testname记录
            （2）error log，只记录错误日志，日志将被记录在html结果文件中
    """

    def __init__(self, logger_name='Auto Test'):
        self.logger = logging.getLogger(logger_name)
        # 日志输出格式
        self.formatter = logging.Formatter("%(asctime)s - %(levelname)-4s - %(message)s")
        # 指定日志的最低输出级别，默认为WARN级别
        self.logger.setLevel(logging.INFO)

    def get_handler(self, file_path):
        # 生成文件日志的handler
        p, f = os.path.split(file_path)
        if not (os.path.exists(p)):
            os.makedirs(p)  # 判断是否存在该路径，如果不存在就新创建
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(self.formatter)
        return file_handler


my_logger = My_Logger()
my_lock = threading.RLock()


def DebugLogger(log_info, file_path):
    """debug日志，记录所有日志"""
    try:
        if my_lock.acquire():
            file_handler = my_logger.get_handler(file_path)
            my_logger.logger.addHandler(file_handler)
            my_logger.logger.info(log_info)
            my_logger.logger.removeHandler(file_handler)

            my_lock.release()
    except Exception as e:
        print("Failed to record debug log. Reason:\n %s" % str(e))


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


def run():
    # 通过Spy++ 获取window_name，即标题文本
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t != "":
            if t == wechatWindowTitle:
                global wechatWindowClassName
                wechatWindowClassName = win32gui.GetClassName(h)
            if t == addCustomerWindowTitle:
                global addCustomerWindowClassName
                addCustomerWindowClassName = win32gui.GetClassName(h)
            if t == noCustomerConfirmTitle:
                global noCustomerConfirmClassName
                noCustomerConfirmClassName = win32gui.GetClassName(h)
            if t == authenticMessageConfirmTitle:
                global authenticMessageClassName
                authenticMessageClassName = win32gui.GetClassName(h)
            DebugLogger('{0}--{1}--{2}'.format(t, h, win32gui.GetClassName(h)), log_path)

    # 获取excel数据
    # 获取模板数据信息
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    mouldInfoPath = os.path.join(BASE_PATH, 'customers', 'messageMould.xls')
    mould_list = xlrd.open_workbook(mouldInfoPath)  # 获取reRun plan file的数据表
    mould_table = mould_list.sheet_by_name('mould')  # 获取sheet名为mould的表
    authenticMessage = str(mould_table.cell_value(1, 0))
    global customerInfoPath
    customerInfoPath = os.path.join(BASE_PATH, 'customers', 'customers.xls')
    customer_list = xlrd.open_workbook(customerInfoPath)  # 获取reRun plan file的数据表
    table = customer_list.sheet_by_name('customerInfo')  # 获取sheet名为customerInfo的表

    row_count = table.nrows  # 获取行数
    for i in range(1, row_count):
        needInsert = table.cell_value(i, 3)
        if needInsert is None or needInsert == '' or needInsert == 'N':
            ctype = table.cell(i, 2).ctype  # 表格的数据类型
            cell = table.cell_value(i, 2)
            if ctype == 2 and cell % 1 == 0.0:  # ctype为2且为浮点
                cell = int(cell)  # 浮点转成整型
            mobileV = str(cell).replace('-', '')
            customInfoDic[mobileV] = authenticMessage.format(table.cell_value(i, 1))
    i = 0
    customerLen = len(customInfoDic)  # 获取所有客户
    while True:
        if len(resultList) >= customerLen:
            break
        if i > customerLen:
            break
        DebugLogger('插入数据：%s ' % str(customInfoDic), log_path)
        iteratorProcess(customInfoDic, i)
        i = i + 1

    work_book = xlwt.Workbook()
    work_result_sheet = work_book.add_sheet("result")  # 新增Summary的sheet
    work_result_sheet.col(0).width = 256 * 20
    work_result_sheet.col(1).width = 256 * 100
    work_result_sheet.col(2).width = 256 * 20
    customerResultPath = os.path.join(BASE_PATH, 'customers')
    for i in range(len(resultList)):
        result = resultList[i]
        work_result_sheet.write(i, 0, result[0])
        work_result_sheet.write(i, 1, result[1])
        work_result_sheet.write(i, 2, result[2])
    work_book.save(os.path.join(customerResultPath, 'result',
                                "customerResult_{0}.xls".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))))
    DebugLogger('导入完成！！', log_path)
    app = Pywin()
    app.run(tool_name)
    app.connect(wechatWindowTitle)
    # 后期准备（将不必要的dialog都删除）
    authenticMessageWindow = win32gui.FindWindow(authenticMessageClassName, authenticMessageConfirmTitle)
    if authenticMessageWindow > 0:
        app.close(authenticMessageConfirmTitle)
    noCustomerConfirmWindow = win32gui.FindWindow(noCustomerConfirmClassName, noCustomerConfirmTitle)
    if noCustomerConfirmWindow > 0:
        app.close(noCustomerConfirmTitle)
    addCustomerWindow = win32gui.FindWindow(addCustomerWindowClassName, addCustomerWindowTitle)
    if addCustomerWindow > 0:
        app.close(addCustomerWindowTitle)
    app.close(wechatWindowTitle)


def iteratorProcess(customInfoDic, times):
    customInfoDicTemp = customInfoDic.copy()
    app = Pywin()
    app.run(tool_name)
    app.connect(wechatWindowTitle)
    app.max_window(wechatWindowTitle)
    # 获取企业微信主窗口相对屏幕大小
    wechatWindowDialog = win32gui.FindWindow(wechatWindowClassName, wechatWindowTitle)
    win32gui.SetForegroundWindow(wechatWindowDialog)
    weChatWindow = win32gui.GetWindowRect(wechatWindowDialog);
    left, top, right, bottom = weChatWindow
    xRatio = (right + left) / 1920
    yRatio = (bottom + top) / 1040
    DebugLogger('weChatWindow：%s！' % str(weChatWindow), log_path)
    try:
        # 前期准备（将不必要的dialog都删除）
        authenticMessageWindow = win32gui.FindWindow(authenticMessageClassName, authenticMessageConfirmTitle)
        if authenticMessageWindow > 0:
            app.close(authenticMessageConfirmTitle)
        noCustomerConfirmWindow = win32gui.FindWindow(noCustomerConfirmClassName, noCustomerConfirmTitle)
        if noCustomerConfirmWindow > 0:
            app.close(noCustomerConfirmTitle)
        addCustomerWindow = win32gui.FindWindow(addCustomerWindowClassName, addCustomerWindowTitle)
        if addCustomerWindow > 0:
            app.close(addCustomerWindowTitle)
        DebugLogger('前期准备完成', log_path)
        # 获取通讯录的位置
        time.sleep(.5)

        # 点击通讯录
        app.app.window(title=wechatWindowTitle, class_name=wechatWindowClassName).click_input(
            coords=(floatToInt(34 * xRatio), floatToInt(150 * yRatio)))
        time.sleep(.5)
        # 点击新的联系人
        DebugLogger('新的客户元素找到！', log_path)
        app.app.window(title=wechatWindowTitle, class_name=wechatWindowClassName).click_input(
            coords=(floatToInt(88 * xRatio), floatToInt(94 * yRatio)))
        time.sleep(.5)
        DebugLogger('添加客户Icon元素找到！', log_path)
        app.app.window(title=wechatWindowTitle, class_name=wechatWindowClassName).click_input(
            coords=(floatToInt(1848 * xRatio), floatToInt(40 * yRatio)))
        time.sleep(.5)
        for mobileV, authenticMessage in customInfoDicTemp.items():
            starttime = datetime.datetime.now()
            if ONE_TIME_NUMBER > 0 and AFTER_ONE_TIME_DELAY > 0 and len(resultList) > 0:
                if len(resultList) % ONE_TIME_NUMBER == 0:
                    sleep(AFTER_ONE_TIME_DELAY * 60)
            app.app.window(title=addCustomerWindowTitle, class_name=addCustomerWindowClassName).double_click(
                coords=(floatToInt(74 * xRatio), floatToInt(90 * yRatio)))
            k.press_key(k.delete_key)
            app.inputText(mobileV)
            sleep(.5)
            k.press_key(k.enter_key)
            # ImageGrab.grab(customerWindow).save('addCustomerDialogSubmitIcon.png')
            # findCustomerSubmitIConPosition = app.get_screenxy_from_bmp(u'addCustomerDialogSubmitIcon.png', u'customerSubmitIcon.png')
            # app.app.window(title=addCustomerWindowTitle, class_name=addCustomerWindowClassName).click_input(
            #     coords=(findCustomerSubmitIConPosition[0] + 20, findCustomerSubmitIConPosition[1] + 10))
            sleep(3)
            noCustomerHandler = win32gui.FindWindow(noCustomerConfirmClassName, noCustomerConfirmTitle)
            hasCustomer = True
            if noCustomerHandler > 0:

                k.press_key(k.enter_key)
                app.app.window(title=addCustomerWindowTitle, class_name=addCustomerWindowClassName).double_click(
                    coords=(floatToInt(74 * xRatio), floatToInt(90 * yRatio)))
                k.press_key(k.delete_key)
                resultTupl = (mobileV, authenticMessage, '该账号不存在')
                updateResult(mobileV, '该账号不存在', starttime)
                resultList.append(resultTupl)
                del customInfoDic[mobileV]
                sleep(1)
            else:
                for i in range(2):
                    DebugLogger('添加确认按钮找到！', log_path)
                    if i == 0:
                        app.app.window(title=addCustomerWindowTitle, class_name=addCustomerWindowClassName).click_input(
                            coords=(floatToInt(304 * xRatio), floatToInt(188 * yRatio)))  # 点击添加按钮
                    elif i == 1:
                        app.app.window(title=addCustomerWindowTitle,
                                       class_name=addCustomerWindowClassName).click_input(
                            coords=(floatToInt(304 * xRatio), floatToInt(269 * yRatio)))  # 点击添加按钮
                    sleep(1)
                    authenticMessageConfirmWindow = win32gui.FindWindow(authenticMessageClassName,
                                                                        authenticMessageConfirmTitle)
                    if authenticMessageConfirmWindow > 0:
                        app.app.window(title=authenticMessageConfirmTitle,
                                       class_name=authenticMessageClassName).click_input(
                            coords=(floatToInt(330 * xRatio), floatToInt(98 * yRatio)))  # 点击删除输入框文本icon
                        sleep(.5)
                        app.app.window(title=authenticMessageConfirmTitle,
                                       class_name=authenticMessageClassName).click_input(
                            coords=(floatToInt(292 * xRatio), floatToInt(99 * yRatio)))  # 点击输入框
                        sleep(.5)
                        app.inputText(authenticMessage)
                        app.app.window(title=authenticMessageConfirmTitle,
                                       class_name=authenticMessageClassName).click_input(
                            coords=(floatToInt(171 * xRatio), floatToInt(168 * yRatio)))
                        sleep(.5)
                        resultTupl = (mobileV, authenticMessage, '插入成功')
                        resultList.append(resultTupl)
                        if i == 0:
                            updateResult(mobileV, '插入成功', starttime)
                            del customInfoDic[mobileV]
                        sleep(3)
            sleep((DELAY_TIME))
        DebugLogger('导入第%s' % times + '次成功！', log_path)
    except Exception as e:
        authenticMessageWindow = win32gui.FindWindow(authenticMessageClassName, authenticMessageConfirmTitle)
        if authenticMessageWindow > 0:
            app.close(authenticMessageConfirmTitle)
        noCustomerConfirmWindow = win32gui.FindWindow(noCustomerConfirmClassName, noCustomerConfirmTitle)
        if noCustomerConfirmWindow > 0:
            app.close(noCustomerConfirmTitle)
        addCustomerWindow = win32gui.FindWindow(addCustomerWindowClassName, addCustomerWindowTitle)
        if addCustomerWindow > 0:
            app.close(addCustomerWindowTitle)
        app.close(wechatWindowTitle)
        DebugLogger('导入第%s' % times + '次失败！，错误原因：%s' % str(sys.exc_info()), log_path)
        traceback.print_exc(file=open(log_path, 'a'))


def floatToInt(f):
    return int(f)


def updateResult(mobile, result, starttime):
    endtime = datetime.datetime.now();
    duration = str(endtime - starttime).split(".")[0]
    customerInfoBook = xlrd.open_workbook(customerInfoPath, formatting_info=True)
    table = customerInfoBook.sheet_by_name('customerInfo')  # 获取sheet名为customerInfo的表

    row_count = table.nrows  # 获取行数
    targetRow = 0
    for i in range(1, row_count):
        ctype = table.cell(i, 2).ctype  # 表格的数据类型
        cell = table.cell_value(i, 2)
        if ctype == 2 and cell % 1 == 0.0:  # ctype为2且为浮点
            cell = int(cell)  # 浮点转成整型
        mobileV = str(cell).replace('-', '')
        if mobileV == mobile:
            targetRow = i
    customerInfoBook4write = copy.copy(customerInfoBook)
    customerInfoSheet = customerInfoBook4write.get_sheet('customerInfo')
    customerInfoSheet.write(targetRow, 3, 'Y')
    customerInfoSheet.write(targetRow, 4, result)
    customerInfoSheet.write(targetRow, 5, duration)
    customerInfoBook4write.save(customerInfoPath)


if __name__ == "__main__":
    global hwnd_title
    hwnd_title = dict()  # 所有句柄字典
    global customInfoDic
    customInfoDic = dict()  # 客户信息字典
    global resultList
    resultList = []  # 结果集
    global BASE_PATH
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    global CONFIG_INI
    CONFIG_INI = os.path.join(BASE_PATH, "config", "config.ini")
    global WEWORK_PATH
    WEWORK_PATH = IniReader(CONFIG_INI, "WeWorkAddress", "WeWorkAddress").data
    global DELAY_TIME
    DELAY_TIME = int(IniReader(CONFIG_INI, "timeConfig", "delayTime").data)
    global ONE_TIME_NUMBER
    ONE_TIME_NUMBER = int(IniReader(CONFIG_INI, "timeConfig", "oneTimeNumber").data)
    global AFTER_ONE_TIME_DELAY
    AFTER_ONE_TIME_DELAY = int(IniReader(CONFIG_INI, "timeConfig", "oneTimeNumber").data)
    global log_path
    log_path = os.path.join(BASE_PATH, 'log', "run_%s.log" % datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    global tool_name
    tool_name = WEWORK_PATH
    global wechatWindowTitle
    wechatWindowTitle = u"企业微信"
    global wechatWindowClassName
    wechatWindowClassName = u"WeWorkWindow"
    global addCustomerWindowTitle
    addCustomerWindowTitle = u"添加客户"
    global addCustomerWindowClassName
    addCustomerWindowClassName = u"SearchExternalsWnd"
    global noCustomerConfirmTitle
    noCustomerConfirmTitle = u"该用户不存在"
    global noCustomerConfirmClassName
    noCustomerConfirmClassName = u"WeWorkMessageBoxFrame"
    global authenticMessageConfirmTitle
    authenticMessageConfirmTitle = u"输入认证信息"
    global authenticMessageClassName
    authenticMessageClassName = u"InputReasonWnd"
    global app
    run()
