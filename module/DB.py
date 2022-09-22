
import pymysql, pymysql.cursors
import hashlib

# 나중에 DB 데이터 받아올 때 클레스로 받아올 수 있게 가볍게 구상해둔 것
class DB:
    def __init__(self):
        db = pymysql.connect(host='localhost',
        port=3306,
        user='root',
        passwd='0225',
        db='test_db',
        charset='utf8')

        self.db = db

    # 회원가입
    def insert_join(self, id, pw, name, email, phone):
        password_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
        cursor = self.db.cursor()

        user_data = [id, password_hash, name, email, phone]

        sql = """insert into user_data (id, pw, name, email, phone)
                values(%s, %s, %s, %s, %s)"""

        cursor.execute(sql, user_data)
        self.db.commit()  

    # 아이디 중복검사
    def id_overlap(self, id):
        cursor = self.db.cursor()


        sql = """select t1.id from user_data t1 where t1.id = '{0}'""".format(id)

        cursor.execute(sql)
        
        if(len(cursor.fetchall()) != 0):
            result = True
        else:
            result = False
        return result

    # 회원 정보 수정
    def change_userdata(self, id, pw, name):
        password_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
        cursor = self.db.cursor()

        sql = """update user_data set pw = '{}', name = '{}' where id = '{}'"""\
            .format(password_hash, name, id)

        cursor.execute(sql)
        self.db.commit()
    
    # 로그인 체크
    def join_check(self, id, pw):
        password_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
        cursor = self.db.cursor()

        sql = """select t1.id, t1.pw, t1.name from user_data t1 where t1.id = 
                '{0}' and t1.pw = '{1}'""".format(id, password_hash)

        cursor.execute(sql)
        result = cursor.fetchall()

        return result

    # 아이디 찾기
    def find_id(self, solve, value):
        # value가 0이면 전화번호로 찾는 것
        if value == 0:
            cursor = self.db.cursor()

            sql = """select t1.id from user_data t1 where t1.phone = 
                    '{0}'""".format(solve)

            cursor.execute(sql)
            result = cursor.fetchall()

        # value가 1이면 이메일로 찾는 것
        elif value == 0:
            cursor = self.db.cursor()

            sql = """select t1.id from user_data t1 where t1.email = 
                    '{0}'""".format(solve)

            cursor.execute(sql)
            result = cursor.fetchall()
        
        return result

    # 비밀번호 찾기 과정 중 1. 아이디를 찾는다
    def find_password(self, solve):
        cursor = self.db.cursor()

        sql = """select t1.id from user_data t1 where t1.id = 
                '{0}'""".format(solve)

        cursor.execute(sql)
        result = cursor.fetchall()

        return result
    
    # 비밀번호 찾기 과정 중 2. 아이디로 고칠 데이터를 찾는다
    def revise_pw(self, solve, pw):
    # value가 0이면 전화번호로 찾는 것
        cursor = self.db.cursor()

        sql = """update user_data set pw = '{}' where 
                id = '{}'""".format(solve, pw)

        cursor.execute(sql)
        self.db.commit()


    # 제품 id 조회
    def product_check(self, id):
        cursor = self.db.cursor()

        sql = """select t1.user_id 
                from t_product t1 
                where t1.user_id = '{}'""".format(id)

        cursor.execute(sql)
        result = cursor.fetchall()

        return result

    # 제품 등록
    def insert_product(self, product_id, product_name, product_price, categori, tags, detail, club, path, user_id):
        cursor = self.db.cursor()

        sql = """insert into t_product (product_id, product_name, product_price, categori, tags, product_detail, club_check, path, user_id)
                values({}, '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}')"""\
                .format(product_id, product_name, product_price, categori, tags, detail, club, path, user_id)

        cursor.execute(sql)
        self.db.commit()

    # 제품 조회
    def get_product_list(self, data):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        if data == "crew":
            sql = """SELECT t1.product_id, t1.product_name,t1.product_price,t1.categori, 
                    t1.tags, t1.club_check, t1.path, t1.user_id 
                    FROM t_product t1 
                    where t1.club_check = '{}'""".format("Y")
        else:
            sql = """SELECT t1.product_id, t1.product_name, t1.product_price, t1.categori, 
                    t1.tags, t1.path, t1.user_id 
                    FROM t_product t1 
                    where t1.categori = '{}'""".format(data)

        cursor.execute(sql)
        result = cursor.fetchall()

        if(len(result) == 0):
            result = "failed"
            
        return result

    def get_product_detail(self, categori, UID, PID):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        
        sql = """SELECT t1.product_id, t1.product_name,t1.product_price,t1.categori, 
                    t1.tags, t1.product_detail, t1.created_date, t1.club_check, t1.path, t1.user_id  
                    FROM t_product t1 
                    where t1.categori = '{}' and t1.user_id = '{}' and t1.product_id = {}"""\
                        .format(categori, UID, PID)

        cursor.execute(sql)
        result = cursor.fetchall()
            
        return result

    
    def get_user_product_list(self, data):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        sql = """SELECT t1.product_id, t1.product_name, t1.product_price, t1.categori, 
                t1.tags, t1.path
                FROM t_product t1 
                where t1.user_id = '{}'""".format(data)

        cursor.execute(sql)
        result = cursor.fetchall()

        if(len(result) == 0):
            result = "failed"

        return result

    def delete_product(self, user_id, product_id):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        sql = """DELETE FROM t_product WHERE t1.product_id = {} and t1.user_id = '{}';""".format(user_id, product_id)

        cursor.execute(sql)
        result = cursor.fetchall()

        if(len(result) > 1):
            sql= """
                SET @COUNT = 0;
                UPDATE t_product SET id = @COUNT:=@COUNT+1;
                UPDATE t_product SET user_id = @COUNT:=@COUNT+1;"""
            cursor.execute(sql)