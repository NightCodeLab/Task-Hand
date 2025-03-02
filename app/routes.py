from flask import render_template, redirect, session, request
from app import app, db, bcrypt
from app.models import User, Task

def user_logged_in():
    return "user_id" in session

@app.route("/")
def index():
    return redirect("/notes" if user_logged_in() else "/register")

@app.route("/register", methods=["GET", "POST"])
def register():
    if user_logged_in():
        return redirect("/notes")
    
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode('utf-8')
        
        user = User(name=name, username=username, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            return redirect("/notes")
        except Exception as e:
            return str(e)
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if user_logged_in():
        return redirect("/notes")
    
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            session["user_id"] = user.id
            return redirect("/notes")
        return "ERROR"
    
    return render_template("login.html")

@app.route("/notes", methods=["GET", "POST"])
def notes():
    if user_logged_in():
        return render_template("notes.html", notes=Task.query.filter_by(user_id=session["user_id"]).all())
    return redirect("/register")

@app.route("/note-create", methods=["GET", "POST"])
def note_create():
    if user_logged_in():
        if request.method == "POST":
            note = Task(title=request.form["title"], text=request.form["text"], user_id=session["user_id"])
            try:
                db.session.add(note)
                db.session.commit()
                return redirect("/notes")
            except Exception as e:
                return str(e)
        
        return render_template("note_create.html")
    return redirect("/register")

@app.route("/delete-note/<int:id>")
def delete_note(id):
    if user_logged_in():
        note = Task.query.get(id)
        if note and note.user_id == session["user_id"]:
            db.session.delete(note)
            db.session.commit()
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")
