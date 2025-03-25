import time
import random
import pymysql
import sys
import os


DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(DIR_PATH, "..", ".."))
if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

from conf import env
## 数据库配置
DATABASE_HOST = env.DATABASE_HOST
DATABASE_USER = env.DATABASE_USER
DATABASE_PASSWORD = env.DATABASE_PASSWORD
DATABASE_NAME = env.DATABASE_NAME


class MysqlHelper():
    
    def __init__(self, host, user, password, database, port=3306, charset='utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset
    
    def get_connect(self):
        connect = pymysql.Connect(host=self.host, port=self.port, user=self.user, passwd=self.password, database=self.database, charset=self.charset)
        return connect
        
    def query_many(self, sql, args = None):
        result = []
        try: 
            conn = self.get_connect()
            with conn.cursor() as cursor:
                cursor.execute(sql, args)
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f'异常为：{e}')
            # 事务回滚
            conn.rollback()
        finally:
            # 关闭游标
            cursor.close()
            # 关闭连接
            conn.close()
            return result
    
    def query_many_as_dict(self, sql, args = None):
        """优化成字典"""
        
        rows_as_dict = []
        try: 
            conn = self.get_connect()
            with conn.cursor() as cursor:
                cursor.execute(sql, args)
                results = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                # 将结果转换为字典列表
                
                for row in results:
                    row_dict = dict(zip(columns, row))
                    rows_as_dict.append(row_dict)
                
        except pymysql.MySQLError as e:
            print(f'异常为：{e}')
            # 事务回滚
            conn.rollback()
        finally:
            # 关闭游标
            cursor.close()
            # 关闭连接
            conn.close()
            return rows_as_dict
    
    def query_one(self, sql, args = None):
        """单行执行"""
        result = {}
        try: 
            conn = self.get_connect()
            with conn.cursor() as cursor:
                cursor.execute(sql, args)
                result = cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f'异常为：{e}')
            # 事务回滚
            conn.rollback()
        finally:
            # 关闭游标
            cursor.close()
            # 关闭连接
            conn.close()
            return result
    
    def exec_sql(self, sql, args = None):
        """sql语句提交"""
        try: 
            conn = self.get_connect()
            with conn.cursor() as cursor:
                cursor.execute(sql, args)
            conn.commit()   
        except pymysql.MySQLError as e:
            print(f'异常为：{e}')
            # 事务回滚
            conn.rollback()
        finally:
            # 关闭游标
            cursor.close()
            # 关闭连接
            conn.close()
         

class AutoDatabase():
    def __init__(self) -> None:
        self.auto_sql = MysqlHelper(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    
    def set_case_result(self,case_id: int, step_result: int):
        """设置用例的结果"""
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        sql = f"UPDATE webtestcase set result=%s,run_time=%s where id=%s"
        param = (step_result,now,int(case_id))
        self.auto_sql.exec_sql(sql,param)
    
    def init_step_result(self,case_id: int):
        """初始化用例的所有步骤的结果"""
        sql = f"UPDATE webteststep set result=%s where case_id=%s"
        param = (0,int(case_id))
        self.auto_sql.exec_sql(sql,param)
    
    def set_step_result(self,step_id, result,run_log: str = None):
        """设置步骤的结果"""
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        sql = "UPDATE webteststep set result=%s,run_time=%s,run_log=%s where id=%s"
        param = (result, now,run_log,str(step_id))
        self.auto_sql.exec_sql(sql, param)
        
    def add_case_step(self,data: dict):
        id = str(int(time.time()*1000)) + str(random.randint(1001,9999))
        
        sql = f"INSERT INTO `webteststep`(`id`, `case_id`, `step_order`, `name`, `action`,`find_method`, `find_value`, `input_value`, `result`) VALUES ('{id}', {data.get('case_id')}, {data.get('step_order')}, '{data.get('name')}', '{data.get('action')}', '{data.get('find_method',)}', '{data.get('find_value')}', '{data.get('input_value')}',0)"
        self.auto_sql.exec_sql(sql)
        
    def get_case_info(self,id: int):
        """获取用例信息"""
        sql = f"SELECT * FROM webtestcase WHERE id={id}"
        return self.auto_sql.query_one(sql)
        
    def get_case_step(self,case_id: int,run_step: int = 0):
        """_summary_

        Args:
            case_id (int): _description_
            run_step (int, optional): 0获取所有步骤. Defaults to 0.

        Returns:
            _type_: _description_
        """
        if run_step:
            sql = f"select id,step_order,action,find_method,find_value,input_value from webteststep where case_id={case_id} and step_order<={run_step} ORDER BY step_order ASC"
        else:
            sql = f"select id,step_order,action,find_method,find_value,input_value from webteststep where case_id={case_id} ORDER BY step_order ASC"
        return self.auto_sql.query_many_as_dict(sql)
    
    
if __name__ == '__main__':
    auto_db = AutoDatabase()
    # case_step_data = {'case_id': 1,'step_order':3,'name':'点击搜索','action':'click','find_method': 'find_element_by_id','find_value': 'su'}
    # auto_db.add_case_step(case_step_data)
    # auto_db.get_case_step(1234)