from dash import Dash, html, dcc, callback, clientside_callback, Input, Output, State, Patch
import dash_bootstrap_components as dbc
import datetime as dt
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from aio.date_pick_aio import DatePickAIO
from aio.scenario_addin_aio import ScenarioAddinAIO
from common import months
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
                    html.Span('Start Month/Year', className='vertical-align label-margin-right'),
                    DatePickAIO(2000, dt.date.today().year, 'start_loan_date_pick'),
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
                    dbc.Button('Compute Baseline', color='primary', id='compute_baseline_btn', className='label-margin-left'),
                    html.Img(src='/assets/AddInTile.svg', className='label-margin-left', id='add_scenario_btn')
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
    ], className='row mt-2'),
    dbc.Modal(
        dbc.ModalBody([], id = 'scenario_addin_modal_body'),
        id='scenario_addin_modal',
        size='lg'
    )
], className='container-fluid')

def convert_date_input(month: int, year: int) -> dt.date:
    return dt.date(year, month, 1)

def calc_rate(rate_percent: int)-> float:
    return rate_percent/100

def add_month(cur_date: dt.date) -> dt.date:
    if cur_date.month < 12:
        return dt.date(cur_date.year, cur_date.month+1, cur_date.day)
    return dt.date(cur_date.year+1, 1, cur_date.day)

def add_year(cur_date: dt.date) -> dt.date:
    return dt.date(cur_date.year+1, cur_date.month, cur_date.day)

clientside_callback("""function(clicks){
        return true;
    }""",
    Output('scenario_addin_modal', 'is_open', allow_duplicate=True),
    Input('add_scenario_btn', 'n_clicks'),
    prevent_initial_call=True)

@callback(
    Output('scenario_addin_modal', 'is_open'),
    Input(ScenarioAddinAIO.ids.one_time_compute_btn('scenario_addin'), 'n_clicks'),
    Input(ScenarioAddinAIO.ids.uniform_compute_btn('scenario_addin'), 'n_clicks'),
    Input(ScenarioAddinAIO.ids.custom_compute_btn('scenario_addin'), 'n_clicks'),
    prevent_initial_call=True
)
def close_scenario_modal(one_time_compute_click, uniform_compute_click, custom_compute_click):
    return False

@callback(
    Output('outcomes_chart', 'figure', allow_duplicate=True),
    Output('scenario_addin_modal_body', 'children'),
    Input('compute_baseline_btn', 'n_clicks'),
    State(DatePickAIO.ids.month_drpdwn('start_loan_date_pick'), 'value'),
    State(DatePickAIO.ids.year_input('start_loan_date_pick'), 'value'),
    State('duration_dropdown', 'value'),
    State('interest_rate_input', 'value'),
    State('loan_amount_input', 'value'),
    prevent_initial_call=True
)
def update_outcomes_chart(_, start_month: int, start_year: int, duration: int, rate: float, amount: float):
    start_date =convert_date_input(start_month, start_year)
    cond_rate =calc_rate(rate)
    agent = LoanAgent()
    baseline_df, fig = agent.calc_baseline_amor_schedule(amount, start_date, cond_rate, duration)
    addIn = ScenarioAddinAIO(baseline_df['payment_date'].dt.date.to_list(), 'scenario_addin')
    return fig, [addIn]

@callback(
    Output('outcomes_chart', 'figure', allow_duplicate=True),
    Input(ScenarioAddinAIO.ids.one_time_compute_btn('scenario_addin'), 'n_clicks'),
    State(DatePickAIO.ids.month_drpdwn('start_loan_date_pick'), 'value'),
    State(DatePickAIO.ids.year_input('start_loan_date_pick'), 'value'),
    State('duration_dropdown', 'value'),
    State('interest_rate_input', 'value'),
    State('loan_amount_input', 'value'),
    State(DatePickAIO.ids.month_drpdwn('one_time_date_pick'), 'value'),
    State(DatePickAIO.ids.year_input('one_time_date_pick'), 'value'),
    State(ScenarioAddinAIO.ids.one_time_amount_input('scenario_addin'), 'value'),
    State(ScenarioAddinAIO.ids.name_input('scenario_addin'), 'value'),
    prevent_initial_call=True
)
def add_one_time_scenario(compute_clicks, start_month: int, start_year: int, duration: int, rate: float, amount: float, 
    pay_month: int, pay_year: int, pay_amount: int, addin_name:str):
    patch_fig = Patch()
    if compute_clicks is None:
        return patch_fig

    start_date = convert_date_input(start_month, start_year)
    cond_rate =calc_rate(rate)
    pay_date = convert_date_input(pay_month, pay_year)
    agent = LoanAgent()
    mod_df, trace = agent.calc_mod_amor_schedule(amount, start_date, cond_rate, duration, {pay_date: pay_amount}, addin_name)
    patch_fig['data'].append(trace)
    return patch_fig

@callback(
    Output('outcomes_chart', 'figure', allow_duplicate=True),
    Input(ScenarioAddinAIO.ids.uniform_compute_btn('scenario_addin'), 'n_clicks'),
    State(DatePickAIO.ids.month_drpdwn('start_loan_date_pick'), 'value'),
    State(DatePickAIO.ids.year_input('start_loan_date_pick'), 'value'),
    State('duration_dropdown', 'value'),
    State('interest_rate_input', 'value'),
    State('loan_amount_input', 'value'),
    State(DatePickAIO.ids.month_drpdwn('uniform_date_pick'), 'value'),
    State(DatePickAIO.ids.year_input('uniform_date_pick'), 'value'),
    State(ScenarioAddinAIO.ids.uniform_freq_drpdwn('scenario_addin'), 'value'),
    State(ScenarioAddinAIO.ids.uniform_num_payments_input('scenario_addin'), 'value'),
    State(ScenarioAddinAIO.ids.uniform_amount_input('scenario_addin'), 'value'),
    State(ScenarioAddinAIO.ids.name_input('scenario_addin'), 'value'),
    prevent_initial_call=True
)
def add_uniform_scenario(compute_clicks, start_month: int, start_year: int, duration: int, rate: float, amount: float,
    pay_start_month: int, pay_start_year: int, pay_freq: str, num_payments: int, pay_amount: int, addin_name: str):
    patch_fig = Patch()
    if compute_clicks is None:
        return patch_fig
    
    start_date = convert_date_input(start_month, start_year)
    pay_start_date = convert_date_input(pay_start_month, pay_start_year)
    cond_rate =calc_rate(rate)

    extra_payments = {}
    cur_date =pay_start_date
    for i in range(num_payments):
        pay_date = add_month(cur_date) if pay_freq == 'Month' else add_year(cur_date)
        extra_payments[pay_date] = pay_amount
        cur_date = pay_date
    agent = LoanAgent()
    mod_df, trace = agent.calc_mod_amor_schedule(amount, start_date, cond_rate, duration, extra_payments, addin_name)

    patch_fig['data'].append(trace)
    return patch_fig

@callback(
    Output('outcomes_chart', 'figure', allow_duplicate=True),
    Input(ScenarioAddinAIO.ids.custom_compute_btn('scenario_addin'), 'n_clicks'),
    State(DatePickAIO.ids.month_drpdwn('start_loan_date_pick'), 'value'),
    State(DatePickAIO.ids.year_input('start_loan_date_pick'), 'value'),
    State('duration_dropdown', 'value'),
    State('interest_rate_input', 'value'),
    State('loan_amount_input', 'value'),
    State(ScenarioAddinAIO.ids.custom_grid('scenario_addin'), 'rowData'),
    State(ScenarioAddinAIO.ids.name_input('scenario_addin'), 'value'),
    prevent_initial_call=True
)
def add_custom_scenario(compute_clicks, start_month: int, start_year: int, duration: int, rate: float, amount: float,
    custom_schedule: list, addin_name):
    patch_fig = Patch()
    if compute_clicks is None:
        return patch_fig
    start_date = convert_date_input(start_month, start_year)
    cond_rate =calc_rate(rate)
    
    extra_payments = {}
    for sched_item in custom_schedule:
        if sched_item['amount'] == 0:
            continue
        pay_date = dt.datetime.strptime(sched_item['date'], '%Y-%m-%d').date()
        extra_payments[pay_date] = sched_item['amount']

    agent = LoanAgent()
    mod_df, trace = agent.calc_mod_amor_schedule(amount, start_date, cond_rate, duration, extra_payments, addin_name)
    patch_fig['data'].append(trace)
    return patch_fig







if __name__  == '__main__':
        app.run(debug=True, host='0.0.0.0', port='8050', dev_tools_hot_reload=True)