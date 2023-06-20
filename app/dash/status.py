import dash_bootstrap_components as dbc
import pandas
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from flask import Flask

from app.dash.flask import FlaskDash
from app.models import RequestCount


def fetch_request_counts(count_limit=600):
    return RequestCount.query.order_by(RequestCount.tick).limit(count_limit)


def init_dash(server: Flask) -> Flask:
    dash_app = FlaskDash(
        server=server,
        routes_pathname_prefix="/",
    )

    fig1 = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=1,
            align="center",
            title={"text": "MIDL-NA-CLUSTER"},
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={"axis": {"range": [None, 1]}},
        )
    )

    fig2 = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=0,
            align="center",
            title={"text": "MIDL-EU-CLUSTER"},
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={"axis": {"range": [None, 1]}},
        )
    )

    request_counts = fetch_request_counts()
    df = pandas.DataFrame(
        [row.__dict__ for row in request_counts],
        columns=request_counts[0].__table__.columns.keys(),
    )
    fig = px.area(
        df,
        x="tick",
        y="count",
        labels={
            "tick": "date",
            "count": "tezos rpc calls",
        },
        color="cluster",
        facet_row="cluster",
    )

    app_layout = html.Div(
        children=[
            html.H2("MIDL Tezos RPC nodes"),
            html.Div(
                children=[
                    dcc.Graph(
                        id="graph1", figure=fig1, style={"display": "inline-block"}
                    ),
                    dcc.Graph(
                        id="graph2", figure=fig2, style={"display": "inline-block"}
                    ),
                ]
            ),
            html.H2("MIDL Tezos RPC traffic"),
            dcc.Graph(id="time-series-chart", figure=fig),
        ]
    )
    dash_app.layout = app_layout
    dash_app.external_stylesheets = [dbc.themes.BOOTSTRAP]
    return dash_app.server


if __name__ == "__main__":
    app = FlaskDash(__name__)
    app.run_server(debug=True)
