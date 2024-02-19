# Flask version of the activities: Paralympics Flask app

## Check the app runs

Check that the app runs before starting any of the activities.

1. `flask --app paralympics_flask run --debug`
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

This version of the activities assumes you are using `pytest-flask` with their live_server fixture. If you are using
Windows you may need to try it and see if it works, last year it didn't work for windows, but they may have corrected
that.

``

If you don't want to use `pytest-flask` then you can create your own `live_server` fixture in `conftest.py`:

The Flask app needs to run and be accessible in a browser, while tests are being executed. To achieve this the app needs
to be run in a thread.

Here is an example fixture based on this [forum post](https://github.com/pytest-dev/pytest-flask/issues/54):

```python
import socket
import subprocess
import time
import pytest


@pytest.fixture(scope="session")
def flask_port():
    """Gets a free port from the operating system."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port


@pytest.fixture(scope="session")
def live_server_flask(flask_port):
    """Runs the Flask app as a live server for Selenium tests (Paralympic app)

    Renamed to live_server_flask to avoid issues with pytest-flask live_server
    """
    # Construct the command string to run flask with formatted dictionary
    command = """flask --app 'paralympics_flask:create_app(test_config={"TESTING": True, "WTF_CSRF_ENABLED": False})' run --port """ + str(
        flask_port)
    try:
        server = subprocess.Popen(command, shell=True)
        # Allow time for the app to start
        time.sleep(3)
        yield server
        server.terminate()
    except subprocess.CalledProcessError as e:
        print(f"Error starting Flask app: {e}")
```

## Test the server is running

This uses the requests library. The chrome driver navigates the page but does not get HTTP responses. Requests will make
an HTTP request and receives an HTTP response object.

You can [check the documentation](https://requests.readthedocs.io/en/latest/api/#requests.Response) to see what values
you can access from the response. This test checks the status code is 200 and checks the content includes the word '
paralympics'.

Since the port is dynamically allocated then to get the home page url you need to get the port from the flask_port
fixture.

Add the code to `test_paralympics_flask.py` (or other file name):

```python
import requests


def test_server_is_up_and_running(live_server_flask, flask_port):
    """
    GIVEN a live server
    WHEN a GET HTTP request to the home page is made
    THEN the HTTP response should have a bytes string "paralympics" in the data and a status code of 200
    """
    url = f'http://127.0.0.1:{flask_port}/'
    response = requests.get(url)
    assert response.status_code == 200
    assert b"Paralympics" in response.content
```

Run the tests, e.g. `pytest -v` or a run tests command in your IDE.

## Test a value of an element on the page

This test uses the chrome_driver fixture to get information about the page. In this example the page title.

This introduces a wait for an expected condition.

```python
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_home_page_title(chrome_driver, live_server_flask, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    THEN the value of the page title should be "Paralympics - Home"
    """
    url = f'http://127.0.0.1:{flask_port}/'
    chrome_driver.get(url)
    # Wait for the title to be there and its value to be "Paralympics - Home", times out after 2 seconds
    WebDriverWait(chrome_driver, 2).until(EC.title_is("Paralympics - Home"))
    assert chrome_driver.title == "Paralympics - Home"
```

Add the code to your test module and run it to check it works.

## Test that navigates the page then gets a value from an element

This test requires:

- Go to the home page
- Click on the element with an id=1
- Find the element with an id=highlights
- Find the text value of the highlights element

This test uses
a [selenium interaction function](https://www.selenium.dev/documentation/webdriver/elements/interactions/). Interaction
functions include
click(), send_keys(), submit() and clear().

If you need other interactions, such as hover or click and hold then investigate
the [Actions API](https://www.selenium.dev/documentation/webdriver/actions_api/). There is an example of this in
the [dash tests](2-dash.md).

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def test_event_detail_page_selected(chrome_driver, live_server_flask, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND the user clicks on the event with the id="1"
    THEN the page should contain an element with the id "highlights" that contains "First Games" in the text
    """
    url = f'http://127.0.0.1:{flask_port}/'
    chrome_driver.get(url)
    # Wait until element with id="1" is on the page then click it (this will be the URL for Rome)
    # https://www.selenium.dev/documentation/webdriver/waits/
    el_1 = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "1")
    )
    el_1.click()
    # Clicking on the links takes you to the event details page for Rome
    # Wait until event highlights is visible
    highlight = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "highlights")
    )
    # Find the text value of the 
    assert "First Games" in highlight.text
```

## Test that passes values to a form

Please see [the Iris app test guidance](3-flask.md) which includes this.

## Using pytest-flask

`pytest-flask` requires you to create a fixture called `app` in `conftest.py`. 'live_server' has a scope of session by
default so the app fixture matches this.

Add this to `conftest.py`:

```python
import pytest
from paralympics_flask import create_app


@pytest.fixture(scope="session")
def app():
    """Fixture to create the paralympics_flask app and configure it for testing

    Required by the pytest-flask library; must be called 'app'
    See https://pytest-flask.readthedocs.io/en/latest/
    """
    test_cfg = {
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    }
    app = create_app(test_config=test_cfg)
    yield app
```

Note: I could not get pytest-flask to work with the chrome_driver fixture. If you wish to debug my
code [see](https://github.com/nicholsons/comp0034-wk9-complete/tree/master/tests/test_para_with_pytest_flask). If you
get it working please let me know the solution!

## Other options

I have not tried this but there is a [pretty printed video tutorial](https://www.youtube.com/watch?v=T-y3_T1HgTI)
covering the use of Playwright instead
of [Selenium Webrowser](https://playwright.dev/python/)