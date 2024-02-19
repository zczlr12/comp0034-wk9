# Flask version of the activities

## Check the Flask app runs

Check that the app runs before starting any of the activities.

1. `flask --app paralympics_flask run --debug`

   You may need to change the port number if you already have something running on the default port 5000
   e.g. `flask --app paralympics_flask run --debug --port=5050`.
2. Go to the URL that is shown in the terminal. By default, this is http://127.0.0.1:5000
3. Stop the app using `CTRL+C`

## Create a fixture to run the Flask app as a live server

If you are using `pytest-flask` then there is already a live server fixture. If you are using Windows you may need to
try
it and see if it works, last year it didn't work for windows, but they may have corrected that.

Otherwise, you can create your own in `conftest.py`.

The Flask app needs to run and be accessible in a browser, while tests are being executed. To achieve this the app needs
to be run in a thread.

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
def live_server(app):
    """Fixture to run the Flask app for Selenium tests"""
    process = multiprocessing.Process(target=app.run, args=())
    process.start()
    yield process
    process.terminate()
```

## Other options

I have not tried this but there is a [pretty printed video tutorial](https://www.youtube.com/watch?v=T-y3_T1HgTI) covering the use of Playwright instead
of [Selenium Webrowser](https://playwright.dev/python/)