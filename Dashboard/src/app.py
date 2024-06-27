from dash import Dash, html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import datetime as dt
import plotly.graph_objects as go

from utils.loan_agent import LoanAgent

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout =html.Div([
    html.Div([
        html.Div([
            html.H1("Mortgage Analytics"),
            html.P('Explore how loan factors (interest rate, monthly payments, etc.) influence outcomes (total cost, termination date, etc.).', className='mt-auto')
        ], className='col-12 d-flex')        
    ], className='row'),
    html.Div([
        html.Div([
            dbc.Card(
                dbc.CardBody([
                    html.Span('Start Date', className='vertical-align label-margin-right'),
                    dcc.DatePickerSingle(
                        id='start_date_picker',
                        date = dt.date(dt.date.today().year,1,1),
                        month_format='MMMM Y',
                        placeholder='MMMM Y',
                    ),
                    html.Span('Duration', className='vertical-align label-margin-left label-margin-right'),
                    dcc.Dropdown(
                        id='duration_dropdown',
                        options=[{'label': f'{x} years', 'value': x} for x in range(5,31,1)],
                        value=30,
                        style={'width':'125px', 'marginTop':'auto', 'marginBottom':'auto'}
                    ),
                    html.Span('Interest Rate (%)', className='vertical-align label-margin-left label-margin-right'),
                    dbc.Input(
                        id='interest_rate_input',
                        type='number', 
                        min=0, 
                        max=25, 
                        step=0.001,
                        value=5.15,
                        className='d-inline-block vertical-align',
                        style={'width':'125px'}
                    ),
                    html.Span('Loan Amount ($)', className='vertical-align label-margin-left label-margin-right'),
                    dbc.Input(
                        id='loan_amount_input',
                        type='number',
                        min=0,
                        max=10000000,
                        step=1000,
                        value=250000,
                        className='d-inline-block vertical-align',
                        style={'width':'150px'}
                    ),
                    dbc.Button('Compute Baseline', color='primary', id='compute_baseline_btn', className='label-margin-left')
                ], className='d-flex')
            )
        ], className='col-lg-12')
    ], className='row'),
    html.Div([
        html.Div([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id='outcomes_chart')
            ]))
        ], className='col-lg-12')
    ], className='row mt-2')
], className='container-fluid')

def convert_date_input(date_txt: str) -> dt.date:
    return dt.datetime.strptime(date_txt, '%Y-%m-%d').date()

@callback(
    Output('outcomes_chart', 'figure'),
    Input('compute_baseline_btn', 'n_clicks'),
    State('start_date_picker', 'date'),
    State('duration_dropdown', 'value'),
    State('interest_rate_input', 'value'),
    State('loan_amount_input', 'value')
)
def update_outcomes_chart(_, start_picker_val: str, duration: int, rate: float, amount: float):
    start_date =convert_date_input(start_picker_val)
    cond_rate =rate/100
    agent = LoanAgent()
    baseline_df, fig = agent.calc_baseline_amor_schedule(amount, start_date, cond_rate, duration)
    return fig



if __name__  == '__main__':
        app.run(debug=True, host='0.0.0.0', port='8049', dev_tools_hot_reload=True)

