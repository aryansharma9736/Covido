from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class AddForm(FlaskForm):

    id = IntegerField('ID of the record',validators=[DataRequired()])
    name = StringField('Name of the hospital:',validators=[DataRequired()])
    beds = IntegerField('No. of beds available',validators=[DataRequired()])
    cylinder = IntegerField('No. of oxygen cylinders available ',validators=[DataRequired()])
    phone = IntegerField('Contact of hospital',validators=[DataRequired()])
    source_name = StringField('Name of Source',validators=[DataRequired()])
    numbers = IntegerField('Contact number of source',validators=[DataRequired()])
    submit = SubmitField('Submit')



class DelForm(FlaskForm):

    id = IntegerField('Id Number of Hospital to Remove:')
    submit = SubmitField('Remove Hospital')
