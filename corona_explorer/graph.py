"""
Module for generating graphs from the data
"""

import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from datetime import datetime

from .retrieval import fetch_country_all_data


def graph(args):
    Path(args.graph_path).mkdir(parents=True, exist_ok=True)

    for country in args.countries:
        country_data = fetch_country_all_data(country, args.db)
        filename = "{date}.{country}.{model_type}.png".format(
            country=country_data["country_name"],
            date=datetime.utcnow().strftime("%Y-%m-%d"),
            model_type=args.model_type,
        )
        line_fit(country_data, Path(args.graph_path, filename), args.model_type)


def line_fit(country_data, filename, model_type):
    deaths = []
    confirmed = []

    for day in country_data["history"]:
        deaths.append(getattr(day, "deaths"))
        confirmed.append(getattr(day, "confirmed_cases"))

    days = np.linspace(1, len(confirmed), len(confirmed))

    days_predict = np.linspace(1, 100, 100)
    title = "COVID 19: {country} - {model_type}\nGenerated: {date}".format(
        country=country_data["country_name"], date=datetime.utcnow().strftime("%Y-%m-%d"), model_type=model_type
    )
    plt.title(title)

    plt.xlabel("Time (days)")

    # Confirmed
    confirmed = np.array(confirmed)
    model_confirmed = np.polyfit(days, confirmed, 1)
    forecast_confirmed = np.poly1d(model_confirmed)

    plt.scatter(days, confirmed, label="Confirmed Cases")
    plt.plot(days_predict, forecast_confirmed(days_predict), label="Confirmed Cases Predicted", linestyle="dashed")

    # Deaths
    deaths = np.array(deaths)
    model_deaths = np.polyfit(days, deaths, 1)
    forecast_deaths = np.poly1d(model_deaths)

    plt.scatter(days, deaths, label="Deaths")
    plt.plot(days_predict, forecast_deaths(days_predict), label="Deaths Predicted", linestyle="dotted")

    plt.legend()
    plt.savefig(filename)
    plt.close()
