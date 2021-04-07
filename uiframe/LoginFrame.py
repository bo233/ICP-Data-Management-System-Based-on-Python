# coding=utf-8

import wx
from uiframe.MainFrame import MainApp
from database.dbUtil import DBHelper


class LoginFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='', pos=wx.DefaultSize, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.InitUI()
        pass

    def InitUI(self):
        self.SetBackgroundColour('white')
        self.scorePanel = wx.Panel(self)
        self.Center(wx.BOTH)
        self.title = wx.StaticText(self, label="输入用户名和密码", pos=(140, 20))
        self.lUser = wx.StaticText(self, label="用户名", pos=(50, 50))
        self.tUser = wx.TextCtrl(self, size=(235, 25), pos=(100, 50), style=wx.TE_LEFT)
        self.lPwd = wx.StaticText(self, label="密  码", pos=(50, 90))
        self.tPwd = wx.TextCtrl(self, size=(235, 25), pos=(100, 90), style=wx.TE_PASSWORD)
        self.bLogin = wx.Button(self, label="登陆", pos=(100, 130))
        self.bReg = wx.Button(self, label="注册", pos=(200, 130))
        self.bReg.Bind(wx.EVT_BUTTON, self.OnClickReg)
        self.bLogin.Bind(wx.EVT_BUTTON, self.OnClickLogin)

    def OnClickReg(self, event):
        dlg = wx.MessageDialog(None, "开发中，敬请期待。", "信息", wx.OK | wx.ICON_INFORMATION)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Close(True)
        dlg.Destroy()

    # 登陆
    def OnClickLogin(self, event):
        msg = ""
        flag = 0
        name = self.tUser.GetValue()
        pwd = self.tPwd.GetValue()

        if name == "" or pwd == "":
            wx.MessageBox("用户名或密码不能为空！")
        elif DBHelper.loginCheck(name, pwd):
                wx.MessageBox("登陆成功！")
                self.Close(True)
                app = MainApp()
                app.MainLoop()
        else:
            wx.MessageBox("用户名或密码错误！")


class LoginApp(wx.App):
    def OnInit(self):
        self.frame = LoginFrame(id=-1, title='颅内压数据管理系统', pos=(3600, 240), size=(500, 300))
        self.frame.Show()
        return True


def main():
    app = LoginApp()
    app.MainLoop()


if __name__ == "__main__":
    main()
