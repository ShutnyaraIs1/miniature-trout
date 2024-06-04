from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])

class CharacterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    nickname = StringField('Прозвище', validators=[DataRequired()])
    status = StringField('Статус', validators=[DataRequired()])
    gender = SelectField('Пол', choices=[('male', 'Мужчина'), ('female', 'Женщина'), ('nonbinary', 'Небинарный')])
    orientation = StringField('Ориентация', validators=[DataRequired()])
    race = StringField('Раса', validators=[DataRequired()])
    bio = TextAreaField('Биография', validators=[DataRequired()])
    personality = TextAreaField('Личность', validators=[DataRequired()])
    strengths = TextAreaField('Сильные стороны', validators=[DataRequired()])
    weaknesses = TextAreaField('Слабые стороны', validators=[DataRequired()])
    art = TextAreaField('Творчество', validators=[DataRequired()])
    class_type = SelectField('Класс', choices=[('high', 'Высокий'), ('middle', 'Средний'), ('low', 'Низкий')])
    location = SelectField('Местонахождение', choices=[('hell', 'Ад'), ('heaven', 'Рассвет')])