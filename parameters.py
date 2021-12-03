"""
General paramaters and configuration options
"""

from pathlib import Path

# BigQuery

## Project
PROJECT_ID = 'coki-unesco'

## Tables

DOI_TABLE_RECENT = 'academic-observatory.observatory.doi20211127'
DOI_TABLE_PREVIOUS = 'academic-observatory.observatory.doi20211002'
DOI_TABLE = DOI_TABLE_RECENT

# SQL PATHS

SQL_DIRECTORY = Path('report_data_processing/sql')