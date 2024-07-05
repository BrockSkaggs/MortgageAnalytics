from dash import html
import dash_bootstrap_components as dbc
import uuid

class LoanSummaryAIO(html.Div):

    class ids:
        ...

    ids = ids

    def __init__(
        self,
        name: str,
        aio_id=None
    ):

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        super().__init__(
            self._gen_layout(name, aio_id)
        )

    def _gen_layout(self, name: str, aio_id: str):
        return dbc.Card(dbc.CardBody([
            html.Div([
                html.Div([
                    html.Div([
                        html.H4(name)
                    ], className='col-12')
                ], className='row')
            ], className='containter-fluid')
        ]))

    

