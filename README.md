# calendar_web

Sungmin Maeng(Leader) - Server, Front(Main page, Details , Delete)
Dahyae Lee - Database
Sujueng Hwang - Front(Create, Revise, Join Page)

templates - html file
static > css - css file
static > js - javascrip file

main.py는 서버 파일입니다. DB 연결 전에 잘 보여지는지 확인할 때 만져주세요.
Flask나 jinja라고 검색하면 문법이나 이것저것 나올 겁니다.
하지만 커밋하지 않게 조심해주세요. 충돌 일어납니다...

create.html은 임의로 만들어둔 글 추가 페이지입니다. 수정 씨가 수정하고 싶으시면 얼마든지 해주세요.

from flask import Flask, render_template
app = Flask(**name**)

@app.route('/')
def index():
return render_template("index.html")
@app.route("/create")
def create():
return render_template("create.html")
if **name** == '**main**':
app.run(debug=True)

혹시 몰라 main.py 파일의 초기본을 백업해두겠습니다. 안되면 이걸 써주세요. 조금씩 수정할 때마다 여기 올려놓겠습니다.

2022.09.08 - html flask 서버에 추가해둠. mysql DB에 연동함.

이후에 카드를 리스트화 해서 보여주는 기능 구현
채팅기능 구현
메인 페이지 만들기
UI적 부분 수정
