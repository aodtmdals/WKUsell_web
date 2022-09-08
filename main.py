from flask import Flask, render_template
import pymysql

# 나중에 DB 데이터 받아올 때 클레스로 받아올 수 있게 가볍게 구상해둔 것
# class DB:
#     def __init__(self) -> None:
#         db = pymysql.connect(host='localhost',
#         port=3306,
#         user='root',
#         passwd='accle10032',
#         db='cheese',
#         charset='utf8')

#     def insert_login(self, id, name):
#         cursor = self.db.cursor()

def db_connector():
    db = pymysql.connect(host='localhost',
    port=3306,
    user='root',
    passwd='accle10032', # 만들어뒀던 DB 비밀번호 기재 (DB 연동시)
    db='cheese',         # 만들어뒀던 DB 이름 기재 (DB 연동시)
    charset='utf8')

    cursor = db.cursor()

    sql = """CREATE TABLE userdata(
            id VARCHAR(15) NOT NULL PRIMARY KEY,
            password VARCHAR(15) NOT NULL
            );"""
            
                
    stmt = "SHOW TABLES LIKE 'userdata'"
    cursor.execute(stmt)
    result = cursor.fetchone()
    if result:
        pass   
    else:
        cursor.execute(sql)
        db.commit()  
            
    db.close()
    return str("DB connected!")
        
      

app = Flask(__name__)

@app.route('/')
#def index():
#    return render_template("index.html")
# 일단 리스트 보여주는 페이지를 메인 페이지로 둠 추후에 변경
def product_list():
    return render_template("list.html")
@app.route("/create")
def create():
    return render_template("create.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/detail")
def detail():
    return render_template("detail.html")
#@app.route("/list")
if __name__ == '__main__':
    print(db_connector())
    app.run(host='0.0.0.0', debug=True, port=1000)
