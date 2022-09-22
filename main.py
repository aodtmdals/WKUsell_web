from flask import Flask, render_template, redirect, flash, url_for, jsonify
from flask import session, request
from flask_wtf import *
import os
from module.DB import DB

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
        userID = session.get("userID")

        # 2. id를 이용해 몇 개의 상품을 등록했는지 조회하고
        # 갯수를 return한다 (product_id가 됨)
        product_id = db.product_check(userID)
        product_id = len(product_id) + 1

        product_name = request.form["productname"]
        product_price = request.form["price"]
        product_price = int(product_price)
        category = request.form["category"]
        tags = request.form["tags"]
        detail = request.form["detail"]

        # 2-1. 동아리 물품 여부 체크
        club = request.form["club"]
        if club == False:
            club = "N"
        else:
            club = "Y"
        
        print(club)

        # 2-2. 태그에 아무것도 안 들어가있으면 tags = "Null"로 값이 없다는 표시 넣어주기
        if tags == "":
            tags = "Null"

        # 3. 사진 외 모든 데이터 먼저 db에 commit
        db.insert_product(product_id, product_name, product_price, category, tags, detail, club, userID)

        # 4. 이미지 처리
        t_image = request.files["tImage"]
        print(t_image)
        t_image_path = "D:\WKUsell_web\img\{}\{}\\thumnail\\".format(userID, product_id)
        os.makedirs(t_image_path, exist_ok=True)
        t_image_name = t_image.filename
        t_image.save(os.path.join(t_image_path, t_image_name))
        save_tImg_path = t_image_path + t_image_name
        print(save_tImg_path)

        #다중 이미지 업로드 오류
        p_image = request.files.getlist("pImage")
        p_image_path = "D:\WKUsell_web\img\{}\{}\product-image\\".format(userID, product_id)
        os.makedirs(p_image_path, exist_ok=True)
        save_pImg_path = ""
        for p_image_name in p_image:
            p_image_name.save(os.path.join(p_image_path, p_image_name.filename))
            save_pImg_path += p_image_path + p_image_name.filename + ","
        print(save_pImg_path)

        # DB에 이미지 경로 업로드
        db.insert_thumnail_img(product_id, save_tImg_path, userID)        
        db.insert_product_img(product_id, save_pImg_path, userID)

        return jsonify({'result': 'success'})

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

#아이디 찾기
@app.route("/join-in/find/id")
def find_id():
    return render_template("find-id.html")
@app.route("/join-in/find/id/request", methods=["POST"])
def find_id_request():
    result = request.form["result"]

    # 함수 실행시켜 아이디 받아오기
    id = db.find_id(result)
    return jsonify({"result": "success", "msg" : "{}".format(id)})
#비밀번호 찾기
@app.route("/join-in/find/pw")
def find_pw():
    return render_template("find-pw.html")
#DB 검색할 아이디 찾기
@app.route("/join-in/find/pw/check", methods=["POST"])
def find_pw_check():
    result = request.form["result"]

    # 함수 실행시키기
    id = db.find_id(result)
    session["id"] = id
        
    return jsonify({"result": "success", "msg" : "{}".format(session.get("id"))})
# 비밀번호 변경
@app.route("/join-in/find/pw/request", methods=["POST"])
def find_pw_request():
    pw = request.form["result"]
    id = session.get("id")

    # 함수 실행시켜 아이디 받아오기
    db.revise_pw(id, pw)
    session.pop("id")
    
    return jsonify({"result": "success"})

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
        password = request.form["pw"]
        nickname = request.form["nickname"]
        email = request.form["email"]
        phone = request.form["phone"]

        print("id = {}, password = {}, email = {}, phone = {}, nickname = {}".format(id, password, email, phone, nickname))
        db.insert_join(id, password, nickname ,email, phone)
        return jsonify({"result": "success"})
    else:
        return render_template("join.html")
# 2. 아이디 중복 검사
@app.route('/join/checkDup', methods=['POST'])
def check_dup():
    id_receive = request.form['id']
    exists = db.id_overlap(id_receive)
    return jsonify({'result': 'success', 'exists': exists})

# 상품 디테일 페이지 관련 코드
@app.route("/detail")
def detail():
    username = session.get("username", None)

    #상품 정보 받아오기

    return render_template("detail.html", username = username)




# 이상한 부분 과정 3
@app.route("/list", methods=["GET"])
def get_list_categori():
    datas = "failed"
    return render_template("list.html", datas=datas)






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
        password = request.form["pw"]
        nickname = request.form["nickname"]

        print("id = {}, password = {}, nickname = {}".\
            format(id, password, nickname))
        db.change_userdata(id, password, nickname)
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
