import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from data_loader import DataSchema


def render(app: Dash, data: dict) -> dbc.Container:
    columns = dict()
    for df_name, cmp in data.items():
        # fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=cmp[cmp[DataSchema.RETS] < 0].index,
                             y=cmp[cmp[DataSchema.RETS] < 0][DataSchema.VOLUME],
                             opacity=0.15,
                             name="Volume",
                             marker=dict(color="red")),
                      secondary_y=True)
        fig.add_trace(go.Bar(x=cmp[cmp[DataSchema.RETS] >= 0].index,
                             y=cmp[cmp[DataSchema.RETS] >= 0][DataSchema.VOLUME],
                             opacity=0.15,
                             name="Volume",
                             marker=dict(color="green")),
                      secondary_y=True)
        # fig.add_trace(go.Scatter(x=cmp.index, y=cmp[DataSchema.CLOSE], mode='lines'))
        fig.add_trace(go.Candlestick(x=cmp.index, open=cmp[DataSchema.OPEN],
                                     high=cmp[DataSchema.HIGH], low=cmp[DataSchema.LOW],
                                     close=cmp[DataSchema.CLOSE],
                                     name=f"{df_name}",))
        fig.add_trace(go.Scatter(x=cmp.index, y=cmp[DataSchema.VWAP], name="VWAP", mode='lines'))
        fig.add_trace(go.Scatter(x=cmp[cmp[DataSchema.VWAP_LOCAL] == 1].index,
                                 y=cmp[cmp[DataSchema.VWAP_LOCAL] == 1][DataSchema.VWAP],
                                 mode='markers', marker=dict(size=12, color='green',
                                                             symbol='triangle-up',
                                                             line=dict(width=1,
                                                                       color='DarkSlateGrey'))),
                      secondary_y=False)
        fig.add_trace(go.Scatter(x=cmp[cmp[DataSchema.VWAP_LOCAL] == -1].index,
                                 y=cmp[cmp[DataSchema.VWAP_LOCAL] == -1][DataSchema.VWAP],
                                 mode='markers', marker=dict(size=12, color='red',
                                                             symbol='triangle-down',
                                                             line=dict(width=1,
                                                                       color='DarkSlateGrey'))),
                      secondary_y=False)

        fig.update_layout(showlegend=False, margin=dict(l=0, r=0, b=0, t=0, pad=0))
        columns[df_name] = fig

    bottom_panel = dbc.Container(
        [
            dbc.Row(html.Div(children=[html.H5(df_name),
                                       dcc.Graph(figure=cmp),
                                       ]
                             )
                    )
            for df_name, cmp in columns.items()
        ]
    )
    return bottom_panel
