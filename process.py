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
from plotly.subplots import make_subplots

from precipy.analytics_function import AnalyticsFunction

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
                               parameters=dict(
                                   doi_table=DOI_TABLE,
                                   start_year=START_YEAR,
                                   end_year=END_YEAR),
                               directory=SQL_DIRECTORY)
    region_oa = pd.read_gbq(query=query,
                            project_id=PROJECT_ID)

    region_oa.to_csv('region_oa.csv', index=False)
    af.add_existing_file('region_oa.csv')


def get_discipline_oa(af: AnalyticsFunction):
    """
    Get COKI OA levels by discipline (OpenAlex Level0 Concepts)
    """

    # Disciplines Query
    print("Running disciplines query")

    query = load_sql_to_string('discipline_oa.sql',
                               parameters=dict(
                                   doi_table=DOI_TABLE,
                                   start_year=START_YEAR,
                                   end_year=END_YEAR),
                               directory=SQL_DIRECTORY)
    discipline_oa = pd.read_gbq(query=query,
                                project_id=PROJECT_ID)

    discipline_oa.to_csv('discipline_oa.csv', index=False)
    af.add_existing_file('discipline_oa.csv')


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
                  range_y=[0, 100],
                  template=TEMPLATE
                  )
    fig.update_layout(font_family=FONT)
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
                  range_y=[0, 100],
                  template=TEMPLATE
                  )
    fig.update_layout(font_family=FONT)
    fig.write_image('oa_global_coki.png')


def oa_regions_graph(af: AnalyticsFunction):
    """
    Graph OA by Region Over Time
    """

    region_oa = pd.read_csv('region_oa.csv')
    global_oa = pd.read_csv('global_oa.csv')

    region_oa = region_oa[region_oa.published_year.isin(range(2012, 2022))]
    global_oa = global_oa[global_oa.published_year.isin(range(2012, 2022))]
    global_totals = global_oa.sum()
    region_oa.dropna(inplace=True)
    region_totals = region_oa.groupby('region').sum()
    region_totals.loc['Global OA'] = global_totals[[col for col in global_totals.index if col in region_totals.columns]]
    categories = ['diamond', 'gold', 'hybrid', 'bronze']
    for category in categories:
        region_totals[f'pc_{category}'] = region_totals[f'count_{category}'] / region_totals.count_ao_total * 100

    figdata = region_totals[[f'count_{category}' for category in categories]]

    labels = [PAIC[category]['printname'] for category in categories]
    marker_colors = [PAIC[category]['color'] for category in categories]
    fig = make_subplots(2,
                        4,
                        specs=[
                            [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}],
                            [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]
                        ],
                        subplot_titles=figdata.index)
    for i, region in enumerate(figdata.index):
        fig.add_trace(go.Pie(
            labels=labels,
            values=figdata.loc[region],
            marker_colors=marker_colors),
            1 if i < 4 else 2, i + 1 if i < 4 else i - 3)
    fig.update_traces(hole=.4)
    fig.update_layout(
        font_family="Myriad Pro"
    )
    fig.write_image('regions_oa.png', width=800)


def sdg_graph(af: AnalyticsFunction):
    """
    Graph OA by Sustainable Development Goal
    """

    sdgs_oa = pd.read_csv('sdg_oa_by_year.csv')

    sdgs_oa = sdgs_oa[sdgs_oa.published_year.isin(range(2012, 2022))]
    sdg_totals = sdgs_oa.set_index('published_year').sum(axis=0)

    sdgs = [s for s in SDG_PARAMS.keys()]
    for sdg in sdgs:
        sdg_totals[f'SDG-{sdg} {SDG_PARAMS[sdg]["title"]}'] = sdg_totals[f'sdg_{sdg}_oa'] / sdg_totals[
            f'sdg_{sdg}'] * 100
    sdg_totals[' '] = 0
    sdg_totals['SDGs Overall'] = sdg_totals.any_sdg_oa / sdg_totals.any_sdg * 100
    sdg_totals['Global Open Access'] = sdg_totals.is_oa / sdg_totals.total_outputs * 100
    sdg_totals.to_csv('sdg_oa_totals.csv')
    af.add_existing_file('sdg_oa_totals.csv')

    items = [f'SDG-{sdg} {SDG_PARAMS[sdg]["title"]}' for sdg in sdgs]
    items.extend([' ', 'SDGs Overall', 'Global Open Access'])
    figdata = sdg_totals[items]
    color_map = {
        f'SDG-{sdg} {SDG_PARAMS[sdg]["title"]}': SDG_PARAMS[sdg]['hex_color'] for sdg in sdgs
    }
    color_map.update({
        ' ': 'white',
        'SDGs Overall': 'black',
        'Global Open Access': 'black'
    })
    fig = px.bar(data_frame=figdata,
                 orientation='h',
                 range_x=[0, 100],
                 color=figdata.index,
                 color_discrete_map=color_map,
                 text_auto=True,
                 labels=dict(
                     value="Share of Open Access (%)",
                     index=""
                 ),
                 template=TEMPLATE)
    fig.update_traces(
        texttemplate="%{value:.3s}%",
        textposition="outside"
    )
    fig.update_traces(
        selector=dict(name=' '),
        texttemplate=''
    )
    fig.update_layout(
        showlegend=False,
        font_family="Myriad Pro")
    fig.write_image('sdg_oa.png')


def discipline_graph(af: AnalyticsFunction):
    discipline_oa = pd.read_csv('discipline_oa.csv')
    discipline_oa = discipline_oa[discipline_oa.published_year.isin(range(2012, 2022))]
    discipline_totals = discipline_oa.groupby('display_name').sum()

    global_oa = pd.read_csv('global_oa.csv')
    global_oa = global_oa[global_oa.published_year.isin(range(2012, 2022))]
    global_totals = global_oa.sum()

    for oa_categories in [COKI, PAIC]:
        for oa_class in oa_categories.keys():
            discipline_totals[oa_categories[oa_class]['printname']] = discipline_totals[oa_class] / discipline_totals[
                'total_outputs'] * 100
            global_totals[oa_categories[oa_class]['printname']] = global_totals[f'count_{oa_class}'] / global_totals[
                'count_ao_total'] * 100

        figdata = discipline_totals[[oa_categories[oa_class]['printname'] for oa_class in oa_categories.keys()]]
        figdata.loc['Global Open Access'] = global_totals[
            [oa_categories[oa_class]['printname'] for oa_class in oa_categories.keys()]]

        figdata['total_oa'] = np.round((100 - figdata["Not Open Access"]), 1)
        figdata['total_oa_str'] = figdata.total_oa.apply(lambda x: str(x) + ' %')


        color_map = {oa_categories[k]['printname']: oa_categories[k]['color'] for k in oa_categories.keys()}
        fig = px.bar(figdata,
                     x=[col for col in figdata.columns if col in [oa_categories[oa_class]['printname'] for oa_class in oa_categories.keys() if oa_class is not 'closed']],
                     y=figdata.index,
                     # orientation='h',
                     range_x=[0, 100],

                     color_discrete_map=color_map,
                     # text='total_oa',
                     labels=dict(
                         value="Share of Open Access (%)",
                         index=""
                     ),
                     template=TEMPLATE
                     )
        # fig.update_traces(
        #     texttemplate="%{value:.3s}%",
        #     textposition="outside"
        # )

        fig.add_trace(go.Scatter(
            x=figdata.total_oa,
            y=figdata.index,
            text=figdata.total_oa_str,
            mode='text',
            textposition='middle right',
            showlegend=False
        ))
        fig.update_yaxes(autorange="reversed",
                         title="")
        fig.update_layout(font_family="Myriad Pro",
                          legend=dict(title='Mode of Open Access'))
        if oa_categories == COKI:
            catname = 'coki'
        elif oa_categories == PAIC:
            catname = 'paic'
        fig.write_image(f'{catname}_discipline_oa.png')
    pass