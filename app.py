import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session
from database import (
    get_all_events,
    search_events,
    get_user,
    add_event,
    get_event_by_id,
    update_event,
    delete_event,
    count_events,
    total_capacity,
    upcoming_events,
    next_event,
    register_event,
    is_registered,
    get_all_registrations,
    total_registrations,
    recent_registrations,
    count_registrations,
    count_users,
    registration_exists,
    add_user,
    user_exists,
    get_my_events,
    cancel_registration,
    most_popular_event,
    least_popular_event,
    event_capacity_status,
    home_statistics,
    upcoming_event_list,
    registration_chart_data
)

app = Flask(__name__)

app.secret_key = "campus_event_secret"

@app.context_processor
def ui_context():
    from datetime import date
    return {"today": date.today().isoformat()}

from functools import wraps
def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if session.get("role") != "Admin":

            return render_template("403.html"), 403

        return f(*args, **kwargs)

    return decorated_function

DATABASE = "events.db"

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():

    total_events, total_users, total_registrations, upcoming = home_statistics()

    upcoming_list = upcoming_event_list()

    return render_template(
        "index.html",
        total_events=total_events,
        total_users=total_users,
        total_registrations=total_registrations,
        upcoming=upcoming,
        upcoming_list=upcoming_list
    )

@app.route("/events")
def events():

    keyword = request.args.get("search", "").strip()

    if keyword:
        events = search_events(keyword)
    else:
        events = get_all_events()

    return render_template(
        "events.html",
        events=events,
        keyword=keyword
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user_id = request.form["user_id"]

        user = get_user(user_id)

        if user:

            session["user_id"] = user["user_id"]
            session["name"] = user["name"]
            session["role"] = user["role"]

            return redirect(url_for("home"))

        flash("User ID does not exist.", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    
    return redirect(url_for("home"))

@app.route("/event/<int:event_id>")
def event_details(event_id):

    event = get_event_by_id(event_id)

    if not event:
        return "Event not found", 404
    
    registered = count_registrations(event_id)
    remaining = event["capacity"] - registered
    
    return render_template(
        "event_details.html",
        event=event,
        registered=registered,
        remaining=remaining
    )

@app.route("/my-events")
def my_events():
    
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))
    
    events = get_my_events(session["user_id"])

    return render_template(
        "my_events.html",
        events=events
    )

@app.route("/statistics")
@admin_required
def statistics():

    total = count_events()
    
    capacity = total_capacity()

    upcoming = upcoming_events()

    next_evt = next_event()

    users = count_users()

    registrations = total_registrations()

    most_event = most_popular_event()

    least_event = least_popular_event()

    recent = recent_registrations()

    capacity_status = event_capacity_status()

    chart_data = registration_chart_data()

    return render_template(
        "statistics.html",
        total=total,
        users=users,
        registrations=registrations,
        capacity=capacity,
        upcoming=upcoming,
        next_event=next_evt,
        most_event=most_event,
        least_event=least_event,
        recent=recent,
        capacity_status=capacity_status,
        chart_data=chart_data
    )

@app.route("/registrations")
@admin_required
def registrations():
    registrations = get_all_registrations()

    return render_template(
        "registrations.html",
        registrations=registrations
    )

@app.route("/search")
def search():
    return redirect(url_for("events", search=request.args.get("keyword", "")))

@app.route("/add-event", methods=["GET", "POST"])
@admin_required
def add_event_page():

    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        location = request.form["location"]
        capacity = request.form["capacity"]

        add_event(name, date, location, capacity)

        return render_template(
            "success.html",
            title="Event Created Successfully!",
            message="Redirecting to Events..."
        )

    return render_template("add_event.html")

@app.route("/edit-event/<int:event_id>", methods=["GET", "POST"])
@admin_required
def edit_event_page(event_id):

    event = get_event_by_id(event_id)

    if not event:
        return "Event not found", 404

    if request.method == "POST":

        name = request.form["name"]
        date = request.form["date"]
        location = request.form["location"]
        capacity = request.form["capacity"]

        update_event(
            event_id,
            name,
            date,
            location,
            capacity
        )

        return render_template(
            "success.html",
            title="Event Updated Successfully!",
            message="Redirecting to Events..."
        )

    return render_template(
        "edit_event.html",
        event=event
    )

@app.route("/delete-event/<int:event_id>")
@admin_required
def delete_event_page(event_id):
    delete_event(event_id)

    return render_template(
    "success.html",
    title="Event Deleted Successfully!",
    message="Redirecting to Events..."
)

@app.route("/register/<int:event_id>", methods=["GET", "POST"])
def register_page(event_id):

    event = get_event_by_id(event_id)

    if not event:
        return "Event not found", 404

    if "user_id" not in session:

        flash("Please login first.", "warning")

        return redirect(url_for("login"))

    registered = count_registrations(event_id)
    remaining = event["capacity"] - registered

    user_id = session.get("user_id")

    already_registered = registration_exists(user_id, event_id)

    if request.method == "POST":

        if remaining <= 0:

            flash("This event is already full.", "danger")

            return redirect(
                url_for(
                    "register_page",
                    event_id=event_id
                )
            )

        if already_registered:

            flash(
                "You have already registered for this event.",
                "warning"
            )

            return redirect(
                url_for(
                    "register_page",
                    event_id=event_id
                )
            )

        register_event(user_id, event_id)

        return render_template(
            "success.html",
            title="Registration Successful!",
            message="Redirecting to Events..."
        )

    return render_template(
        "register_event.html",
        event=event,
        registered=registered,
        remaining=remaining,
        already_registered=already_registered
    )

@app.route("/register", methods=["GET", "POST"])
def register_account():

    if request.method == "POST":

        user_id = request.form["user_id"].strip()
        name = request.form["name"].strip()

        if user_exists(user_id):

            flash("User ID already exists.", "danger")

            return redirect(url_for("register_account"))

        add_user(user_id, name)

        flash("Account created successfully. Please login.", "success")

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/cancel-registration/<int:event_id>")
def cancel_registration_page(event_id):

    if "user_id" not in session:

        flash("Please login first.", "warning")

        return redirect(url_for("login"))

    cancel_registration(
        session["user_id"],
        event_id
    )

    flash("Registration cancelled successfully.", "success")

    return redirect(url_for("my_events"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)