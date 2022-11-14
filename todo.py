from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
import os

PWD = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(PWD, 'todo.db'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    return app,db

app,db = create_app()

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos = todos)

@app.route("/add",methods=["POST"])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title=title,complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5001)