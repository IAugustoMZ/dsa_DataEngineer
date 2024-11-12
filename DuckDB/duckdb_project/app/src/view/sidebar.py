from dash import html, dcc
import dash_bootstrap_components as dbc
from src.controller.database.quality_olap import QualityDatabaseQueryHandler

# query handler
query_handler = QualityDatabaseQueryHandler()

# get production line
production_lines = query_handler.get_production_line()

# create options for the production line
production_line_options = [{'label': line, 'value': line} for line in production_lines]

# set side bar layout
layout = dbc.Col([

    # hidden div to store data
    dcc.Store(id='analysis-data'),

    # logo and title
    dbc.CardGroup([
        dbc.Card([
            html.H2('✅ Quality Management System', className='title-primary'),
        ], id='title-card')
    ]),
    html.Hr(),

    dbc.Row([
        dbc.Col(
            html.Div([
                dbc.Label('Start Date', className='input-label'),
                dcc.DatePickerSingle(
                    id='start-date',
                    display_format='YYYY-MM-DD',
                    date='2021-01-01'
                )
            ]),
            width=6 
        ),
        dbc.Col(
            html.Div([
                dbc.Label('End Date', className='input-label'),
                dcc.DatePickerSingle(
                    id='end-date',
                    display_format='YYYY-MM-DD',
                    date='2021-12-31'
                )
            ]),
            width=6
        ),
    ], align="center"),

    html.Br(),

    dbc.Nav([
        dbc.NavLink('📈 Internal Non-Conformity Dashboard', href='/internal-dashboard', id='internal-link', active=True),
        dbc.NavLink('📉 External Non-Conformity Dashboard', href='/external-dashboard', id='external-link', active=True)
    ], vertical=True, pills=False),

    html.Br(),

    # add select box for production line
    html.Div([
        dbc.Label('Report for Production Line', className='input-label'),
        dcc.Dropdown(
            id='report-desired',
            options=production_line_options
        )
    ], className='inputs-field'),

    html.Br(),

    # submit button
    html.Div([
        dbc.Button([
            html.H4('Submit to Analysis')
        ], color='success', id='send-data')
    ], id='button-div'),

    html.Hr()

], id='sidebar-complete')