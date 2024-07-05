from dash import html, dcc
from dash_bootstrap_components import Input
import datetime as dt
import uuid

from common import months

class DatePickAIO(html.Div):

    class ids:
        month_drpdwn = lambda aio_id: {
            'component': 'DatePickerAIO',
            'subcomponent': 'month_drpdwn',
            'aio_id': aio_id
        }

        year_input = lambda aio_id: {
            'component': 'DatePickerAIO',
            'subcomponent': 'year_input',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(
        self,
        min_year: int, 
        max_year: int,
        aio_id=None
    ):

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        super().__init__(
            html.Div([
                dcc.Dropdown(
                    id=self.ids.month_drpdwn(aio_id),
                    options=[{'label': m, 'value': months[m]} for m in months.keys()],
                    value=1,
                    style={'width':'125px', 'marginTop':'auto', 'marginBottom':'auto', 'marginRight':'5px'}
                ),
                Input(
                    id=self.ids.year_input(aio_id),
                    type='number',
                    min=min_year, max=max_year, step=1,
                    value=dt.date.today().year,
                    className='d-inline-block vertical-align',
                    style={'width':'125px'}
                )
            ], className='d-flex')
        )