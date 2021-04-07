# coding=utf-8

import wx
import numpy
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from util.dataproc import *
from util.DS import *


class MainFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='', pos=wx.DefaultSize, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.InitUI()
        pass

    def InitUI(self):
        self.SetBackgroundColour('white')
        panel = wx.Panel(self)
        self.Center(wx.BOTH)

        lPntInfo = wx.StaticText(panel, label="患者信息", pos=(960, 50))
        # pntInfoBox = wx.BoxSizer(wx.VERTICAL)
        # hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        lId = wx.StaticText(panel, label='ID：', pos=(900, 80))
        # hbox1.Add(lId, flag=wx.RIGHT, border=5)
        tId = wx.TextCtrl(panel, size=(130, 25), pos=(940, 80))
        bId = wx.Button(panel, label='查询', pos=(1080, 80))
        lName = wx.StaticText(panel, label='姓名：', pos=(900, 120))
        tName = wx.StaticText(panel, label='XXX', pos=(940, 120))
        lAge = wx.StaticText(panel, label='年龄：', pos=(900, 160))
        tAge = wx.StaticText(panel, label='XX', pos=(940,160))
        lGen = wx.StaticText(panel, label='性别：', pos=(900, 200))
        tGen = wx.StaticText(panel, label='X', pos=(940, 200))
        lSymp = wx.StaticText(panel, label='症状：', pos=(900, 240))
        tSymp = wx.TextCtrl(panel, size=(240, 200), pos=(940, 240), style=wx.TE_MULTILINE)
        lDiag = wx.StaticText(panel, label='诊断：', pos=(900, 460))
        tDiag = wx.TextCtrl(panel, size=(240, 200), pos=(940, 460), style=wx.TE_MULTILINE)
        lData = wx.StaticText(panel, label='日期：', pos=(900, 680))
        tData = wx.StaticText(panel, label='xxxx-xx-xx', pos=(940, 680))
        bSave = wx.Button(panel, label='保存', pos=(920, 740))
        bClear = wx.Button(panel, label='清除', pos=(1040, 740))



        # hbox1.Add(tId, proportion=1)
        # pntInfoBox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=5)

        # pntInfoBox.Add((1000, 50))

        # panel.SetSizer(pntInfoBox)

        data = read("/Users/bo233/Projects/Graduation-Project/data/data.dat")
        scores = []
        for i in data:
            scores.append(i.icp)
        t_score = numpy.arange(1, len(scores) + 1, 1)
        s_score = numpy.array(scores)

        self.waveGraph = Figure()
        self.waveGraph.set_figheight(6)
        self.waveGraph.set_figwidth(9)
        self.axes_score = self.waveGraph.add_subplot(111)

        self.axes_score.plot(t_score, s_score, 'ro', t_score, s_score, 'k')
        # self.axes_score.axhline(y=average, color='r')
        # self.axes_score.set_title(u'My Scores')
        self.axes_score.grid(True)
        self.axes_score.set_xlabel('Data')
        self.axes_score.set_ylabel('ICP')
        FigureCanvas(panel, -1, self.waveGraph)



class MainApp(wx.App):
    def OnInit(self):
        style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        self.frame = MainFrame(id=-1, title='颅内压数据管理系统', pos=(3600, 240), size=(1200, 850), style=style)
        self.frame.Show()
        return True


def main():
    app = MainApp()
    app.MainLoop()


if __name__ == "__main__":
    main()

