from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.core import StringField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired

class RedirectToFolder(FlaskForm):
    bucket_name = HiddenField('bucket_name')
    submit = SubmitField('Open')

class CreateFolderForm(FlaskForm):
    bucket_name = HiddenField('bucket_name')
    folder_name = StringField('folder_name',validators=[DataRequired()])
    submit = SubmitField('Create')

class RenameFileForm(FlaskForm):
    old_name = HiddenField('old_name')
    bucket_name = HiddenField('bucket_name')
    folder_name = HiddenField('folder_name')
    new_name = StringField('new_name')
    submit = SubmitField('Rename')
    