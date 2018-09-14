from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField


class NeTextForm(FlaskForm):
    carrier = RadioField('', choices=[('att', 'att'), ('verizon', 'verizon'), ('uscc', 'uscc')])
    first_name = StringField()
    last_name = StringField()
    search_first = StringField()
    search_last = StringField()
    phone_num = StringField()
    search = StringField()
    submit = SubmitField('Submit')
