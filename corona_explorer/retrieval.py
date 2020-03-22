"""
Functions for retrieving data from the database
"""
import sqlite3
import os

from collections import namedtuple
from datetime import datetime


def fetch_country_all_data(country, db):
    """
    Returns all data about a country as a dictionary
    """
    country_data = {"history": []}

    db_file = os.path.realpath(db)
    conn = sqlite3.connect(db_file)
    curse = conn.cursor()

    Day = namedtuple("day", ["date", "confirmed_cases", "deaths"])

    # Get country info, query based on the length of the country string provided (2 characters is the country code)
    if len(country) == 2:
        country_data["country_code"] = country
        curse.execute("SELECT country_name, pop FROM COUNTRY_INFO WHERE country_code=?", (country,))
        country_data["country_name"], country_data["population"] = curse.fetchone()

    else:
        country_data["country_name"] = country
        curse.execute("SELECT country_code, pop FROM COUNTRY_INFO WHERE country_name=?", (country,))
        country_data["country_code"], country_data["population"] = curse.fetchone()

    for row in curse.execute(
        "SELECT timestamp, confirmed_cases, deaths FROM country_cases WHERE country_code=? ORDER BY timestamp",
        (country_data["country_code"],),
    ):
        date = datetime.utcfromtimestamp(row[0]).strftime("%Y-%m-%d")

        cur_day = Day(date=date, confirmed_cases=row[1], deaths=row[2])
        country_data["history"].append(cur_day)

    return country_data
