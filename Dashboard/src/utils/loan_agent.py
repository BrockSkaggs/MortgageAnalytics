import datetime as dt
import plotly.graph_objects as go

from utils.loan_calc_util import LoanCalc

class LoanAgent:
    def __init__(self):
        ...

    def calc_baseline_amor_schedule(self, loan_val: int, start_date: dt.date, rate: float, term: int):
        loan_calc = LoanCalc()
        df = loan_calc.calc_amor_schedule(loan_val, start_date, rate, term)

        traces = [go.Scatter(
            x=df['payment_date'],
            y=df['balance'],
            name='Baseline'
        )]

        layout = {
            'margin':{'l':5,'r':5,'b':10, 't':60},
            'title':{'text':'Loan Balance Trajectory', 'x': 0.5, 'font': {'color':'black', 'size':30}}
        }
        fig = go.Figure(data=traces, layout=layout)
        return (df, fig)