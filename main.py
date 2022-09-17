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

    # 회원 정보 수정
    def change_userdata(self, id, pw, name, email, phone):
        password_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
        cursor = self.db.cursor()

        sql = """update user_data set pw = '{}', name = '{}', email = '{}', phone = '{}' where id = '{}'"""\
            .format(password_hash, name, email, phone, id)

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

    # 제품 조회
    def product_check(self, id):
        cursor = self.db.cursor()

        sql = """select t1.user_id 
                from t_product t1 
                where t1.user_id = '{}'""".format(id)

        cursor.execute(sql)
        result = cursor.fetchall()

        return result

    # 제품 등록
    def insert_product(self, product_id, product_name, product_price, categori, club, user_id):
        cursor = self.db.cursor()

        sql = """insert into t_product (product_id, product_name, product_price, categori, club_check, user_id)
                values({}, '{}', {}, '{}', '{}', '{}')""".format(product_id, product_name, product_price, categori, club, user_id)

        cursor.execute(sql)
        self.db.commit()  


        
      

app = Flask(__name__)
app.secret_key = "secret key"
db = DB()

@app.route('/')
def index():
    username = session.get("username", None)
    return render_template("index.html", username = username)
@app.route("/create")
def create():
    username = session.get("username", None)
    return render_template("create.html", username = username)    
@app.route("/create/request", methods=["POST"])
# 1. 제품 데이터 DB에 저장
def create_request():
    if request.method == "POST":
        # 1. 로그인 된 아이디를 받아온다
        id = session.get("userID")

        # 2. id를 이용해 몇 개의 상품을 등록했는지 조회하고
        # 갯수를 return한다 (product_id가 됨)
        product_id = db.product_check(id)
        product_id = len(product_id) + 1

        product_name = request.form["pdName"]
        product_price = request.form["price"]
        product_price = int(product_price)
        category = request.form["category"]

        # 2-1. 동아리 물품 여부 체크
        club = request.form.get("club")
        if club == None:
            club = "N"
        else:
            club = "Y"
        
        print(club)
        # 3. 무조건 입력해야하는 데이터들 먼저 db에 commit
        db.insert_product(product_id, product_name, product_price, category, club, id)

        # 4. 태그 처리
        tag = request.form["tag"]

        # 5. 이미지 처리
        # thum_img = request.files["thumImg"].filename
        # pd_img = request.files["pdImg"]

        # save_thum_img = f"./static/img/thumnails/{id}/{product_id}"
        # save_thum_url = save_thum_img + thum_img
        # thum_img.save(save_thum_img)

        # print("pd_img = {}, thum_img = {}".format(save_thum_url, thum_img.filename))
        return redirect(url_for("product_list"))
    else:
        return render_template("join.html")

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
            return redirect(url_for("join_in"))
        else:
            session["userID"] = result[0][0]
            session["username"] = result[0][2]
            return redirect(url_for("index"))
# 로그아웃 코드
@app.route("/join-out")
def join_out():
    session.pop("userID", None)
    session.pop("username", None)
    return redirect(url_for("index"))

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
        nickname = request.form["nickname"]
        email = request.form["email"] + "@" + request.form["email_url"]
        phone = request.form["phone"]

        print("id = {}, password = {}, email = {}, phone = {}, nickname = {}".format(id, password, email, phone, nickname))
        db.insert_join(id, password, nickname ,email, phone)
        return render_template("index.html")
    else:
        return render_template("join.html")

# 2. 아이디 중복 검사 부분. 추후에 추가 예정
# @app.route('/join/checkDup', methods=['POST'])
# def check_dup():
#     id_receive = request.form['id']
#     exists = db.id_overlap(id_receive)
#     return jsonify({'result': 'success', 'exists': exists})

# 상품 디테일 페이지 관련 코드
@app.route("/detail")
def detail():
    username = session.get("username", None)
    return render_template("detail.html", username = username)
@app.route("/list")
def product_list():
    username = session.get("username", None)
    return render_template("list.html", username = username)

# 마이페이지 관련 코드
@app.route("/user")
def userpage():
    username = session.get("username", None)
    return render_template("userpage.html", username = username)
@app.route("/user/revise")
def user_revise():
    username = session.get("username", None)
    return render_template("join-revise.html", username = username)
@app.route("/user/revise/request", methods=["POST"])
def user_revise_request():
    username = session.get("username", None)
    userID = session.get("userID", None)
    if request.method == "POST":
        id = userID
        password = request.form["password"]
        nickname = request.form["nickname"]
        email = request.form["email"] + "@" + request.form["email_url"]
        phone = request.form["phone"]

        print("id = {}, password = {}, email = {}, phone = {}, nickname = {}".\
            format(id, password, email, phone, nickname))
        db.change_userdata(id, password, nickname, email, phone)
        return redirect(url_for("userpage", username = username))
    else:
        return render_template("index.html", username = username)

@app.route("/user/product")
def user_product():
    username = session.get("username", None)
    return render_template("user-product.html", username = username)
@app.route("/cart")
def cart():
    username = session.get("username", None)
    return render_template("cart.html", username = username)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
