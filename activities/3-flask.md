# Flask version of the activities

## Testing the Iris Prediction app

## Check the app runs

Check that the app runs before starting any of the activities.

1. `flask --app "flask_iris:create_app('development')" run`
2. Go to the URL that is shown in the terminal. By default, this is http://127.0.0.1:5000
3. Stop the app using `CTRL+C`

## Create a fixture for the chrome driver

Add this to `conftest.py`:

```python
import os
import pytest
from selenium.webdriver import Chrome, ChromeOptions


@pytest.fixture(scope="module")
def chrome_driver():
    """
    Fixture to create a Chrome driver. 
    
    On GitHub or other container it needs to run headless, i.e. the browser doesn't open and display on screen.
    Running locally you may want to display the tests in a large window to visibly check the behaviour. 
    """
    options = ChromeOptions()
    if "GITHUB_ACTIONS" in os.environ:
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
    else:
        options.add_argument("start-maximized")
    driver = Chrome(options=options)
    yield driver
    driver.quit()
```

## Create a fixture to run the Flask app as a live server

If you are using `pytest-flask` then there is already a live_server fixture.

If you are using Windows you may need to try it and see if it works, last year it didn't work for windows, but they may
have corrected that.

Otherwise, you can create your own in `conftest.py`. Note: you will run into problems if you create two fixtures named
live_server so if you install pytest-flask and define your own, then change the name of your own.

The Flask app needs to run and be accessible in a browser simultaneously with tests being run. To achieve this; run the
app in a separate thread.

The first version should be OK on a Mac but will fail on Windows.

```python
import multiprocessing
import pytest
from paralympics_flask import create_app


@pytest.fixture(scope='session')
def app():
    """Fixture to create the Flask app and configure for testing"""
    test_cfg = {"TESTING": True, }
    app = create_app(test_config=test_cfg)
    yield app


@pytest.fixture(scope="session")
def live_server_iris(app):
    """Fixture to run the Flask app for Selenium tests
    
    This version runs on Mac only.
    """
    # start multiprocessing in fork only once per session
    try:
        multiprocessing.set_start_method("fork")
    except RuntimeError:
        pass

    process = multiprocessing.Process(target=app.run, args=())
    process.start()
    yield process
    process.terminate()
```

This version should work on MacOS and Windows.

```python
import subprocess
import time
import pytest


@pytest.fixture(scope='module')
def live_server_iris():
    """Fixture to run the Flask app as a live server.
    
    This version should run on Windows and mac
    """

    # Use subprocess to run the Flask app using the command line runner
    try:
        # You can customize the command based on your Flask app structure
        server_process = subprocess.Popen(
            ["flask", "--app", "flask_iris:create_app('test')", "run", "port", "5000"])
        # wait for the server to start
        time.sleep(2)
        yield server_process
        server_process.terminate()

    except subprocess.CalledProcessError as e:
        print(f"Error starting Flask app: {e}")
```    

## Write a test to check the server is up and running

This uses the requests library. The chrome driver navigates the page but does not get HTTP responses. Requests will make
a HTTP request and receive a HTTP response object.

You can [check the documentation](https://requests.readthedocs.io/en/latest/api/#requests.Response) to see what values
you can access from the response.

This test just checks that the app is running on the localhost on port 5000 so expects a status code of 200.

```python
import requests


def test_server_is_up_and_running(live_server_iris):
    """Check the app is running"""
    # Chrome_driver navigates to the page, whereas requests.get makes an HTTP request and returns an HTTP response
    response = requests.get("http://127.0.0.1:5000")
    assert response.status_code == 200
```

## Test that passes values to a form

You need to find the form fields on the page. The form field ids by default are set to the field name in
the `PredictionForm` class in `forms.py`.

The id for the button is defined in the `index.html` template.

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def test_prediction_returns_value(live_server_iris, chrome_driver):
    """
    GIVEN a chrome driver and live server running the Iris app
    WHEN appropriate values are passed to the prediction form
    THEN there should be element that has an id="prediction-text"
    """
    # Values to use in the test. You can find other values to use in 'data/iris.csv'
    iris = {"sepal_length": 4.8, "sepal_width": 3.0, "petal_length": 1.4, "petal_width": 0.1, "species": "iris-setosa"}

    # Go to the home page
    chrome_driver.get("http://127.0.0.1:5000/")

    # Wait until the form field for sep_len is present
    sep_len = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.NAME, "sepal_length")
    )

    # Complete the fields in the form. Clear the default values and then enter the values the iris variable defined earlier
    # sep_len = chrome_driver.find_element(By.ID, "sepal_length")
    sep_len.clear()
    sep_len.send_keys(iris["sepal_length"])
    sep_wid = chrome_driver.find_element(By.ID, "sepal_width")
    sep_wid.clear()
    sep_wid.send_keys(iris["sepal_width"])
    pet_len = chrome_driver.find_element(By.ID, "petal_length")
    pet_len.clear()
    pet_len.send_keys(iris["petal_length"])
    pet_wid = chrome_driver.find_element(By.ID, "petal_width")
    pet_wid.clear()
    pet_wid.send_keys(iris["petal_width"])
    
    # Click the submit button
    chrome_driver.find_element(By.ID, "btn-predict").click()
    
    # Wait for the prediction text to appear on the page and then get the <p> with the id=“prediction-text”
    pt = WebDriverWait(chrome_driver, timeout=3).until(lambda d: d.find_element(By.ID, "prediction-text"))
    
    # Assert that 'setosa' is in the text value of the <p> element.
    assert iris["species"] in pt.text
```

## Try it yourself

The iris app only has one function, to get a prediction. You could still write additional tests e.g. to check for
extreme values, to check for errors if you don't complete all the fields etc. See if you can write at least one more
test.
