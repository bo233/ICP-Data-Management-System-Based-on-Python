# coding=utf-8

import wx
import numpy
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
from util.dataproc import *
from util.DS import *
from database.dbUtil import DBHelper


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

        self.lPntInfo = wx.StaticText(panel, label="患者信息", pos=(960, 50))
        # pntInfoBox = wx.BoxSizer(wx.VERTICAL)
        # hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.lId = wx.StaticText(panel, label='ID：', pos=(900, 80))
        # hbox1.Add(lId, flag=wx.RIGHT, border=5)
        self.tId = wx.TextCtrl(panel, size=(130, 25), pos=(940, 80))
        self.bId = wx.Button(panel, label='查询', pos=(1080, 80))
        self.lName = wx.StaticText(panel, label='姓名：', pos=(900, 120))
        self.tName = wx.StaticText(panel, pos=(940, 120))
        self.lAge = wx.StaticText(panel, label='年龄：', pos=(900, 160))
        self.tAge = wx.StaticText(panel, pos=(940,160))
        self.lGen = wx.StaticText(panel, label='性别：', pos=(900, 200))
        self.tGen = wx.StaticText(panel, pos=(940, 200))
        self.lSymp = wx.StaticText(panel, label='症状：', pos=(900, 240))
        self.tSymp = wx.TextCtrl(panel, size=(240, 200), pos=(940, 240), style=wx.TE_MULTILINE)
        self.lDiag = wx.StaticText(panel, label='诊断：', pos=(900, 460))
        self.tDiag = wx.TextCtrl(panel, size=(240, 200), pos=(940, 460), style=wx.TE_MULTILINE)
        self.lDate = wx.StaticText(panel, label='日期：', pos=(900, 680))
        self.tDate = wx.StaticText(panel, label=str(datetime.date.today()), pos=(940, 680))
        self.bSave = wx.Button(panel, label='保存', pos=(920, 740))
        self.bClear = wx.Button(panel, label='清除', pos=(1040, 740))

        self.bId.Bind(wx.EVT_BUTTON, self.OnClickId)
        self.bClear.Bind(wx.EVT_BUTTON, self.OnClickClear)
        self.bSave.Bind(wx.EVT_BUTTON, self.OnClickSave)

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

    def OnClickId(self, event):
        self.pId = str(self.tId.GetValue())
        if self.pId.isdigit():
            ptData = DBHelper.getPtData(self.pId)
            if ptData is not None :
                self.tName.SetLabel(ptData.name)
                self.tAge.SetLabel(str(ptData.age))
                self.tGen.SetLabel(ptData.gender)
                # self.tDiag.SetValue(ptData.cons[0].diag)
                # self.tSymp.SetValue(ptData.cons[0].sx)
                # self.tDate.SetLabel(str(ptData.cons[0].date))

    def OnClickClear(self, event):
        self.tSymp.SetValue("")
        self.tDiag.SetValue("")

    def OnClickSave(self, event):
        symp = self.tSymp.GetValue()
        diag = self.tDiag.GetValue()
        cons = Cons(datetime.date.today(), symp, diag)
        DBHelper.addPtCons(self.pId, cons)
        wx.MessageBox("保存成功！")


class MainApp(wx.App):
    def OnInit(self):
        style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        self.frame = MainFrame(id=-1, title='颅内压数据管理系统', pos=(3600, 240), size=(1200, 900), style=style)
        self.frame.Show()
        return True


def main():
    app = MainApp()
    app.MainLoop()


if __name__ == "__main__":
    main()

