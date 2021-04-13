# coding=utf-8

import wx
import numpy
import time
import datetime
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
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

        self.dHelper = None

        self.InitUI()

    def InitUI(self):
        self.SetBackgroundColour('Black')
        # self.panel = wx.Panel(self)
        self.panel = FigureCanvas(self, -1, Figure(facecolor=(0.2, 0.2, 0.2)))
        self.panel.SetBackgroundColour('Black')
        self.Center(wx.BOTH)

        # 相关变量定义
        self.alarmThreshold = 20     # 报警阈值
        self.sclPos = 0              # 滑块位置
        self.sclSize = 100           # 滑块大小
        self.SCLLEN = 1000           # 滑块总长度
        self.axLen  = 0              # 长度
        self.axRange = [0, 10000]    # 显示范围
        self.dataLen = 0             # 数据总长度

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
        self.Bind(wx.EVT_TIMER, self.timeFresh, self.timer_sec)  # 绑定事件
        self.Bind(wx.EVT_TIMER, self.handle, self.timer_hnd)
        self.timer_sec.Start(1000)  # 每隔1秒触发一次事件
        self.timer_hnd.Start(100)


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

        self.bHourView = GenButton(self.panel, label='小时视图', pos=(100, 680), style=wx.BORDER_NONE)
        self.bHourView.SetForegroundColour('white')
        self.bHourView.SetBackgroundColour('#707070')

        self.bMinView = GenButton(self.panel, label='分钟视图', pos=(250, 680), style=wx.BORDER_NONE)
        self.bMinView.SetForegroundColour('white')
        self.bMinView.SetBackgroundColour('#707070')


        # 波形图
        data = read("/Users/bo233/Projects/Graduation-Project/data/data.dat")
        scores = []
        for i in data:
            scores.append(i.icp)
        self.t_score = numpy.arange(1, len(scores) + 1, 1)
        self.s_score = numpy.array(scores)

        self.dataLen = len(scores)

        self.ax = self.panel.figure.add_subplot(111)
        self.ax.set_facecolor('black')
        self.panel.figure.subplots_adjust(left=0.05, bottom=0.3, right=0.75, top=0.9 )
        self.ax.plot(self.t_score, self.s_score, '-g')
        # self.axes.fill_between(0, self.s_score, color='green')
        self.ax.fill_between(self.t_score, self.s_score, 0, color='g', alpha=0.7)
        self.ax.hlines(self.alarmThreshold, 0, 10000, color='#FF9912')
        self.ax.grid(True, c='gray')
        # self.axes.set_xlabel('Time')
        # self.axes.set_ylabel('ICP')

        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        # self.axes.set_xlim(self.axRange)
        self.panel.draw()


    # 刷新波形图
    def refresh(self):
        l = self.dataLen * self.sclPos / self.SCLLEN
        r = self.dataLen * (self.sclPos + self.sclSize) / self.SCLLEN
        self.axRange = [l, r]
        self.ax.cla()
        self.ax.grid(True)
        self.ax.set_xlim(self.axRange)
        self.ax.plot(self.t_score, '-g')
        self.panel.draw()
        time.sleep(0.01)

    # 时间更新
    def timeFresh(self, evt):
        time_now = datetime.datetime.now()
        time_str = time_now.strftime("%Y-%m-%d %H:%M:%S")
        self.tTime.SetLabel(time_str)

    def handle(self, evt):
        if self.dHelper is not None:
             pass

    def OnClickConDev(self, evt):
        dlg = wx.TextEntryDialog(self.panel, '输入设备地址：', '连接设备')
        path = ""
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetValue()
            self.dHelper = DataHelper(path)

    def OnClickSetAlm(self, evt):
        dlg = wx.TextEntryDialog(self.panel, '输入报警阈值（mmHg）：', '设置报警阈值')
        if dlg.ShowModal() == wx.ID_OK:
            self.alarmThreshold = dlg.GetValue()
        self.lAlarm.SetLabel('报警阈值：'+str(self.alarmThreshold))
        # self.ax.hlines(self.alarmThreshold, 0, 10000, color='#FF9912')


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

