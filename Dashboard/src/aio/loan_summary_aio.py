from dash import html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import uuid

class LoanSummaryAIO(html.Div):

    class ids:
        ...

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
        total_interst = pay_sched_df['interest_paid'].sum()
        total_cost = pay_sched_df['interest_paid'].sum() + pay_sched_df['principal_paid'].sum()
        date_obj = "d3.timeParse('%Y-%m-%d')(params.data.payment_date)"

        return dbc.Card(dbc.CardBody([
            html.Div([
                html.Div([
                    html.Div([
                        html.H4(name)
                    ], className='col-12')
                ], className='row'),
                html.Div([
                    html.Div([
                        dbc.Tabs([
                            dbc.Tab([
                                html.Div([
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
                                            html.Span(f'${total_interst:,.2f}')
                                        ], className='col-lg-6')
                                    ], className='row'),
                                    html.Div([
                                        html.Div([
                                            html.Span('Total Cost')
                                        ], className='col-lg-6'),
                                        html.Div([
                                            html.Span(f'${total_cost:,.2f}')
                                        ], className='col-lg-6')
                                    ], className='row')
                                ], className='container-fluid mt-2')
                            ], label='Summary'),
                            dbc.Tab([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            dag.AgGrid(
                                                columnDefs=[
                                                    {'field': 'payment_date', 'headerName': 'Date', 'width': 120,
                                                        'valueGetter': {'function': date_obj},
                                                        'valueFormatter': {'function': f"d3.timeFormat('%m/%d/%Y')({date_obj})"}},
                                                    {'field': 'interest_paid', 'headerName':'Interest', 'width':110,
                                                         "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"}},
                                                    {'field': 'principal_paid', 'headerName':'Principal', 'width': 110,
                                                        "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"}},
                                                    {'field': 'balance', 'headerName':'Balance',
                                                        "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"}}
                                                ],
                                                rowData=pay_sched_df.to_dict('records'),
                                                style={'height':250},
                                                getRowStyle={
                                                    "styleConditions":[
                                                        {"condition": "params.data.extra_principal_paid > 0", "style": {"backgroundColor": "lightgray"}}
                                                    ]
                                                }
                                            )
                                        ], className='col-12')
                                    ], className='row')
                                ], className='container-fluid mt-2')
                            ], label='Schedule')
                        ])
                    ], className='col-12')
                ], className='row'),





                
            ], className='containter-fluid')
        ]))