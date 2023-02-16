import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
from components.HeaderGraph import render as header_render
from components.BodyGraph import render as body_render
from components.ids import INDEX_PANEL, TICKER_PANEL, TIMER
from data_loader import load_tickers, load_indices


def create_layout(app: Dash) -> html.Div:

    @app.callback([
        Output(INDEX_PANEL, "children"),
        Output(TICKER_PANEL, "children"),
        Input(TIMER, "n_intervals")
    ])
    def update_graphs(_: int) -> tuple[dbc.Container, dbc.Container]:
        return header_render(app, load_indices()), body_render(app, load_tickers())

    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(id=INDEX_PANEL, children=header_render(app, load_indices())),
            html.Div(id=TICKER_PANEL, children=body_render(app, load_tickers())),
            dcc.Interval(
                id=TIMER,
                interval=24 * 3600 * 1000,  # in milliseconds
                n_intervals=0
            ),
        ]
    )
