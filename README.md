# corona-explorer

Collecting and experimenting with some COVID-19 related data

## Features

* Import CSV data from Open Covid-19 project into SQLite
* Generate country-specific CSV files
* TODO:
  * Update SQLite from CSV
  * Add records imported from worldometer
  * Generate useful graph output

## Requirements

* [python3](https://www.python.org/downloads)
* [pip3](https://pip.pypa.io/en/stable/installing)
* [virtualenv >= 16.6.0](https://virtualenv.pypa.io/en/latest/installation/)

## Setup

* Clone repository: `git clone git@github.com:eugene-davis/corona-explorer.git`
* Clone Open Covid 19 data repository: `git clone git@github.com:open-covid-19/data.git`
  * [Optional] Update the data repository
* Create a virtual environment: `python3 -mvenv virt`
* Activate the evironment: `source virt/bin/activate`
* Install package:
  * Normal installation: `python setup.py install`
  * Developer install:
    * Install developer dependencies: `pip install -r requirements_dev.txt`
    * Install development package: `python setup.py develop`
* Intialize database: `corona-explorer init --source /path/to/open-covid-data/output/world.csv`

## Basic Usage Examples

### Exporting Country files for US, India and Germany

`corona-explorer export US India Germany`

This will generate a CSV for each country into the `export` directory.

## Credits

This packages uses data from [the Open Covid-19 Project](https://github.com/open-covid-19/data).

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [tomtom-international/cookiecutter-python](https://github.com/tomtom-international/cookiecutter-python) project template.
