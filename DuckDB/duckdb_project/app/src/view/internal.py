from app import app
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from src.model.filters.filter import Filter
from src.controller.database.quality_olap import QualityDatabaseQueryHandler

# query handler
query_handler = QualityDatabaseQueryHandler()

# layout of the internal non-conformity dashboard
layout = dbc.Container([
    dbc.Row([
        # two columns - metrics total non-conformities and total non-conformities cost
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2('❌ Total Non-Conformities', className='card-title'),
                    html.H3('0', className='card-value', id='total-ncs-metric')
                ])
            ], className='metric-card')
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2('💰 Total Non-Conformities Cost', className='card-title'),
                    html.H3('0', className='card-value', id='total-ncs-cost-metric')
                ])
            ], className='metric-card')
        ], md=6)
    ]),
    # one column - line graph showing the evolution of non-conformities quantity
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2('📈 Evolution of Internal Non-Conformities', className='card-title'),
                    dcc.Graph(id='non-conformities-quantity')
                ])
            ], className='metric-card')
        ])
    ]),

    # one column - bar chart showing the non-conformities by product
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2('📊 Internal Non-Conformities by Product', className='card-title'),
                    dcc.Graph(id='non-conformities-by-product')
                ])
            ], className='metric-card')
        ])
    ]),

    # two columns - defects distribution by process step and defects distribution by root cause
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2('📊 Defects Distribution by Process Step', className='card-title'),
                    dcc.Graph(id='defects-distribution-process-step')
                ])
            ], className='metric-card')
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2('📊 Defects Distribution by Root Cause', className='card-title'),
                    dcc.Graph(id='defects-distribution-root-cause')
                ])
            ], className='metric-card')
        ], md=6)
])
], fluid=True)

# callback to update the internal non-conformity dashboard after the button send-data is clicked
# it should update the metrics, the line graph, the bar chart
@app.callback(
    [
        Output('total-ncs-metric', 'children'),
        Output('total-ncs-cost-metric', 'children'),
    #     Output('non-conformities-quantity', 'figure'),
    #     Output('non-conformities-by-product', 'figure'),
    #     Output('defects-distribution-process-step', 'figure'),
    #     Output('defects-distribution-root-cause', 'figure'),
    ],
    Input('analysis-data', 'data')
)
def update_internal_dashboard(data):
    # get the filter
    filter = Filter(
        start_date=str(data['start_date']), 
        end_date=str(data['end_date']),
        production_line=data['report_desired']
    )

    # get total non-conformities
    total_ncs = query_handler.get_total_internal_ncs(filter)

    # if total_ncs is a number, split thousands with comma
    if type(total_ncs) in [int, float]:
        total_ncs = f'{total_ncs:,}'

    # get total defects cost
    total_defects_cost = query_handler.get_total_defects_cost(filter)

    # if total_defects_cost is a number, split thousands with comma and add dollar sign
    if type(total_defects_cost) in [int, float]:
        total_defects_cost = f'${total_defects_cost:,}'
        
    # # get the evolution of defects
    # evolution = query_handler.get_evolution_defects(filter)

    # # get most defective product
    # most_defective_product = query_handler.get_most_defective_product(filter)

    # # defects distribution by process step
    # defects_by_process_step = query_handler.get_defects_distribution_by_process_step(filter)

    # # defects distribution by root cause
    # defects_by_root_cause = query_handler.get_defects_distribution_by_root_cause(filter)

    return f'{total_ncs}', f'{total_defects_cost}'#, evolution, most_defective_product, defects_by_process_step, defects_by_root_cause