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
import plotly.express as px
import plotly.graph_objects as go

from precipy.analytics_function import AnalyticsFunction

from observatory.reports import report_utils
from parameters import *
from report_data_processing.sql import load_sql_to_string

PROJECT_ID = 'coki-unesco'


def get_global_oa(af: AnalyticsFunction):
    """
    Collect Global OA levels for PAIC and COKI OA categories
    """

    query = load_sql_to_string('global_oa.sql',
                               parameters=dict(doi_table=DOI_TABLE,
                                               start_year=START_YEAR,
                                               end_year=END_YEAR),
                               directory=SQL_DIRECTORY)
    global_oa = pd.read_gbq(query=query,
                            project_id=PROJECT_ID)

    global_oa.to_csv('global_oa.csv', index=False)
    af.add_existing_file('global_oa.csv')


def get_region_oa(af: AnalyticsFunction):
    """
    Collect OA percentages for Regions
    """

    # Regions Query
    query = load_sql_to_string('unesco_regions_oa.sql',
                               parameters=dict(table=DOI_TABLE),
                               directory=SQL_DIRECTORY)
    region_oa = pd.read_gbq(query=query,
                            project_id=PROJECT_ID)

    # # Global Query
    # query = load_sql_to_string('unesco_global_oa.sql',
    #                            parameters=dict(table=DOI_TABLE),
    #                            directory=SQL_DIRECTORY)
    # global_oa = pd.read_gbq(query=query,
    #                         project_id=PROJECT_ID)
    #
    # region_oa = region_oa.append(global_oa)
    region_oa.sort_values(['region', 'published_year'], inplace=True)
    region_oa.to_csv('region_oa.csv', index=False)
    af.add_existing_file('region_oa.csv')


def get_collaboration_oa(af: AnalyticsFunction):
    """
    OA percentages by inter-region Collaboration
    """

    query = load_sql_to_string('region_collaborations.sql',
                               parameters=dict(table=DOI_TABLE),
                               directory=SQL_DIRECTORY)
    collab_oa = pd.read_gbq(query=query,
                            project_id=PROJECT_ID)
    collab_oa.to_csv('collab_oa.csv', index=False)
    af.add_existing_file('collab_oa.csv')


def get_sdgs_oa(af: AnalyticsFunction):
    """
    OA by SDG Globally


    """

    query = load_sql_to_string('sdg_oa.sql',
                               parameters=dict(table=DOI_TABLE,
                                               start_year=START_YEAR,
                                               end_year=END_YEAR),
                               directory=SQL_DIRECTORY)
    sdgs_oa = pd.read_gbq(query=query,
                          project_id=PROJECT_ID)

    sdgs = [sdg for sdg in sdgs_oa.columns if not sdg.endswith('_oa')]
    sdgs.remove('published_year')
    sdgs.remove('total_outputs')

    for sdg in sdgs:
        sdgs_oa[f'{sdg}_pc_oa'] = sdgs_oa[f'{sdg}_oa'] / sdgs_oa[sdg] * 100

    sdgs_oa['pc_oa'] = sdgs_oa.is_oa / sdgs_oa.total_outputs * 100
    sdgs_oa.to_csv('sdg_oa_by_year.csv', index=False)
    af.add_existing_file('sdg_oa_by_year.csv')


def oa_global_graph(af: AnalyticsFunction):
    """
    Graph OA globally by category and publication year
    """

    figdata = pd.read_csv('global_oa.csv')

    cols = ['diamond', 'gold', 'hybrid', 'bronze', 'green', 'closed']
    for col in cols:
        figdata[PAIC[col]['printname']] = figdata[f'count_{col}']
    fig = px.area(data_frame=figdata,
                  x='published_year',
                  y=[PAIC[col]['printname'] for col in cols],
                  color_discrete_map={PAIC[col]['printname']: PAIC[col]['color'] for col in cols},
                  groupnorm='percent',
                  labels=LABELS,
                  range_y=[0, 100]
                  )
    fig.write_image('oa_global_paic.png')

    cols = ['publisher_only', 'both', 'other_platform_only', 'closed']
    for col in cols:
        figdata[COKI[col]['printname']] = figdata[f'count_{col}']
    fig = px.area(data_frame=figdata,
                  x='published_year',
                  y=[COKI[col]['printname'] for col in cols],
                  color_discrete_map={COKI[col]['printname']: COKI[col]['color'] for col in cols},
                  groupnorm='percent',
                  labels=LABELS,
                  range_y=[0, 100]
                  )
    fig.write_image('oa_global_coki.png')


def oa_regions_graph(af: AnalyticsFunction):
    """
    Graph OA by Region Over Time
    """

    region_oa = pd.read_csv('region_oa.csv')

    fig = px.line(data_frame=region_oa,
                  x='published_year',
                  y='percent_oa',
                  color='region',
                  labels=dict(
                      published_year='Year of Publication',
                      percent_oa='Open Access (%)',
                      region='UNESCO Region'
                  ))
    fig.write_image('oa_regions.png')
    af.add_existing_file('oa_regions.png', remove=True)
    fig.write_html('oa_regions.html')
    af.add_existing_file('oa_regions.html', remove=True)


def oa_citations_graph(af: AnalyticsFunction):
    """
    OA Advantage by Region
    """

    region_oa = pd.read_csv('region_oa.csv')
    region_oa['Open Access'] = region_oa.avg_oa_citations_two_years
    region_oa['Non-Open Access'] = region_oa.avg_noa_citations_two_years
    regions = list(region_oa.region.unique())
    regions.remove('Global')
    dynamic_figure = px.bar(data_frame=region_oa[region_oa.published_year.isin(range(2010, 2019))],
                            x='region',
                            y=['Open Access', 'Non-Open Access'],
                            barmode='group',
                            animation_frame='published_year',
                            animation_group='region',
                            category_orders=dict(
                                region=regions + ['Global'],
                                variable=['Open Access', 'Non-Open Access']
                            ),
                            hover_name='region',
                            hover_data=dict(
                                published_year=True,
                                region=False,
                                variable=True,
                                value=':.2f',
                                total_outputs=':,',
                                oa_outputs=':,'
                            ),
                            labels=dict(
                                region='UNESCO Region',
                                published_year='Year of Publication',
                                value='Average Citation Count at Two Years',
                                variable='Access Status'
                            ))
    dynamic_figure.write_html('citations_region.html')
    af.add_existing_file('citations_region.html', remove=True)

    static_figure = px.bar(data_frame=region_oa[region_oa.published_year == 2018],
                           x='region',
                           y=['Open Access', 'Non-Open Access'],
                           barmode='group',
                           category_orders=dict(
                               region=regions + ['Global'],
                               variable=['Open Access', 'Non-Open Access']
                           ),
                           hover_name='region',
                           hover_data=dict(
                               published_year=True,
                               region=False,
                               variable=True,
                               value=':.2f',
                               total_outputs=':,',
                               oa_outputs=':,'
                           ),
                           labels=dict(
                               region='UNESCO Region',
                               published_year='Year of Publication',
                               value='Average Citation Count at Two Years',
                               variable='Access Status'
                           ))
    static_figure.write_image('citations_region_2018.png')
    af.add_existing_file('citations_region_2018.png', remove=True)

    static_figure = px.bar(data_frame=region_oa[region_oa.published_year.isin([2010, 2014, 2018])],
                           x='region',
                           y=['Open Access', 'Non-Open Access'],
                           barmode='group',
                           category_orders=dict(
                               region=regions + ['Global'],
                               variable=['Open Access', 'Non-Open Access']
                           ),
                           facet_row='published_year',
                           hover_name='region',
                           hover_data=dict(
                               published_year=True,
                               region=False,
                               variable=True,
                               value=':.2f',
                               total_outputs=':,',
                               oa_outputs=':,'
                           ),
                           labels=dict(
                               region='UNESCO Region',
                               published_year='Year of Publication',
                               value='Average Citation Count at Two Years',
                               variable='Access Status'
                           ))
    static_figure.write_image('citations_region_2010-14-18.png')
    af.add_existing_file('citations_region_2010-14-18.png', remove=True)


def collab_oa_graph(af: AnalyticsFunction):
    """
    Graph of OA levels as a function of regional collaboration
    """

    collab_oa = pd.read_csv('collab_oa.csv')

    fig = px.line(data_frame=collab_oa,
                  x='published_year',
                  y='percent_oa',
                  color='collab_regions',
                  labels=dict(
                      published_year='Year of Publication',
                      percent_oa='Open Access (%)',
                      collab_regions='Number of regions collaborating'
                  ))
    fig.write_image('collab_regions.png')
    af.add_existing_file('collab_regions.png', remove=True)
    fig.write_html('collab_regions.html')
    af.add_existing_file('collab_regions.html', remove=True)


def sdg_graph(af: AnalyticsFunction):
    """
    Graph OA by Sustainable Development Goal
    """

    sdgs_oa = pd.read_csv('sdg_oa.csv')
    region_oa = pd.read_csv('region_oa.csv')

    sdg_totals = sdgs_oa.set_index('published_year').sum(axis=1)

    sdgs = [s for s in SDG_PARAMS.keys()]
    for sdg in sdgs:
        sdg_totals[f'{sdg}_pc_oa'] = sdg_totals[f'{sdg}_oa'] / sdgs_oa[sdg] * 100
    sdg_totals['pc_oa'] = sdg_totals.is_oa / sdg_totals.total_outputs * 100
    sdg_totals.to_csv('sdg_oa_totals.csv', index=False)
    af.add_existing_file('sdg_oa_totals.csv')

    figdata = sdgs_oa.merge(region_oa[region_oa.region == 'Global'][['published_year', 'percent_oa']],
                            on='published_year')
    figdata['SDG Outputs'] = figdata.any_sdg_pc_oa
    figdata['All Global Outputs'] = figdata.percent_oa

    fig = px.line(data_frame=figdata,
                  x='published_year',
                  y=['SDG Outputs', 'All Global Outputs'],
                  range_y=[0, 100],
                  labels=dict(
                      published_year='Year of Publication',
                      value='Open Access (%)',
                      variable='Outputs Analysed'
                  ))
    fig.write_image('any_sdg.png')
    af.add_existing_file('any_sdg.png', remove=True)
    fig.write_html('any_sdg.html')
    af.add_existing_file('any_sdg.html', remove=True)

    sdg_data = [s for s in sdgs_oa.columns if s.endswith('_pc_oa')]
    cols = {sdg: f'SDG{sdg.replace("_", " ").title()[3:-5]}' for sdg in sdg_data}
    cols.update(dict(
        sdgs_ref_in_title_abs_pc_oa='Goals referred to in Title or Abstract',
        any_sdg_pc_oa='All SDGs'
    ))
    for s, c in cols.items():
        sdgs_oa[c] = sdgs_oa[s]

    fig = px.line(data_frame=sdgs_oa,
                  x='published_year',
                  y=[c for c in cols.values()],
                  range_y=[0, 100],
                  hover_name='variable',
                  hover_data=dict(
                      variable=False,
                      value=':.2f'
                  ),
                  labels=dict(
                      published_year='Year of Publication',
                      value='Open Access (%)',
                      variable='Sustainable Development Goal'
                  ))
    fig.write_image('sdgs_oa.png')
    af.add_existing_file('sdgs_oa.png', remove=True)
    fig.write_html('sdgs_oa.html')
    af.add_existing_file('sdgs_oa.html', remove=True)
