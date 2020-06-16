import plotly.graph_objects as go
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Data Import
df_combined = pd.read_pickle("wgms_combined")
df_thickness = pd.read_pickle("wgms_thickness")

# Satellite Map
def update_satellite_map():

    data = go.Scattermapbox(
        lon=df_combined["LONGITUDE"],
        lat=df_combined["LATITUDE"],
        customdata=df_combined["WGMS_ID"],
        mode="markers",
        marker=go.scattermapbox.Marker(size=8),
    )
    layout = dict(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=0,
        mapbox_center_lon=0,
        mapbox_zoom=0,
        autosize=True,
        height=300,
        margin=dict(l=0, r=0, b=0, t=0, pad=50),
    )

    figure = go.Figure(data=data, layout=layout)
    return figure


def update_thickness_change():
    tid = 4630
    d2020 = pd.DataFrame({"YEAR": [2020], "THICKNESS_CHG": [0]})

    df_t = (
        df_thickness[df_thickness["WGMS_ID"] == tid]
        .drop("WGMS_ID", axis=1)
        .append(d2020)
    )

    data = go.Bar(x=df_t.YEAR, y=df_t.THICKNESS_CHG, width=1)
    layout = dict(
        xaxis_title="Year",
        yaxis_title="\delta (mm)",
        autosize=True,
        height=300,
        margin=dict(l=20, r=20, b=20, t=50, pad=0),
    )

    figure = go.Figure(data=data, layout=layout)
    return figure


# Dash App
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
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            [html.H3("XXk"), "Glaciers"],
                                            className="mini_container",
                                        ),
                                    ],
                                    width=3,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [html.H3("19XX"), "Oldest Record"],
                                        className="mini_container",
                                    ),
                                    width=3,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [html.H3("XXX+"), "Contributors"],
                                        className="mini_container",
                                    ),
                                    width=3,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [html.H3("XX"), "Countries"],
                                        className="mini_container",
                                    ),
                                    width=3,
                                ),
                            ],
                        ),
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    [
                                        html.H5(
                                            "Satellite Overview",
                                            className="text-center",
                                        ),
                                        dcc.Graph(
                                            figure=update_satellite_map(), id="mapbox"
                                        ),
                                    ],
                                    className="mini_container satellite_container",
                                ),
                                width=12,
                            ),
                        ),
                    ],
                    md=8,
                ),
                dbc.Col(
                    html.Div(
                        "RIGHT PANEL", className="mini_container selection_panel",
                    ),
                    md=4,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        "BOTTOM LEFT PANEL",
                        id="glacier_info",
                        className="mini_container ",
                    ),
                    md=6,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H5("Thickness Change", className="text-center",),
                            dcc.Graph(
                                figure=update_thickness_change(), id="thickness_chg"
                            ),
                        ],
                        className="mini_container ",
                    ),
                    md=6,
                ),
            ]
        ),
    ],
    fluid=True,
    className="main_container",
)


@app.callback(
    Output(component_id="glacier_info", component_property="children"),
    [Input(component_id="mapbox", component_property="clickData")],
)
def update_glacier_info_div(input_value):
    wgms_id = "N/A"
    if input_value:
        point_data = input_value["points"][0]
        wgms_id = point_data["customdata"]

    return f"{wgms_id}"


app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
