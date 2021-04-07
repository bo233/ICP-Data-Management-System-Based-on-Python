# coding=utf-8

import wx
import hashlib
from uiframe.MainFrame import MainApp
import uiframe.LoginFrame as LoginFrame
from database.dbUtil import DBHelper


class RegisFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='', pos=wx.DefaultSize, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.InitUI()
        pass

    def InitUI(self):
        self.SetBackgroundColour('white')
        self.scorePanel = wx.Panel(self)
        self.Center(wx.BOTH)
        self.title = wx.StaticText(self, label="注  册", pos=(220, 20))
        self.lName = wx.StaticText(self, label="姓  名", pos=(80, 50))
        self.tName = wx.TextCtrl(self, size=(235, 25), pos=(150, 50), style=wx.TE_LEFT)
        self.lUser = wx.StaticText(self, label="用户名", pos=(80, 90))
        self.tUser = wx.TextCtrl(self, size=(235, 25), pos=(150, 90), style=wx.TE_LEFT)
        self.lPwd = wx.StaticText(self, label="密  码", pos=(80, 130))
        self.tPwd = wx.TextCtrl(self, size=(235, 25), pos=(150, 130), style=wx.TE_PASSWORD)
        self.lPwd2 = wx.StaticText(self, label="确认密码", pos=(80, 170))
        self.tPwd2 = wx.TextCtrl(self, size=(235, 25), pos=(150, 170), style=wx.TE_PASSWORD)
        self.lTel = wx.StaticText(self, label="电  话", pos=(80, 210))
        self.tTel = wx.TextCtrl(self, size=(235, 25), pos=(150, 210), style=wx.TE_LEFT)

        self.bReg = wx.Button(self, label="注册", pos=(140, 270))
        self.bCancel = wx.Button(self, label="取消", pos=(280, 270))
        self.bCancel.Bind(wx.EVT_BUTTON, self.OnClickCancel)
        self.bReg.Bind(wx.EVT_BUTTON, self.OnClickReg)

    def OnClickCancel(self, event):
        self.Close(True)
        LoginFrame.main()

    # 登陆
    def OnClickReg(self, event):
        name = self.tName.GetValue()
        id = self.tUser.GetValue()
        pwd = self.tPwd.GetValue()
        pwd2 = self.tPwd2.GetValue()
        tel = self.tTel.GetValue()
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        encode = str(md5.hexdigest())

        if name == "" or pwd == "" or id == "" or tel == "":
            wx.MessageBox("信息不能为空！")
        elif pwd != pwd2:
            wx.MessageBox("两次密码不一致！")
        elif DBHelper.docIdExist(id):
            wx.MessageBox("用户名已存在！")
        elif DBHelper.docRegister(id, name, tel, encode):
            wx.MessageBox("注册成功！")
            self.Close(True)
            LoginFrame.main()
        else:
            wx.MessageBox("注册失败，请重试。")


class RegisApp(wx.App):
    def OnInit(self):
        self.frame = RegisFrame(id=-1, title='颅内压数据管理系统', pos=(3600, 240), size=(500, 350))
        self.frame.Show()
        return True


def main():
    app = RegisApp()
    app.MainLoop()


if __name__ == "__main__":
    main()
