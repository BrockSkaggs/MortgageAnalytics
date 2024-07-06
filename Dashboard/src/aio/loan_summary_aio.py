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

        loan_start = pay_sched_df['payment_date'].min()
        loan_end = pay_sched_df['payment_date'].max()
        loan_dur_days = (loan_end - loan_start).days
        total_interst = pay_sched_df['interest_paid'].sum()
        total_cost = pay_sched_df['interest_paid'].sum() + pay_sched_df['principal_paid'].sum()

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
                                        ], className='col-lg-3'),
                                        html.Div([
                                            html.Span(f"{loan_start.strftime('%Y-%m-%d')}")
                                        ], className='col-lg-3'),
                                                html.Div([
                                            html.Span('Loan Start')
                                        ], className='col-lg-3'),
                                        html.Div([
                                            html.Span(f"{loan_end.strftime('%Y-%m-%d')}")
                                        ], className='col-lg-3')
                                    ], className='row'),
                                    html.Div([
                                        html.Div([
                                            html.Span('Qty. Payments')
                                        ], className='col-lg-3'),
                                        html.Div([
                                            html.Span(f"{pay_sched_df.shape[0]:,}")
                                        ], className='col-lg-3'),
                                        html.Div([
                                            html.Span('Duration')
                                        ], className='col-lg-3'),
                                        html.Div([
                                            html.Span(f"{loan_dur_days/365.25:.2f} yrs.")
                                        ], className='col-lg-3')
                                    ], className='row'),
                                    html.Div([
                                        html.Div([
                                            html.Span('Total Interest')
                                        ], className='col-lg-3'),
                                        html.Div([
                                            html.Span(f'${total_interst:,.2f}')
                                        ], className='col-lg-3')
                                    ], className='row'),
                                    html.Div([
                                        html.Div([
                                            html.Span('Total Cost')
                                        ], className='col-lg-3'),
                                        html.Div([
                                            html.Span(f'${total_cost:,.2f}')
                                        ], className='col-lg-3')
                                    ], className='row')
                                ], className='container-fluid mt-2')
                            ], label='Summary'),
                            dbc.Tab([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            dag.AgGrid(
                                                
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