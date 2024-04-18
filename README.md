# django-base

A basic boilerplate Django project prepped with poetry and Rollup. It uses the Django project default database SQLite.

## Setup

For history's sake, this setup was based off of the instructions here: https://builtwithdjango.com/blog/basic-django-setup.

1. We only test and develop this base project with Python 3.12 (specified in pyproject.toml). If you can't or don't want to install this version of Python, you can change the version requirement in pyproject.toml. While we can't guarantee other versions' compatibility, it is quite unlikely that recent versions will encounter any issues. You can install the [latest version of Python here](https://www.python.org/downloads/).

2. Install [poetry](https://python-poetry.org/docs/#installation). This allows us to run our project in a virtual environment and will handle the installation of Django and other python libraries.

3. Run `poetry install` to install dependencies.

4. Rename `myproject` to whatever you'd like your project to be named. You will want to change the name in `pyproject.toml`, the Django project directory name `myproject/`, `manage.py`, and `settings.py`.

5. Change `TIME_ZONE` in `settings.py` to your timezone.

6. Run `poetry run python manage.py migrate` to initialize your local database.

7. Create a superuser for your local Django instance. Run `poetry run python manage.py createsuperuser`. Be sure to save your username and password in a responsible location.

8. Install [node](https://nodejs.org/en).

9. Run `npm install`.

10. Run `npm run build`.

## Running the server

Run `poetry run python manage.py runserver`.

## Running other Django commands

See Django documentation for other commands, such as generating and applying migrations. Commands can be used as normal, preceded by `poetry run`. For example, see "Running the server" above.

## Running tests

To run python tests, use `poetry run python manage.py test pages`.
To run TS/JS tests, use `npm run test`.

# Write Up

## Implementation Overview

1. Basic Setup:

Three Models (Event, EventTag, Revision) to store data for analysis. Two Management Commands to handle data retrieval process through command prompt. One main view to display Time Series Chart showing changes in revision count over time and markers with when Solar Events occurred.

2. Data Retrieval:

To retrieve events data from CSV file, use `poetry run python manage.py load_events {path to CSV File}` (NOTE: For the sake of simplicity, this command can only handle CSV files)

To retrieve revision data from MediaWiki, use `poetry run python manage.py get_revisions "{page title}"` (NOTE: page title must be surrounded by double quotes)

3. View: 

Once database has been populated, visit '/pages/graph' to see the interactive Plotly graph. The graph consists of two different filters. The first filter allows you to filter the event markers by specific event tags. The second filter allows you to filter by Page Title for the Wikipedia page.

## Approach/Solution

1. Data Modeling: I included a Many-To-Many relationship between Event and EventTag because I thought that it would be helpful to visualize if Events with specific EventTags have more impact on the number of revisions. 

2. Data Importing: For the initial implementation, I created two management commands to import events from CSV file and to fetch revisions using MediaWiki. This allows for easy data maintainabilty and performance optimization especially with large set of data. Things to note is that I've also made sure that database will not create duplicate entries for duplicate calls made.

3. Data visualization: For the main analysis, I created a Time Series Chart that displayed changes in revision history for each of the Wikipedia titles that exist in the database. I made the visualization function flexible so that if user fetch revision data for different title, that data will be added in the visualization automatically. To better visualize the possible relationship, I've added vertical line markers to indicate time when events occurred. I had hoped that this will allow us to visualize any spikes in revision numbers after an event occurred. I've also implemented filter functionality that allows user to filter for any events that are associated with a specific event tag for better analysis. 

## Analysis

With my approach, I was not able to find any concrete correlation between events and revisions. As shown in the chart, occurrence of an event does not lead to clear increase in number of revisions for any three pages. Further analysis may be needed to separate any revisions that do not have any concrete content in the revision to see if events lead to significant revisions in the Wikipedia pages.

## Next Steps...

For future implementations, I think additional method to analyze the content field for Wikipedia revision data could be beneficial. This will allow us to separate out revisions that are more significant than others.

Additionally, I think web-based importing feature could allow for more user interactions. Through the UI, they can possibly input different Wikipedia titles for the application to fetch and import additional event files. Additional implementations are also needed to handle different types of input files besides CSV.

Due to time limitations, I also was not able to draft more test cases to check for possible edge cases. 