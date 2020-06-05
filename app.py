import plotly.graph_objects as go
import pandas as pd

fig = go.Figure()

df_combined = pd.read_pickle("wgms_combined")

fig = go.Figure(
    data=go.Scattermapbox(
        lon=df_combined["long"],
        lat=df_combined["lat"],
        mode="markers",
        marker=go.scattermapbox.Marker(size=8),
    )
)
fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=45)
fig.update_layout(autosize=True, height=300, margin=dict(l=0, r=0, b=0, t=0, pad=50))

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://codepen.io/chriddyp/pen/bWLwgP.css",
    ]
)


app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            "World Glacier Monitoring Service", className="text-center"
                        ),
                        html.H5("Data Explorer", className="text-center"),
                    ],
                    md=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div("One of three columns", style={"backgroundColor": "blue"}),
                    md=4,
                ),
                dbc.Col(
                    [
                        html.Div(
                            [html.H3("XXk"), "Glaciers"], className="mini_container"
                        ),
                    ],
                    md=2,
                ),
                dbc.Col(
                    html.Div(
                        [html.H3("19XX"), "Oldest Record"], className="mini_container"
                    ),
                    md=2,
                ),
                dbc.Col(
                    html.Div(
                        [html.H3("XXX+"), "Contributors"], className="mini_container"
                    ),
                    md=2,
                ),
                dbc.Col(
                    html.Div([html.H3("XX"), "Countries"], className="mini_container"),
                    md=2,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div("One of four columns", className="mini_container"), md=4
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H5("Satellite Overview", className="text-center"),
                            dcc.Graph(figure=fig),
                        ],
                        className="mini_container satellite_container",
                    ),
                    md=8,
                ),
            ]
        ),
    ],
    fluid=True,
    className="main_container",
)

app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
