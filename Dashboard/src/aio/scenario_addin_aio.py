import base64
from dash import html, dcc, callback, Input, Output, MATCH, ctx
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import datetime as dt
import uuid

from aio.date_pick_aio import DatePickAIO

class ScenarioAddinAIO(html.Div):

    class ids:
        name_input = lambda aio_id: {
            'component': 'ScenarioAddinAIO',
            'subcomponent': 'name_input',
            'aio_id': aio_id
        }

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

        baseline_store = lambda aio_id: {
            'component': 'ScenarioAddinAIO',
            'subcomponent': 'baseline_store',
            'aio_id': aio_id
        }

        custom_grid = lambda aio_id: {
            'component': 'ScenarioAddinAIO',
            'subcomponent': 'custom_grid',
            'aio_id': aio_id
        }

        custom_compute_btn = lambda aio_id: {
            'component': 'ScenarioAddinAIO',
            'subcomponent': 'custom_compute_btn',
            'aio_id': aio_id
        }

        custom_grid_export_btn = lambda aio_id: {
            'component': 'ScenarioAddinAIO',
            'subcomponent': 'custom_grid_export_btn',
            'aio_id': aio_id
        }

        custom_grid_upload = lambda aio_id: {
            'component': 'ScenarioAddinAIO',
            'subcomponent': 'custom_grid_upload',
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
                    dbc.Input(type='text', placeholder='Enter scenario name...', id=self.ids.name_input(aio_id))
                ], className='col-12')
            ], className='row mt-2'),
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
                            html.Div([
                                html.Div([
                                    html.Div([
                                        dag.AgGrid(
                                            id=self.ids.custom_grid(aio_id),
                                            defaultColDef={'filter':True},
                                            columnSize='responsiveSizeToFit',
                                            columnDefs=[
                                                {'field':'date', 'headerName':'Date', 'editable':False},
                                                {'field':'amount', 'headerName':'Additional Principal', 'editable':True,
                                                  "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"}},
                                            ],
                                            csvExportParams={'filename':'custom_payments.csv'}
                                        )
                                    ], className='col-lg-12')
                                ], className='row'),
                                html.Div([
                                    html.Div([
                                        dbc.Button('Export Grid', color='secondary', outline=True, className='label-margin-right', id=self.ids.custom_grid_export_btn(aio_id)),
                                        dcc.Upload(dbc.Button('Load Grid From File', outline=True, color='secondary', className='label-margin-right'), id=self.ids.custom_grid_upload(aio_id)),
                                        dbc.Button('Compute', color='primary', id=self.ids.custom_compute_btn(aio_id))
                                    ], className='col-lg-12 d-flex')
                                ], className='row mt-2')
                            ], className='container-fluid mt-2')
                        ], label='Custom')
                    ])
                ], className='col-12')
            ], className='row mt-2'),
            dcc.Store(id=self.ids.baseline_store(aio_id))
        ], className='container-fluid')

    
    @callback(
        Output(ids.custom_grid(MATCH),'rowData'),
        Input(ids.baseline_store(MATCH),'data'),
        Input(ids.custom_grid_upload(MATCH),'contents'),
        prevent_initial_call=True
    )
    def init_custom_grid(store_data, upload_contents):
        def parse_csv_line(csv_line: str) -> dict:
            line_data = csv_line.split(',',1)
            amount = float(line_data[1].replace('$','').replace(',','').replace('"',''))
            return {
                'date': dt.datetime.strptime(line_data[0],'%m/%d/%Y').strftime('%Y-%m-%d'),
                'amount': amount
            }

        data = []
        if 'baseline_store' in ctx.triggered_id['subcomponent']:
            for date_txt in store_data:
                data.append({
                    'date': date_txt,
                    'amount':0
                })
        else:
            if upload_contents is not None:
                content_type, content_string = upload_contents.split(',')
                decoded = base64.b64decode(content_string).decode('utf-8')
                is_first = True
                for csv_line in decoded.split('\r\n'):
                    if is_first:
                        is_first = False
                        continue
                    if csv_line.strip() != '': 
                        data.append(parse_csv_line(csv_line))

        return data

    @callback(
        Output(ids.custom_grid(MATCH), 'exportDataAsCsv'),
        Input(ids.custom_grid_export_btn(MATCH), 'n_clicks'),
        prevent_initial_call=True
    )
    def export_custom_grid(_):
        return True