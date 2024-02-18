# Plotly Dash version of the activities

Please complete the [test intro](1-testintro.md) before starting this part of the activities.

## Check the Dash app runs

1. `python src/paralympics_dash/paralympics_dash.py`
2. Go to the URL that is shown in the terminal. By default, this is <http://127.0.0.1:8050>.
3. Stop the app using `CTRL+C`

## Running the Dash app in tests

The `dash_duo` fixture runs the Dash app in a local server for testing. This fixture is available once you have
installed `dash[testing]`.

Plotly testing documentation examples define the app to be tested inside each test case.

[This post in the plotly forum](https://community.plotly.com/t/how-you-can-integration-test-your-app-by-dash-testing/25002)
which
recommends using a function called `import_app` which is imported from `dash.testing.application_runners`.

I cannot find any examples or documentation of creating the app as a fixture that is only run once per session. It
relies on the dash_duo fixture which has a function scope.

You can see the same approach used
in [Dash's own integration tests on GitHub](https://github.com/plotly/dash/tree/dev/tests/integration).

```python

```
