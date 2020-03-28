"""
Functions for retrieving data from the database
"""
import sqlite3
import os

from collections import namedtuple
from datetime import datetime


def fetch_region_all_data(region, country, db):
    """
    Returns all data about a region as a dictionary
    """
    region_data = {"history": []}

    db_file = os.path.realpath(db)
    conn = sqlite3.connect(db_file)
    curse = conn.cursor()

    Day = namedtuple("day", ["date", "confirmed_cases", "deaths"])

    # Get country code if a name is provided, query based on the length of the country string provided (2 characters is the country code)
    if len(country) == 2:
        region_data["country_code"] = country
        curse.execute("SELECT country_name FROM COUNTRY_INFO WHERE country_code=?", (country,))
        region_data["country_name"] = curse.fetchone()[0]
    else:
        region_data["country_name"] = country
        curse.execute("SELECT country_code FROM country_info WHERE country_name=?", (country,))
        region_data["country_code"] = curse.fetchone()[0]

    # Get regional info by name or code
    if len(region) == 2:
        region_data["region_code"] = region
        curse.execute(
            "SELECT region_name, pop FROM region_info WHERE country_code=? AND region_code=?",
            (region_data["country_code"], region),
        )
        region_data["region_name"], region_data["population"] = curse.fetchone()

    else:
        region_data["region_name"] = region
        curse.execute(
            "SELECT region_code, pop FROM region_info WHERE country_code=? and region_name=?",
            (region_data["country_code"], region),
        )
        region_data["region_code"], region_data["population"] = curse.fetchone()

    for row in curse.execute(
        "SELECT timestamp, confirmed_cases, deaths FROM region_cases WHERE country_code=? and region_code=? ORDER BY timestamp",
        (region_data["country_code"], region_data["region_code"]),
    ):
        date = datetime.utcfromtimestamp(row[0]).strftime("%Y-%m-%d")

        cur_day = Day(date=date, confirmed_cases=row[1], deaths=row[2])
        region_data["history"].append(cur_day)

        region_data["title"] = region_data["country_name"] + "." + region_data["region_name"]

    return region_data


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
        curse.execute("SELECT country_name, pop FROM country_info WHERE country_code=?", (country,))
        country_data["country_name"], country_data["population"] = curse.fetchone()

    else:
        country_data["country_name"] = country
        curse.execute("SELECT country_code, pop FROM country_info WHERE country_name=?", (country,))
        country_data["country_code"], country_data["population"] = curse.fetchone()

    for row in curse.execute(
        "SELECT timestamp, confirmed_cases, deaths FROM country_cases WHERE country_code=? ORDER BY timestamp",
        (country_data["country_code"],),
    ):
        date = datetime.utcfromtimestamp(row[0]).strftime("%Y-%m-%d")

        cur_day = Day(date=date, confirmed_cases=row[1], deaths=row[2])
        country_data["history"].append(cur_day)

        country_data["title"] = country_data["country_name"]

    return country_data
