from app import app
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from src.model.filters.filter import Filter
from src.controller.graph_builder import GraphBuilder
from src.controller.database.quality_olap import QualityDatabaseQueryHandler

# query handler
query_handler = QualityDatabaseQueryHandler()

# graph builder
graph_builder = GraphBuilder()

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
    ]),

    # two columns - defects distrbution by recurring issues and by 8M's root cause
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2('📊 Defects Distribution by Recurring Issues', className='card-title'),
                    dcc.Graph(id='defects-distribution-recurring-issues')
                ])
            ], className='metric-card')
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2('📊 Defects Distribution by Ishikawa\'s Root Cause', className='card-title'),
                    dcc.Graph(id='defects-distribution-ishikawa-root-cause')
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
        Output('non-conformities-quantity', 'figure'),
        Output('non-conformities-by-product', 'figure'),
        Output('defects-distribution-process-step', 'figure'),
        Output('defects-distribution-root-cause', 'figure'),
        Output('defects-distribution-recurring-issues', 'figure'),
        Output('defects-distribution-ishikawa-root-cause', 'figure')
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
        
    # get the evolution of defects
    evolution_data = query_handler.get_evolution_defects(filter)
    evolution = graph_builder.build_line_chart(evolution_data, 'date', 'total_ncs', 'Date', 'Total Non-Conformities')

    # get most defective product
    most_defective_product_data = query_handler.get_most_defective_product(filter)
    most_defective_product = graph_builder.build_bar_chart(most_defective_product_data, 'product_name', 'total_ncs', 'Product', 'Total Non-Conformities')

    # defects distribution by process step
    defects_by_process_step_data = query_handler.get_defects_distribution_by_process_step(filter)
    defects_by_process_step = graph_builder.build_h_bar_chart(defects_by_process_step_data, 'process_step_name', 'total_ncs', y_title='Process Step', x_title='Total Non-Conformities')

    # defects distribution by root cause
    defects_by_root_cause_data = query_handler.get_defects_distribution_by_issues(filter)
    defects_by_root_cause = graph_builder.build_h_bar_chart(defects_by_root_cause_data, 'issue_name', 'total_ncs', y_title='Root Cause', x_title='Total Non-Conformities')

    # defects distribution by recurring issues
    defects_distribution_recurring_issues_data = query_handler.get_defects_distribution_by_recurring_issues(filter)
    defects_distribution_recurring_issues = graph_builder.build_pie_chart(defects_distribution_recurring_issues_data, 'is_recurrent', 'total_ncs')

    # builds a ishikawa diagram
    ishikawa_data = query_handler.get_defects_distribution_by_ishikawa_root_cause(filter)
    ishikawa = graph_builder.build_h_bar_chart(ishikawa_data, 'issue_name', 'total_ncs', y_title='Ishikawa Root Cause', x_title='% Non-Conformities')

    return f'{total_ncs}', f'{total_defects_cost}', evolution, most_defective_product, defects_by_process_step, defects_by_root_cause, defects_distribution_recurring_issues, ishikawa