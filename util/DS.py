class DatatimeFormat:
    def __init__(self, y, m, d, h, mi, s):
        self.year = y
        self.month = m
        self.day = d
        self.hour = h
        self.minute = mi
        self.second = s

    def toString(self):
        s = "%d-%02d-%02d %02d:%02d:%02d" % (self.year, self.month, self.day, self.hour, self.minute, self.second)
        return s


class Data:
    def __init__(self, data:DatatimeFormat, icp, ict):
        self.data:DatatimeFormat = data
        self.icp = icp
        self.ict = ict

    def toString(self):
        s = "data:" + self.data.toString() + " icp:" + str(self.icp) + " ict:" + str(self.ict)
        return s
