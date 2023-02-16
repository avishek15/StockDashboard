import plotly.graph_objects as go
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from data_loader import IndexSchema


def render(app: Dash, data: dict) -> dbc.Container:
    columns = dict()
    for idx_name, cmp in data.items():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=cmp.index, y=cmp[IndexSchema.CLOSE], mode='lines'))
        fig.add_trace(go.Scatter(x=cmp.index, y=cmp[IndexSchema.SCLOSE], mode='lines'))
        fig.add_trace(go.Scatter(x=cmp[cmp[IndexSchema.LOCAL] == 1].index,
                                 y=cmp[cmp[IndexSchema.LOCAL] == 1][IndexSchema.CLOSE],
                                 mode='markers', marker=dict(size=8, color='green',
                                                             symbol='triangle-up',
                                                             line=dict(width=1,
                                                                       color='DarkSlateGrey'))))
        fig.add_trace(go.Scatter(x=cmp[cmp[IndexSchema.LOCAL] == -1].index,
                                 y=cmp[cmp[IndexSchema.LOCAL] == -1][IndexSchema.CLOSE],
                                 mode='markers', marker=dict(size=8, color='red',
                                                             symbol='triangle-down',
                                                             line=dict(width=1,
                                                                       color='DarkSlateGrey'))))
        fig.update_layout(showlegend=False, margin=dict(l=0, r=0, b=0, t=0, pad=0), height=155)
        columns[idx_name] = fig

    top_panel = dbc.Container(
        dbc.Row(
            [
                dbc.Col(html.Div(children=[html.H5(idx_name),
                                           dcc.Graph(figure=cmp),
                                           ]
                                 )
                        )
                for idx_name, cmp in columns.items()
            ]
        )
    )
    return top_panel
