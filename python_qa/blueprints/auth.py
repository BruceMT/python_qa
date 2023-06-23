from flask import Blueprint, request, render_template, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
from .forms import RegisterForms,LoginForm
#密码加密
from werkzeug.security import generate_password_hash, check_password_hash
import string
import random

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            #
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("not such user")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                # cookie
                session['user_id'] = user.id
                return redirect("/")
            else:
                print("password wrong")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))



@bp.route("/register", methods=['GET', 'POST'])
def register():
    #表单验证
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForms(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            #数据填入，密码加密
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            #重定向到login，用url_for实现直接用函数名字定向
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            #普通方法跳转
            return redirect("/auth/register")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@bp.route("/captcha/email")
def get_email_captcha():
    email = request.args.get("email")
    #随机取四位
    source = string.digits*4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)

    message = Message(subject="code", recipients=[email], body=f"Your code is: {captcha}")
    mail.send(message)
    #用数据库的方式存储
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()


    return jsonify({"code":200,"message":"","data":None})



#test email
@bp.route("/mail/test")
def mail_test():
    message = Message(subject="test", recipients=["brucemwb2018@gmail.com"], body="hello noob")
    mail.send(message)
    return "send success"
