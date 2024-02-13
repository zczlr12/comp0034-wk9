from flask import current_app as app, render_template, flash, request, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from paralympics_flask.figures import line_chart
from paralympics_flask import db
from paralympics_flask.forms import EventForm
from paralympics_flask.models import Event, Region


@app.route('/', methods=['GET'])
def index():
    """ Returns the home page."""
    events = db.session.execute(db.select(Event).order_by(Event.year)).scalars()
    return render_template('index.html', events=events)


@app.get('/events/<event_id>')
def get_event(event_id):
    """ Returns an event details page. """
    event = db.get_or_404(Event, event_id)
    return render_template('event.html', event=event)


@app.route("/events", methods=["GET", "POST"])
def add_event():
    """ Adds a new event to the database. """
    # Create a form, if this is a POST then it will have the values from the form, otherwise empty fields
    form = EventForm(request.form)

    # If the form passes the validators set in the EventForm field
    if form.validate_on_submit():
        # Empty event object
        event = Event()
        # Add attributes to the event object using the form fields
        form.populate_obj(event)

        # Change the event.country from an object to just the region name
        country = event.country.region
        event.country = country

        # Find the region to add the foreign key field to the event
        region = db.session.execute(db.select(Region).filter_by(region=country)).scalar_one()
        event.NOC = region.NOC

        # Calculate the duration by subtracting the start date from the end date if they are not None
        if event.start and event.end:
            duration = event.end - event.start
            # duration is a timedelta so get just the days as this will be an int
            event.duration = duration.days

        # disabilites_included from the form is a list even when empty, the database expects a string not a list
        # Convert the list to a string
        disabilities = ','.join(map(str, event.disabilities_included))
        event.disabilities_included = disabilities

        # Check that the event host and year do not already exist.
        exists = db.session.execute(db.select(Event).filter_by(country=event.country, year=event.year)).first()
        if not exists:
            try:
                db.session.add(event)
                db.session.commit()
                # If successful, return to the homepage and use Flask Flash to display a success message
                flash('Event added!', 'success')
                return redirect(url_for('index'))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'An error occured while saving.{e}', 'error')
                return render_template('add_event.html', form=form)
        else:
            flash('This event already exists.', 'error')
            render_template('add_event.html', form=form)

    # Otherwise display the page with the Event template
    return render_template('add_event.html', form=form)


@app.get('/chart')
def display_chart():
    """ Returns a page with a line chart. """
    line_fig_html = line_chart(feature="participants", db=db)
    return render_template('chart.html', fig_html=line_fig_html)
