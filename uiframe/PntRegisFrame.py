# coding=utf-8

import wx
import hashlib
from uiframe import PntLoginFrame
from database.dbUtil import DBHelper


class PntRegisFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='颅内压数据管理系统', pos=(3600, 240), size=(850, 450),
                 style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.InitUI()
        pass

    def InitUI(self):
        self.SetBackgroundColour('white')
        self.scorePanel = wx.Panel(self)
        self.Center(wx.BOTH)
        self.title = wx.StaticText(self, label="注  册", pos=(220, 20))
        self.lName = wx.StaticText(self, label="*姓  名", pos=(80, 50))
        self.tName = wx.TextCtrl(self, size=(235, 25), pos=(150, 50), style=wx.TE_LEFT)
        self.tGend = wx.StaticText(self, label="*性  别", pos=(80, 90))
        self.rMale = wx.RadioButton(self, -1, "男", pos=(150, 90), style=wx.RB_GROUP)
        self.rFemale = wx.RadioButton(self, -1, "女", pos=(200, 90))
        self.lPwd = wx.StaticText(self, label="*密  码", pos=(80, 130))
        self.tPwd = wx.TextCtrl(self, size=(235, 25), pos=(150, 130), style=wx.TE_PASSWORD)
        self.lPwd2 = wx.StaticText(self, label="*确认密码", pos=(80, 170))
        self.tPwd2 = wx.TextCtrl(self, size=(235, 25), pos=(150, 170), style=wx.TE_PASSWORD)
        self.lHeight = wx.StaticText(self, label="*身高(cm)", pos=(80, 210))
        self.tHeight = wx.TextCtrl(self, size=(70, 25), pos=(150, 210), style=wx.TE_LEFT)
        self.lWeight = wx.StaticText(self, label="*体重(kg)", pos=(240, 210))
        self.tWeight = wx.TextCtrl(self, size=(70, 25), pos=(310, 210), style=wx.TE_LEFT)
        self.lAge = wx.StaticText(self, label='*年  龄', pos=(80, 250))
        self.tAge = wx.TextCtrl(self, size=(235, 25), pos=(150, 250), style=wx.TE_LEFT)
        self.lTel = wx.StaticText(self, label="*电  话", pos=(80, 290))
        self.tTel = wx.TextCtrl(self, size=(235, 25), pos=(150, 290), style=wx.TE_LEFT)

        self.tBloodType = wx.StaticText(self, label='*血  型', pos=(460,50))
        self.rBTA = wx.RadioButton(self, -1, "A型", pos=(530, 50), style=wx.RB_GROUP)
        self.rBTB = wx.RadioButton(self, -1, 'B型', pos=(600, 50))
        self.rBTAB = wx.RadioButton(self, -1, 'AB型', pos=(670, 50))
        self.rBTO = wx.RadioButton(self, -1, "O型", pos=(740, 50))
        self.lAllergy = wx.StaticText(self, label='过敏史', pos=(460, 90))
        self.tAllergy = wx.TextCtrl(self, size=(235, 60), pos=(530, 90), style=wx.TE_MULTILINE)
        self.lFaHis = wx.StaticText(self, label='家族病史', pos=(460, 170))
        self.tFaHis = wx.TextCtrl(self, size=(235, 60), pos=(530, 170), style=wx.TE_MULTILINE)
        self.lMediHis = wx.StaticText(self, label='过往病史', pos=(460, 250))
        self.tMediHis = wx.TextCtrl(self, size=(235, 60), pos=(530, 250), style=wx.TE_MULTILINE)


        self.bReg = wx.Button(self, label="注  册", pos=(280, 360))
        self.bCancel = wx.Button(self, label="取  消", pos=(520, 360))
        self.bCancel.Bind(wx.EVT_BUTTON, self.OnClickCancel)
        self.bReg.Bind(wx.EVT_BUTTON, self.OnClickReg)

    def OnClickCancel(self, event):
        self.Close(True)
        f = PntLoginFrame.PntLoginFrame()
        f.Show()


    # 登陆
    def OnClickReg(self, event):
        name = self.tName.GetValue()
        pwd = self.tPwd.GetValue()
        pwd2 = self.tPwd2.GetValue()
        tel = self.tTel.GetValue()
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        encode = str(md5.hexdigest())
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


        if name == "" or pwd == "" or tel == "" or age == '' or height == '' or weight == '' \
                or gen == '' or bld_type == '':
            wx.MessageBox("信息不能为空！")
        elif pwd != pwd2:
            wx.MessageBox("两次密码不一致！")
        else:
            id = DBHelper.ptRegister(name, age, gen, encode, allergy, family_his,
                               height, weight, bld_type, tel, medi_his)
            if id is not None:
                wx.MessageBox("注册成功！您的ID为：%d"%(id))
                self.Close(True)
                f = PntLoginFrame.PntLoginFrame()
                f.Show()
            else:
                wx.MessageBox("注册失败，请重试。")


class PntRegisApp(wx.App):
    def OnInit(self):
        self.frame = PntRegisFrame()
        self.frame.Show()
        return True


def main():
    app = PntRegisApp()
    app.MainLoop()


if __name__ == "__main__":
    main()
