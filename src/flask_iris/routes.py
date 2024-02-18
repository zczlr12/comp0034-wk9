from pathlib import Path
import pickle
from flask import render_template, current_app as app
import numpy as np
from flask_iris.forms import PredictionForm


@app.route("/", methods=["GET", "POST"])
def index():
    """Create the homepage"""
    form = PredictionForm()

    if form.validate_on_submit():
        # Get all values from the form
        features_from_form = [
            form.sepal_length.data,
            form.sepal_width.data,
            form.petal_length.data,
            form.petal_width.data,
        ]

        # Make the prediction
        prediction = make_prediction(features_from_form)

        prediction_text = f"Predicted Iris type: {prediction}"

        return render_template(
            "index.html", form=form, prediction_text=prediction_text
        )
    return render_template("index.html", form=form)


def make_prediction(flower_values):
    """Takes the flower values, makes a model using the prediction and returns a string of the predicted flower variety

    To make a prediction with the model:
    prediction = model.predict(
        [[sepal_length, sepal_width, petal_length, petal_width]])
    e.g. p = model.predict([[5.1,3.5,1.4,0.2]])
    To access the prediction value use p[0]

    Parameters:
    flower_values (List): List of sepal length, sepal width, petal length, petal width

    Returns:
    variety (str): Name of the predicted iris variety
    """

    # Convert to a 2D numpy array with float values, needed as input to the model
    input_values = np.asarray([flower_values], dtype=float)

    # Get a prediction from the model
    pickle_file = Path(__file__).parent.joinpath("model.pkl")
    model = pickle.load(open(pickle_file, "rb"))
    prediction = model.predict(input_values)

    # convert the prediction to the variety name
    varieties = {0: "iris-setosa", 1: "iris-versicolor", 2: "iris-virginica"}
    variety = np.vectorize(varieties.__getitem__)(prediction[0])

    return variety
