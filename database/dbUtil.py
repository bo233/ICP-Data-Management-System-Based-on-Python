#coding=utf-8
import pymysql
import datetime
from util.DS import *
from util.dataproc import load, save


class MySQLHelper:
    def __init__(self):
        pass

    def init(self,host='localhost',port=3306,db='ICP_db',user='bo233',passwd='123456',charset='utf8'):
        self.conn=pymysql.connect(host=host,port=port,db=db,user=user,passwd=passwd,charset=charset)

    def exec(self, sql, params):
        return self.__cud(sql,params)

    def __cud(self,sql,params=[]):
        self.init()
        try:
            # self.conn.ping(reconnect=True)
            #用来获得python执行Mysql命令的方法,也就是我们所说的操作游标
            #cursor 方法将我们引入另外一个主题：游标对象。通过游标扫行SQL 查询并检查结果。
            #游标连接支持更多的方法，而且可能在程序中更好用。
            cs1 = self.conn.cursor()
            #真正执行MySQL语句
            rows=cs1.execute(sql, params)
            self.conn.commit()
            #完成插入并且做出某些更改后确保已经进行了提交，这样才可以将这些修改真正地保存到文件中。
            cs1.close()
            self.conn.close()
            return rows #影响到了哪行
        except Exception as e:
            print(e)
            self.conn.rollback()

    def fetchone(self, sql, params=[]):
        self.init()
        #一次只返回一行查询到的数据
        try:
            cs1 = self.conn.cursor()
            cs1.execute(sql , params)
            row = cs1.fetchone()
            #把查询的结果集中的下一行保存为序列
            #print(row)
            #row是查询的值
            cs1.close()
            self.conn.close()
            return row
        except Exception as e:
            print("None", e)

    def fetchall(self,sql,params):
        self.init()
        #接收全部的返回结果行
        #返回查询到的全部结果值
        try:
            cs1=self.conn.cursor()
            cs1.execute(sql,params)
            rows=cs1.fetchall()
            cs1.close()
            self.conn.close()

            return rows
        except Exception as e:
            print("None", e)

    def docLoginCheck(self, id, pwd):
        # self.init()
        sql = "SELECT d_pwd from doctor_tbl where d_id = %s"
        params = [id]
        flag = False
        res = self.fetchone(sql, params)
        if res is not None and res[0] == pwd:
            flag = True
        return flag

    def getDocName(self, id):
        sql = "SELECT d_name from doctor_tbl where d_id = %s"
        params = [id]
        name = self.fetchone(sql, params)
        return name

    def ptLoginCheck(self, id, pwd):
        # self.init()
        sql = "SELECT p_pwd from patient_tbl where p_id = %s"
        params = [id]
        flag = False
        res = self.fetchone(sql, params)
        if res is not None and res[0] == pwd:
            flag = True
        return flag

    def docIdExist(self, id):
        # self.init()
        sql = "SELECT d_name from doctor_tbl where d_id = %s"
        params = [id]
        flag = False
        res = self.fetchone(sql, params)
        if res is not None:
            flag = True
        return flag

    def docRegister(self, id, name, tel, pwd):
        # self.init()
        sql = 'INSERT INTO doctor_tbl values(%s,%s,%s,%s)'
        params = [id, name, tel, pwd]
        row = self.exec(sql, params)
        # return row is not None
        return True

    def ptRegister(self, name, age, gender, pwd, allergy, family_history,
                   height, weight, blood_type, tel, medical_history):
        # self.init()
        if allergy == '': allergy = '无'
        if family_history == '': family_history = '无'
        if medical_history == '': medical_history = '无'
        sql = 'INSERT INTO patient_tbl (p_name, p_age, p_gender, p_pwd, allergy, family_history, ' \
              'height, weight, blood_type, p_tel, past_medical_history) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        params = [name, age, gender, pwd, allergy, family_history,
                   height, weight, blood_type, tel, medical_history]
        row = self.exec(sql, params)
        sql = 'select max(p_id) from patient_tbl'
        res = self.fetchone(sql, [])
        # return row is not None
        return res

    def getPtData(self, id:str):
        # get info
        sql = 'SELECT * from patient_tbl where p_id = %s'
        params = [id]
        tInfo = self.fetchone(sql, params)
        if tInfo is None: return None
        info = list(tInfo)

        name = info[1]
        age = int(info[2])
        gender = info[3]
        allergy = info[5]
        family_his = info[6]
        height = float(info[7])
        weight = float(info[8])
        bld_type = info[9]
        tel = info[10]
        medi_his = info[11]

        ptData = PtData(int(id), name, age, gender, height, weight, bld_type, tel,
                 medi_his, allergy, family_his)

        # get consultations
        sql = 'SELECT * from consultation_tbl where p_id = %s'
        params = [id]
        rows = self.fetchall(sql, params)
        for res in rows:
            cons = Cons(res[2], res[3], res[4])
            ptData.cons.append(cons)
        ptData.cons.sort(key=lambda x:x.date, reverse=True)

        return ptData

    # def getPtData(self, id:str):
    #     ptData = self.getPtInfo(id)
    #     if ptData is not None:
    #         sql = 'SELECT c_date,symptom,diagnosis from consultation_tbl where p_id = %s'
    #         params = [id]
    #         cons = self.fetchall(sql, params)
    #         for i in cons:
    #             con = Cons(i[0], i[1], i[2])
    #             ptData.cons.append(con)
    #         ptData.cons.sort(key=lambda x:x.date, reverse=True)
    #
    #     return ptData

    def addPtCons(self, id, consultations:Cons):
        sql = 'INSERT into consultation_tbl (p_id,c_date,symptom, diagnosis) values(%s, %s, %s, %s)'
        params = [id, str(consultations.date), consultations.sx, consultations.diag]
        self.exec(sql, params)

    def modifyPtInfo(self, id, name, age, gender, allergy, family_history,
                   height, weight, blood_type, tel, medical_history):
        if allergy == '': allergy = '无'
        if family_history == '': family_history = '无'
        if medical_history == '': medical_history = '无'
        sql = 'UPDATE patient_tbl SET p_name=%s, p_age=%s, p_gender=%s, allergy=%s, family_history=%s, ' \
              'height=%s, weight=%s, blood_type=%s, p_tel=%s, past_medical_history=%s WHERE p_id=%s'
        params = [name, age, gender, allergy, family_history,
                   height, weight, blood_type, tel, medical_history, id]
        row = self.exec(sql, params)
        return True

    def addIcp(self, id, path, date:datetime):
        sql = 'INSERT into icp_tbl (p_id,i_date,i_data) values(%s,%s,%s)'
        params = [id, date, path]
        self.exec(sql, params)

    def getIcp(self, id):
        sql = 'SELECT i_data,i_date from icp_tbl where p_id = %s'
        params = [id]
        rows = self.fetchall(sql, params)
        rows = list(rows)
        icp_path:list[str] = []
        rows.sort(key=lambda x: x[1], reverse=True)
        for res in rows:
            icp_path.append(res[0])
        return icp_path


DBHelper = MySQLHelper()
