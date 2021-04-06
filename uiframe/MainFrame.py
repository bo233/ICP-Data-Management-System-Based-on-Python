# coding=utf-8
"""
程序的主入口
"""
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
        self.scorePanel = wx.Panel(self)
        self.Center(wx.BOTH)
        # scores = [89, 98, 70, 80, 60, 78, 85, 90]
        # sum = 0
        # for s in scores:
        #     sum += s
        # average = sum / len(scores)

        data = read("/Users/bo233/Projects/Graduation-Project/data/data.dat")

        scores = []
        for i in data:
            scores.append(i.icp)

        t_score = numpy.arange(1, len(scores) + 1, 1)
        s_score = numpy.array(scores)

        self.figure_score = Figure()
        self.figure_score.set_figheight(5)
        self.figure_score.set_figwidth(10)
        self.axes_score = self.figure_score.add_subplot(111)

        self.axes_score.plot(t_score, s_score, 'ro', t_score, s_score, 'k')
        # self.axes_score.axhline(y=average, color='r')
        # self.axes_score.set_title(u'My Scores')
        self.axes_score.grid(True)
        self.axes_score.set_xlabel(u'Data')
        self.axes_score.set_ylabel(u'ICP')
        FigureCanvas(self.scorePanel, -1, self.figure_score)
        pass


class MainApp(wx.App):
    def OnInit(self):
        style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        self.frame = MainFrame(id=-1, title=u'颅内压数据管理系统', pos=(3600, 240), size=(1000, 600), style=style)
        self.frame.Show()
        return True


def main():
    app = MainApp()
    app.MainLoop()


if __name__ == "__main__":
    main()

