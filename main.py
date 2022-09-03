from flask import Flask, render_template
app = Flask(__name__)
student_data = {
    1: {"name": "슈퍼맨", "author": "아무개", "score": {"국어": 90, "수학": 65}},
    2: {"name": "배트맨", "author": "아무개", "score": {"국어": 75, "영어": 80, "수학": 75}}
}
@app.route('/')
def index():
    return render_template("index.html", 
            template_students = student_data)
@app.route("/student/<int:id>")
def student(id):
    return render_template("student.html", 
            template_name=student_data[id]["name"],
            template_author=student_data[id]["author"], 
            template_score=student_data[id]["score"])
@app.route("/create")
def create():
    return render_template("create.html")
if __name__ == '__main__':
    app.run(debug=True)