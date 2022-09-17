from unittest import result
from flask import Flask, render_template, redirect, flash, url_for, jsonify
from flask import session, request
from flask_wtf import *
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
            False
        print(result)
    
    # 로그인 체크
    def join_check(self, id, pw):
        password_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
        cursor = self.db.cursor()

        sql = """select t1.id, t1.pw, t1.name from user_data t1 where t1.id = '{0}' and t1.pw = '{1}'""".format(id, password_hash)

        cursor.execute(sql)
        result = cursor.fetchall()

        return result


        
      

app = Flask(__name__)
app.secret_key = "secret key"
db = DB()

@app.route('/')
def index():
    username = session.get("username", None)
    userID = session.get("userID", None)
    return render_template("index.html", username = username)
@app.route("/create")
def create():
    return render_template("create.html")
# 로그인 관련 코드
@app.route("/join-in")
def join_in():
    return render_template("join-in.html")
@app.route("/join-in/confirm", methods=["POST"])
def join_in_confirm():
    if request.method == "POST":
        id = request.form["join-id"]
        password = request.form["password"]
        result = db.join_check(id, password)

        # 튜플에 값이 없으면 DB에 같은 값이 없는 것이므로
        # 로그인 실패
        if len(result) == 0:
            flash("잘못된 입력입니다.")
            return redirect(url_for('join_in'))
        else:
            session["userID"] = result[0][0]
            session["username"] = result[0][2]
            return redirect(url_for('index'))
# 로그아웃 코드
@app.route("/join-out")
def join_out():
    session.pop("userID", None)
    session.pop("username", None)
    return redirect(url_for('index'))

# - 회원가입 관련 코드
@app.route("/join")
def join():
    return render_template("join.html")
@app.route("/join/request", methods=["POST"])
# 1. 회원가입 데이터 DB에 저장
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

# 2. 아이디 중복 검사 부분. 추후에 추가 예정
@app.route('/join/checkDup', methods=['POST'])
def check_dup():
    id_receive = request.form['id']
    exists = db.id_overlap(id_receive)
    return jsonify({'result': 'success', 'exists': exists})

# 상품 디테일 페이지 관련 코드
@app.route("/detail")
def detail():
    return render_template("detail.html")
@app.route("/list")
def product_list():
    return render_template("list.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
