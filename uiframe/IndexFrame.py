# coding=utf-8

import wx

from uiframe import DocLoginFrame, PntLoginFrame


class IndexFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='', pos=wx.DefaultSize, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.InitUI()
        pass

    def InitUI(self):
        self.SetBackgroundColour('white')
        self.scorePanel = wx.Panel(self)
        self.Center(wx.BOTH)
        self.title = wx.StaticText(self, label="欢迎使用颅内压管理系统", pos=(110, 30))
        self.title.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.bDoc = wx.Button(self, label="我是医生", pos=(130, 130))
        self.bPnt = wx.Button(self, label="我是患者", pos=(260, 130))
        self.bPnt.Bind(wx.EVT_BUTTON, self.OnClickPnt)
        self.bDoc.Bind(wx.EVT_BUTTON, self.OnClickDoc)

    def OnClickPnt(self, event):
        self.Close(True)
        PntLoginFrame.main()

    def OnClickDoc(self, event):
        self.Close(True)
        DocLoginFrame.main()


class IndexFrameApp(wx.App):
    def OnInit(self):
        self.frame = IndexFrame(id=-1, title='颅内压数据管理系统', pos=(3600, 240), size=(500, 300))
        self.frame.Show()
        return True


def main():
    app = IndexFrameApp()
    app.MainLoop()


if __name__ == "__main__":
    main()
