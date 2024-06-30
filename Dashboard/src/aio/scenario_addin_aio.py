from dash import html, dcc
import dash_bootstrap_components as dbc
import datetime as dt
import uuid

from aio.date_pick_aio import DatePickAIO

class ScenarioAddinAIO(html.Div):

    class ids:
        one_time_amount_input = lambda aio_id: {
            'component': 'ScenarioAddinAIO',
            'subcomponent': 'one_time_amount_input',
            'aio_id': aio_id
        }

        one_time_compute_btn = lambda aio_id: {
            'component': 'ScenarioAddinAIO',
            'subcomponent': 'one_time_compute_btn',
            'aio_id': aio_id
        }

        uniform_amount_input = lambda aio_id: {
            'component': 'ScenarioAddinAIO',
            'subcomponent': 'uniform_amount_input',
            'aio_id': aio_id
        }

        uniform_freq_drpdwn = lambda aio_id: {
            'component': 'ScenarioAddinAIO',
            'subcomponent': 'uniform_freq_drpdwn',
            'aio_id': aio_id
        }
        
        uniform_num_payments_input = lambda aio_id: {
            'component': 'ScenarioAddinAIO',
            'subcomponent': 'uniform_num_payments_input',
            'aio_id': aio_id
        }

        uniform_compute_btn = lambda aio_id: {
            'component': 'ScenarioAddinAIO',
            'subcomponent': 'uniform_compute_btn',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(
        self,
        aio_id=None
    ):

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        super().__init__(
            self._gen_layout(aio_id)
        )

    def _gen_layout(self, aio_id: str):
        return html.Div([
            html.Div([
                html.Div([
                    html.H1('Scenario Add-In')
                ], className='col-12')
            ], className='row'),
            html.Div([
                html.Div([
                    dbc.Tabs([
                        dbc.Tab([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        'Payment Date'
                                    ], className='col-lg-3 vertical-align'),
                                    html.Div([
                                        DatePickAIO('one_time_date_pick')
                                    ], className='col-lg-9')
                                ], className='row'),
                                html.Div([
                                    html.Div([
                                        'Payment Amount'
                                    ], className='col-lg-3 vertical-align'),
                                    html.Div([
                                        dbc.Input(
                                            type='number',
                                            min=0,
                                            max=1000000,
                                            step=10,
                                            value=1000,
                                            style={'width':'150px'},
                                            id=self.ids.one_time_amount_input(aio_id)
                                        ),
                                    ], className='col-lg-9 d-flex')
                                ], className='row mt-2'),
                                html.Div([
                                    html.Div([
                                        dbc.Button('Compute', color='primary', id=self.ids.one_time_compute_btn(aio_id))
                                    ], className='col-12')
                                ], className='row mt-2')
                            ], className='container-fluid mt-2')
                        ], label='One-Time'),
                        dbc.Tab([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        'Start Date'
                                    ], className='col-lg-3 vertical-align'),
                                    html.Div([
                                        DatePickAIO('uniform_date_pick')
                                    ], className='col-lg-3')
                                ], className='row'),
                                html.Div([
                                    html.Div([
                                        'Frequency'
                                    ], className='col-lg-3 vertical-align'),
                                    html.Div([
                                        dcc.Dropdown(['Month','Year'], 'Year', id=self.ids.uniform_freq_drpdwn(aio_id))
                                    ], className='col-lg-3')
                                ], className='row mt-2'),
                                html.Div([
                                    html.Div([
                                        'Number of Payments'
                                    ], className='col-lg-3 vertical-align'),
                                    html.Div([
                                        dbc.Input(
                                            type='number',
                                            min=0,
                                            max=100,
                                            step=1,
                                            value=4,
                                            style={'width':'150px'},
                                            id=self.ids.uniform_num_payments_input(aio_id)
                                        )
                                    ], className='col-lg-9')
                                ], className='row mt-2'),
                                html.Div([
                                    html.Div([
                                        'Payment Amount'
                                    ], className='col-lg-3 vertical-align'),
                                    html.Div([
                                        dbc.Input(
                                            type='number',
                                            min=0,
                                            max=1000000,
                                            step=10,
                                            value=1000,
                                            style={'width':'150px'},
                                            id=self.ids.uniform_amount_input(aio_id)
                                        )
                                    ], className='col-lg-9')
                                ], className='row mt-2'),
                                html.Div([
                                    html.Div([
                                        dbc.Button('Compute', color='primary', id=self.ids.uniform_compute_btn(aio_id))
                                    ], className='col-12')
                                ], className='row mt-2')
                            ], className='container-fluid mt-2')
                        ], label='Uniform'),
                        dbc.Tab([

                        ], label='Custom')
                    ])
                ], className='col-12')
            ], className='row')
        ], className='container-fluid')
    