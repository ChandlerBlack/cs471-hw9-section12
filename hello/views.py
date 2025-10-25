from django.shortcuts import render

from .models import Greeting
from .models import RequestRecord
import secrets

from django.db import connection

import requests
from django.http import HttpResponse

# Create your views here.

def index(request):
    r = requests.get('https://httpbin.org/status/418', timeout=10)
    return HttpResponse('<pre>' + r.text + '</pre>')



def db(request):
    # If you encounter errors visiting the `/db/` page on the example app, check that:
    #
    # When running the app on Heroku:
    #   1. You have added the Postgres database to your app.
    #   2. You have uncommented the `psycopg` dependency in `requirements.txt`, and the `release`
    #      process entry in `Procfile`, git committed your changes and re-deployed the app.
    #
    # When running the app locally:
    #   1. You have run `./manage.py migrate` to create the `hello_greeting` database table.

    # Save the simple Greeting as before
    greeting = Greeting()
    greeting.save()

    # Create a RequestRecord with a securely generated random token
    token = secrets.token_urlsafe(16)
    record = RequestRecord(token=token)
    record.save()

    greetings = Greeting.objects.all()
    records = RequestRecord.objects.all().order_by("-when")

    # Also perform the raw-SQL behavior similar to the Java sample app:
    # - create a table if not exists
    # - insert (now(), random_string)
    # - select all rows and pass them to the template
    sql_records = []
    with connection.cursor() as cursor:
        cursor.execute(
            "DROP TABLE IF EXISTS table_timestamp_and_random_string"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS table_timestamp_and_random_string (tick timestamp, random_string varchar(256))"
        )
        random_string = secrets.token_urlsafe(16)
        cursor.execute(
            "INSERT INTO table_timestamp_and_random_string (tick, random_string) VALUES (now(), %s)",
            [random_string],
        )
        cursor.execute(
            "SELECT tick, random_string FROM table_timestamp_and_random_string ORDER BY tick DESC"
        )
        for row in cursor.fetchall():
            # row is (tick_datetime, random_string)
            sql_records.append({"when": row[0], "random_string": row[1]})

    return render(
        request,
        "db.html",
        {"greetings": greetings, "records": records, "sql_records": sql_records},
    )
