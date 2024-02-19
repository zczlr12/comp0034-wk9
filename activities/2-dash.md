# Plotly Dash version of the activities

Please complete the [test intro](1-testintro.md) before starting this part of the activities.

The examples below pick some of the trickier ways to find elements on a page and interact with them as these are less
easy to find in the documentation.

For the coursework, you may be able to avoid these using ids and classes to find elements. This is harder to control in
Dash than in Flask apps though as the chart HTML is rendered by Plotly and not directly defined by you.

Contents:

- [Check the Dash app runs](#check-the-dash-app-runs)
- [Configure the chrome driver](#configure-the-chrome-driver)
- [Use the dash_duo fixture to run the app](#use-the-dash_duo-fixture-to-run-the)
- [Write a test to check that the server is up and running](#write-a-test-to-check-that-the-server-is-up-and-running)
- [Write a test that uses the chrome driver to access an element on the page](#write-a-test-that-uses-the-chrome-driver-to-access-an-element-on-the-page)
- [Write a test that uses the chrome driver to carry out a series of user actions](#write-a-test-that-uses-the-chrome-driver-to-carry-out-a-series-of-user-actions)
- [Write a test where you do not know the id, class or tag of an element](#write-a-test-where-you-do-not-know-the-id-class-or-tag-of-an-element)
- [Links for more info](#links)

## Check the Dash app runs

1. `python src/paralympics_dash/paralympics_dash.py`
2. Go to the URL that is shown in the terminal. By default, this is <http://127.0.0.1:8050>.
3. Stop the app using `CTRL+C`

## Configure the chrome driver

This assumes you already completed the testing intro activity and have downloaded a chrome driver to your computer.

Add the following to `conftest.py`. This is not a fixture, however pytest will automatically use anything
in `conftest.py`.

There following optimises the configuration for running tests on GitHub. However, if you want to run the tests on your
computer and see what is happening then rather than setting "headless" instead set to "maximised-window".

```python
import os
from selenium.webdriver.chrome.options import Options


def pytest_setup_options():
    """pytest extra command line arguments for running chrome driver

     For GitHub Actions or similar container you need to run it headless.
     When writing the tests and running locally it may be useful to
     see the browser and so you need to see the browser.
    """
    options = Options()
    if "GITHUB_ACTIONS" in os.environ:
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
    else:
        options.add_argument("start-maximized")
    return options

```

## Use the dash_duo fixture to run the

The `dash_duo` fixture is used to run the Dash app in a local server for testing. This fixture is available once you
have
installed `dash[testing]`.

Plotly testing documentation examples define the app to be tested inside each test case.

[This post in the plotly forum](https://community.plotly.com/t/how-you-can-integration-test-your-app-by-dash-testing/25002)
which
recommends using a function called `import_app` which is imported from `dash.testing.application_runners`.

I cannot find any examples or documentation of creating the app as a fixture that is only run once per session. It
relies on the dash_duo fixture which has a function scope.

You need to explicitly start the server, though there is no method to stop the server, this is handled by the fixture at
the end of each test.

An example of how to do this within a test for the paralympics_dash app where the package name is paralympics_dash and
the module is paralympics_app.py:

```python
from dash.testing.application_runners import import_app


def test_server_live(dash_duo):
    # Create the app
    app = import_app(app_file="paralympics_dash.paralympics_app")
    # Start the server with the app using the dash_duo fixture
    dash_duo.start_server(app)

    # test code will follow here
```

Note: It causes issues when trying to create the app in the tests if the package and the module that runs the app have
the same name so please avoid this.

## Write a test to check that the server is up and running

You can specify which URL to run the server on. However, to avoid needing to know this, the following code gets the
server url and then uses that in the test.

The Python requests library is used to make a HTTP request to the server. This returns
a [response object](https://www.w3schools.com/python/ref_requests_response.asp) allowing you to check the status_code,
content, headers etc.

You can then use pytest assertions to check for a condition.

You can add this to `test_paralympics_dash.py`:

```python
import requests
from dash.testing.application_runners import import_app


def test_server_live(dash_duo):
    """
    GIVEN the app is running
    WHEN a HTTP request to the home page is made
    THEN the HTTP response status code should be 200
    """

    # Start the app in a server
    app = import_app(app_file="paralympics_dash.paralympics_app")
    dash_duo.start_server(app)

    # Delay to wait 2 seconds for the page to load
    dash_duo.driver.implicitly_wait(2)

    # Get the url for the web app root
    # You can print this to see what it is e.g. print(f'The server url is {url}')
    url = dash_duo.driver.current_url

    # Requests is a python library and here is used to make a HTTP request to the sever url
    response = requests.get(url)

    # Finally, use the pytest assertion to check that the status code in the HTTP response is 200
    assert response.status_code == 200
```

Run the test e.g. `pytest -v` in a terminal, or use a run test function in your IDE.

## Write a test that uses the chrome driver to access an element on the page

The next example uses the driver rather than requests to navigate to a url. The driver allows you to navigate the web
page and carry out actions such as clicking, selecting, entering data in forms etc. This is not a HTTP request, i.e. you
will not get a response object back; instead you get a value from an element on the page and use that with an assertion.

This example waits until an element, the 'h1' heading appears, rather than waiting a set amount of time as was used in
the previous test.

There are some [shorthand API functions](https://dash.plotly.com/testing#browser-apis) that are provided by
the `dash_duo` fixture, e.g. `dash_duo.find_element("h1")`. You can also
use [selenium functions found in their documentation](https://www.selenium.dev/documentation/webdriver/) or
on [this site](https://selenium-python.readthedocs.io/api.html) by using
`dash_duo.driver` then appending the function e.g. `dash_duo.driver.find_element(By.TAG_NAME, "h1")`

```python
def test_home_h1textequals(dash_duo):
    """
    GIVEN the app is running
    WHEN the home page is available
    THEN the H1 heading text should be "Paralympics Dashboard"
    """
    app = import_app(app_file="paralympics_dash.paralympics_app")
    dash_duo.start_server(app)

    # Wait for the H1 heading to be visible, timeout if this does not happen within 4 seconds
    dash_duo.wait_for_element("h1", timeout=4)

    # Find the text content of the H1 heading element
    h1_text = dash_duo.find_element("h1").text

    # Check the heading has the text we expect
    assert h1_text == "Paralympics Dashboard"
```

Run the test.

## Write a test where you do not know the id, class or tag of an element

This next example uses the driver to make a selection from a dropdown menu before trying to find a value to assert.

A further complication is that the element that changes is the chart. The chart is HTML generated by Plotly, and do you
do not have control over the use of tags, classes, ids etc.

If you run the Dash app, open it in Chrome, right-click on the chart and then Inspect you should be taken to the
developer console into the Element window to the element you clicked on. You will need to expand the elements in
the `<div id='map'>` then `<div class=plot-container plotly>` section until you find the element with `class="main-svg"`
and then the one with `class=infolayer` then `class=g-gtitle`. Once you find the title, if you right-click there are
options to 'copy selector' and 'copy full Xpath'.

![Chrome Inspector to find css selector or xpath](chrome-selector.png)

If you copy the selector, you can then paste to this to your code to define the element:

```python
css_selector = '#line > div.js-plotly-plot > div > div > svg:nth-child(3) > g.infolayer > g.g-gtitle > text'
chart_title = dash_duo.find_element(css_selector)
```

If you copy the Xpath it looks more like this which you can then use with the selenium driver `find_element(By.XPATH)`:

```python
from selenium.webdriver.common.by import By

fullxpath = '/html/body/div/div/div/div[3]/div[1]/div/div/div[3]/div[1]/div/div[2]/div/div/svg[2]/g[4]/g[2]/text'
chart_title = dash_duo.driver.find_element(By.XPATH, xpath)
```

Note: xpath fails for me but the css-selector approach worked.

```python
def test_line_chart_selection(dash_duo):
    """
    GIVEN the app is running
    WHEN the dropdown for the line chart is changed to
    THEN the H1 heading text should be "Paralympics Dashboard"
    """
    app = import_app(app_file="paralympics_dash.paralympics_app")
    dash_duo.start_server(app)
    # To find an element by id you use '#id-name'; to find an element by class use '.class-name'
    dash_duo.wait_for_element("#type-dropdown", timeout=2)

    # See https://github.com/plotly/dash/blob/dev/components/dash-core-components/tests/integration/dropdown/test_dynamic_options.py#L31
    # Not easy to follow but give syntax for selecting values in a dropdown list
    dropdown_input = dash_duo.find_element("#type-dropdown")
    dropdown_input.send_keys("Sports")
    dash_duo.driver.implicitly_wait(2)

    # Run the app and use Chrome browser, find the element, right click and choose Select, find the element in the 
    # Elements console and select 'copy selector'. Pate this as the value of the variable e.g. see css_selector below.
    css_selector = '#line > div.js-plotly-plot > div > div > svg:nth-child(3) > g.infolayer > g.g-gtitle > text'
    chart_title = dash_duo.find_element(css_selector)
    assert ("sports" in chart_title.text), "'sports' should appear in the chart title"

```

## Write a test that uses the chrome driver to carry out a series of user actions

For this test:

- Find the <div id=card></div> which should initially have no children or no elements below it. You could do this using
  syntax like `parent.findElements(By.xpath("./child::*"))` which should be empty. The code below counts the number of
  cards on the page which should be 0.
- Find the chart with the 'id=map'
- Find a map marker and hover which should display a card. This will require the Chrome Inspector again to get the
  selector for a point.
- Find the <div id=card></div> again, could the number of cards in it which should now be 1.

[Selenium interaction functions](https://www.selenium.dev/documentation/webdriver/elements/interactions/) include
click(), send_keys(), submit() and clear(). To cover is more complex and requires the use of
the [Actions API](https://www.selenium.dev/documentation/webdriver/actions_api/).

```python
from selenium.webdriver import ActionChains


def test_map_marker_select_updates_card(dash_duo):
    """
    GIVEN the app is running which has a <div id='map>
    THEN there should not be any elements with a class of 'card' one the page
    WHEN a marker in the map is selected
    THEN there should be one more card on the page then there was at the start
    AND there should be a text value for the h6 heading in the card
    """
    app = import_app(app_file="paralympics_dash.paralympics_app")
    dash_duo.start_server(app)
    # Wait for the div with id of card to be on the page
    dash_duo.wait_for_element("#card", timeout=2)
    # There is no card so finding elements with a bootstrap class of 'card' should return 0
    cards = dash_duo.driver.find_elements(By.CLASS_NAME, "card")
    cards_count_start = len(cards)

    # Find the first map marker
    marker_selector = '#map > div.js-plotly-plot > div > div > svg:nth-child(1) > g.geolayer > g > g.layer.frontplot > g > g > path:nth-child(1)'
    marker = dash_duo.driver.find_element(By.CSS_SELECTOR, marker_selector)
    # Use the Actions API and build a chain to move to the marker and hover
    ActionChains(dash_duo.driver).move_to_element(marker).pause(1).perform()

    # Check there is now 1 card on the page
    cards_end = dash_duo.driver.find_elements(By.CLASS_NAME, "card")
    cards_count_end = len(cards_end)
    # There should be 1 more card
    assert cards_count_end - cards_count_start == 1

    # Wait for the element with class of 'card'
    dash_duo.wait_for_element(".card", timeout=1)
    # Find the h6 element of the card
    card = dash_duo.find_element("#card > div > div > h6")
    # The test should be Rome as it is the first point, though this assertion just checks the length of the text
    assert len(card.text) > 2
```

Run the test.

## Try it yourself

Run the Dash app so that you know what it contains.

Try to identify a few more tests you could write.

Write the tests and try running them.

## Links

Dash have [tests for their code in GitHub](https://github.com/plotly/dash/tree/dev/tests). It can be useful
to see how they structure their own tests.

[Sean McCarthy's Dash testing tutorial](https://mccarthysean.dev/005-03-Dash-Testing). He uses the dash_thread_server
and dash_br fixtures rather than dash_duo, however it gives a number of examples of different ways to select elements on
the page for testing.

[Building unit tests for dash applications](https://plotly.com/blog/building-unit-tests-for-dash-applications/). This
goes beyond what is expected for the coursework and tests callbacks and uses mocks. Useful if you are already familiar
with testing and want to expand your knowledge.

[Plotly Dash Testing official documentation](https://dash.plotly.com/testing)

