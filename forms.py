from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
class InputForm(FlaskForm):
    periodLength = SelectField(label="Period Length", choices=[3, 5, 7, 10, 14])
    start_of_startDate = DateField('Start', format = '%d/%m/%Y')
    end_of_startDate = DateField()
    start_of_endDate = DateField()
    end_of_endDate = DateField()
    interval = SelectField(label='% Interval', choices=[1,2,3,4,5,6,7,8])
    submit = SubmitField()