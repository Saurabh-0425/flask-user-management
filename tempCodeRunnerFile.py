from flask import Flask,session,request,Response,redirect,url_for,render_template,flash
from flask_sqlalchemy import SQLAlchemy
from forms import Registration
app = Flask(__name__)
app.secret_key="123"
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
        user = User(name=name,password=password,email=email)
        db.session.add(user)
        db.session.commit()
        if name=="saurabh" and password =="12345678":
              session["user"]= name
              return redirect(url_for("dashboard"))
        else :
            flash(f"Inavlid Credentials")
    return render_template("login.html",form=form)
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html",user = session["user"])
    return redirect("invalid")
@app.route("/invalid")
def invalid():
    return render_template("invalid.html")

if __name__=="__main__":
    app.run(debug=True)