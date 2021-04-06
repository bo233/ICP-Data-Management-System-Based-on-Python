from util.DS import *

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

        date = DatatimeFormat(y, m, d, h, mi, s)
        data = Data(date, icp, ict)
        dataList.append(data)

    file.close()
    return dataList


if __name__ == "__main__":
    data = read("/Users/bo233/Projects/Graduation-Project/data/data.dat")
    print(data[0].toString())
