"""
Module for generating graphs from the data
"""

import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from datetime import datetime

from .retrieval import fetch_country_all_data, fetch_region_all_data


def graph(args):
    Path(args.graph_path).mkdir(parents=True, exist_ok=True)

    data = []

    if args.regions and len(args.countries) > 1:
        raise ValueError("A region was provided with multiple countries, only one country can be provided.")

    elif not args.regions:
        for country in args.countries:
            country_data = fetch_country_all_data(country, args.db)
            data.append(country_data)
    else:
        for region in args.regions:
            region_data = fetch_region_all_data(region, args.countries[0], args.db)
            data.append(region_data)

    for entity_data in data:
        filename = "{date}.{title}.{model_type}.png".format(
            title=entity_data["title"], date=datetime.utcnow().strftime("%Y-%m-%d"), model_type=args.model_type
        )
        if args.model_type == "scatter-plot":
            scatter_plot(entity_data, Path(args.graph_path, filename), args.scale)

        elif args.model_type == "linear-regression":
            line_fit(entity_data, Path(args.graph_path, filename), args.scale)


def prepare_data(entity_data):
    deaths = []
    confirmed = []

    for day in entity_data["history"]:
        deaths.append(getattr(day, "deaths"))
        confirmed.append(getattr(day, "confirmed_cases"))

    days = np.linspace(1, len(confirmed), len(confirmed))

    days_predict = np.linspace(1, 200, 200)

    return confirmed, deaths, days, days_predict


def scatter_plot(entity_data, filename, scale):
    title = "COVID 19: {title} - Scatter Plot: {scale}-Scale\nGenerated: {date}".format(
        title=entity_data["title"], scale=scale, date=datetime.utcnow().strftime("%Y-%m-%d")
    )

    confirmed, deaths, days, days_predict = prepare_data(entity_data)

    plt.title(title)

    plt.xlabel("Time (days)")
    plt.yscale(scale)

    plt.scatter(days, confirmed, label="Confirmed Cases")
    plt.scatter(days, deaths, label="Deaths")

    plt.legend()
    plt.savefig(filename)
    plt.close()


def line_fit(entity_data, filename, scale):
    title = "COVID 19: {title} - Linear Regression: {scale}-Scale\nGenerated: {date}".format(
        title=entity_data["country_name"], scale=scale, date=datetime.utcnow().strftime("%Y-%m-%d")
    )

    confirmed, deaths, days, days_predict = prepare_data(entity_data)

    plt.title(title)

    plt.xlabel("Time (days)")
    plt.yscale(scale)

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
