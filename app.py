from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired
from sqlalchemy.exc import IntegrityError
from hashlib import sha256

#===================================================

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ali:ali2004hh@localhost/login'
app.config["SECRET_KEY"] = "^#*al@12a110olopj)*(*/=2fkj>3o&^%$("
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#===================================================

class LoginForm(FlaskForm):
    username = TextField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    email = TextField(validators=[DataRequired()])

#=====================================================

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True,unique=True)
    username = Column(String(90),nullable=False,unique=True)
    password = Column(String(130),nullable=False)
    email = Column(String(150),nullable=False)
db.create_all()

#=======================================================

@app.route("/",methods=['POST','GET'])
def index():
    return render_template("index.html")

#===========================================================

@app.route("/login",methods=["POST","GET"])
def login():
    loginform = LoginForm()
    return(render_template("login.html",loginform=loginform))

#==========================================================

@app.route("/register",methods=["POST","GET"])
def rig():
    loginform = LoginForm()
    return(render_template("rig.html",loginform=loginform))

#==========================================================

@app.route("/log_res",methods=["POST","GET"])
def log():
    login_fr = LoginForm(request.form)
    if not login_fr.validate_on_submit():
            return "Error!!"
    use = request.form[('username')]
    passw = request.form[('password')]
    em = request.form [('email')]
    q = 'ascii'
    hashs = passw.encode()
    passw_ = sha256(hashs).hexdigest()
    user = User.query.filter(User.username == use, User.password == passw_,User.email == em).first()
    if not user:
        return("""<body dir="rtl">یوزر موجود نیست ):<br> یا پسورد درست نیست </br> یا ایمیلت </body>""")
    return("""<body dir="rtl"><h2 align="center">خوش امدی <br> {} </h2></body>""".format(user.username))

#==========================================================

@app.route("/delete_user")
def dele():
    loginform = LoginForm()
    return(render_template("del.html",loginform=loginform))

@app.route("/del_res",methods=["POST"])
def del_re():
    login_fr = LoginForm(request.form)
    if not login_fr.validate_on_submit():
            return "Error!!"
    use = request.form[('username')]
    passw = request.form[('password')]
    em = request.form[('email')]
    hashs = passw.encode()
    passw_ = sha256(hashs).hexdigest()
    user = User.query.filter(User.username == use, User.password == passw_,User.email == em).first()
    if not user:
        return("""<h2 dir="rtl" align="center">یوزر موجود نیست <br> یا رمز اشتباه است <br> یا ایمیل :(</h2>""")
    #===============
    db.session.delete(User.username)
    db.session.commit()

    return("""<h2 align="center">یوزر با موفقیت حذف شد</h2>""")

#==========================================================

@app.route("/re_res",methods=["POST","GET"])
def ri():
    login_fr = LoginForm(request.form)
    if not login_fr.validate_on_submit():
            return "Error!!"
    use = request.form[('username')]
    passw = request.form[('password')]
    em = request.form [('email')]
    hashs = passw.encode()
    passw_ = sha256(hashs).hexdigest()
    new_user = User()
    new_user.username = use
    new_user.password = passw_
    new_user.email = em
    try:
        db.session.add(new_user)
        db.session.commit()
        return("""<body dir="rtl"><h2 align="center">یوزر اضافه شد میتوانید از قسمت ورود وارد شوید</h2></br></br><h3 align="center">نام یوزر : {}</h3></br></br><h4 align="center" style="color:blue">رفتن به صفحه ورود<span style="color:red"><a href="/login">  [Click]</a></span></h4></body>""".format(use))
    except IntegrityError:
        db.session.rollback()
        return("""<body dir="rtl"><h1 align="center">یوزر تکراری است</h1><script>alert("یوزر موجود است یک یوزر دیگر بنویسید");</script></body>""")

#==========================================================

@app.errorhandler(404)
def notf (error):
	return (render_template ("404.html"))
#============================================================

if __name__ == '__main__':
	app.run('127.0.0.2')
