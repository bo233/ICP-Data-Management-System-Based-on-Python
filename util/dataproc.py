from util.DS import *
from util.COM import COMHelper
from util.COM import COMConst as COM
from struct import *
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
    def __init__(self, com='/dev/cu.usbserial-14310', bps=115200, timeout=5):
        self.com = COMHelper(com, bps, timeout)
        self.rtnQue = queue.Queue()
        self.devNo = 0

    def handle(self):
        cmd, data = self.com.receive()

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
            # print('data:',d)
            self.devNo += 1
            self.com.send(COM.SND_RegRsp, d)

        # 数据上报
        # AB CD 41 08 NN(1) No(4) ICP(1) ICT(2) SS SS EE FF
        # 接收数据：设备号(NN), 数据序号(No), ICP和ICT
        # AB CD 81 05 NN(1) No(4) SS SS EE FF
        # 发送数据：设备号(NN), 序号(No)
        elif cmd == COM.REC_DataSnd:
            # print('len:', len(data))
            # nn, no, icp, ict = unpack("BIBH", data)
            nn = data[0]
            no = int.from_bytes(data[1:5], byteorder="little", signed=False)
            icp = data[5]
            ict = int.from_bytes(data[6:8], byteorder="little", signed=False)
            d = pack("BI", nn, no)
            self.com.send(COM.SND_DataCnf, d)
            rtn = Data(datetime.datetime.now(), icp - 50, ict / 10)
            state = const.DATA
            self.rtnQue.put((state, rtn))

        # 报警上报
        # AB CD 42 0F NN(1) No(1) Evt(1) OnOff(1) Time(8) SS SS EE FF
        # 发送数据：设备号(NN), 报警序号(No), 报警类型(Alarm), 出现/消失(OnOff), 绝对时间(Time)
        # AB CD 82 05 NN(1) No(4) SS SS EE FF
        # 数据内容：设备号(NN), 序号(No)
        elif cmd == COM.REC_AlmSnd:
            nn, no, evt, onoff, time = unpack('BBBBQ')
            d = pack('BB', nn, no)
            self.com.send(COM.SND_AlmCnf, d)

        # 电量上报
        # AB CD 43 02 NN(1) Bat(1) SS SS EE FF
        # 数据内容：设备号(NN), 电量等级(Bat)
        # AB CD 83 01 NN(1) SS SS EE FF
        # 数据内容：设备号(NN)
        elif cmd == COM.REC_BatSnd:
            nn, b = unpack("BB", data)
            # bat = int.from_bytes(b, signed=False, byteorder='little')
            state = const.BATTERY
            self.rtnQue.put((state, b))

        # 清零上报
        # AB CD 44 18 NN(1) No(1) MODE(1) ID(5) AI(4) DI(4) TIME(8) SS SS EE FF
        #  数据内容：设备号(NN), 清零序号(No), 清零方式(MODE), 探头ID(ID), 报警序号(AI), 数据序号(DI), 绝对时间(TIME)
        # AB CD 84 01 NN(1) SS SS EE FF
        # 数据内容：设备号(NN)
        elif cmd == COM.REC_ZeroSnd:
            nn, no, mode, id, id_, ai, di, time = unpack('BBBIBLLQ', data)
            d = pack('B', nn)
            self.com.send(COM.SND_ZeroReq, d)

        # 可以同步数据
        # AB CD 46 11 NN(1) AI(4) DI(4) ZI(1) TIME(8) SS SS EE FF
        # 数据内容：设备号(NN), 报警序号(AI), 数据序号(DI), 清零序号(ZI), 绝对时间(TIME)
        elif cmd == COM.REC_Sync:
            pass

        # Ping回复
        # AB CD 47 01 NN(1) SS SS EE FF
        # 数据内容：设备号(NN)
        elif cmd == COM.REC_PingRsq:
            pass

        # 时间同步
        # AB CD 48 01 NN(1) SS SS EE FF
        # 数据内容：设备号(NN)
        # AB CD 88 08 NN(1) Y(2) MON(1) D(1) H(1) MIN(1) SEC(1) SS SS EE FF
        # 数据内容：年(Y) 月(MON) 日(D) 时(H) 分(MIN) 秒(SEC)
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
            self.com.send(COM.SND_OffRsp, d)
            state = const.OFF
            self.rtnQue.put((state, nn))

        # 历史报警上报
        # AB CD 50 0F NN(1) No(1) Evt(1) OnOff(1) Time(8) SS SS EE FF
        # 数据内容：设备号(NN), 报警序号(No), 报警类型(Alarm), 出现/消失(OnOff), 绝对时间(Time)
        # AB CD 90 09 NN(1) No(4) No(4) SS SS EE FF
        # 数据内容：设备号(NN), 起始序号(No), 结束序号(No)
        elif cmd == COM.REC_HESnd:
            pass

        # 报警上报完成
        # AB CD 53 0A NN(1) No(4) No(4) 4F 4B SS SS EE FF
        # 数据内容：设备号(NN), 起始序号(No), 结束序号(No), 完成标志("OK")
        elif cmd == COM.REC_HEok:
            pass

        # 报警完成回复
        # AB CD 55 05 NN(1) 44 4F 4E 45 SS SS EE FF
        # 数据内容：设备号(NN), 完成标志("DONE")
        elif cmd == COM.REC_HERsp:
            pass

        # 历史数据上报
        # AB CD 53 ??(3n+6) NN(1) No(4) Inc(1) Data(3n) SS SS EE FF
        # 数据内容：设备号(1), 序号(4), 增量(1), 数据集(Data)
        elif cmd == COM.REC_HDSnd:
            pass

        # 数据上报完成
        # AB CD 53 0A NN(1) No(4) No(4) 4F 4B SS SS EE FF
        # 数据内容：设备号(NN), 起始序号(No), 结束序号(No), 完成标志("OK")
        elif cmd == COM.REC_HDok:
            pass

        # 数据完成回复
        #  AB CD 55 05 NN(1) 44 4F 4E 45 SS SS EE FF
        # 数据内容：设备号(NN), 完成标志("DONE")
        elif cmd == COM.REC_HDRsp:
            pass

        # 历史清零上报
        # AB CD 56 18 NN(1) No(1) MODE(1) ID(5) AI(4) DI(4) TIME(8) SS SS EE FF
        #  数据内容：设备号(NN), 清零序号(No), 清零方式(MODE), 探头ID(ID), 报警序号(AI), 数据序号(DI), 绝对时间(TIME)
        elif cmd == COM.REC_HZSnd:
            pass

        # 历史清零上报完成
        # AB CD 57 0B NN(1) No(4) No(4) 4F 4B SS SS EE FF
        # 数据内容：设备号(NN), 起始序号(No), 结束序号(No), 完成标志("OK")
        elif cmd == COM.REC_HZok:
            pass

        # 历史清零完成回复
        # AB CD 58 05 NN(1) 44 4F 4E 45 SS SS EE FF
        # 数据内容：设备号(NN), 完成标志("DONE")
        elif cmd == COM.REC_HZRsp:
            pass

        # return state, rtn

    def getRtn(self):
        if self.rtnQue.empty():
            return const.INVALID, None
        else:
            return self.rtnQue.get()


class const:
    INVALID = -1
    ERR = -2
    DATA = 1
    BATTERY = 2
    OFF = 3

if __name__ == "__main__":
    # data = read("/Users/bo233/Projects/Graduation-Project/data/data.dat")
    # print(data[0].toString())
    dHelper = DataHelper()
    # cmd, data = dHelper.com.receive()
    # print(cmd, data)
    while True:
        dHelper.handle()
        state, rtn = dHelper.getRtn()
        print("state: ",state, " return: ",rtn)