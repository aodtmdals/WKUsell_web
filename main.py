from flask import Flask, render_template, request, redirect
from flask import session
import pymysql
import hashlib

# 나중에 DB 데이터 받아올 때 클레스로 받아올 수 있게 가볍게 구상해둔 것
class DB:
    def __init__(self):
        db = pymysql.connect(host='localhost',
        port=3306,
        user='root',
        passwd='accle10032',
        db='wku_market',
        charset='utf8')

        self.db = db

    #회원가입
    def insert_join(self, id, pw, name, email, phone):
        password_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
        cursor = self.db.cursor()

        user_data = [id, pw, name, email, phone]

        sql = """insert into user_data (id, pw, name, email, phone)
                values(%s, %s, %s, %s, %s)"""

        cursor.execute(sql, user_data)
        self.db.commit()  

    def id_overlap(self):
        cursor = self.db.cursor()

        sql = """select t1.id from user_data t1"""

        cursor.execute(sql)
        id = cursor.fetchall()
        return id


        
      

app = Flask(__name__)
app.secret_key = "secret key"
db = DB()

@app.route('/')
def index():
    return render_template("index.html")
@app.route("/create")
def create():
    return render_template("create.html")
@app.route("/join-in")
def join_in():
    return render_template("join-in.html")
@app.route("/join-out")
def join_out():
    return render_template("index.html")
@app.route("/join")
def join():
    return render_template("join.html")
@app.route("/join/request", methods=["POST"])
def join_request():
    if request.method == "POST":
        id = request.form["id"]
        password = request.form["password"]
        email = request.form["email"] + "@" + request.form["email_url"]
        phone = request.form["phone"]
        nickname = request.form["nickname"]

        print("id = {}, password = {}, email = {}, phone = {}, nickname = {}".format(id, password, email, phone, nickname))
        db.insert_join(id, password, nickname ,email, phone)

        return render_template("index.html")
    else:
        return render_template("join.html")

#아이디 중복 검사 부분. 추후에 추가 예정
@app.route("/join/id-overlap")
def id_overlap():
    id_receive = request.form["id"]
    saved_id = db.id_overlap()


@app.route("/detail")
def detail():
    return render_template("detail.html")
@app.route("/list")
def product_list():
    return render_template("list.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
