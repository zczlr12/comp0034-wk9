from pathlib import Path
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle


def create_model(alg):
    """Creates a model using the algorithm provided. Output serialised using pickle.

    Args:
    alg: either lr (LogisticRegression) or dt (DecisionTreeClassifier)

    Returns:
    .pkl Pickled model

    """
    # Check if the model.pkl file exists
    path_exists = Path.exists(Path(__file__).parent.joinpath("model.pkl"))

    if not path_exists:
        # Read the data into a DataFrame
        iris_file = Path(__file__).parent.joinpath("data", "iris.csv")
        df = pd.read_csv(iris_file)

        # Convert categorical data to numeric
        le = LabelEncoder()
        df["species"] = le.fit_transform(df["species"])

        # X = feature values (case sepal length, sepal width, petal length, petal width)
        X = df.iloc[:, 0:-1]
        X = X.values
        # y = target values, last column of the data frame
        y = df.iloc[:, -1]

        # Split the data into 80% training and 20% testing (type of iris)
        x_train, x_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Initialize the model
        if alg == "dt":
            model = DecisionTreeClassifier()
        elif alg == "lr":
            model = LogisticRegression()
        else:
            raise ValueError("Must provide either 'dt' (DecisionTree) or 'lr' (LogisticRegression)")

        # Train the model
        model.fit(x_train, y_train)

        # Pickle the model and save current folder
        pickle_file = Path(__file__).parent.joinpath("model.pkl")
        pickle.dump(model, open(pickle_file, "wb"))
