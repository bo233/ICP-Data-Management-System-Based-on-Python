# coding=utf-8

import wx
import numpy
import time
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import datetime
from util.dataproc import *
from util.DS import *
from database.dbUtil import DBHelper
from uiframe import ICPFrame
from uiframe import PntModifyFrame as PntModFrame


class MainFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='', pos=wx.DefaultSize, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.InitUI()

    def InitUI(self):
        self.SetBackgroundColour('white')
        # self.panel = wx.Panel(self)
        self.panel = FigureCanvas(self, -1, Figure())
        self.Center(wx.BOTH)
        # wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL)

        # 相关变量定义
        self.sclPos = 0              # 滑块位置
        self.sclSize = 100           # 滑块大小
        self.SCLLEN = 1000           # 滑块总长度
        self.axLen  = 0              # 长度
        self.axRange = [0, 10000]    # 显示范围
        self.dataLen = 0             # 数据总长度

        # 患者信息控件
        self.lPntInfo = wx.StaticText(self.panel, label="患者信息", pos=(960, 50))
        # pntInfoBox = wx.BoxSizer(wx.VERTICAL)
        # hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.lId = wx.StaticText(self.panel, label='ID：', pos=(900, 80))
        # hbox1.Add(lId, flag=wx.RIGHT, border=5)
        self.tId = wx.TextCtrl(self.panel, size=(130, 25), pos=(940, 80))
        self.bId = wx.Button(self.panel, label='查  询', pos=(1080, 80))
        self.lName = wx.StaticText(self.panel, label='姓名：', pos=(900, 120))
        self.tName = wx.StaticText(self.panel, pos=(940, 120))
        self.lBld_type = wx.StaticText(self.panel, label='血型：', pos=(1030, 120))
        self.tBld_type = wx.StaticText(self.panel, pos=(1070, 120))
        self.lAge = wx.StaticText(self.panel, label='年龄：', pos=(900, 160))
        self.tAge = wx.StaticText(self.panel, pos=(940,160))
        self.lHeight = wx.StaticText(self.panel, label='身高：', pos=(1030, 160))
        self.tHeight = wx.StaticText(self.panel, pos=(1070, 160))
        self.lGen = wx.StaticText(self.panel, label='性别：', pos=(900, 200))
        self.tGen = wx.StaticText(self.panel, pos=(940, 200))
        self.lWeight = wx.StaticText(self.panel, label='体重：', pos=(1030, 200))
        self.tWeight = wx.StaticText(self.panel, pos=(1070, 200))
        self.lAllergy = wx.StaticText(self.panel, label='过敏：', pos=(900, 240))
        self.tAllergy = wx.TextCtrl(self.panel, size=(240, 50), pos=(940, 240), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.lMediHis = wx.StaticText(self.panel, label='过往病史：', pos=(875, 300))
        self.tMediHis = wx.TextCtrl(self.panel, size=(240, 50), pos=(940, 300), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.lFamHis = wx.StaticText(self.panel, label='家族病史：', pos=(875, 360))
        self.tFamHis = wx.TextCtrl(self.panel, size=(240, 50), pos=(940, 360), style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.lSymp = wx.StaticText(self.panel, label='症状：', pos=(900, 420))
        self.tSymp = wx.TextCtrl(self.panel, size=(240, 100), pos=(940, 420), style=wx.TE_MULTILINE)
        self.lDiag = wx.StaticText(self.panel, label='诊断：', pos=(900, 530))
        self.tDiag = wx.TextCtrl(self.panel, size=(240, 100), pos=(940, 530), style=wx.TE_MULTILINE)
        self.lDate = wx.StaticText(self.panel, label='日期：', pos=(900, 680))
        self.tDate = wx.StaticText(self.panel, label=str(datetime.date.today()), pos=(940, 680))
        self.bSave = wx.Button(self.panel, label='保  存', pos=(940, 740))
        self.bClear = wx.Button(self.panel, label='清  除', pos=(1060, 740))

        self.bId.Bind(wx.EVT_BUTTON, self.OnClickId)
        self.bClear.Bind(wx.EVT_BUTTON, self.OnClickClear)
        self.bSave.Bind(wx.EVT_BUTTON, self.OnClickSave)

        # 波形图
        data = read("/Users/bo233/Projects/Graduation-Project/data/data.dat")
        scores = []
        for i in data:
            scores.append(i.icp)
        self.t_score = numpy.arange(1, len(scores) + 1, 1)
        self.s_score = numpy.array(scores)
        self.dataLen = len(scores)
        self.axes = self.panel.figure.add_subplot(111)
        self.panel.figure.subplots_adjust(left=0.1, bottom=0.4, right=0.7, top=0.9 )
        self.axes.plot(self.t_score, self.s_score, 'k')
        self.axes.grid(True)
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('ICP')
        self.axes.set_xlim(self.axRange)
        self.panel.draw()

        # FigureCanvas(self.panel, -1, self.figure)

        # 滚动条相关
        self.scrollBar = wx.ScrollBar(self.panel, id = -1, pos=(150, 600), size=(620, 20),
                                      style=wx.SB_HORIZONTAL)
        self.scrollBar.SetScrollbar(self.sclPos, self.sclSize, self.SCLLEN, self.sclSize)
        self.scrollBar.Bind(wx.EVT_SCROLL, self.OnScroll)
        self.bSclSub = wx.Button(self.panel, label='-', pos=(130, 600), size=(20, 20))
        self.bSclAdd = wx.Button(self.panel, label='+', pos=(770,600), size=(20, 20))
        self.bSclAdd.Bind(wx.EVT_BUTTON, self.OnClickAdd)
        self.bSclSub.Bind(wx.EVT_BUTTON, self.OnClickSub)

        self.bCon = wx.Button(self.panel, label='连接设备', pos=(200, 700))
        self.bCon.Bind(wx.EVT_BUTTON, self.OnClickCon)

        self.bModify = wx.Button(self.panel, label='修改信息', pos=(300, 700))
        self.bModify.Bind(wx.EVT_BUTTON, self.OnClickModify)

    # 刷新波形图
    def refresh(self):
        l = self.dataLen * self.sclPos / self.SCLLEN
        r = self.dataLen * (self.sclPos + self.sclSize) / self.SCLLEN
        self.axRange = [l, r]
        self.axes.cla()
        self.axes.grid(True)
        self.axes.set_xlim(self.axRange)
        self.axes.plot(self.t_score, self.s_score, 'k')
        self.panel.draw()
        time.sleep(0.01)

    # 查询ID按钮
    def OnClickId(self, event):
        self.pId = str(self.tId.GetValue())
        if self.pId.isdigit():
            ptData = DBHelper.getPtData(self.pId)
            if ptData is not None :
                self.tName.SetLabel(ptData.name)
                self.tAge.SetLabel(str(ptData.age))
                self.tGen.SetLabel(ptData.gender)
                self.tWeight.SetLabel(str(ptData.weight)+' kg')
                self.tHeight.SetLabel(str(ptData.height)+' cm')
                self.tBld_type.SetLabel(str(ptData.blood_type)+'型')
                self.tAllergy.SetValue(ptData.allergy)
                self.tMediHis.SetValue(ptData.medical_history)
                self.tFamHis.SetValue(ptData.family_history)
                # self.tDiag.SetValue(ptData.cons[0].diag)
                # self.tSymp.SetValue(ptData.cons[0].sx)
                # self.tDate.SetLabel(str(ptData.cons[0].date))

    # 清除按钮
    def OnClickClear(self, event):
        self.tSymp.SetValue("")
        self.tDiag.SetValue("")

    # 保存按钮
    def OnClickSave(self, event):
        symp = self.tSymp.GetValue()
        diag = self.tDiag.GetValue()
        cons = Cons(datetime.date.today(), symp, diag)
        DBHelper.addPtCons(self.pId, cons)
        wx.MessageBox("保存成功！")

    # 滚动条响应
    def OnScroll(self, event):
        self.sclPos = self.scrollBar.GetThumbPosition()
        self.refresh()
        # time.sleep(0.05)
        # print(self.sclPos)

    # +按钮响应
    def OnClickAdd(self, event):

        self.sclSize -= 100
        if self.sclSize < 100:
            self.sclSize = 100
        self.scrollBar.SetScrollbar(self.sclPos, self.sclSize, self.SCLLEN, self.sclSize)
        self.refresh()

    # -按钮响应
    def OnClickSub(self, event):
        self.sclSize += 100
        if self.sclSize > 1000:
            self.sclSize = 1000
        if self.sclPos > 1000 - self.sclSize:
            self.sclPos = 1000 - self.sclSize
        self.scrollBar.SetScrollbar(self.sclPos, self.sclSize, self.SCLLEN, self.sclSize)
        self.refresh()

    def OnClickCon(self, evt):
        self.Close(True)
        ICPFrame.main()

    def OnClickModify(self, evt):
        # PntModifyFrame.main(self, id)
        frame = PntModFrame.PntModifyFrame(id=-1, title='颅内压数据管理系统', pos=(3600, 240), size=(850, 450),
                                           p_id=self.tId.GetValue())
        frame.Show()

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

