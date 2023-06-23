import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCaptchaModel
from exts import db


class RegisterForms(wtforms.Form):

    email = wtforms.StringField(validators=[Email("email form wrong !")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="captcha form wrong !")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="username form wrong !")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="password form wrong !")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    def validate_email(self, filed):
        email = filed.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="The email has been registered")

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()

        if not captcha_model:
            raise wtforms.ValidationError(message="code wrong!")
        else:
            db.session.delete(captcha_model)
            db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email("email form wrong !")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="password form wrong !")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=1, max=100, message="title form wrong !")])
    content = wtforms.StringField(validators=[Length(min=3,  message="content form wrong !")])


class AnswerForm(wtforms.Form):
    question_id = wtforms.IntegerField(validators=[InputRequired(message="must input something")])
    content = wtforms.StringField(validators=[Length(min=3,  message="content form wrong !")])

