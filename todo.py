from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Lenovo/Desktop/ToDoApp/todo.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all() #Veritabanındaki tablodan verilerimizi çekiyoruz.
    return render_template("index.html", todos = todos)

@app.route("/complete/<string:id>") #Dinamik id olarak alıyoruz.
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    """if todo.complete == True:
        todo.complete = False
    else:
        todo.complete = True"""
    todo.complete = not todo.complete # Yoruma aldığımız kısım ile aynı işlevi görüyor.

    db.session.commit()
    return redirect(url_for("index"))

@app.route("/add", methods = ["POST"])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title = title, complete = False) #Obje oluşturduk.
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

if __name__ == "__main__":
    db.create_all() #Bu fonksiyon ile oluşturduğumuz bütün class'lar database'e bir tablo olarak eklenecek.
    app.run(debug=True)