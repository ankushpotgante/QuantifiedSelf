from application.workers import celery
from application.models import Tracker, Log, User
from application.mail import send_email, send_alert_mail, send_html_report_mail
from datetime import datetime
from celery.schedules import crontab
import jinja2





@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(crontab(hour=14, minute=20), daily_remainders.s(), name="Daily remainder task")

    #sender.add_periodic_task(60.0, test_mail.s(), name="email task")

    sender.add_periodic_task(
        crontab(0,0, day_of_month=1),
        #crontab(hour=9, minute=21),
        monthly_reports.s(),
    )


def has_logs_today(tid):
    t = Tracker.query.get(tid)

    logs = t.logs.all()

    logs_today = []

    for l in logs:
        if l.log_time.date() == datetime.now().date():
            logs_today.append(l)

    return len(logs_today) > 0
    

def get_user_trackers_html(uid):
    e = jinja2.Environment()

    user = User.query.get(uid)

    template = e.from_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <style>
                table, tr, td, th{
                    border: 1px solid black;
                    border-collapse: collapse;
                }
            </style>
        </head>
        <body>
            Hello {{ user.first_name }}, <br>

            <p>Following are the trackers</p>

            <br>

            {% if user.trackers %}

                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Description</th>
                            <th>Tracker Type</th>
                            <th>Settings</th>
                            <th>Last Tracked</th>
                        </tr>
                    </thead>

                    <tbody>
                        {% for t in user.trackers %}
                        <tr>
                            <td>{{t.name}}</td>
                            <td>{{t.description}}</td>
                            <td>{{t.tracker_type}}</td>
                            <td>{{t.settings}}</td>
                            <td>{{t.last_tracked}}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>

            {% else %}
                <h4>You don't have any tracker</h4>
            {% endif %}
                <br><br>
            <p>Thank you!</p>
        </body>
        </html>
    """)

    result_html = template.render(user=user)

    return result_html


def get_tracker_html(tid):
    e = jinja2.Environment()

    tracker = Tracker.query.get(tid)

    user = User.query.get(tracker.uid)

    template = e.from_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <style>
                table, tr, td, th{
                    border: 1px solid black;
                    border-collapse: collapse;
                }
            </style>
        </head>
        <body>
            Hello {{ user.first_name }}, <br>

            <h3>Tracker Details</h3>
            <p>Name: {{ tracker.name }}</p>
            <p>Description: {{ tracker.description1 }}</p>
            <p>Type: {{ tracker.tracker_type }}</p>
            <p>Settings: {{ tracker.settings }}</p>
            <p>Last tracked: {{ tracker.last_tracked }}</p>

            <br>

            {% if tracker.logs %}
                <h3>Logs</h3>
                <table>
                    <thead>
                        <td>
                            <th>Time</th>
                            <th>Value</th>
                            <th>Notes</th>
                        </td>
                    </thead>
                    <tbody>
                        {% log in tracker.logs %}
                            <tr>
                                <td>{{ log.log_time }}</td>
                                <td>{{ log.value }}</td>
                                <td>{{ log.notes }}</td>
                            </tr>
                        (% endfor %)
                    </tbody>
                </table>
            {% endif %}

            <br><br>
            <p>Thank you!</p>
        </body>
        </html>
    """)

    result_html = template.render(user=user)

    return result_html


@celery.task
def test_mail():
    send_email()
    print("Mail send done!")


@celery.task()
def daily_remainders():
    
    users = User.query.all()

    for u in users:
        
        logged_today = False

        for t in u.trackers.all():
            if has_logs_today(t.tid):
                logged_today = True
        
        if not logged_today:
            send_alert_mail(u.email)
    print("Done with daily remainders!")


@celery.task
def hello(msg):
    print("Hello from celery", msg)
    return f"Hello from celery, {msg}" 

@celery.task()
def monthly_reports():
    
    users = User.query.all()

    for u in users:

        data = get_user_trackers_html(u.uid)

        send_html_report_mail(u.email, data)


@celery.task()
def export_user_trackers(uid):
    
    u = User.query.get(uid)

    data = get_user_trackers_html(u.uid)

    send_html_report_mail(u.email, data)


@celery.task()
def export_tracker_logs(tid):
    
    tracker = Tracker.query.get(tid)

    u = User.query.get(tracker.uid)

    data = get_tracker_html(tracker.tid)

    send_html_report_mail(u.email, data)

    


