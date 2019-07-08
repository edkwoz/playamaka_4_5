from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, FileField, RadioField, SelectField


class SupaPlayaMaka(FlaskForm):
    amount = IntegerField('How many files to input?')
    submit = SubmitField('Submit')
    filename = StringField('Enter file name')
    videofile = FileField('Select files', render_kw={'multiple': True})
    entryid = StringField('Entry ID')
    playerchoice = RadioField('Player Type', choices=[('standardplayer','Standard Player'),('audioplayer','Audio Player'), ('chapterplayer','Chapter Player')], default='standardplayer')
    width = StringField('Width', render_kw={"placeholder": "Width"})
    height = StringField('Height', render_kw={"placeholder": "Height"})
    downloadopts = RadioField('Player Type', choices=[('downloadable','Downloads Enabled'),('downloaddisable','Downloads Disabled')], default='downloadable')
    captionfile = FileField('Select files', render_kw={'multiple': True})
    sendmetadata = SubmitField('Populate video ids')
    folderpath = FileField('Select file')
    continuetonext = SubmitField('Continue')
    college = SelectField(
    'College',
    choices=[('CAS', 'CAS'), ('CFA', 'CFA'), ('COM', 'COM'), ('ENG', 'ENG'), ('GMS', 'GMS'), ('LAW', 'LAW'), ('MET/AR', 'MET/AR'),
    ('MET/CIS', 'MET/CIS'), ('MET/CJ', 'MET/CJ'), ('CET/CPE', 'MET/CPE'), ('MET/HCOM', 'MET/HCOM'), ('MET/MS_M', 'MET/MS_M'), ('MET/ODE', 'MET/ODE'), ('MET/UDCP', 'MET/UDCP'), ('PUBLIC', 'PUBLIC'),
    ('SAR', 'SAR'), ('SED', 'SED'), ('SMG', 'SMG'), ('SSW/IGSW', 'SSW/IGSW'), ('SSW/MSW', 'SSW/MSW'), ('STH', 'STH')]
    )
    course = StringField('Course number', render_kw={"placeholder": "Course"})
