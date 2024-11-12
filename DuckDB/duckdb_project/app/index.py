from app import app
import dash_bootstrap_components as dbc
from dash import html, Output, Input, dcc, State
from src.view import sidebar, internal, external

# set layout for the app
app.layout = dbc.Container(children=[
    dcc.Location(id='url', refresh=False),

    dbc.Row([
        # include sidebar
        dbc.Col([
            sidebar.layout
        ], md=3),

        # include dashboads
        dbc.Col(id='page-content', md=9)
    ])
], fluid=True, class_name='main-container')

# callback to update the page content
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/internal-dashboard':
        return internal.layout
    elif pathname == '/external-dashboard':
        return external.layout
    else:
        return html.H1('404 - Page not found')
    
# callback to update the data in the store
@app.callback(
    Output('analysis-data', 'data'),
    Input('send-data', 'n_clicks'),
    State('start-date', 'date'),
    State('end-date', 'date'),
    State('report-desired', 'value')
)
def update_data(n_clicks, start_date, end_date, report_desired):
    if n_clicks is None:
        return {}
    else:
        return {
            'start_date': start_date, 
            'end_date': end_date, 
            'report_desired': report_desired, 
        }

if __name__ == '__main__':
    app.run_server(port=8051, debug=True)