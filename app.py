from flask import *  # Flask, render_template, url_for, request,check_password_hash
from forms import *
from flask_bootstrap import Bootstrap
from io import BytesIO
from captcha.image import ImageCaptcha
from random import randint
from models import *
from wtforms.validators import DataRequired, NoneOf
from flask_login import login_required, login_user

app = Flask(__name__)
app.config["SECRET_KEY"] = b'_5#y2L"Ffgjfgjh4Q8z\n\xec]/'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

bootstrap = Bootstrap(app)
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route("/", methods=["GET", "POST"])
def hello():
    # db.create_all()
    # return "<h1>初始化完成</h1>"
    return redirect(url_for("login"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route("/index")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            session["username"] = username
            flash("登录成功")
            return redirect(url_for("index"))
        else:
            flash("账号或密码错误")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    form.username.validators = [
        DataRequired("请填写此字段"),
        NoneOf(Ope_sqlit().get_ex_name(), "账号已存在"),
    ]

    if request.method == "POST" and form.validate_on_submit():
        if session["captcha"].lower() == form.captcha.data.lower():
            user = User(form.username.data, form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("注册成功")
            return redirect(url_for("login"))
        else:
            flash("验证码错误")
    # get请求或者是发生报错，都返回这个
    return render_template("register.html", form=form)


@app.route("/captcha")
def get_captcha():
    # image, code = gvcode.generate()生成的太模糊，不用了
    code = str(randint(1111, 9999))
    image = ImageCaptcha().generate_image(code)
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, "jpeg")
    buf_str = buf.getvalue()
    # 把buf_str作为response返回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers["Content-Type"] = "image/jpeg"
    # 将验证码字符串储存在session中
    session["captcha"] = code
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
