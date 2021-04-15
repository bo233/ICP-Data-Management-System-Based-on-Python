# coding=utf-8

import wx
import numpy
import time
import datetime
import pandas as pd
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdata
import matplotlib.animation as animation
from matplotlib.dates import AutoDateLocator
import datetime
from util.dataproc import *
from util.DS import *
from database.dbUtil import DBHelper
from wx.lib.buttons import GenButton
from util.dataproc import *


class ICPFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='', pos=wx.DefaultSize, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.dHelper:DataHelper = None

        self.InitUI()

    def InitUI(self):
        self.SetBackgroundColour('Black')
        # self.panel = wx.Panel(self)
        self.panel = FigureCanvas(self, -1, Figure(facecolor=(0.2, 0.2, 0.2)))
        self.panel.SetBackgroundColour('Black')
        self.Center(wx.BOTH)

        # 相关变量定义
        self.alarmThreshold = 20  # 报警阈值
        bigFont = wx.Font(65, wx.SWISS, wx.NORMAL, wx.NORMAL)
        midFont = wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL)
        normalFont = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
        green = (115, 194, 97)
        orange = (255, 153, 18)
        white = (210, 210, 210)

        # 颅内压设备信息控件
        self.lICP = wx.StaticText(self.panel, label='ICP:', pos=(920, 120))
        self.lICP.SetFont(midFont)
        self.lICP.SetForegroundColour(green)

        self.tICP = wx.StaticText(self.panel, label='--', pos=(1010, 170))
        self.tICP.SetFont(bigFont)
        self.tICP.SetForegroundColour(green)

        self.lAlarm = wx.StaticText(self.panel, label='报警阈值：'+str(self.alarmThreshold), pos=(920, 280))
        self.lAlarm.SetFont(normalFont)
        self.lAlarm.SetForegroundColour(orange)

        self.lmmHg = wx.StaticText(self.panel, label='mmHg', pos=(1100, 280))
        self.lmmHg.SetFont(normalFont)
        self.lmmHg.SetForegroundColour(green)

        self.lTemp = wx.StaticText(self.panel, label='温度：', pos=(920, 400))
        self.lTemp.SetFont(midFont)
        self.lTemp.SetForegroundColour(white)

        self.tTemp = wx.StaticText(self.panel, label='--', pos=(980, 470))
        self.tTemp.SetFont(bigFont)
        self.tTemp.SetForegroundColour(white)

        self.lTempIco = wx.StaticText(self.panel, label='°C', pos=(1120, 470))
        self.lTempIco.SetFont(normalFont)
        self.lTempIco.SetForegroundColour(white)

        self.tTime = wx.StaticText(self.panel, label='1971-01-01 00:00:00', pos=(980, 600))
        self.tTime.SetFont(normalFont)
        self.tTime.SetForegroundColour(white)


        # 计时器
        self.timer_sec = wx.Timer(owner=self)
        self.timer_hnd = wx.Timer(owner=self)
        self.timer_simu = wx.Timer(owner=self)
        self.Bind(wx.EVT_TIMER, self.timeFresh, self.timer_sec)  # 绑定事件
        self.Bind(wx.EVT_TIMER, self.handle, self.timer_hnd)
        self.Bind(wx.EVT_TIMER, self.simuHandle, self.timer_simu)
        self.timer_sec.Start(1000)  # 每隔1秒触发一次事件


        # 功能区
        y = 730
        self.bConDev = GenButton(self.panel, label='连接设备', pos=(100, y), style=wx.BORDER_NONE)
        self.bConDev.SetForegroundColour('white')
        self.bConDev.SetBackgroundColour('#707070')
        self.bConDev.Bind(wx.EVT_BUTTON, self.OnClickConDev)

        self.bSetAlarm = GenButton(self.panel, label='报警阈值', pos=(250, y), style=wx.BORDER_NONE)
        self.bSetAlarm.SetForegroundColour('white')
        self.bSetAlarm.SetBackgroundColour('#707070')
        self.bSetAlarm.Bind(wx.EVT_BUTTON, self.OnClickSetAlm)

        self.bOpState = GenButton(self.panel, label='手术阶段', pos=(400, y), style=wx.BORDER_NONE)
        self.bOpState.SetForegroundColour('white')
        self.bOpState.SetBackgroundColour('#707070')

        self.bDisconDev = GenButton(self.panel, label='断开设备', pos=(550, y), style=wx.BORDER_NONE)
        self.bDisconDev.SetForegroundColour('white')
        self.bDisconDev.SetBackgroundColour('#707070')

        self.bSimuCon = GenButton(self.panel, label='模拟连接', pos=(700, y), style=wx.BORDER_NONE)
        self.bSimuCon.SetForegroundColour('white')
        self.bSimuCon.SetBackgroundColour('#707070')
        self.bSimuCon.Bind(wx.EVT_BUTTON, self.OnClickSimuCon)

        self.bDayView = GenButton(self.panel, label='日期视图', pos=(100, 680), style=wx.BORDER_NONE)
        self.bDayView.SetForegroundColour('white')
        self.bDayView.SetBackgroundColour('#707070')

        self.bHourView = GenButton(self.panel, label='小时视图', pos=(250, 680), style=wx.BORDER_NONE)
        self.bHourView.SetForegroundColour('white')
        self.bHourView.SetBackgroundColour('#707070')

        self.bMinView = GenButton(self.panel, label='分钟视图', pos=(400, 680), style=wx.BORDER_NONE)
        self.bMinView.SetForegroundColour('white')
        self.bMinView.SetBackgroundColour('#707070')


        # ####### 波形图
        # 变量
        self.axLen = 0  # 长度
        self.axRange = [0, 10000]  # 显示范围
        self.dataLen = 0  # 数据总长度
        self.latestData: Data = None
        self.simuI = 0
        self.DAYVIEWLEN = 86400
        self.HOURVIEWLEN = 10800
        self.MINVIEWLEN = 1800
        # 数据
        self.datas = []
        self.icps = [0]*1000
        self.dates = ['']*1000
        # for i in range(0, 100):
        #     self.icps.append(self.datas[i].icp)
        #     self.dates.append(str(self.datas[i].date))
        # for i in data:
        #     icps.append(i.icp)
        #     dates.append(str(i.date))
        self.y = numpy.array(self.dates)
        self.x = numpy.array(self.icps)
        self.dataLen = len(self.icps)
        # 坐标轴
        self.ax = self.panel.figure.add_subplot(111)
        self.ax.set_facecolor('black')
        self.panel.figure.subplots_adjust(left=0.05, bottom=0.3, right=0.75, top=0.9 )
        # self.panel.figure.set_size_inches(0.2, 0.2)
        # self.ax.plot(self.y, self.x, '-g')
        self.line, = self.ax.plot([], [], '-g')
        # self.ax.fill_between(self.y, self.x, 0, color='g', alpha=0.7)
        self.ax.hlines(self.alarmThreshold, 0, self.dataLen, color='#FF9912')
        self.ax.grid(True, c='gray')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.set_yticks([0, 10, 20, 30])
        self.ax.set_yticks([0, 5, 10, 15, 20, 25, 30], minor=True)
        # my_y_ticks = numpy.arange(0, 30, 5)
        # plt.yticks(my_y_ticks)
        self.panel.figure.autofmt_xdate()
        # self.axes.set_xlim(self.axRange)
        # self.panel.draw()
        # plt.show()

    # 刷新波形图
    # def refresh(self):
    #     l = self.dataLen * self.sclPos / self.SCLLEN
    #     r = self.dataLen * (self.sclPos + self.sclSize) / self.SCLLEN
    #     self.axRange = [l, r]
    #     self.ax.cla()
    #     self.ax.grid(True)
    #     self.ax.set_xlim(self.axRange)
    #     self.ax.plot(self.y, '-g')
    #     self.panel.draw()
    #     time.sleep(0.01)

    # 时间更新
    def timeFresh(self, evt):
        time_now = datetime.datetime.now()
        time_str = time_now.strftime("%Y-%m-%d %H:%M:%S")
        self.tTime.SetLabel(time_str)

    def handle(self, evt):
        # TODO
        if self.dHelper is not None:
            state, rtn = self.dHelper.getRtn()
            if state == const.DATA:
                self.latestData = rtn

    def simuHandle(self, evt):
        if self.simuI > 9000:
            self.simuI = 0
        self.latestData = self.datas[self.simuI]
        self.simuI += 1
        # print(str(self.latestData))

    # def setXTick(self, st_time, ed_time, flag=0):
    #     x = pd.date_range(start=st_time, end=ed_time, freq="10")

    # 自定义时间刻度如何显示
    # def MinTick(self, x, pos):
    #     x = mdata.num2date(x)
    #
    #     if pos == 0:
    #         fmt = '%Y-%m-%d %H:%M:%S'
    #     else :
    #         fmt = '%H:%M:%S.%f'
    #
    #     label = x.strftime(fmt)
    #     return label

    # 流式显示时更新ICP数据
    def updataData(self, frame):
        # while True:
        self.icps[:] = numpy.roll(self.icps, -1)
        self.icps[-1] = self.latestData.icp
        self.dates[:] = numpy.roll(self.dates, -1)
        self.dates[-1] = str(self.latestData.date)
        self.line.set_data(self.dates, self.icps)
        # self.ax.set_data(())
        print(self.icps[-1])
        # yield self.icps
        return self.line,

    # 开始实时显示
    def steamingDisp(self):
        ani = animation.FuncAnimation(self.panel.figure, self.updataData, interval=1000)
        plt.show()

    def OnClickConDev(self, evt):
        dlg = wx.TextEntryDialog(self.panel, '输入设备地址：', '连接设备')
        path = ""
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetValue()
            self.dHelper = DataHelper(path)
            # TODO: check if connect successfully
            if True:
                self.steamingDisp()
                self.timer_hnd.Start(100)

    def OnClickSetAlm(self, evt):
        dlg = wx.TextEntryDialog(self.panel, '输入报警阈值（mmHg）：', '设置报警阈值')
        if dlg.ShowModal() == wx.ID_OK:
            self.alarmThreshold = dlg.GetValue()
        self.lAlarm.SetLabel('报警阈值：'+str(self.alarmThreshold))
        # self.ax.hlines(self.alarmThreshold, 0, 10000, color='#FF9912')

    def OnClickSimuCon(self, evt):
        self.datas = read("/Users/bo233/Projects/Graduation-Project/data/data.dat")
        ani = animation.FuncAnimation(self.panel.figure, self.updataData, interval=1000, blit=False)
        plt.show()
        self.timer_simu.Start(1000)
        print('OnClickSimuCon')


class ICPApp(wx.App):
    def OnInit(self):
        style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        self.frame = ICPFrame(id=-1, title='颅内压数据管理系统', pos=(3600, 240), size=(1200, 900), style=style)
        self.frame.Show()
        return True


def main():
    app = ICPApp()
    app.MainLoop()


if __name__ == "__main__":
    main()

