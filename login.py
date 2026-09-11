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
@app.route("/update/<int:id>",methods=["GET","POST"])
def update(id):
    user = User.query.get(id)
    if request.method=="POST":
        user.name=request.form["name"]
        user.email=request.form["email"]
        user.password=request.form["password"]
        db.session.commit()
        
        return redirect(url_for("users"))
    return render_template("update.html",user=user)
@app.route("/delete/<int:id>")
def delete(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
      
    return redirect(url_for("users"))
if __name__=="__main__":
    app.run(debug=True)