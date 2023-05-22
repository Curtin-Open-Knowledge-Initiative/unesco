"""
General paramaters and configuration options
"""

from pathlib import Path
import json

# General Parameters
START_YEAR = 2010
END_YEAR = 2022 # Use range convention so this year is not included

with open("sdgs.json") as f:
    SDG_PARAMS = json.load(f)

# BigQuery

## Project
PROJECT_ID = 'coki-unesco'

## Tables

DOI_TABLE_RECENT = 'academic-observatory.observatory.doi20230325'
DOI_TABLE_PREVIOUS = 'academic-observatory.observatory.doi20211002'
DOI_TABLE = DOI_TABLE_RECENT

# SQL PATHS

SQL_DIRECTORY = Path('report_data_processing/sql')

# Graph Parameters

PAIC = dict(
    diamond=dict(
        printname='Diamond OA',
        color='darkgrey'
    ),
    gold=dict(
        printname='Gold OA (DOAJ)',
        color='gold'
    ),
    hybrid=dict(
        printname='Hybrid',
        color='orange'
    ),
    bronze=dict(
        printname='Bronze',
        color='brown'
    ),
    green=dict(
        printname='Green',
        color='darkgreen'
    ),
    closed=dict(
        printname='Closed',
        color='lightgrey'
    )
)

COKI = dict(
    publisher_only=dict(
        printname='Publisher Open',
        color='#fad649'
    ),
    both=dict(
        printname='Publisher and Other Platform',
        color='#5a9bd4'
    ),
    other_platform_only=dict(
        printname='Other Platform Open',
        color='#a9cf87'
    ),
    closed=dict(
        printname='Not Open Access',
        color='lightgrey'
    )
)

LABELS = dict(
    published_year='Year of Publication',
    variable='Open Access Category',
    value='Proportion of Total (%)'
)