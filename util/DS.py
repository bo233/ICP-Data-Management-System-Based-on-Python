import datetime
import struct


class DatatimeFormat:
    def __init__(self):
        now = datetime.datetime.now()
        self.set(now.year, now.month, now.day, now.hour, now.minute, now.second)

    def set(self, y, m, d, h, mi, s):
        self.year = y
        self.month = m
        self.day = d
        self.hour = h
        self.minute = mi
        self.second = s


    def toString(self):
        s = "%d-%02d-%02d %02d:%02d:%02d" % (self.year, self.month, self.day, self.hour, self.minute, self.second)
        return s

    def __str__(self):
        s = "%d-%02d-%02d %02d:%02d:%02d" % (self.year, self.month, self.day, self.hour, self.minute, self.second)
        return s

    def encode(self):
        s = struct.pack("=H5B", self.year, self.month, self.day, self.hour, self.minute, self.second)
        return s

    def toDatetime(self):
        d = datetime.datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)
        return d


class Data:
    def __init__(self, date:datetime, icp, ict):
        self.date:datetime = date
        self.icp = icp
        self.ict = ict

    def toString(self):
        s = "data:" + str(self.date) + " icp:" + str(self.icp) + " ict:" + str(self.ict)
        return s

    def __str__(self):
        s = "data:" + str(self.date) + " icp:" + str(self.icp) + " ict:" + str(self.ict)
        return s


class Cons:
    def __init__(self, date:datetime, symptom="", diagnosis=""):
        self.sx = symptom
        self.diag = diagnosis
        self.date = date


class PtData:
    # name, age, gender, pwd, allergy, family_history,
    #                    height, weight, blood_type, tel, medical_history
    def __init__(self, id:int, name:str, age:int, gender:str, height:float, weight:float, blood_type:str, tel:str,
                 medical_history='', allergy='', family_history='', consultations=None, icpPath=None):
        if icpPath is None:
            icpPath = []
        if consultations is None:
            consultations = []
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.cons:list[Cons] = consultations
        self.icpPath:list[str] = icpPath
        self.allergy = allergy
        self.family_history = family_history
        self.height = height
        self.weight = weight
        self.blood_type = blood_type
        self.tel = tel
        self.medical_history = medical_history

