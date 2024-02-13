from decimal import Decimal

from flask_wtf import FlaskForm
from wtforms import DecimalField
from wtforms.validators import DataRequired


class PredictionForm(FlaskForm):
    """Fields to a form to input the values required for an iris species prediction"""

    # Uses DecimalField not float see https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.DecimalField

    # The , render_kw={'step': '0.1'} pass the 'step=1' parameter to the HTML input so the values goes -0.1, 0.2 etc.
    # when the arrow keys are used
    sepal_length = DecimalField(validators=[DataRequired()], default=Decimal(0.2), render_kw={'step': '0.1'})
    sepal_width = DecimalField(validators=[DataRequired()], default=Decimal(0.2), render_kw={'step': '0.1'})
    petal_length = DecimalField(validators=[DataRequired()], default=Decimal(0.2), render_kw={'step': '0.1'})
    petal_width = DecimalField(validators=[DataRequired()], default=Decimal(0.2), render_kw={'step': '0.1'})
