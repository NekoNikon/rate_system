import psycopg2
from flask import json
from psycopg2.extras import DictCursor ,RealDictCursor ,RealDictRow
from app.database.QueryFactory import QF
from argon2 import PasswordHasher , exceptions

dsn_web = "dbname='d1ufc7dp4m125k' user='kzkoadpajawjfo' host='ec2-54-235-114-242.compute-1.amazonaws.com' password='5bcd5e361babc3229beac6b0e6a2c7c509b7a576360dc7281806ab7744daf98b' port='5432'"
dsn = "dbname='rate_system' user='postgres' host='localhost' password='jojodio' port='5432'"
dsn_web2 = "dbname='d8qqm1tdt7a7p8' user='ehieysywbgqwmy' host='ec2-54-225-242-183.compute-1.amazonaws.com' password='846ad9e7a623935894144cada5935b40fd6e332cd9001ccb1fc19eeb742d12d5' port='5432'"
#dsn_old = "dbname='d8qqm1tdt7a7p8' user='ehieysywbgqwmy' host='ec2-54-225-242-183.compute-1.amazonaws.com' password=''"
psql = psycopg2
dcurs= DictCursor
qf  =   QF()
ph  =   PasswordHasher(hash_len=100)

class DataManager():

    def Connect(self):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        return  curs
# main

    def AddInd(self, id , name):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        curs.execute('''
            INSERT INTO indicator(indicator_name , indicator_group_id)
            VALUES          ('%(name)s' , %(id)i)
        ''' % {'id':id , 'name':name})
        conn.commit()

    def GetIndsByTeacher(self, id):
        curs = self.Connect()
        curs.execute('''
            SELECT

            rate_id,    indicator_name , rate_value
            FROM
                indicator
            INNER JOIN
                rate
                ON rate_indicator_id=indicator_id
            WHERE rate_teacher_id='%i'
        ''' % id)
        return curs.fetchall()

    def DelRate(self , id):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        curs.execute('''
            DELETE FROM rate
            WHERE
                rate_id = '%i'
        ''' % (id,))
        conn.commit()

    def AddRate(self , IS,ID,IT,VAL):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        curs.execute(qf.add_rate(IS,ID,IT,VAL))
        conn.commit()


    def GetListTeachers(self):
        curs = self.Connect()
        curs.execute('''
            SELECT
                teachers_id,
                teachers_second_name
            FROM
                teachers
        ''')
        return curs.fetchall()

    def GetTeachers(self):
        curs = self.Connect()
        curs.execute('''SELECT
                            rate_id,
                            teachers.teachers_second_name,
                            rate_value ,
                            indicator.indicator_name,
                            season_date
                        FROM
                            rate
                        INNER JOIN
                            teachers
                            ON teachers.teachers_id = rate.rate_teacher_id
                        INNER JOIN
                            indicator
                            ON indicator.indicator_id = rate.rate_indicator_id
                        INNER JOIN
                            season
                            ON season.season_id = rate.rate_season_id
                        ''')
        return curs.fetchall()

    def CheckUser(self , username):
        curs = self.Connect()
        curs.execute("SELECT * FROM manage_persons WHERE manage_persons_login = '%s'" %(username,))
        if curs.fetchall():
            return True
        else:
            return False

    def GetDate(self):
        curs = self.Connect()
        curs.execute("select * from season")
        return curs.fetchall()

    # def ShowAll(self):
    #     curs = self.Connect()
    #     curs.execute(qf.select_all())
    #     return curs.fetchall()

    def user_is_exist(self , log):
        is_user = False
        curs = self.Connect()
        curs.execute("SELECT manage_persons_login FROM manage_persons WHERE manage_persons_login = '%s'" % (log,) )
        if curs.fetchall():
            return True
        else:
            return False


    def AddUser(self ,login , password , privileges , name):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        if  self.user_is_exist(login):
            print('user is exist')
            return False
        #     not add user
        else:
            print('user is not exist')
        #     add user
            h_password = ph.hash(password)
            curs.execute(qf.add_user_in_manage_persons(login,h_password,privileges , name))
            conn.commit()
# working //////////////////////////////////////////////////////////////////////////////////////////
    def GetIDTeacherByIIN(self , iin):
        curs = self.Connect()
        curs.execute("SELECT id_teacher FROM teachers WHERE iin_teacher = %s " , (iin,))
        return curs.fetchall()[0]

    def GetAllRecordsByTable(self , table ):
        curs = self.Connect()
        curs.execute("SELECT * FROM "+table)
        return curs.fetchall()

    def VerifyPassword(self , login , password):
        curs = self.Connect()
        curs.execute("SELECT manage_persons.manage_persons_password FROM manage_persons WHERE manage_persons.manage_persons_login=%s" , (login,))
        data = curs.fetchone()[0]
        try:
            if ph.verify(data,password):
                return True
        except exceptions.VerifyMismatchError:
            print('wrong password in ajax\n')
            return False

    def EditRecord(self , table , index):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        curs.execute("UPDATE ")
        conn.commit()

    def GetTeacherRateByIin(self , IIN):
        curs = self.Connect()
        curs.execute(qf.get_teacher_rate_by_iin(IIN))
        return curs.fetchall()

    def GetManagePersonsPrivileges(self , username):
        curs = self.Connect()
        curs.execute("SELECT manage_persons.manage_persons_priv_value FROM manage_persons WHERE manage_persons_login= %s" , (username,))
        return curs.fetchone()[0]

    def GetSeasonsId(self):
        curs = self.Connect()
        curs.execute('''
                        SELECT * FROM season ORDER BY season_date DESC
                    ''')

        return curs.fetchall()

    def GetRateByTeacher(self , id_teach):
        ret = []
        seasons = self.GetSeasonsId()
        curs = self.Connect()
        # print(seasons)
        for s in seasons:
            print(s[0])
            curs.execute('''SELECT 
                            rate_indicator_id , rate_value , rate_season_id ,season_date
                        FROM rate 
                        INNER JOIN indicator ON indicator.indicator_id = rate_indicator_id
                        INNER JOIN season  ON season_id = %i
                        WHERE rate_teacher_id = %s and rate_season_id = %i ''' % (s[0] ,id_teach, s[0]))
            ret.append(curs.fetchall())
        return ret

    #dev
    def GetIndicators(self , group):
        curs = self.Connect()
        curs.execute("SELECT indicator.indicator_id , indicator.indicator_name FROM indicator INNER JOIN indicator_group ON indicator_group.indicator_group_id ='%i' and indicator.indicator_group_id=indicator_group.indicator_group_id" % group)
        return curs.fetchall()

    #dev
    def GetGroupIndicators(self):
        curs = self.Connect()
        curs.execute("SELECT * FROM indicator_group ORDER BY indicator_group_id")
        return curs.fetchall()

    #dev
    def AddGroupInds(self , name):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        curs.execute("INSERT INTO indicator_group(indicator_group_name) VALUES('%s')" % name)
        conn.commit()
        curs.execute('''SELECT indicator_group.indicator_group_id FROM indicator_group ORDER BY indicator_group.indicator_group_id DESC LIMIT 1''')
        idi = curs.fetchall()[0][0]
        curs.execute('''INSERT INTO indicator(indicator_name , indicator_group_id) VALUES('Новый индикатор' , %i)''' % idi ) 
        conn.commit()
    #dev
    def DelGroupInds(self , id):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        curs.execute("DELETE FROM indicator_group WHERE indicator_group_id = '%i'" % id)
        conn.commit()
    #dev

    #dev
    # def DelInds(self , id):
    #     conn = psql.connect(dsn)
    #     curs = conn.cursor()
    #     curs.execute("DELETE FROM indicator WHERE indicator_id = '%i'" % id)
    #     conn.commit()

    def GetTeachersByManagePerson(self , id_mp , id_season):
        curs = self.Connect()
        curs.execute(QF.get_teachers_and_rate_value_by_manager_teachers(self ,id_mp , id_season))
        return curs.fetchall()
    #dev
    def JOIN(self):
        curs = self.Connect()
        curs.execute('''
					SELECT
					  teachers.sname_t , login
					FROM
					  teachers
					INNER JOIN
					  manage_persons
					ON
					  manage_persons.id_user=1
						AND
					  teachers."Id_teacher_group" = manage_persons.id_user;
					''')
        # curs.execute("SELECT * FROM teachers")
        return curs.fetchall()

    #dev
    def GetInds(self):
        curs = self.Connect()
        curs.execute("SELECT indicator.indicator_id , indicator.indicator_name From indicator")
        return curs.fetchall()

    def GetIndsWithGroup(self):
        ret = []
        curs = self.Connect()
        groups = self.GetGroupIndicators()
        for gr in groups:
            curs.execute('''
                SELECT * FROM indicator
                INNER JOIN indicator_group
                    ON indicator_group.indicator_group_id = %i
                    AND indicator_group.indicator_group_id = indicator.indicator_group_id
            ''' % (gr[0]))
            ret.append(curs.fetchall())
        return ret
            
    def GetMP(self):
        curs = self.Connect()
        curs.execute('''
            SELECT 
                manage_persons_id,
                manage_persons_name,
                manage_persons_login,
                manage_persons_priv_value
            FROM manage_persons
        ''')
        return curs.fetchall()

    def UpdateGroupInd(self , idi , value):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        curs.execute('''
            UPDATE indicator_group SET indicator_group_name = '%(value)s' WHERE indicator_group_id = %(id)i
        ''' % {'value':value , 'id':idi})
        conn.commit()

    def UpdateInd(self , id , name):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        curs.execute('''
            UPDATE indicator SET indicator_name = '%(name)s' WHERE indicator_id = %(id)i
        ''' % {'id':id ,'name':name})
        conn.commit()

    def DelInd(self , id):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        curs.execute('''DELETE from indicator WHERE indicator_id = %i ''' % id)
        conn.commit()

    def EditUser(self , l , n  , i):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        curs.execute('''
            UPDATE manage_persons SET
                manage_persons_name = '%(name)s' ,
                manage_persons_login = '%(login)s'
                WHERE manage_persons_id = %(id)i
        ''' % {'login':l , 'name':n , 'id':i} )
        conn.commit()

    def DelUser(self , id):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        curs.execute('''DELETE from manage_persons WHERE manage_persons_id = %i''' % id)
        conn.commit()
    
    # def AddHead(self,s,f,t,tg,c):
    #     conn = psql.connect(dsn)
    #     curs = conn.cursor()
    #     curs.execute('''
    #         INSERT INTO teachers(teachers_second_name , teachers_first_name , teachers_third_name , teachers_iin, teachere_tg_id )
    #         VALUES ('%s' , '%s' , '%s' , '%s') 
    #     ''' % (s , f , t ,c))
    #     conn.commit()
        

    def AddTeacher(self,s , f ,t ,c):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        curs.execute('''
            INSERT INTO teachers(teachers_second_name , teachers_first_name , teachers_third_name , teachers_iin)
            VALUES ('%s' , '%s' , '%s' , '%s') 
        ''' % (s , f , t ,c))
        conn.commit()

    def DelTeacher(self , id):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        curs.execute('''DELETE from teachers WHERE teachers_id = %i''' % id)
        conn.commit()
    
    def EditTeacher(self ,i, s ,f, t,c):
        conn = psql.connect(dsn)
        curs = conn.cursor()
        curs.execute('''
            UPDATE teachers SET
                teachers_second_name = '%(sn)s' ,
                teachers_first_name = '%(fn)s' , 
                teachers_third_name = '%(tn)s' , 
                teachers_iin = '%(code)s' 
                WHERE teachers_id = %(id)i
        ''' % {'id':i , 'sn':s , 'fn':f , 'tn':t , 'code':c} )
        conn.commit()

    def GetSummRateByTeacher(self,id):
        curs = self.Connect()
        curs.execute("SELECT sum(rate_value) FROM rate WHERE rate_teacher_id = %i" % id)
        return curs.fetchall()

    def GetAvg(self,id):
        curs = self.Connect()
        curs.execute("SELECT avg(rate_value) FROM rate WHERE rate_teacher_id = %i" % id)
        return curs.fetchall()