from dash import html, callback, Input, Output, State, MATCH, dcc
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import json
import pandas as pd
import uuid

class LoanSummaryAIO(html.Div):

    class ids:
        open_sched_btn = lambda aio_id: {
            'component': 'LoanSummaryAIO',
            'subcomponent': 'open_sched_btn',
            'aio_id': aio_id
        }

        sched_modal = lambda aio_id: {
            'component': 'LoanSummaryAIO',
            'subcomponent': 'sched_modal',
            'aio_id': aio_id
        }

        export_btn = lambda aio_id: {
            'component': 'LoanSummaryAIO',
            'subcomponent': 'export_btn',
            'aio_id': aio_id
        }

        export_dwnload = lambda aio_id: {
            'component': 'LoanSummaryAIO',
            'subcomponent': 'export_dwnload',
            'aio_id': aio_id
        }

        export_store = lambda aio_id: {
            'component': 'LoanSummaryAIO',
            'subcomponent': 'export_store',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(
        self,
        name: str,
        pay_sched_df: pd.DataFrame,
        aio_id=None
    ):

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        super().__init__(
            self._gen_layout(name, pay_sched_df, aio_id)
        )

    def _gen_layout(self, name: str, pay_sched_df: pd.DataFrame, aio_id: str):
        
        pay_sched_df['payment_date'] = pay_sched_df['payment_date'].dt.date
        loan_start = pay_sched_df['payment_date'].min()
        loan_end = pay_sched_df['payment_date'].max()
        loan_dur_days = (loan_end - loan_start).days
        total_interest = pay_sched_df['interest_paid'].sum()
        total_cost = pay_sched_df['interest_paid'].sum() + pay_sched_df['principal_paid'].sum()
        date_obj = "d3.timeParse('%Y-%m-%d')(params.data.payment_date)"

        store_data = {
            'name': name,
            'loan_start': loan_start,
            'loan_end': loan_end,
            'loan_dur_years': loan_dur_days/365.25,
            'total_interest': total_interest,
            'total_cost': total_cost,
            'schedule': pay_sched_df.to_dict('records')
        }

        return dbc.Card(dbc.CardBody([
            html.Div([
                html.Div([
                    html.Div([
                        html.H4(name),
                        html.Hr()
                    ], className='col-12')
                ], className='row'),
                html.Div([
                    html.Div([
                        html.Span('Loan Start')
                    ], className='col-lg-6'),
                    html.Div([
                        html.Span(f"{loan_start.strftime('%Y-%m-%d')}")
                    ], className='col-lg-6'),
                ], className='row'),
                html.Div([
                    html.Div([
                        html.Span('Loan End')
                    ], className='col-lg-6'),
                    html.Div([
                        html.Span(f"{loan_end.strftime('%Y-%m-%d')}")
                    ], className='col-lg-6')
                ], className='row'),
                html.Div([
                    html.Div([
                        html.Span('Qty. Payments')
                    ], className='col-lg-6'),
                    html.Div([
                        html.Span(f"{pay_sched_df.shape[0]:,}")
                    ], className='col-lg-6')
                ], className='row'),
                html.Div([
                    html.Div([
                        html.Span('Duration')
                    ], className='col-lg-6'),
                    html.Div([
                        html.Span(f"{loan_dur_days/365.25:.2f} yrs.")
                    ], className='col-lg-6')
                ], className='row'),
                html.Div([
                    html.Div([
                        html.Span('Total Interest')
                    ], className='col-lg-6'),
                    html.Div([
                        html.Span(f'${total_interest:,.2f}')
                    ], className='col-lg-6')
                ], className='row'),
                html.Div([
                    html.Div([
                        html.Span('Total Cost')
                    ], className='col-lg-6'),
                    html.Div([
                        html.Span(f'${total_cost:,.2f}')
                    ], className='col-lg-6')
                ], className='row'),
                html.Div([
                    html.Div([
                        dbc.Button('Open Schedule', color='secondary', outline=True, id=self.ids.open_sched_btn(aio_id)),
                        dbc.Button('Export', color='secondary', outline=True, id=self.ids.export_btn(aio_id), style={'marginLeft':'10px'})
                    ], className='col-12 d-flex')
                ], className='row'),
                dbc.Modal(
                    dbc.ModalBody([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.H3('Schedule of Payments')
                                ], className='col-12 text-center')
                            ], className='row'),
                            html.Div([
                                html.Div([
                                    dag.AgGrid(
                                        columnDefs=[
                                            {'field': 'payment_date', 'headerName': 'Date', 'width': 120,
                                                'valueGetter': {'function': date_obj},
                                                'valueFormatter': {'function': f"d3.timeFormat('%m/%d/%Y')({date_obj})"}},
                                            {'field': 'interest_paid', 'headerName':'Interest', 'width':110,
                                                    "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"}},
                                            {'field': 'principal_paid', 'headerName':'Required Principal', 'width': 145,
                                                "valueFormatter": {"function": "d3.format('($,.2f')(params.data.principal_paid - params.data.extra_principal_paid)"}},
                                            {'field': 'extra_principal_paid', 'headerName':'Extra Principal', 'width': 120,
                                                "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"}},
                                            {'field': 'balance', 'headerName':'Balance',
                                                "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"}}
                                        ],
                                        rowData=pay_sched_df.to_dict('records'),
                                        columnSize='responsiveSizeToFit',
                                        getRowStyle={
                                            "styleConditions":[
                                                {"condition": "params.data.extra_principal_paid > 0", "style": {"backgroundColor": "lightgray"}}
                                            ]
                                        }
                                    )
                                ], className='col-12')
                            ], className='row')
                        ], className='container-fluid mt-2')
                    ]),
                    is_open=False,
                    size='lg',
                    id=self.ids.sched_modal(aio_id)
                ),
                dcc.Store(id=self.ids.export_store(aio_id), data=store_data),
                dcc.Download(id=self.ids.export_dwnload(aio_id))
            ], className='containter-fluid mt-2')
        ]))

    @callback(
        Output(ids.sched_modal(MATCH), 'is_open'),
        Input(ids.open_sched_btn(MATCH), 'n_clicks'),
        prevent_initial_call=True
    )
    def open_sched_modal(_):
        return True


    @callback(
        Output(ids.export_dwnload(MATCH), 'data'),
        Input(ids.export_btn(MATCH), 'n_clicks'),
        State(ids.export_store(MATCH), 'data'),
        prevent_initial_call=True
    )
    def export_dwnload(_, store: dict):
        json_data = json.dumps(store, indent=1)
        return {'content': json_data, 'filename':'mortgage-scenario-export.json'}