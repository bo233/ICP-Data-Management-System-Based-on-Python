# coding=utf-8

from uiframe.LoginFrame import LoginApp
from database.dbUtil import DBHelper


# DBHelper.init()
app = LoginApp()
app.MainLoop()
