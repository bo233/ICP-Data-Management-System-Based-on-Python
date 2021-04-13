import serial
from struct import *


class COMConst:
    # 接收的常量
    REC_RegReq = 0 | 0x40  # 注册请求
    REC_DataSnd = 1 | 0x40  # 数据上报
    REC_AlmSnd = 2 | 0x40  # 报警上报
    REC_BatSnd = 3 | 0x40  # 电量上报
    REC_ZeroSnd = 4 | 0x40  # 清零上报
    REC_Sync = 6 | 0x40  # 可以同步数据
    REC_PingRsq = 7 | 0x40  # Ping回复
    REC_TimeReq = 8 | 0x40  # 时间同步
    REC_OffSnd = 9 | 0x40  # 关机上报
    REC_HESnd = 10 | 0x40  # 历史报警上报
    REC_HEok = 11 | 0x40  # 报警上报完成
    REC_HERsp = 12 | 0x40  # 报警完成回复
    REC_HDSnd = 13 | 0x40  # 历史数据上报
    REC_HDok = 14 | 0x40  # 数据上报完成
    REC_HDRsp = 15 | 0x40  # 数据完成回复
    REC_HZSnd = 16 | 0x40  # 历史清零上报
    REC_HZok = 17 | 0x40  # 历史清零上报完成
    REC_HZRsp = 18 | 0x40  # 历史清零完成回复

    # 发送的常量
    SND_RegRsp = 0 | 0x80  # 注册确认
    SND_DataCnf = 1 | 0x80  # 数据确认
    SND_AlmCnf = 2 | 0x80  # 报警确认
    SND_BatCnf = 3 | 0x80  # 电量确认
    SND_ZeroCnf = 4 | 0x80  # 清零确认
    SND_ZeroReq = 5 | 0x80  # 请求清零数据
    SND_PingReq = 7 | 0x80  # Ping查询
    SND_TimeRsp = 8 | 0x80  # 时间同步回复
    SND_OffRsp = 9 | 0x80  # 关机回复
    SND_HEReq = 10 | 0x80  # 历史报警查询
    SND_HEdone = 12 | 0x80  # 历史报警完成
    SND_HDReq = 13 | 0x80  # 历史数据查询
    SND_HDdone = 15 | 0x80  # 历史数据完成
    SND_HZReq = 16 | 0x80  # 历史清零查询
    SND_HZdone = 18 | 0x80  # 历史清零完成


class COMHelper:
    # 初始化
    def __init__(self, com, bps, timeout):
        self.port = com
        self.bps = bps
        self.timeout = timeout

        global Ret
        try:
            # 打开串口，并得到串口对象
            self.ser = serial.Serial(self.port, self.bps, timeout=self.timeout)
            # 判断是否打开成功
            if (self.ser.is_open):
                Ret = True
        except Exception as e:
            print("---异常---：", e)

    # 打印设备基本信息
    def printDevInfo(self):
        print(self.ser.name)  # 设备名字
        print(self.ser.port)  # 读或者写端口
        print(self.ser.baudrate)  # 波特率
        print(self.ser.bytesize)  # 字节大小
        print(self.ser.parity)  # 校验位
        print(self.ser.stopbits)  # 停止位
        print(self.ser.timeout)  # 读超时设置
        print(self.ser.writeTimeout)  # 写超时
        print(self.ser.xonxoff)  # 软件流控
        print(self.ser.rtscts)  # 软件流控
        print(self.ser.dsrdtr)  # 硬件流控
        print(self.ser.interCharTimeout)  # 字符间隔超时

    # 打开串口
    def open(self):
        self.ser.open()

    # 关闭串口
    def close(self):
        self.ser.close()
        print(self.ser.is_open)  # 检验串口是否打开

    # 打印可用串口列表
    @staticmethod
    def printPorts():
        port_list = list(serial.tools.list_ports.comports())
        print(port_list)

    # 接收指定大小的数据
    # 从串口读size个字节。如果指定超时，则可能在超时后返回较少的字节；如果没有指定超时，则会一直等到收完指定的字节数。
    def read(self, size=1):
        return self.ser.read(size=size)

    # 接收一行数据
    # 使用readline()时应该注意：打开串口时应该指定超时，否则如果串口没有收到新行，则会一直等待。
    # 如果没有超时，readline会报异常。
    def readline(self):
       return self.ser.readline()

    # 发数据
    def write(self, data):
        self.ser.write(data)

    # 更多示例
    # self.main_engine.write(chr(0x06).encode("utf-8"))  # 十六制发送一个数据
    # print(self.main_engine.read().hex())  #  # 十六进制的读取读一个字节
    # print(self.main_engine.read())#读一个字节
    # print(self.main_engine.read(10).decode("gbk"))#读十个字节
    # print(self.main_engine.readline().decode("gbk"))#读一行
    # print(self.main_engine.readlines())#读取多行，返回列表，必须匹配超时（timeout)使用
    # print(self.main_engine.in_waiting)#获取输入缓冲区的剩余字节数
    # print(self.main_engine.out_waiting)#获取输出缓冲区的字节数
    # print(self.main_engine.readall())#读取全部字符。

    # 接收一条完整的数据，返回命令字类型和数据内容
    def receive(self):
        cmd = -1
        data = None
        dataSize = 0
        checkSum = 0
        flag = 0  # 0：等待包头，1：命令字，2：数据长度，3：数据内容，4：校验和，5：包尾
        flag1 = 0
        # 循环接收数据，此为死循环，可用线程实现
        # print("开始接收数据：")
        while True:
            try:
                # 接收
                if self.ser.in_waiting:
                    # 判断包头
                    if flag == 0:
                        readbuf = self.read()
                        read = int(readbuf.hex(), 16)
                        if read == 0xab:
                            flag1 = 1
                        if flag1 == 1:
                            if read == 0xcd:
                                flag += 1
                            flag1 = 0
                    elif flag == 1:
                        readbuf = self.read()
                        cmd = int(readbuf.hex(), 16)
                        checkSum += cmd
                        cmd |= 0x40
                        flag += 1
                    elif flag == 2:
                        readbuf = self.read()
                        dataSize = int(readbuf.hex(), 16)
                        checkSum += dataSize
                        flag += 1
                    elif flag == 3:
                        readbuf = self.read(dataSize)
                        data = readbuf
                        checkSum += int(readbuf.hex(), 16) & 0xffff
                        flag += 1
                    elif flag == 4:
                        readbuf = self.read(2)
                        cs = int(readbuf.hex(), 16)
                        if cs != 0xffff & checkSum:
                            data = None
                        flag += 1
                    elif flag == 5:
                        self.read(2)
                        break

                    # if (way == 0):
                    # for i in range(self.ser.in_waiting):
                        # print("接收ascii数据：" + str(self.read()))
                        # data = int(self.read().hex(), 16)  # 转为十进制
                        # data2 = int(data1, 16)  # 转为十进制
                        # print("收到数据十六进制："+data1+"  收到数据十进制："+str(data2))
                    # if (way == 1):
                        # 整体接收
                        # data = self.main_engine.read(self.main_engine.in_waiting).decode("utf-8")#方式一
                        # data = self.ser.read_all()  # 方式二
                        # print("接收ascii数据：", data)
            except Exception as e:
                print("Exception:", e)

        return cmd, data

    def send(self, cmd, data):
        size = calcsize(data)
        checkSum = 0
        self.write(chr(0xab).encode("utf-8"))
        self.write(chr(0xcd).encode("utf-8"))
        self.write(chr(cmd).encode("utf-8"))
        checkSum += cmd
        checkSum += size
        self.write(chr(size).encode("utf-8"))
        self.write(data)
        self.write(pack("=H", size))
        self.write(chr(0xee).encode("utf-8"))
        self.write(chr(0xff).encode("utf-8"))
