# coding=utf-8

import wx
import numpy
import gc
import os
import _thread
import time
import datetime
import pickle
import pandas as pd
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from matplotlib.dates import AutoDateLocator
import datetime
from util.DS import *
from database.dbUtil import DBHelper
from wx.lib.buttons import GenButton
from util.dataproc import *
from uiframe import MainFrame
# from  util.Data import *
# import util.Data
# import matplotlib
# matplotlib.use('WxAgg')


class ICPFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='颅内压数据管理系统', pos=(3600, 240), size=(1200, 900),
                 style=wx.DEFAULT_FRAME_STYLE, p_id=0):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.p_id = p_id
        self.dHelper:DataHelper = None

        self.InitUI()

    def InitUI(self):
        self.SetBackgroundColour('Black')
        # self.panel = wx.Panel(self)
        self.figure = Figure(facecolor=(0.2, 0.2, 0.2))
        self.panel = FigureCanvas(self, -1, self.figure)
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

        self.tBattery = wx.StaticText(self.panel, label='剩余电量：--%', pos=(1000, 830))
        self.tBattery.SetFont(normalFont)
        self.tBattery.SetForegroundColour(white)


        # 计时器
        self.timer_sec = wx.Timer(owner=self)
        self.timer_hnd = wx.Timer(owner=self)
        self.timer_simu = wx.Timer(owner=self)
        self.Bind(wx.EVT_TIMER, self.timeFresh, self.timer_sec)  # 绑定事件
        self.Bind(wx.EVT_TIMER, self.handle, self.timer_hnd)
        self.Bind(wx.EVT_TIMER, self.simuHandle, self.timer_simu)
        self.timer_sec.Start(1000)  # 每隔1秒触发一次事件


        # 功能区
        y = 740
        self.bConDev = GenButton(self.panel, label='连接设备', pos=(100, y), style=wx.BORDER_NONE)
        self.bConDev.SetForegroundColour('white')
        self.bConDev.SetBackgroundColour('#707070')
        self.bConDev.Bind(wx.EVT_BUTTON, self.OnClickConDev)

        self.bSetAlarm = GenButton(self.panel, label='报警阈值', pos=(250, y), style=wx.BORDER_NONE)
        self.bSetAlarm.SetForegroundColour('white')
        self.bSetAlarm.SetBackgroundColour('#707070')
        self.bSetAlarm.Bind(wx.EVT_BUTTON, self.OnClickSetAlm)

        self.bRtnCon = GenButton(self.panel, label='返回就诊', pos=(400, y), style=wx.BORDER_NONE)
        self.bRtnCon.SetForegroundColour('white')
        self.bRtnCon.SetBackgroundColour('#707070')
        self.bRtnCon.Bind(wx.EVT_BUTTON, self.OnClickRtnCon)

        self.bDisconDev = GenButton(self.panel, label='断开连接', pos=(550, y), style=wx.BORDER_NONE)
        self.bDisconDev.SetForegroundColour('white')
        self.bDisconDev.SetBackgroundColour('#707070')
        self.bDisconDev.Bind(wx.EVT_BUTTON, self.OnClickDiscon)
        self.bDisconDev.Disable()

        self.bSimuCon = GenButton(self.panel, label='从SD卡读取', pos=(700, y), style=wx.BORDER_NONE)
        self.bSimuCon.SetForegroundColour('white')
        self.bSimuCon.SetBackgroundColour('#707070')
        self.bSimuCon.Bind(wx.EVT_BUTTON, self.OnClickSimuCon)

        self.bSimuDiscon = GenButton(self.panel, label='断开模拟连接', pos=(700, y), style=wx.BORDER_NONE)
        self.bSimuDiscon.SetForegroundColour('white')
        self.bSimuDiscon.SetBackgroundColour('#707070')
        self.bSimuDiscon.Bind(wx.EVT_BUTTON, self.OnClickSimuDiscon)
        self.bSimuDiscon.Disable()
        self.bSimuDiscon.Hide()

        self.bDayView = GenButton(self.panel, label='天视图', pos=(100, 680), style=wx.BORDER_NONE)
        self.bDayView.SetForegroundColour('white')
        self.bDayView.SetBackgroundColour('#707070')
        self.bDayView.Bind(wx.EVT_BUTTON, self.OnClickDayView)

        self.bHourView = GenButton(self.panel, label='3小时视图', pos=(250, 680), style=wx.BORDER_NONE)
        self.bHourView.SetForegroundColour('white')
        self.bHourView.SetBackgroundColour('#707070')
        self.bHourView.Bind(wx.EVT_BUTTON, self.OnClickHourView)

        self.bMin30View = GenButton(self.panel, label='30分钟视图', pos=(400, 680), style=wx.BORDER_NONE)
        self.bMin30View.SetForegroundColour('white')
        self.bMin30View.SetBackgroundColour('#707070')
        self.bMin30View.Bind(wx.EVT_BUTTON, self.OnClick30MinView)

        self.bMin5View = GenButton(self.panel, label='5分钟视图', pos=(550, 680), style=wx.BORDER_NONE)
        self.bMin5View.SetForegroundColour('white')
        self.bMin5View.SetBackgroundColour('#707070')
        self.bMin5View.Bind(wx.EVT_BUTTON, self.OnClick5MinView)

        self.alarmHint = wx.StaticText(self.panel, label='⚠️ 颅内压已超过阈值，请注意！', pos=(310, 820))
        self.alarmHint.SetFont(midFont)
        self.alarmHint.SetForegroundColour(orange)
        self.alarmHint.Hide()

        self.bAlmCon = GenButton(self.panel, label='🔔', pos=(740, 815), size=(40,40), style=wx.BORDER_NONE)
        self.bAlmCon.SetForegroundColour('white')
        self.bAlmCon.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.bAlmCon.SetBackgroundColour('#707070')
        self.bAlmCon.Hide()
        self.bAlmCon.Bind(wx.EVT_BUTTON, self.OnClickAlmCon)


        # ####### 波形图
        # 变量
        MAXDATALEN = 86400
        # self.DAYVIEWLEN = 86400
        # self.HOUR3VIEWLEN = 10800
        # self.MIN30VIEWLEN = 1800
        # self.MIN5VIEWLEN = 300
        # self.axisxLen = self.MIN5VIEWLEN  # x轴长度
        # self.dataLen = 0  # 数据总长度
        self.latestData = Data(datetime.datetime.now(), 0, 0)
        self.simuI = 0
        self.dateDelta = datetime.timedelta(minutes=4, seconds=59, microseconds=500)

        # 数据
        self.datas:list[Data] = []
        self.icps = [0] * MAXDATALEN
        # self.dates = [numpy.array(range(0, 1000))]
        # st_time = datetime.datetime(2021, 1, 1, 0, 0, 0)
        # ed_time = datetime.datetime(2021, 1, 1, 0, 4, 59, 500)
        # delta = datetime.timedelta(seconds=1)
        # self.dates = mdates.drange(st_time, ed_time, delta)
        self.dates = []
        # self.dates = mdates.num2date(self.dates)
        # self.dataLen = len(self.icps)
        # 坐标轴
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('black')
        self.figure.subplots_adjust(left=0.05, bottom=0.3, right=0.75, top=0.9)
        # self.panel.figure.set_size_inches(0.2, 0.2)
        # TODO len error
        # self.ax.hlines(self.alarmThreshold, 0, self.MIN5VIEWLEN, color='#FF9912')
        self.ax.grid(True, c='gray')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        # self.line, = self.ax.plot_date(self.dates, [None]*self.MIN5VIEWLEN, '-g')
        self.line, = self.ax.plot_date([], [], '-g')
        # self.ax.set_yticks([0, 5, 10, 15, 20, 25, 30], minor=True)
        self.ax.set_yticks([0, 10, 20, 30])
        self.ax.set_ylim(0, 30)

        # 根据自己定义的方式去画时间刻度
        # formatter = plt.FuncFormatter(self.time_ticks)
        formatter = mdates.DateFormatter("%H:%M")
        # 在图中应用自定义的时间刻度
        self.ax.xaxis.set_major_formatter(formatter)
        # minticks 需要指出，值的大小决定了图是否能按 10min 为单位显示
        # 值越小可能只能按小时间隔显示
        locator = AutoDateLocator(minticks=3)
        # pandas 只生成了满足 10min 的 x 的值，而指定坐标轴以多少的时间间隔画的是下面的这行代码
        # 如果是小时，需要在上面导入相应的东东 YEARLY, MONTHLY, DAILY, HOURLY, MINUTELY, SECONDLY, MICROSECONDLY
        # 并按照下面的格式照葫芦画瓢
        locator.intervald[mdates.MINUTELY] = [1]  # 10min 为间隔
        self.ax.xaxis.set_major_locator(locator=locator)
        # self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        # my_y_ticks = numpy.arange(0, 30, 5)
        # plt.yticks(my_y_ticks)


    # 自定义时间刻度如何显示
    def time_ticks(x, pos):
        # 在 pandas 中，按 10min 生成的时间序列与 matplotlib 要求的类型不一致
        # 需要转换成 matplotlib 支持的类型
        x = mdates.num2date(x)

        # 时间坐标是从坐标原点到结束一个一个标出的
        # 如果是坐标原点的那个刻度则用下面的要求标出刻度
        if pos == 0:
            # %Y-%m-%d
            # 时间格式化的标准是按 2020-10-01 10:10:10 标记的
            fmt = '%Y-%m-%d %H:%M:%S'
        # 如果不是是坐标原点的那个刻度则用下面的要求标出刻度
        else:
            # 时间格式化的标准是按 10:10:10 标记的
            fmt = '%H:%M:%S'
        # 根据 fmt 的要求画时间刻度
        label = x.strftime(fmt)
        return label

    # 时间更新
    def timeFresh(self, evt):
        time_now = datetime.datetime.now()
        time_str = time_now.strftime("%Y-%m-%d %H:%M:%S")
        self.tTime.SetLabel(time_str)

    def handle(self, evt):
        if self.dHelper is not None:
            self.dHelper.handle()
            state, rtn = self.dHelper.getRtn()
            print(state, rtn)
            if state == const.DATA:
                self.latestData = rtn
                self.datas.append(rtn)
                # print(rtn)
            elif state == const.BATTERY:
                self.tBattery.SetLabel('剩余电量：%d%%'%(rtn*25))
            elif state == const.OFF:
                self.timer_hnd.Stop()
                self.ani.event_source.stop()
                self.bConDev.Enable()
                wx.MessageBox('颅内压测量仪器已关机！')
            elif state == const.PING:
                pass


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
        self.dates[-1] = mdates.date2num(self.latestData.date)
        if self.latestData.icp >= self.alarmThreshold:
            self.alarmHint.Show()
            self.bAlmCon.Show()
            # duration = 5  # second
            # freq = 440  # Hz
            # os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
            _thread.start_new_thread(self.alarm, ())

        self.line.set_data(self.dates, self.icps)
        self.p = self.ax.fill_between(self.dates, self.icps, color='g', alpha=0.7)
        self.tICP.SetLabel(str(self.latestData.icp))
        self.tTemp.SetLabel("%.1f"%(self.latestData.ict))
        self.ax.set_xlim([mdates.date2num(self.latestData.date-self.dateDelta), self.dates[-1]])
        gc.collect()
        return self.line, self.p, self.ax.xaxis,

    def alarm(self):
        duration = 1  # second
        freq = 440  # Hz
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))

    # 开始实时显示
    def steamingDisp(self):
        self.ani = animation.FuncAnimation(self.figure, self.updataData, interval=1000, blit=True, save_count=10)

    def OnClickConDev(self, evt):
        choices = COMHelper.getPorts()
        dlg = wx.SingleChoiceDialog(self.panel, '选择设备：', '连接设备', choices)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetStringSelection()
            self.dHelper = DataHelper(path)
            if self.dHelper is not None:
                self.latestData.date = datetime.datetime.now()
                self.timer_hnd.Start(1000)
                delta = datetime.timedelta(days=1)
                ed_time = self.latestData.date
                st_time = ed_time - delta
                self.dates = mdates.drange(st_time, ed_time, datetime.timedelta(seconds=1))
                self.steamingDisp()
                self.bSimuCon.Disable()
                self.bConDev.Disable()
                self.bDisconDev.Enable()

    def OnClickSetAlm(self, evt):
        dlg = wx.TextEntryDialog(self.panel, '输入报警阈值（mmHg）：', '设置报警阈值')
        if dlg.ShowModal() == wx.ID_OK:
            self.alarmThreshold = int(dlg.GetValue())
        self.lAlarm.SetLabel('报警阈值：'+str(self.alarmThreshold))
        # self.ax.hlines(self.alarmThreshold, 0, 10000, color='#FF9912')

    def OnClickSimuCon(self, evt):
        file_wildcard = '数据文件(*.dat)|*.dat'
        dlg = wx.FileDialog(self.panel, '选择文件',style=wx.FD_OPEN, wildcard=file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.datas = readSD(dlg.GetPath())
            self.latestData = self.datas[0]
            self.simuI += 1
            self.timer_simu.Start(1000)
            delta = datetime.timedelta(days=1)
            ed_time = self.latestData.date
            st_time = ed_time - delta
            self.dates = mdates.drange(st_time, ed_time, datetime.timedelta(seconds=1))
            self.steamingDisp()
            self.bSimuCon.Disable()
            self.bSimuCon.Hide()
            self.bSimuDiscon.Enable()
            self.bSimuDiscon.Show()
            self.bConDev.Disable()

    def OnClickSimuDiscon(self, evt):
        self.timer_simu.Stop()
        self.ani.event_source.stop()
        self.bSimuDiscon.Disable()
        self.bSimuDiscon.Hide()
        self.bSimuCon.Enable()
        self.bSimuCon.Show()

    def OnClickAlmCon(self, evt):
        self.alarmHint.Hide()
        self.bAlmCon.Hide()

    def OnClickDayView(self, evt):
        self.dateDelta = datetime.timedelta(days=1)

    def OnClickHourView(self, evt):
        self.dateDelta = datetime.timedelta(hours=3)

    def OnClick30MinView(self, evt):
        self.dateDelta = datetime.timedelta(minutes=30)

    def OnClick5MinView(self, evt):
        self.dateDelta = datetime.timedelta(minutes=4, seconds=59, microseconds=500)

    def OnClickRtnCon(self, evt):
        dlg = wx.MessageDialog(self, '是否返回就诊界面？', '提醒', wx.YES_NO)
        if dlg.ShowModal() == wx.ID_YES:
            self.timer_sec.Stop()
            self.Close(True)
            path = '/Users/bo233/Projects/Graduation-Project/data'
            path += '/' + str(self.p_id)
            folder = os.path.exists(path)
            if not folder:
                os.makedirs(path)
            path += '/' + str(self.datas[0].date.date()) + '.dat'
            save(self.datas, path)
            DBHelper.addIcp(str(self.p_id), path, self.datas[0].date)
            f = MainFrame.MainFrame(p_id=self.p_id)
            f.Show()

    def OnClickDiscon(self, evt):
        DBHelper.conn.close()
        self.timer_hnd.Stop()
        self.ani.event_source.stop()
        self.bConDev.Enable()
        self.bDisconDev.Disable()



class ICPApp(wx.App):
    def OnInit(self):
        self.frame = ICPFrame()
        self.frame.Show()
        return True


def main():
    app = ICPApp()
    app.MainLoop()


if __name__ == "__main__":
    main()

