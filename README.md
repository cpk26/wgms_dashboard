## WGMS Data Exploration Dashboard
This repository contains a dashboard of Fluctuations of Glaciers Database [1] published by the World Glacier Monitoring Services. 

[View Here](https://inletlabs.com/wgms-dash.html)

## Running

The dashboard can be run locally as well as deployed on heroku. The easiest way to run it locally is to setup a new conda environment using `conda_requirements.txt`, and then run `python app.py` within the environment. This will provide a link you can open in your browser to view the dashboard. This conda environment will have all the dependencies used in the data exploration/extraction file `data_import.ipynb` (`data_import.py` is mirrored version created using [jupytext](https://github.com/mwouts/jupytext) for use with an IDE other than jupyter notebooks).

Instructions for deploying the dashboard to Heroku can be found on this [page](https://dash.plotly.com/deployment) under 'Heroku example'.

## Structure

The main files are:

1. `app.py` Plotly app containing the dashboard
2. `data_import.py` / `data_import.ipynb` Import and pre-processs the data
3. `assets/wgms_db.css` CSS file for styling the dashboard
4. `conda_requirements.txt` Contains conda environment for processing the data and running the dashboard
5. `requirements.txt` Minimal requirements for only deploying the dashboard

Most of the remaining files are auxillary files to run on Heroku.

## References

[1]: WGMS (2019): Fluctuations of Glaciers Database. World Glacier Monitoring Service, Zurich, Switzerland. DOI:10.5904/wgms-fog-2019-12. Online access: http://dx.doi.org/10.5904/wgms-fog-2019-12
