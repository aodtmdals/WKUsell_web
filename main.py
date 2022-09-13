import os
from flask import Flask, render_template, request, redirect
from flask import session
from flask_wtf.csrf import CSRFProtect #csrf
import pymysql
from server.models import db, User
from server.form import RegisterForm
from flask_sqlalchemy import SQLAlchemy

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


# db = pymysql.connect(host='localhost',
#     port=3306,
#     user='root',
#     passwd='accle10032', # 만들어뒀던 DB 비밀번호 기재 (DB 연동시)
#     db='cheese',         # 만들어뒀던 DB 이름 기재 (DB 연동시)
#     charset='utf8')

# def db_connector():

#     cursor = db.cursor()

#     sql = """SELECT * 
#             FROM cheese
#             WHERE uid=%s
#             AND upw=%s;"""
            
                
#     stmt = "SHOW TABLES LIKE 'userdata'"
#     cursor.execute(stmt)
#     result = cursor.fetchone()
#     if result:
#         pass   
#     else:
#         cursor.execute(sql)
#         db.commit()  
            
#     return str("DB connected!")
        
      

app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
def index():
    return render_template("index.html")
@app.route("/create")
def create():
    return render_template("create.html")
@app.route("/join-in")
def join_in():
    return render_template("join-in.html")
#대충 해둔 회원가입
@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        usertable = User()
        usertable.userid = request.form.get["id"]
        usertable.password = request.form.get["password"]
        usertable.email = request.form.get["email"]
        usertable.phone = request.form.get["phone"]

        db.session.add(usertable)
        db.session.commit()
    
    return render_template('register.html', form=form)
#@app.route("/join-in/register", methods=["POST"])
# def login_register():

#         if id == "admin" and pw == "admin":
#             return render_template("index.html")
#         else:
#             return render_template("join-in.html")
@app.route("/join-out")
def join_out():
    return render_template("index.html")
@app.route("/join")
def join():
    return render_template("join.html")
@app.route("/detail")
def detail():
    return render_template("detail.html")
@app.route("/list")
def product_list():
    return render_template("list.html")


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #사용자에게 정보 전달완료하면 teadown. 그 때마다 커밋=DB반영
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #추가 메모리를 사용하므로 꺼둔다
    app.config['SECRET_KEY']='asdfasdfasdfqwerty' #해시값은 임의로 적음

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app) #app설정값 초기화
    db.app = app #Models.py에서 db를 가져와서 db.app에 app을 명시적으로 넣는다
    db.create_all() #DB생성

    app.run(host='0.0.0.0', debug=True, port=1000)
