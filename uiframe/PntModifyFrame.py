# coding=utf-8

import wx
from database.dbUtil import DBHelper


class PntModifyFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='', pos=wx.DefaultSize, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER, p_id=-1):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.p_id = p_id
        self.InitUI()

    def InitUI(self):
        self.SetBackgroundColour('white')
        self.scorePanel = wx.Panel(self)
        self.Center(wx.BOTH)
        self.title = wx.StaticText(self, label="修改信息", pos=(400, 20))
        self.lName = wx.StaticText(self, label="*姓  名", pos=(80, 50))
        self.tName = wx.TextCtrl(self, size=(235, 25), pos=(150, 50), style=wx.TE_LEFT)
        self.tGend = wx.StaticText(self, label="*性  别", pos=(80, 90))
        self.rMale = wx.RadioButton(self, -1, "男", pos=(150, 90), style=wx.RB_GROUP)
        self.rFemale = wx.RadioButton(self, -1, "女", pos=(200, 90))
        # self.lPwd = wx.StaticText(self, label="*密  码", pos=(80, 130))
        # self.tPwd = wx.TextCtrl(self, size=(235, 25), pos=(150, 130), style=wx.TE_PASSWORD)
        # self.lPwd2 = wx.StaticText(self, label="*确认密码", pos=(80, 170))
        # self.tPwd2 = wx.TextCtrl(self, size=(235, 25), pos=(150, 170), style=wx.TE_PASSWORD)
        self.lHeight = wx.StaticText(self, label="*身高(cm)", pos=(80, 130))
        self.tHeight = wx.TextCtrl(self, size=(235, 25), pos=(150, 130), style=wx.TE_LEFT)
        self.lWeight = wx.StaticText(self, label="*体重(kg)", pos=(80, 170))
        self.tWeight = wx.TextCtrl(self, size=(235, 25), pos=(150, 170), style=wx.TE_LEFT)
        self.lAge = wx.StaticText(self, label='*年  龄', pos=(80, 210))
        self.tAge = wx.TextCtrl(self, size=(235, 25), pos=(150, 210), style=wx.TE_LEFT)
        self.lTel = wx.StaticText(self, label="*电  话", pos=(80, 250))
        self.tTel = wx.TextCtrl(self, size=(235, 25), pos=(150, 250), style=wx.TE_LEFT)

        self.tBloodType = wx.StaticText(self, label='*血  型', pos=(80,290))
        self.rBTA = wx.RadioButton(self, -1, "A型", pos=(150, 290), style=wx.RB_GROUP)
        self.rBTB = wx.RadioButton(self, -1, 'B型', pos=(210, 290))
        self.rBTAB = wx.RadioButton(self, -1, 'AB型', pos=(270, 290))
        self.rBTO = wx.RadioButton(self, -1, "O型", pos=(330, 290))
        self.lAllergy = wx.StaticText(self, label='过敏史', pos=(460, 50))
        self.tAllergy = wx.TextCtrl(self, size=(235, 70), pos=(530, 50), style=wx.TE_MULTILINE)
        self.lFaHis = wx.StaticText(self, label='家族病史', pos=(460, 140))
        self.tFaHis = wx.TextCtrl(self, size=(235, 70), pos=(530, 140), style=wx.TE_MULTILINE)
        self.lMediHis = wx.StaticText(self, label='过往病史', pos=(460, 230))
        self.tMediHis = wx.TextCtrl(self, size=(235, 70), pos=(530, 230), style=wx.TE_MULTILINE)

        self.bOK = wx.Button(self, label="确  认", pos=(280, 360))
        self.bCancel = wx.Button(self, label="取  消", pos=(520, 360))
        self.bCancel.Bind(wx.EVT_BUTTON, self.OnClickCancel)
        self.bOK.Bind(wx.EVT_BUTTON, self.OnClickOK)

        data = DBHelper.getPtInfo(self.p_id)
        self.tName.SetValue(data.name)
        self.tAge.SetValue(str(data.age))
        self.tHeight.SetValue(str(data.height))
        self.tWeight.SetValue(str(data.weight))
        self.tMediHis.SetValue(data.medical_history)
        self.tFaHis.SetValue(data.family_history)
        self.tAllergy.SetValue(data.allergy)
        self.tTel.SetValue(data.tel)
        if data.blood_type == 'A':
            self.rBTA.SetValue(True)
        elif data.blood_type == 'B':
            self.rBTB.SetValue(True)
        elif data.blood_type == 'AB':
            self.rBTAB.SetValue(True)
        elif data.blood_type == 'O':
            self.rBTO.SetValue(True)
        if data.gender == '男':
            self.rMale.SetValue(True)
        elif data.gender == '女':
            self.rFemale.SetValue(True)

    def OnClickCancel(self, event):
        self.Close(True)

    def OnClickOK(self, event):
        name = self.tName.GetValue()
        tel = self.tTel.GetValue()
        age = self.tAge.GetValue()
        allergy = self.tAllergy.GetValue()
        height = self.tHeight.GetValue()
        weight = self.tWeight.GetValue()
        family_his = self.tFaHis.GetValue()
        medi_his = self.tMediHis.GetValue()
        gen = ""
        if self.rMale.GetValue(): gen = '男'
        if self.rFemale.GetValue(): gen = '女'
        bld_type = ''
        if self.rBTA.GetValue(): bld_type = 'A'
        if self.rBTB.GetValue(): bld_type = 'B'
        if self.rBTAB.GetValue(): bld_type = 'AB'
        if self.rBTO.GetValue(): bld_type = 'O'


        if name == "" or tel == "" or age == '' or height == '' or weight == '' \
                or gen == '' or bld_type == '':
            wx.MessageBox("信息不能为空！")
        else:
            rs = DBHelper.modifyPtInfo(str(self.p_id),name,age,gen,allergy,family_his,
                                  height,weight,bld_type,tel,medi_his)
            if rs:
                wx.MessageBox("修改成功！")
                self.Close(True)
            else:
                wx.MessageBox("修改失败，请重试。")


class PntModifyFrameApp(wx.App):
    def OnInit(self):
        self.frame = PntModifyFrame(id=-1, title='颅内压数据管理系统', pos=(3600, 240), size=(850, 450))
        self.frame.Show()
        return True


def main():
    app = PntModifyFrameApp()
    app.MainLoop()


if __name__ == "__main__":
    main()
