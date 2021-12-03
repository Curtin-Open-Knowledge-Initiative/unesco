# Reporting template
#
# Copyright 2020-21 ######
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: COKI Team
import json
from pathlib import Path
import os
from typing import Optional, Callable, Union

import pandas as pd
import numpy as np
import plotly.graph_objects as go

from precipy.analytics_function import AnalyticsFunction

from observatory.reports import report_utils
from parameters import *
from report_data_processing.sql import load_sql_to_string

PROJECT_ID = 'coki-unesco'


def get_region_oa(af: AnalyticsFunction):
    """
    Collect OA percentages for Regions
    """

    query = load_sql_to_string('unesco_regions_oa.sql',
                               parameters=dict(table=DOI_TABLE),
                               directory=SQL_DIRECTORY)
    region_oa = pd.read_gbq(query=query,
                            project_id=PROJECT_ID)

    query = load_sql_to_string('unesco_global_oa.sql',
                               parameters=dict(table=DOI_TABLE),
                               directory=SQL_DIRECTORY)
    global_oa = pd.read_gbq(query=query,
                            project_id=PROJECT_ID)

    region_oa = region_oa.append(global_oa)
    region_oa.sort_values(['region', 'published_year'], inplace=True)
    region_oa.to_csv('region_oa.csv')


def get_collaboration_oa(af: AnalyticsFunction):
    """
    OA percentages by inter-region Collaboration
    """

    query = load_sql_to_string('region_collaborations.sql',
                               parameters=dict(table=DOI_TABLE),
                               directory=SQL_DIRECTORY)
    collab_oa = pd.read_gbq(query=query,
                            project_id=PROJECT_ID)
    collab_oa.to_csv('collab_oa.csv')


def get_sdgs_oa(af: AnalyticsFunction):
    """
    OA by SDG Globally
    """

    query = load_sql_to_string('sdg_oa.sql',
                               parameters=dict(table=DOI_TABLE),
                               directory=SQL_DIRECTORY)
    sdgs_oa = pd.read_gbq(query=query,
                          project_id=PROJECT_ID)

    sdgs = [sdg for sdg in sdgs_oa.columns if not sdg.endswith('_oa')]
    for sdg in sdgs:
        sdgs_oa[f'{sdg}_pc_oa'] = sdgs_oa[f'{sdg}_oa'] / sdgs_oa[sdg] * 100

    sdgs_oa['pc_oa'] = sdgs_oa.is_oa / sdgs_oa.total_outputs * 100
    sdgs_oa.to_csv('sdg_oa.csv')
