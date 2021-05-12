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
    def __init__(self, parent=None, id=-1, title='颅内压数据管理系统', pos=(3600, 240), size=(1200, 850),
                 style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER, d_id=-1, p_id=-1):
        self.d_id = d_id
        self.p_id = p_id
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
        self.axRange = [0, 0]    # 显示范围
        self.dataLen = 0             # 数据总长度
        self.cons:list[Cons] = []
        self.icpPaths:list[str] = []
        self.icpDatas:list[Data] = []
        self.conIdx = -1
        self.icpIdx = -1

        # 患者信息控件
        self.lPntInfo = wx.StaticText(self.panel, label="患者信息", pos=(980, 50))
        self.lPntInfo.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL))
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
        self.lDate = wx.StaticText(self.panel, label='日期：', pos=(900, 660))
        self.tDate = wx.StaticText(self.panel, label=str(datetime.date.today()), pos=(940, 660))
        self.bFront = wx.Button(self.panel, label='前一次', pos=(1040, 640))
        self.bFront.Disable()
        self.bNext = wx.Button(self.panel, label='后一次', pos=(1040, 670))
        self.bNext.Disable()
        self.bToday = wx.Button(self.panel, label='回到今天', pos=(1040, 700))
        self.bToday.Disable()
        self.bSave = wx.Button(self.panel, label='保  存', pos=(940, 740))
        self.bClear = wx.Button(self.panel, label='清  除', pos=(1060, 740))

        self.lDocName = wx.StaticText(self.panel, label='就诊医生：', pos=(1040, 780))
        self.tDocName = wx.StaticText(self.panel, label='刘医生', pos=(1100, 780))
        if self.d_id != -1:
            self.tDocName.SetLabel(DBHelper.getDocName(self.d_id))
        if self.p_id != -1:
            self.tId.SetValue(str(self.p_id))
            self.OnClickId(None)

        self.bId.Bind(wx.EVT_BUTTON, self.OnClickId)
        self.bClear.Bind(wx.EVT_BUTTON, self.OnClickClear)
        self.bSave.Bind(wx.EVT_BUTTON, self.OnClickSave)
        self.bNext.Bind(wx.EVT_BUTTON, self.OnClickNext)
        self.bFront.Bind(wx.EVT_BUTTON, self.OnClickFront)
        self.bToday.Bind(wx.EVT_BUTTON, self.OnClickToday)

        # 波形图
        self.lTitle = wx.StaticText(self.panel, label='就诊系统', pos=(500, 30))
        self.lTitle.SetFont(wx.Font(36, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # data = readSD("/Users/bo233/Projects/Graduation-Project/data/data.dat")
        # scores = []
        # for i in data:
        #     scores.append(i.icp)
        # self.t_score = numpy.arange(1, len(scores) + 1, 1)
        # self.s_score = numpy.array(scores)
        self.dates = []
        self.icps = []
        self.icts = []
        self.dataLen = 0
        self.axes = self.panel.figure.add_subplot(111)
        self.panel.figure.subplots_adjust(left=0.1, bottom=0.4, right=0.7, top=0.9 )
        # self.axes.plot(self.t_score, self.s_score, 'k')
        self.axes.plot([], [], 'k')
        self.axes.grid(True)
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('ICP')
        self.axes.set_xlim(self.axRange)
        self.axes.set_ylim([0, 30])
        self.panel.draw()

        # FigureCanvas(self.panel, -1, self.figure)

        # 滚动条相关
        self.scrollBar = wx.ScrollBar(self.panel, id = -1, pos=(150, 550), size=(620, 20),
                                      style=wx.SB_HORIZONTAL)
        self.scrollBar.SetScrollbar(self.sclPos, self.sclSize, self.SCLLEN, self.sclSize)
        self.scrollBar.Bind(wx.EVT_SCROLL, self.OnScroll)
        self.bSclSub = wx.Button(self.panel, label='-', pos=(130, 550), size=(20, 20))
        self.bSclAdd = wx.Button(self.panel, label='+', pos=(770,550), size=(20, 20))
        self.bSclAdd.Bind(wx.EVT_BUTTON, self.OnClickAdd)
        self.bSclSub.Bind(wx.EVT_BUTTON, self.OnClickSub)
        self.lICPTitile = wx.StaticText(self.panel, label='历史颅内压数据', pos=(400, 600))
        self.lICPTitile.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.bCon = wx.Button(self.panel, label='连接设备', pos=(200, 700))
        self.bCon.Bind(wx.EVT_BUTTON, self.OnClickCon)

        self.bModify = wx.Button(self.panel, label='修改患者信息', pos=(340, 700))
        self.bModify.Bind(wx.EVT_BUTTON, self.OnClickModify)

        self.bSelectPt = wx.Button(self.panel, label='患者总览', pos=(480, 700))
        self.bSelectPt.Bind(wx.EVT_BUTTON, self.OnClickSelectPt)

        self.bModifyDoc = wx.Button(self.panel, label='修改医生信息', pos=(620, 700))
        self.bModifyDoc.Bind(wx.EVT_BUTTON, self.OnClickModifyDoc)

    # 刷新波形图
    def refresh(self):
        l = self.dataLen * self.sclPos / self.SCLLEN
        r = self.dataLen * (self.sclPos + self.sclSize) / self.SCLLEN
        self.axRange = [l, r]
        self.axes.cla()
        self.axes.grid(True)
        self.axes.set_xlim(self.axRange)
        self.axes.set_ylim([0, 30])
        self.axes.plot(self.dates, self.icps, 'k')
        self.panel.draw()
        time.sleep(0.01)

    def OnClickSelectPt(self, evt):
        info = DBHelper.getAllPtNameId()
        choices = []
        for i in info:
            choices.append(str(i[0])+'('+str(i[1])+')')
        dlg = wx.SingleChoiceDialog(self.panel, '选择患者：', '患者总览', choices)
        if dlg.ShowModal() == wx.ID_OK:
            idx = dlg.GetSelection()
            self.tId.SetValue(str(info[idx][1]))
            self.OnClickId(None)

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
                self.cons = ptData.cons
                self.icpPaths = ptData.icpPath
                # print('print icp path:')
                # for i in self.icpPaths:
                #     print(i)
                if len(self.cons) == 0:
                    self.bFront.Disable()
                    self.bNext.Disable()
                    self.bToday.Disable()
                else:
                    self.bFront.Enable()
                    # self.bNext.Enable()
                    self.bToday.Enable()
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
        if symp == '' or diag == '':
            wx.MessageBox("就诊内容不能为空!")
        else:
            cons = Cons(datetime.date.today(), symp, diag)
            DBHelper.addPtCons(self.pId, cons)
            wx.MessageBox("保存成功！")

    # 滚动条响应
    def OnScroll(self, event):
        self.sclPos = self.scrollBar.GetThumbPosition()
        self.refresh()

    # +按钮响应
    def OnClickAdd(self, event):

        self.sclSize -= 100
        if self.sclSize < 100:
            self.sclSize = 50
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
        f = ICPFrame.ICPFrame(p_id=int(self.tId.GetValue()))
        f.Show()

    def OnClickModify(self, evt):
        frame = PntModFrame.PntModifyFrame(id=-1, title='颅内压数据管理系统', pos=(3600, 240), size=(850, 450),
                                           p_id=self.tId.GetValue())
        frame.Show()

    def OnClickModifyDoc(self, evt):
        pass

    def OnClickFront(self, evt):
        self.conIdx += 1
        if self.conIdx == len(self.cons) - 1:
            self.bFront.Disable()
            self.dates = []
            self.icps = []
            self.icts = []
            self.refresh()
        else:
            self.bNext.Enable()
        self.tDiag.SetValue(self.cons[self.conIdx].diag)
        self.tSymp.SetValue(self.cons[self.conIdx].sx)
        self.tDate.SetLabel(str(self.cons[self.conIdx].date.date()))
        self.bClear.Disable()
        self.bSave.Disable()

        self.icpIdx += 1
        if self.icpIdx < len(self.icpPaths):
            self.icpDatas = load(self.icpPaths[self.icpIdx])
            self.dates = []
            self.icps = []
            self.icts = []
            if self.icpDatas[0].date.date() == self.cons[self.conIdx].date.date():
                for i in self.icpDatas:
                    # self.dates.append(i.date)
                    self.icps.append(i.icp)
                    self.icts.append(i.ict)
                self.dates = list(range(0, len(self.icpDatas)))
                self.dataLen = len(self.icps)
                # print('-------')
            else:
                self.icpIdx -= 1
        else:
            if self.icpIdx > len(self.icpPaths):
                self.icpIdx = len(self.icpPaths)
        # print(self.icpIdx)

        self.refresh()


    def OnClickNext(self, evt):
        self.conIdx -= 1
        if self.conIdx == -1:
            self.bNext.Disable()
            self.tDiag.SetValue("")
            self.tSymp.SetValue("")
            self.tDate.SetLabel(str(datetime.date.today()))
            self.bClear.Enable()
            self.bSave.Enable()
            self.dates = []
            self.icps = []
            self.icts = []
            self.refresh()
        else:
            self.tDiag.SetLabel(self.cons[self.conIdx].diag)
            self.tSymp.SetLabel(self.cons[self.conIdx].sx)
            self.tDate.SetLabel(str(self.cons[self.conIdx].date.date()))
            self.bFront.Enable()
            self.bClear.Disable()
            self.bSave.Disable()

        self.icpIdx -= 1
        if self.icpIdx >= 0:
            self.icpDatas = load(self.icpPaths[self.icpIdx])
            self.dates = []
            self.icps = []
            self.icts = []
            if self.icpDatas[0].date.date() == self.cons[self.conIdx].date.date():
                for i in self.icpDatas:
                    # self.dates.append(i.date)
                    self.icps.append(i.icp)
                    self.icts.append(i.ict)
                self.dates = list(range(0, len(self.icpDatas)))
                self.dataLen = len(self.icps)
                # print('-------')
            else:
                self.icpIdx += 1
        else:
            self.dates = []
            self.icps = []
            self.icts = []
            if self.icpIdx < -1:
                self.icpIdx = -1
        # print(self.icpIdx)

        self.refresh()

    def OnClickToday(self, evt):
        self.conIdx = -1
        self.bNext.Disable()
        self.bFront.Enable()
        self.tDiag.SetValue("")
        self.tSymp.SetValue("")
        self.tDate.SetLabel(str(datetime.date.today()))
        self.bClear.Enable()
        self.bSave.Enable()
        self.icpIdx = -1
        self.dates = []
        self.icps = []
        self.icts = []
        self.refresh()


class MainApp(wx.App):
    def OnInit(self):
        style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        self.frame = MainFrame(id=-1)
        self.frame.Show()
        return True


def main():
    app = MainApp()
    app.MainLoop()


if __name__ == "__main__":
    main()

