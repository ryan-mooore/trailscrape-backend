#!/bin/sh
pipenv install
echo ----- update regions -----
pipenv run python src/update_regions.py
echo ----- update trailforks regions -----
pipenv run python src/update_trailforks_regions.py
echo ----- create trail status template -----
pipenv run python src/create_trail_status_template.py
echo -----  update trail status -----
pipenv run python src/update_trail_status.py