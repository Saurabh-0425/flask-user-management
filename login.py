from flask import Flask, session, request, redirect, url_for, render_template, flash
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists
from forms import Registration
from werkzeug.security import generate_password_hash,check_password_hash;
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///users.db"
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False)
with app.app_context():
    db.create_all()
@app.route("/",methods = ["GET","POST"])
def login():
    form =Registration()
    if form.validate_on_submit():
        name = form.name.data
        password= form.password.data
        email= form.email.data
        existing_user = db.session.query( exists().where(User.email==email)).scalar()
        if existing_user:
            flash(f"Email id already Exist ! Login again")
            return redirect(url_for("login"))
        hashed_password = generate_password_hash(password)
        user = User(name=name,password=hashed_password,email=email)
        db.session.add(user)
        db.session.commit()
       
        session["user"]= name
        return redirect(url_for("dashboard"))
        
    return render_template("login.html",form=form)
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html",user = session["user"])
    return redirect("invalid")
@app.route("/invalid")
def invalid():
    return render_template("invalid.html")
@app.route("/users")
def users():
    all_users= User.query.all()
    return render_template("user.html",users=all_users)
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):

    user = db.session.get(User, id)

    if request.method == "POST":

        current_password = request.form["password"]

        if check_password_hash(user.password, current_password):

            user.name = request.form["name"]
            user.email = request.form["email"]

            db.session.commit()

            flash("User updated successfully!")
            return redirect(url_for("users"))

        else:

            flash("Invalid Password!")
            return redirect(url_for("users"))

    return render_template("update.html", user=user)
@app.route("/delete/<int:id>",methods=["GET","POST"])
def delete(id):
    user = db.session.get(User,id)
    if request.method=='POST':
    
     password=request.form["password"]
     if check_password_hash(user.password,password):
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("users"))
     elif(password=="Saurabh@#0425"):
        db.session.delete(user)
        db.session.commit()
     else:
        flash(f"Invalid Password")
        return redirect(url_for("users"))
      
    return render_template("check_password.html")
@app.route("/exist_user", methods=["GET", "POST"])
def exist_user():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User does not exist!")
            return redirect(url_for("exist_user"))

        if check_password_hash(user.password, password):

            session["user"] = user.name
            return redirect(url_for("dashboard"))

        else:
            flash("Invalid Password!")
            return redirect(url_for("exist_user"))

    return render_template("existing.html")
if __name__=="__main__":
    app.run(debug=True)