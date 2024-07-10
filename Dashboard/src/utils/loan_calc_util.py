import datetime as dt
import pandas as pd
from typing import Optional, Dict

class LoanCalc:
    def __init__(self):
        self.amor_sched = None
        self.pmi_cancel_frac = 0.80

    @property
    def interest_sum(self) -> float:
        if self.amor_sched is None or self.amor_sched.shape[0] == 0:
            return 0
        return self.amor_sched['interest_paid'].sum()

    @property
    def total_cost(self) -> float:
        if self.amor_sched is None or self.amor_sched.shape[0] == 0:
            return 0
        return self.amor_sched['interest_paid'].sum() + self.amor_sched['principal_paid'].sum()

    @property
    def end_date(self) -> Optional[dt.date]:
        if self.amor_sched is None or self.amor_sched.shape[0] == 0:
            return None
        return self.amor_sched['payment_date'].max().date()

    def _next_month(self, current_date: dt.date)-> dt.date:
        next_month = current_date.month + 1
        year = current_date.year
        if (next_month > 12):
            next_month = 1
            year += 1
        return dt.date(year, next_month, 1)
    
    def _baseline_interest_principal_payment(self, loan_val: int, term: int, rate_mon: float) -> float:
        """Computes baseline monthly payment.
            Parameters:
                loan_val: Original loan value
                term: Duration of the loan in months.
                rate_mon: Interest rate per month expressed as a decimal.
        """
        return loan_val*((rate_mon*(1+rate_mon)**term)/(((1+rate_mon)**term)-1))

    def calc_amor_schedule(self, loan_val: int, start_date: dt.date, rate: float, term: int, 
        consider_pmi:bool = False, appraised_val:Optional[int] = None, extra_principal_funds:Dict[dt.date, float] = {}) -> pd.DataFrame:
        """Computation of the amoritization schedule for the loan.
            Parameters:
                loan_val: Original loan value.
                start_date: Date at which loan begins.
                rate: Interest rate per year expressed as a decimal.
                term: Duration of the loan in years.
                consider_pmi: Flag to determine if private mortgage insurace should be considered.
                appraised_val: Appraised value of property at the start of the loan.
        """
        
        loan_status_dicts = []
        payment_date = start_date
        balance = loan_val
        term_mon = term*12
        rate_mon = rate/12
        payment= self._baseline_interest_principal_payment(loan_val, term_mon, rate_mon)
        for j in range(term_mon):
            if balance <= 0.01:
                break
            payment_date = self._next_month(payment_date)
            month_interest = balance*rate_mon
            month_principal = payment-month_interest
            extra_principal = 0
            if month_principal >= balance:
                month_principal = balance
            else:
                if payment_date in extra_principal_funds.keys() and balance > 0:
                    extra_principal = extra_principal_funds[payment_date]
            total_principal = month_principal + extra_principal
            if total_principal > balance:
                total_principal = balance
                extra_principal = balance - month_principal
                    
            balance -= total_principal
            loan_status_dicts.append({
                'month_id': j, 
                'payment_date': payment_date,
                'interest_paid':month_interest,
                'principal_paid':total_principal,
                'extra_principal_paid': extra_principal,
                'balance': balance
            })

        loan_status_df = pd.DataFrame(loan_status_dicts)
        loan_status_df['payment_date'] = loan_status_df['payment_date'].astype('datetime64[ns]')
        self.amor_sched = loan_status_df
        return loan_status_df