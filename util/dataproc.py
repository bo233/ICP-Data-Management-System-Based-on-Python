from util.DS import *
from util.COM import COMHelper
from util.COM import COMConst as COM
from struct import *
from threading import Thread
import queue


def read(path):
    dataList = []
    file = open(path,"rb")
    while True:
        line = file.read(16)
        if not line:
            break

        sNum = line[0:4]
        sYear = line[4:6]
        m = line[6]
        d = line[7]
        h = line[8]
        mi = line[9]
        s = line[10]
        icp = line[11] - 37
        sIct1 = line[12]
        sIct2 = line[13]

        y = int.from_bytes(sYear, byteorder="little", signed=False)
        ict = sIct1 / 10 + sIct2 / 10

        date = datetime.datetime(y, m, d, h, mi, s)
        data = Data(date, icp, ict)
        dataList.append(data)

    file.close()
    return dataList


class DataHelper:
    def __int__(self, com, bps=921600, timeout=5):
        self.com = COMHelper(com, bps, timeout)
        self.rtnQue = queue.Queue()
        self.devNo = 0

    def handle(self):
        cmd, data = self.com.receive()
        state = const.INVALID
        rtn = None

        if data is None:
            pass

        # 注册请求
        # AB CD 40 12 ID(12) SS SS EE FF
        # 接收数据：主机芯片ID(ID)
        # AB CD 80 13 NN(1) ID(12) SS SS EE FF
        # 发送数据：设备号(NN), 主机芯片ID(ID)
        elif cmd == COM.REC_RegReq:
            ID = data
            d = pack("B", self.devNo) + ID
            self.devNo += 1
            self.com.send(COM.SND_RegRsp, d)

        # 数据上报
        # AB CD 41 08 NN(1) No(4) ICP(1) ICT(2) SS SS EE FF
        # 接收数据：设备号(NN), 数据序号(No), ICP和ICT
        # AB CD 81 05 NN(1) No(4) SS SS EE FF
        # 发送数据：设备号(NN), 序号(No)
        elif cmd == COM.REC_DataSnd:
            nn, no, icp, ict = unpack("BIBH", data)
            d = pack("BI", nn, no)
            self.com.send(COM.SND_DataCnf, d)
            rtn = Data(DatatimeFormat(), icp / 10, ict - 50)
            state = const.DATA
            self.rtnQue.put((state, rtn))

        # 报警上报
        # AB CD 42 0F NN(1) No(1) Evt(1) OnOff(1) Time(8) SS SS EE FF
        # 发送数据：设备号(NN), 报警序号(No), 报警类型(Alarm), 出现/消失(OnOff), 绝对时间(Time)
        elif cmd == COM.REC_AlmSnd:
            pass

        # 电量上报
        # AB CD 43 02 NN(1) Bat(1) SS SS EE FF
        # 数据内容：设备号(NN), 电量等级(Bat)
        # AB CD 83 01 NN(1) SS SS EE FF
        # 数据内容：设备号(NN)
        elif cmd == COM.REC_BatSnd:
            nn, b = unpack("BB", data)
            bat = int.from_bytes(b, signed=False)
            state = const.BATTERY
            self.rtnQue.put((state, bat))

        # 清零上报
        elif cmd == COM.REC_ZeroSnd:
            pass
        # 可以同步数据
        elif cmd == COM.REC_Sync:
            pass
        # Ping回复
        elif cmd == COM.REC_PingRsq:
            pass
        # 时间同步
        elif cmd == COM.REC_TimeReq:
            now = DatatimeFormat()
            NN = data
            d = NN + now.encode()
            self.com.send(COM.SND_TimeRsp, d)

        # 关机上报
        # AB CD 49 04 NN(1) 4F 46 46 SS SS EE FF
        # 数据内容：设备号(NN), 关机标志("OFF")
        # AB CD 89 01 NN(1) SS SS EE FF
        # 数据内容：设备号(NN
        elif cmd == COM.REC_OffSnd:
            nn, _, _, _ = unpack("4B", data)
            d = pack("B", nn)
            self.com.send(d)
            state = const.OFF
            self.rtnQue.put((state, int.from_bytes(nn, signed=False)))

        # 历史报警上报
        elif cmd == COM.REC_HESnd:
            pass
        # 报警上报完成
        elif cmd == COM.REC_HEok:
            pass
        # 报警完成回复
        elif cmd == COM.REC_HERsp:
            pass
        # 历史数据上报
        elif cmd == COM.REC_HDSnd:
            pass
        # 数据上报完成
        elif cmd == COM.REC_HDok:
            pass
        # 数据完成回复
        elif cmd == COM.REC_HDRsp:
            pass
        # 历史清零上报
        elif cmd == COM.REC_HZSnd:
            pass
        # 历史清零上报完成
        elif cmd == COM.REC_HZok:
            pass
        # 历史清零完成回复
        elif cmd == COM.REC_HZRsp:
            pass

        # return state, rtn

    def getRtn(self):
        if self.rtnQue.empty():
            return None
        else:
            return self.rtnQue.get()


class const:
    INVALID = -1
    ERR = -2
    DATA = 1
    BATTERY = 2
    OFF = 3

if __name__ == "__main__":
    data = read("/Users/bo233/Projects/Graduation-Project/data/data.dat")
    print(data[0].toString())
