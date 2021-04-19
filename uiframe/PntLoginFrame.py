# coding=utf-8

import wx
import hashlib
from uiframe.MainFrame import MainApp
from uiframe import PntRegisFrame
from database.dbUtil import DBHelper


class PntLoginFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='', pos=wx.DefaultSize, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.InitUI()
        pass

    def InitUI(self):
        self.SetBackgroundColour('white')
        self.scorePanel = wx.Panel(self)
        self.Center(wx.BOTH)
        self.title = wx.StaticText(self, label="患者您好，请输入ID和密码", pos=(130, 20))
        self.title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.lUser = wx.StaticText(self, label="      ID", pos=(70, 70))
        self.tUser = wx.TextCtrl(self, size=(235, 25), pos=(120, 70), style=wx.TE_LEFT)

        self.lPwd = wx.StaticText(self, label="密  码", pos=(70, 110))
        self.tPwd = wx.TextCtrl(self, size=(235, 25), pos=(120,110), style=wx.TE_PASSWORD)

        self.bLogin = wx.Button(self, label="登  陆", pos=(125, 170))
        self.bReg = wx.Button(self, label="注  册", pos=(225, 170))
        self.bReg.Bind(wx.EVT_BUTTON, self.OnClickReg)
        self.bLogin.Bind(wx.EVT_BUTTON, self.OnClickLogin)

    # 注册
    def OnClickReg(self, event):
        self.Close(True)
        PntRegisFrame.main()

    # 登陆
    def OnClickLogin(self, event):
        name = self.tUser.GetValue()
        pwd = self.tPwd.GetValue()
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        encode = str(md5.hexdigest())

        if name == "" or pwd == "":
            wx.MessageBox("用户名或密码不能为空！")
        elif DBHelper.ptLoginCheck(name, encode):
                wx.MessageBox("登陆成功！")
                self.Close(True)
                app = MainApp()
                app.MainLoop()
        else:
            wx.MessageBox("用户名或密码错误！")


class PntLoginApp(wx.App):
    def OnInit(self):
        self.frame = PntLoginFrame(id=-1, title='颅内压数据管理系统', pos=(3600, 240), size=(500, 300))
        self.frame.Show()
        return True


def main():
    app = PntLoginApp()
    app.MainLoop()


if __name__ == "__main__":
    main()
